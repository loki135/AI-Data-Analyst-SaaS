"""Tests for app.analysis.service – AnalysisService."""

import pandas as pd
import pytest

from app.analysis.service import AnalysisResult, AnalysisService


@pytest.fixture()
def svc() -> AnalysisService:
    return AnalysisService()


class TestFullAnalysis:
    def test_returns_result(self, svc: AnalysisService, numeric_df: pd.DataFrame) -> None:
        result = svc.full_analysis(numeric_df)
        assert isinstance(result, AnalysisResult)
        assert len(result.column_stats) == 3
        assert isinstance(result.outlier_counts, dict)

    def test_outlier_counts_keys(self, svc: AnalysisService, numeric_df: pd.DataFrame) -> None:
        result = svc.full_analysis(numeric_df)
        assert set(result.outlier_counts.keys()) == {"x", "y", "z"}


class TestQuickSummary:
    def test_returns_dict(self, svc: AnalysisService, sample_df: pd.DataFrame) -> None:
        summary = svc.quick_summary(sample_df)
        assert summary["rows"] == 5
        assert summary["columns"] == 4
        assert "age" in summary["numeric_columns"]
        assert "grade" in summary["categorical_columns"]
        assert isinstance(summary["memory_mb"], float)
