"""Tests for database setup, models, and synthetic dataset ingestion."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from reliability_agent.database import Base
from reliability_agent.models import (
    ReliabilityDatasetModel,
    ComponentTestRecordModel,
    AuditLogModel,
)
from reliability_agent.schemas import DatasetIngestRequest
from reliability_agent.ingestion import generate_synthetic_reliability_dataset


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database session for testing."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_synthetic_dataset_generation():
    request: DatasetIngestRequest = generate_synthetic_reliability_dataset(
        name="test_bearing_dataset", num_components=10, seed=123
    )
    assert request.name == "test_bearing_dataset"
    assert len(request.records) == 10
    assert request.records[0].component_id == "COMP-001"
    assert request.records[0].operating_hours >= 0.0
    assert request.records[0].failed in (0, 1)


def test_database_model_crud(db_session):
    # Create dataset model
    dataset = ReliabilityDatasetModel(
        name="production_pump_test",
        description="Test records for centrifugal pumps",
        source_type="synthetic",
    )
    db_session.add(dataset)
    db_session.commit()
    db_session.refresh(dataset)

    assert dataset.id is not None
    assert dataset.name == "production_pump_test"

    # Add component test record
    record = ComponentTestRecordModel(
        dataset_id=dataset.id,
        component_id="PUMP-001",
        operating_hours=1250.5,
        failed=1,
        failure_mode="wear_out",
        covariates={"temperature_c": 78.5, "pressure_bar": 4.2},
    )
    db_session.add(record)

    # Add audit log
    audit = AuditLogModel(
        actor="system",
        action="INGEST_DATASET",
        input_summary={"dataset_name": dataset.name, "records": 1},
        correlation_id="corr-12345",
    )
    db_session.add(audit)
    db_session.commit()

    # Query back
    fetched_record = db_session.query(ComponentTestRecordModel).filter_by(component_id="PUMP-001").first()
    assert fetched_record is not None
    assert fetched_record.operating_hours == 1250.5
    assert fetched_record.covariates["temperature_c"] == 78.5

    fetched_audit = db_session.query(AuditLogModel).filter_by(correlation_id="corr-12345").first()
    assert fetched_audit is not None
    assert fetched_audit.action == "INGEST_DATASET"
