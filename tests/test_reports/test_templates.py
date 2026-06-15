"""Tests for app.reports.templates."""

import pytest

from app.reports.templates import (
    BASIC_TEMPLATE,
    FULL_TEMPLATE,
    TEMPLATES,
    ReportSection,
    ReportTemplate,
    SectionKind,
    get_template,
)


class TestReportTemplate:
    def test_basic_template(self) -> None:
        assert BASIC_TEMPLATE.name == "basic"
        assert SectionKind.SUMMARY in BASIC_TEMPLATE.sections
        assert SectionKind.STATISTICS in BASIC_TEMPLATE.sections

    def test_full_template(self) -> None:
        assert FULL_TEMPLATE.name == "full"
        assert len(FULL_TEMPLATE.sections) == 5

    def test_has_section(self) -> None:
        assert BASIC_TEMPLATE.has_section(SectionKind.SUMMARY)
        assert not BASIC_TEMPLATE.has_section(SectionKind.CORRELATIONS)


class TestGetTemplate:
    def test_known(self) -> None:
        t = get_template("basic")
        assert t is BASIC_TEMPLATE

    def test_unknown_raises(self) -> None:
        with pytest.raises(KeyError, match="Unknown template"):
            get_template("nonexistent")

    def test_all_templates_accessible(self) -> None:
        for name in TEMPLATES:
            t = get_template(name)
            assert isinstance(t, ReportTemplate)


class TestReportSection:
    def test_to_dict(self) -> None:
        section = ReportSection(
            kind=SectionKind.SUMMARY,
            title="Test",
            content={"rows": 10},
        )
        d = section.to_dict()
        assert d["kind"] == "summary"
        assert d["title"] == "Test"
        assert d["content"]["rows"] == 10
