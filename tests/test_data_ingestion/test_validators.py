"""Tests for app.data_ingestion.validators."""

import numpy as np
import pandas as pd
import pytest

from app.data_ingestion.validators import ValidationReport, clean_dataframe, validate_dataframe


class TestValidateDataframe:
    def test_basic_valid(self, sample_df: pd.DataFrame) -> None:
        report = validate_dataframe(sample_df)
        assert isinstance(report, ValidationReport)
        assert report.row_count == 5
        assert report.column_count == 4
        assert report.missing_cells == 0
        assert report.missing_pct == 0.0
        assert "age" in report.numeric_columns
        assert "grade" in report.categorical_columns

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            validate_dataframe(pd.DataFrame())

    def test_too_many_missing_raises(self) -> None:
        df = pd.DataFrame({"a": [np.nan, np.nan, 1.0], "b": [np.nan, np.nan, np.nan]})
        with pytest.raises(ValueError, match="Too many missing"):
            validate_dataframe(df, max_missing_pct=50.0)

    def test_high_missing_warning(self) -> None:
        df = pd.DataFrame({"a": [1, 2, 3, np.nan, np.nan], "b": [10, 20, 30, 40, 50]})
        report = validate_dataframe(df, max_missing_pct=50.0)
        assert report.missing_pct == 20.0
        assert any("missing" in w.lower() for w in report.warnings)

    def test_duplicate_rows_warning(self) -> None:
        df = pd.DataFrame({"a": [1, 1, 2], "b": [10, 10, 20]})
        report = validate_dataframe(df)
        assert report.duplicate_rows == 1
        assert any("duplicate" in w.lower() for w in report.warnings)


class TestCleanDataframe:
    def test_drops_duplicates(self) -> None:
        df = pd.DataFrame({"a": [1, 1, 2], "b": [10, 10, 20]})
        cleaned = clean_dataframe(df)
        assert len(cleaned) == 2

    def test_fills_numeric_median(self) -> None:
        df = pd.DataFrame({"val": [1.0, 2.0, np.nan, 4.0, 5.0]})
        cleaned = clean_dataframe(df, fill_strategy="median")
        assert not cleaned["val"].isna().any()
        assert cleaned["val"].iloc[2] == 3.0

    def test_fills_numeric_mean(self) -> None:
        df = pd.DataFrame({"val": [1.0, 2.0, np.nan, 4.0, 5.0]})
        cleaned = clean_dataframe(df, fill_strategy="mean")
        assert not cleaned["val"].isna().any()
        assert cleaned["val"].iloc[2] == 3.0

    def test_fills_categorical_mode(self) -> None:
        df = pd.DataFrame({"cat": ["a", "a", "b", None]})
        cleaned = clean_dataframe(df, drop_duplicates=False)
        assert cleaned["cat"].iloc[3] == "a"

    def test_unknown_strategy_raises(self) -> None:
        df = pd.DataFrame({"val": [1.0]})
        with pytest.raises(ValueError, match="Unknown fill_strategy"):
            clean_dataframe(df, fill_strategy="invalid")

    def test_no_duplicate_drop(self) -> None:
        df = pd.DataFrame({"a": [1, 1, 2]})
        cleaned = clean_dataframe(df, drop_duplicates=False)
        assert len(cleaned) == 3
