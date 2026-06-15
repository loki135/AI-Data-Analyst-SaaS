"""Tests for app.analysis.correlations."""

import pandas as pd
import pytest

from app.analysis.correlations import (
    CorrelationResult,
    compute_correlation_matrix,
    find_top_correlations,
)


class TestComputeCorrelationMatrix:
    def test_pearson(self, numeric_df: pd.DataFrame) -> None:
        corr = compute_correlation_matrix(numeric_df, method="pearson")
        assert corr.shape == (3, 3)
        assert corr.loc["x", "x"] == pytest.approx(1.0)

    def test_spearman(self, numeric_df: pd.DataFrame) -> None:
        corr = compute_correlation_matrix(numeric_df, method="spearman")
        assert corr.shape == (3, 3)

    def test_kendall(self, numeric_df: pd.DataFrame) -> None:
        corr = compute_correlation_matrix(numeric_df, method="kendall")
        assert corr.shape == (3, 3)

    def test_unknown_method_raises(self, numeric_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="Unknown method"):
            compute_correlation_matrix(numeric_df, method="invalid")

    def test_no_numeric_raises(self) -> None:
        df = pd.DataFrame({"a": ["x", "y"], "b": ["z", "w"]})
        with pytest.raises(ValueError, match="No numeric columns"):
            compute_correlation_matrix(df)


class TestFindTopCorrelations:
    def test_basic(self, numeric_df: pd.DataFrame) -> None:
        top = find_top_correlations(numeric_df, n=5, threshold=0.0)
        assert len(top) > 0
        assert all(isinstance(r, CorrelationResult) for r in top)

    def test_sorted_by_absolute_pearson(self, numeric_df: pd.DataFrame) -> None:
        top = find_top_correlations(numeric_df, n=10)
        for i in range(len(top) - 1):
            assert abs(top[i].pearson) >= abs(top[i + 1].pearson)

    def test_excludes_self(self, numeric_df: pd.DataFrame) -> None:
        top = find_top_correlations(numeric_df, n=10)
        for r in top:
            assert r.col_a != r.col_b

    def test_threshold_filter(self, numeric_df: pd.DataFrame) -> None:
        top = find_top_correlations(numeric_df, n=10, threshold=0.99)
        for r in top:
            assert abs(r.pearson) >= 0.99
