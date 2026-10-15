"""Synthetic reliability dataset generation and ingestion utilities."""

import random
from typing import List
from reliability_agent.schemas import ComponentRecordCreate, DatasetIngestRequest


def generate_synthetic_reliability_dataset(
    name: str = "starter_bearing_test",
    num_components: int = 100,
    failure_probability: float = 0.7,
    seed: int = 42,
) -> DatasetIngestRequest:
    """Generate synthetic engineering test data for components (e.g. bearings, pumps)."""
    random.seed(seed)
    records: List[ComponentRecordCreate] = []

    failure_modes = ["wear_out", "fatigue", "overheating", "electrical_short", None]

    for i in range(1, num_components + 1):
        component_id = f"COMP-{i:03d}"
        # Weibull-like operating hours distribution
        base_hours = random.weibullvariate(1500.0, 2.0)
        operating_hours = round(max(50.0, base_hours), 2)

        failed = 1 if random.random() < failure_probability else 0
        failure_mode = random.choice(failure_modes) if failed == 1 else None

        covariates = {
            "temperature_c": round(random.uniform(45.0, 95.0), 1),
            "voltage_v": round(random.uniform(11.5, 12.8), 2),
            "load_n": round(random.uniform(100.0, 500.0), 1),
        }

        records.append(
            ComponentRecordCreate(
                component_id=component_id,
                operating_hours=operating_hours,
                failed=failed,
                failure_mode=failure_mode,
                covariates=covariates,
            )
        )

    return DatasetIngestRequest(
        name=name,
        description=f"Synthetic reliability dataset with {num_components} components generated for testing and analysis.",
        source_type="synthetic",
        records=records,
    )

