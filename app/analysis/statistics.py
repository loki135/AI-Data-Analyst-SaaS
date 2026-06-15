"""Descriptive-statistics helpers."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats as sp_stats


@dataclass
class ColumnStats:
    """Descriptive statistics for a single numeric column."""

    name: str
    count: int
    mean: float
    median: float
    std: float
    min: float
    max: float
    q25: float
    q75: float
    skewness: float
    kurtosis: float


def compute_column_stats(series: pd.Series) -> ColumnStats:
    """Compute descriptive statistics for a numeric *series*.

    Raises ``TypeError`` if *series* is not numeric.
    """
    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError(f"Column '{series.name}' is not numeric")
    clean = series.dropna()
    if clean.empty:
        raise ValueError(f"Column '{series.name}' has no non-null values")
    return ColumnStats(
        name=str(series.name),
        count=int(clean.count()),
        mean=float(clean.mean()),
        median=float(clean.median()),
        std=float(clean.std()),
        min=float(clean.min()),
        max=float(clean.max()),
        q25=float(np.percentile(clean, 25)),
        q75=float(np.percentile(clean, 75)),
        skewness=float(sp_stats.skew(clean)),
        kurtosis=float(sp_stats.kurtosis(clean)),
    )


def compute_dataframe_stats(df: pd.DataFrame) -> list[ColumnStats]:
    """Return ``ColumnStats`` for every numeric column in *df*."""
    results: list[ColumnStats] = []
    for col in df.select_dtypes(include="number").columns:
        try:
            results.append(compute_column_stats(df[col]))
        except ValueError:
            continue
    return results


def detect_outliers_iqr(series: pd.Series, factor: float = 1.5) -> pd.Series:
    """Return a boolean mask marking IQR-based outliers in *series*."""
    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError(f"Column '{series.name}' is not numeric")
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    return (series < lower) | (series > upper)
