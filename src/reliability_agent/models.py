"""SQLAlchemy models for reliability data analysis."""

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, JSON
from reliability_agent.database import Base


class ReliabilityDatasetModel(Base):
    """Represents an ingested dataset of engineering test or component reliability data."""

    __tablename__ = "reliability_datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    source_type = Column(String(50), nullable=False, default="synthetic")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class ComponentTestRecordModel(Base):
    """Represents individual component test or operating records within a dataset."""

    __tablename__ = "component_test_records"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, index=True, nullable=False)
    component_id = Column(String(100), index=True, nullable=False)
    operating_hours = Column(Float, nullable=False)
    failed = Column(Integer, nullable=False)  # 1 if failed, 0 if censored (right-censored)
    failure_mode = Column(String(100), nullable=True)
    covariates = Column(JSON, nullable=True)  # Temperature, voltage, batch, etc.
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class AuditLogModel(Base):
    """Protected audit record for agent and user actions."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    input_summary = Column(JSON, nullable=True)
    correlation_id = Column(String(64), index=True, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


