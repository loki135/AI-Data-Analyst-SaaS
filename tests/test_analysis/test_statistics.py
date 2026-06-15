"""Tests for app.analysis.statistics."""

import numpy as np
import pandas as pd
import pytest

from app.analysis.statistics import (
    ColumnStats,
    compute_column_stats,
    compute_dataframe_stats,
    detect_outliers_iqr,
)


class TestComputeColumnStats:
    def test_basic(self) -> None:
        s = pd.Series([1, 2, 3, 4, 5], name="vals")
        stats = compute_column_stats(s)
        assert isinstance(stats, ColumnStats)
        assert stats.name == "vals"
        assert stats.count == 5
        assert stats.mean == 3.0
        assert stats.median == 3.0
        assert stats.min == 1.0
        assert stats.max == 5.0

    def test_non_numeric_raises(self) -> None:
        s = pd.Series(["a", "b", "c"], name="text")
        with pytest.raises(TypeError, match="not numeric"):
            compute_column_stats(s)

    def test_all_nan_raises(self) -> None:
        s = pd.Series([np.nan, np.nan], name="empty")
        with pytest.raises(ValueError, match="no non-null"):
            compute_column_stats(s)

    def test_skewness_kurtosis(self) -> None:
        s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], name="x")
        stats = compute_column_stats(s)
        assert abs(stats.skewness) < 0.1  # roughly symmetric
        assert isinstance(stats.kurtosis, float)


class TestComputeDataframeStats:
    def test_returns_stats_for_numeric(self, numeric_df: pd.DataFrame) -> None:
        results = compute_dataframe_stats(numeric_df)
        assert len(results) == 3
        names = {r.name for r in results}
        assert names == {"x", "y", "z"}

    def test_skips_all_nan_columns(self) -> None:
        df = pd.DataFrame({"good": [1, 2, 3], "bad": [np.nan, np.nan, np.nan]})
        results = compute_dataframe_stats(df)
        assert len(results) == 1
        assert results[0].name == "good"


class TestDetectOutliersIQR:
    def test_basic_outliers(self) -> None:
        s = pd.Series([1, 2, 3, 4, 5, 100], name="vals")
        mask = detect_outliers_iqr(s)
        assert mask.iloc[-1]  # 100 should be an outlier
        assert not mask.iloc[0]

    def test_non_numeric_raises(self) -> None:
        s = pd.Series(["a", "b"], name="cat")
        with pytest.raises(TypeError, match="not numeric"):
            detect_outliers_iqr(s)

    def test_no_outliers(self) -> None:
        s = pd.Series([1, 2, 3, 4, 5], name="uniform")
        mask = detect_outliers_iqr(s)
        assert not mask.any()
