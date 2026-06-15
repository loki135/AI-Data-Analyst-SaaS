"""Analysis orchestration layer."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.analysis.correlations import CorrelationResult, find_top_correlations
from app.analysis.statistics import ColumnStats, compute_dataframe_stats, detect_outliers_iqr


@dataclass
class AnalysisResult:
    """Full analysis output for a dataset."""

    column_stats: list[ColumnStats]
    top_correlations: list[CorrelationResult]
    outlier_counts: dict[str, int]


class AnalysisService:
    """Run a suite of analyses on a DataFrame."""

    def full_analysis(self, df: pd.DataFrame) -> AnalysisResult:
        """Perform descriptive stats, correlation, and outlier detection."""
        col_stats = compute_dataframe_stats(df)
        top_corr = find_top_correlations(df, n=10, threshold=0.3)

        outlier_counts: dict[str, int] = {}
        for col in df.select_dtypes(include="number").columns:
            mask = detect_outliers_iqr(df[col])
            outlier_counts[str(col)] = int(mask.sum())

        return AnalysisResult(
            column_stats=col_stats,
            top_correlations=top_corr,
            outlier_counts=outlier_counts,
        )

    def quick_summary(self, df: pd.DataFrame) -> dict[str, object]:
        """Return a lightweight summary dict."""
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
            "categorical_columns": (
                df.select_dtypes(include=["object", "category"]).columns.tolist()
            ),
            "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        }
