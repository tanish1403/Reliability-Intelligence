"""FastAPI application entry point for the starter project."""

from typing import Any, List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from reliability_agent.database import get_db, engine, Base
from reliability_agent.models import ReliabilityDatasetModel, ComponentTestRecordModel, AuditLogModel
from reliability_agent.schemas import DatasetIngestRequest, DatasetResponse, ComponentRecordResponse, AuditLogResponse
from reliability_agent.ingestion import generate_synthetic_reliability_dataset
import uuid

# Create tables for starter/demo if not using alembic directly in run
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Reliability Data Analysis Agent",
    version="0.1.0",
    description="Locally runnable reliability data analysis agent platform for engineering test data.",
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class DemoResponse(BaseModel):
    status: str
    message: str
    sample_endpoints: List[str]


@app.get("/health", response_model=HealthResponse, tags=["operations"])
def health() -> HealthResponse:
    """Return a simple liveness response."""
    return HealthResponse(
        status="ok",
        service="reliability-data-analysis-agent",
        version=app.version or "unknown",
    )


@app.get("/", tags=["operations"])
def root() -> dict[str, str]:
    """Point users to the API documentation."""
    return {"message": "Reliability Data Analysis Agent API", "docs": "/docs"}


@app.get("/analytics/demo", tags=["analytics"])
def analytics_demo() -> dict[str, Any]:
    """Demonstrate deterministic reliability analytics with scipy and numpy."""
    import numpy as np
    from scipy.stats import weibull_min

    # Synthetic failure time data (hours)
    failure_times = np.array([120.5, 145.2, 110.0, 160.8, 135.4, 150.1, 125.6, 140.9])
    shape, loc, scale = weibull_min.fit(failure_times, floc=0)
    mean_ttf = float(np.mean(failure_times))
    std_ttf = float(np.std(failure_times))

    return {
        "sample_size": len(failure_times),
        "mean_ttf_hours": mean_ttf,
        "std_ttf_hours": std_ttf,
        "weibull_shape_beta": float(shape),
        "weibull_scale_eta": float(scale),
    }


@app.post("/datasets/ingest-synthetic", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED, tags=["datasets"])
def ingest_synthetic_dataset(
    name: str = "starter_bearing_test",
    num_components: int = 100,
    db: Session = Depends(get_db),
) -> DatasetResponse:
    """Generate and ingest a synthetic reliability dataset."""
    existing = db.query(ReliabilityDatasetModel).filter_by(name=name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Dataset with name '{name}' already exists.")

    request_data = generate_synthetic_reliability_dataset(name=name, num_components=num_components)

    dataset = ReliabilityDatasetModel(
        name=request_data.name,
        description=request_data.description,
        source_type=request_data.source_type,
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    for rec in request_data.records:
        record_model = ComponentTestRecordModel(
            dataset_id=dataset.id,
            component_id=rec.component_id,
            operating_hours=rec.operating_hours,
            failed=rec.failed,
            failure_mode=rec.failure_mode,
            covariates=rec.covariates,
        )
        db.add(record_model)

    # Record audit log
    audit = AuditLogModel(
        actor="api_user",
        action="INGEST_SYNTHETIC_DATASET",
        input_summary={"dataset_name": dataset.name, "num_components": num_components},
        correlation_id=str(uuid.uuid4()),
    )
    db.add(audit)
    db.commit()

    record_count = db.query(ComponentTestRecordModel).filter_by(dataset_id=dataset.id).count()

    return DatasetResponse(
        id=dataset.id,
        name=dataset.name,
        description=dataset.description,
        source_type=dataset.source_type,
        created_at=dataset.created_at,
        record_count=record_count,
    )


@app.get("/datasets", response_model=List[DatasetResponse], tags=["datasets"])
def list_datasets(db: Session = Depends(get_db)) -> List[DatasetResponse]:
    """List all ingested reliability datasets."""
    datasets = db.query(ReliabilityDatasetModel).all()
    results = []
    for d in datasets:
        count = db.query(ComponentTestRecordModel).filter_by(dataset_id=d.id).count()
        results.append(
            DatasetResponse(
                id=d.id,
                name=d.name,
                description=d.description,
                source_type=d.source_type,
                created_at=d.created_at,
                record_count=count,
            )
        )
    return results


