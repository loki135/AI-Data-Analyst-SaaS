"""High-level ingestion orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from app.config import settings
from app.data_ingestion.parsers import parse_csv, parse_excel, parse_json
from app.data_ingestion.validators import ValidationReport, validate_dataframe


@dataclass
class DatasetRecord:
    """Metadata about an ingested dataset."""

    dataset_id: str
    filename: str
    row_count: int
    column_count: int
    columns: list[str]


@dataclass
class IngestionService:
    """Orchestrates file upload → parse → validate → store."""

    _store: dict[str, pd.DataFrame] = field(default_factory=dict)
    _meta: dict[str, DatasetRecord] = field(default_factory=dict)
    _counter: int = 0

    def ingest(self, filename: str, content: bytes) -> tuple[DatasetRecord, ValidationReport]:
        """Ingest a file and return metadata + validation report.

        Raises ``ValueError`` on unsupported extension or invalid data.
        """
        if not settings.is_extension_allowed(filename):
            raise ValueError(f"Unsupported file type: {filename}")

        lower = filename.lower()
        if lower.endswith(".csv"):
            df = parse_csv(content)
        elif lower.endswith(".json"):
            df = parse_json(content)
        elif lower.endswith((".xlsx", ".xls")):
            df = parse_excel(content)
        else:
            raise ValueError(f"Cannot determine parser for: {filename}")

        report = validate_dataframe(df)

        self._counter += 1
        dataset_id = f"ds_{self._counter:06d}"
        record = DatasetRecord(
            dataset_id=dataset_id,
            filename=filename,
            row_count=len(df),
            column_count=len(df.columns),
            columns=df.columns.tolist(),
        )
        self._store[dataset_id] = df
        self._meta[dataset_id] = record
        return record, report

    def get_dataframe(self, dataset_id: str) -> pd.DataFrame | None:
        return self._store.get(dataset_id)

    def list_datasets(self) -> list[DatasetRecord]:
        return list(self._meta.values())
