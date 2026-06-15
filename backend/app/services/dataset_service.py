"""Dataset processing service.

Centralizes file parsing and metadata extraction logic that would
otherwise be duplicated between upload, re-process, and preview endpoints.
"""

from pathlib import Path
from typing import Any

import pandas as pd

from app.core.exceptions import ValidationError

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json", ".parquet"}


def validate_file_extension(filename: str) -> str:
    """Validate and return the file extension."""
    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file type: {ext}",
            errors=[
                {"field": "file", "message": f"Must be one of {SUPPORTED_EXTENSIONS}"}
            ],
        )
    return ext


def read_dataframe(file_path: str) -> pd.DataFrame:
    """Read a file into a pandas DataFrame based on its extension."""
    ext = Path(file_path).suffix.lower()
    readers: dict[str, Any] = {
        ".csv": pd.read_csv,
        ".xlsx": pd.read_excel,
        ".xls": pd.read_excel,
        ".json": pd.read_json,
        ".parquet": pd.read_parquet,
    }
    reader = readers.get(ext)
    if reader is None:
        raise ValidationError(f"Cannot read file with extension: {ext}")
    return reader(file_path)


def extract_metadata(df: pd.DataFrame) -> dict[str, Any]:
    """Extract common metadata from a DataFrame."""
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": [
            {
                "name": col,
                "dtype": str(df[col].dtype),
                "null_count": int(df[col].isna().sum()),
            }
            for col in df.columns
        ],
        "memory_usage_bytes": int(df.memory_usage(deep=True).sum()),
    }


def get_preview(df: pd.DataFrame, rows: int = 10) -> list[dict[str, Any]]:
    """Return the first N rows as a list of dicts for API responses."""
    return df.head(rows).to_dict(orient="records")  # type: ignore[return-value]
