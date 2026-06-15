"""Data-validation helpers."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ValidationReport:
    """Summary produced by ``validate_dataframe``."""

    row_count: int
    column_count: int
    missing_cells: int
    missing_pct: float
    duplicate_rows: int
    numeric_columns: list[str]
    categorical_columns: list[str]
    warnings: list[str]


def validate_dataframe(df: pd.DataFrame, max_missing_pct: float = 50.0) -> ValidationReport:
    """Run basic quality checks on *df* and return a ``ValidationReport``.

    Raises ``ValueError`` if the frame is empty or exceeds *max_missing_pct*.
    """
    if df.empty:
        raise ValueError("DataFrame is empty")

    total_cells = int(np.prod(df.shape))
    missing = int(df.isna().sum().sum())
    missing_pct = round((missing / total_cells) * 100, 2) if total_cells else 0.0

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    warnings: list[str] = []
    if missing_pct > max_missing_pct:
        raise ValueError(
            f"Too many missing values: {missing_pct}% (limit {max_missing_pct}%)"
        )
    if missing_pct > 10:
        warnings.append(f"High missing-value ratio: {missing_pct}%")

    dup_count = int(df.duplicated().sum())
    if dup_count > 0:
        warnings.append(f"Found {dup_count} duplicate row(s)")

    return ValidationReport(
        row_count=len(df),
        column_count=len(df.columns),
        missing_cells=missing,
        missing_pct=missing_pct,
        duplicate_rows=dup_count,
        numeric_columns=numeric_cols,
        categorical_columns=categorical_cols,
        warnings=warnings,
    )


def clean_dataframe(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    fill_strategy: str = "median",
) -> pd.DataFrame:
    """Return a cleaned copy of *df*.

    * Optionally drops duplicate rows.
    * Fills missing numeric values with the column median (default) or mean.
    * Fills missing categorical values with the mode.
    """
    out = df.copy()
    if drop_duplicates:
        out = out.drop_duplicates()

    numeric_cols = out.select_dtypes(include="number").columns
    if fill_strategy == "median":
        out[numeric_cols] = out[numeric_cols].fillna(out[numeric_cols].median())
    elif fill_strategy == "mean":
        out[numeric_cols] = out[numeric_cols].fillna(out[numeric_cols].mean())
    else:
        raise ValueError(f"Unknown fill_strategy: {fill_strategy!r}")

    cat_cols = out.select_dtypes(include=["object", "category"]).columns
    for col in cat_cols:
        mode = out[col].mode()
        if not mode.empty:
            out[col] = out[col].fillna(mode.iloc[0])

    return out
