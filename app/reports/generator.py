"""Report generator – assembles sections from analysis results."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from app.analysis.service import AnalysisResult, AnalysisService
from app.reports.templates import (
    ReportSection,
    ReportTemplate,
    SectionKind,
    get_template,
)
from app.visualization.charts import ChartSpec


@dataclass
class Report:
    """A fully assembled report."""

    title: str
    template_name: str
    generated_at: str
    sections: list[ReportSection] = field(default_factory=list)
    charts: list[ChartSpec] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "template": self.template_name,
            "generated_at": self.generated_at,
            "sections": [s.to_dict() for s in self.sections],
            "charts": [c.to_dict() for c in self.charts],
        }


class ReportGenerator:
    """Build reports by combining analysis results with a template."""

    def __init__(self) -> None:
        self._analysis = AnalysisService()

    def generate(
        self,
        df: pd.DataFrame,
        template_name: str = "full",
        title: str = "Analysis Report",
    ) -> Report:
        """Generate a report for *df* using the named template."""
        template = get_template(template_name)
        analysis = self._analysis.full_analysis(df)
        report = Report(
            title=title,
            template_name=template_name,
            generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        self._fill_sections(report, template, df, analysis)
        return report

    def _fill_sections(
        self,
        report: Report,
        template: ReportTemplate,
        df: pd.DataFrame,
        analysis: AnalysisResult,
    ) -> None:
        for kind in template.sections:
            section = self._build_section(kind, df, analysis)
            if section is not None:
                report.sections.append(section)

    def _build_section(
        self,
        kind: SectionKind,
        df: pd.DataFrame,
        analysis: AnalysisResult,
    ) -> ReportSection | None:
        if kind == SectionKind.SUMMARY:
            return ReportSection(
                kind=kind,
                title="Dataset Summary",
                content={
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": df.columns.tolist(),
                    "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
                },
            )
        if kind == SectionKind.STATISTICS:
            return ReportSection(
                kind=kind,
                title="Descriptive Statistics",
                content={
                    "stats": [
                        {
                            "name": s.name,
                            "mean": s.mean,
                            "median": s.median,
                            "std": s.std,
                            "min": s.min,
                            "max": s.max,
                        }
                        for s in analysis.column_stats
                    ]
                },
            )
        if kind == SectionKind.CORRELATIONS:
            return ReportSection(
                kind=kind,
                title="Top Correlations",
                content={
                    "correlations": [
                        {
                            "col_a": c.col_a,
                            "col_b": c.col_b,
                            "pearson": c.pearson,
                            "spearman": c.spearman,
                        }
                        for c in analysis.top_correlations
                    ]
                },
            )
        if kind == SectionKind.OUTLIERS:
            return ReportSection(
                kind=kind,
                title="Outlier Summary",
                content={"outlier_counts": analysis.outlier_counts},
            )
        return None
