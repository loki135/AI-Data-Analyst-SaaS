"""Tests for app.reports.generator – ReportGenerator."""

import pandas as pd
import pytest

from app.reports.generator import Report, ReportGenerator
from app.reports.templates import SectionKind


@pytest.fixture()
def gen() -> ReportGenerator:
    return ReportGenerator()


class TestGenerate:
    def test_full_report(self, gen: ReportGenerator, numeric_df: pd.DataFrame) -> None:
        report = gen.generate(numeric_df, template_name="full", title="Test Report")
        assert isinstance(report, Report)
        assert report.title == "Test Report"
        assert report.template_name == "full"
        assert report.generated_at  # non-empty ISO timestamp
        kinds = {s.kind for s in report.sections}
        assert SectionKind.SUMMARY in kinds
        assert SectionKind.STATISTICS in kinds
        assert SectionKind.CORRELATIONS in kinds
        assert SectionKind.OUTLIERS in kinds

    def test_basic_report(self, gen: ReportGenerator, numeric_df: pd.DataFrame) -> None:
        report = gen.generate(numeric_df, template_name="basic")
        kinds = {s.kind for s in report.sections}
        assert SectionKind.SUMMARY in kinds
        assert SectionKind.STATISTICS in kinds
        assert SectionKind.CORRELATIONS not in kinds

    def test_unknown_template_raises(self, gen: ReportGenerator, numeric_df: pd.DataFrame) -> None:
        with pytest.raises(KeyError, match="Unknown template"):
            gen.generate(numeric_df, template_name="nonexistent")

    def test_summary_section_content(self, gen: ReportGenerator, numeric_df: pd.DataFrame) -> None:
        report = gen.generate(numeric_df, template_name="full")
        summary = next(s for s in report.sections if s.kind == SectionKind.SUMMARY)
        assert summary.content["rows"] == len(numeric_df)
        assert summary.content["columns"] == len(numeric_df.columns)

    def test_statistics_section_content(
        self, gen: ReportGenerator, numeric_df: pd.DataFrame
    ) -> None:
        report = gen.generate(numeric_df, template_name="full")
        stats = next(s for s in report.sections if s.kind == SectionKind.STATISTICS)
        assert len(stats.content["stats"]) == 3

    def test_to_dict(self, gen: ReportGenerator, numeric_df: pd.DataFrame) -> None:
        report = gen.generate(numeric_df, template_name="basic")
        d = report.to_dict()
        assert d["title"] == "Analysis Report"
        assert isinstance(d["sections"], list)
        assert isinstance(d["charts"], list)
