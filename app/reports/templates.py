"""Report templates and section builders."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SectionKind(Enum):
    SUMMARY = "summary"
    STATISTICS = "statistics"
    CORRELATIONS = "correlations"
    OUTLIERS = "outliers"
    CHART = "chart"
    CUSTOM = "custom"


@dataclass
class ReportSection:
    """One section of a generated report."""

    kind: SectionKind
    title: str
    content: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind.value, "title": self.title, "content": self.content}


@dataclass
class ReportTemplate:
    """Describes which sections a report should contain."""

    name: str
    description: str
    sections: list[SectionKind] = field(default_factory=list)

    def has_section(self, kind: SectionKind) -> bool:
        return kind in self.sections


BASIC_TEMPLATE = ReportTemplate(
    name="basic",
    description="Quick overview with summary statistics",
    sections=[SectionKind.SUMMARY, SectionKind.STATISTICS],
)

FULL_TEMPLATE = ReportTemplate(
    name="full",
    description="Comprehensive analysis report",
    sections=[
        SectionKind.SUMMARY,
        SectionKind.STATISTICS,
        SectionKind.CORRELATIONS,
        SectionKind.OUTLIERS,
        SectionKind.CHART,
    ],
)

TEMPLATES: dict[str, ReportTemplate] = {
    "basic": BASIC_TEMPLATE,
    "full": FULL_TEMPLATE,
}


def get_template(name: str) -> ReportTemplate:
    """Return a named template. Raises ``KeyError`` if not found."""
    if name not in TEMPLATES:
        raise KeyError(f"Unknown template: {name!r}. Available: {list(TEMPLATES)}")
    return TEMPLATES[name]
