"""Pydantic schemas for datasets, test records, and ingestion."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ComponentRecordCreate(BaseModel):
    component_id: str
    operating_hours: float = Field(..., ge=0.0)
    failed: int = Field(..., ge=0, le=1)
    failure_mode: Optional[str] = None
    covariates: Optional[Dict[str, Any]] = None


class DatasetIngestRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    source_type: str = "synthetic"
    records: List[ComponentRecordCreate]


class ComponentRecordResponse(ComponentRecordCreate):
    id: int
    dataset_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DatasetResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    source_type: str
    created_at: datetime
    record_count: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AuditLogResponse(BaseModel):
    id: int
    actor: str
    action: str
    input_summary: Optional[Dict[str, Any]] = None
    correlation_id: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


