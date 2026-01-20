"""
Report Generation Module for creating customizable analysis summaries.
Supports multiple formats, tones, and focus areas.
"""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from ai_agents.graph import AgentState


class ReportTone(Enum):
    """Tone options for reports."""

    EXECUTIVE = "executive"  # High-level, business-focused
    TECHNICAL = "technical"  # Detailed, technical language
    LEGAL = "legal"  # Formal, legally precise
    CASUAL = "casual"  # Accessible, plain language


class ReportFormat(Enum):
    """Output formats for reports."""

    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"
    TEXT = "text"


class ReportFocus(Enum):
    """Analysis focus areas."""

    RISKS = "risks"  # Emphasize risks
    OPPORTUNITIES = "opportunities"  # Highlight positive aspects
    COMPLIANCE = "compliance"  # Focus on compliance
    FINANCIAL = "financial"  # Emphasize financial impact
    BALANCED = "balanced"  # Equal coverage


class ReportConfig:
    """Configuration for report generation."""

    def __init__(
        self,
        tone: ReportTone = ReportTone.EXECUTIVE,
        format: ReportFormat = ReportFormat.MARKDOWN,
        focus: ReportFocus = ReportFocus.BALANCED,
        include_structured: bool = True,
        include_recommendations: bool = True,
        max_length: Optional[int] = None,
        show_raw_analysis: bool = False,
    ):
        """
        Initialize report configuration.

        Args:
            tone: Report tone style
            format: Output format
            focus: Analysis focus area
            include_structured: Include structured JSON data
            include_recommendations: Include action items
            max_length: Maximum report length (None = no limit)
            show_raw_analysis: Include raw agent outputs
        """
        self.tone = tone
        self.format = format
        self.focus = focus
        self.include_structured = include_structured
        self.include_recommendations = include_recommendations
        self.max_length = max_length
        self.show_raw_analysis = show_raw_analysis


class ReportGenerator:
    """Generate customizable reports from agent analysis results."""

    @staticmethod
    def generate(state: AgentState, config: Optional[ReportConfig] = None) -> str:
        """
        Generate a report from analysis state.

        Args:
            state: AgentState with all analysis results
            config: Report configuration (uses defaults if None)

        Returns:
            Formatted report string
        """
        if config is None:
            config = ReportConfig()

        if config.format == ReportFormat.MARKDOWN:
            return ReportGenerator._generate_markdown(state, config)
        elif config.format == ReportFormat.JSON:
            return ReportGenerator._generate_json(state, config)
        elif config.format == ReportFormat.HTML:
            return ReportGenerator._generate_html(state, config)
        else:
            return ReportGenerator._generate_text(state, config)

    @staticmethod
    def _generate_markdown(state: AgentState, config: ReportConfig) -> str:
        """Generate Markdown format report."""
        parts = []

        # Header
        parts.append("# Contract Analysis Report")
        parts.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        parts.append(f"\n**Analysis Type:** {config.focus.value.title()}")
        parts.append(f"\n**Report Tone:** {config.tone.value.title()}\n")

        # Executive Summary
        parts.append("## Executive Summary\n")
        summary = ReportGenerator._create_executive_summary(state, config)
        parts.append(summary)

        # Legal Analysis
        if state.get("legal"):
            parts.append("\n## Legal Analysis\n")
            parts.append(state["legal"])

            if state.get("legal_clauses") and config.include_structured:
                parts.append("\n### Legal Clauses (Structured)\n")
                parts.append("```json")
                parts.append(json.dumps(state["legal_clauses"], indent=2))
                parts.append("```")

        # Compliance Analysis
        if state.get("compliance"):
            parts.append("\n## Compliance Analysis\n")
            parts.append(state["compliance"])

            if state.get("compliance_risks") and config.include_structured:
                parts.append("\n### Compliance Risks (Structured)\n")
                if isinstance(state["compliance_risks"], dict):
                    data = state["compliance_risks"].get("data", state["compliance_risks"])
                    parts.append(f"**Compliance Score:** {data.get('overall_compliance_score', 'N/A')}/100")
                    if data.get("regulations_violated"):
                        parts.append("\n**Violations:**")
                        for violation in data.get("regulations_violated", []):
                            parts.append(f"- {violation.get('regulation')}: {violation.get('description')}")
                    if data.get("priority_actions"):
                        parts.append("\n**Priority Actions:**")
                        for action in data.get("priority_actions", []):
                            parts.append(
                                f"- [{action.get('urgency')}] {action.get('action')} ({action.get('timeline')})"
                            )

        # Financial Analysis
        if state.get("finance"):
            parts.append("\n## Financial Analysis\n")
            parts.append(state["finance"])

            if state.get("finance_risks") and config.include_structured:
                parts.append("\n### Financial Risks (Structured)\n")
                if isinstance(state["finance_risks"], dict):
                    data = state["finance_risks"].get("data", state["finance_risks"])
                    if data.get("total_exposure_estimate"):
                        parts.append(f"**Total Exposure:** {data.get('total_exposure_estimate')}")
                    if data.get("payment_obligations"):
                        parts.append("\n**Payment Obligations:**")
                        for obligation in data.get("payment_obligations", []):
                            parts.append(f"- {obligation.get('type')}: {obligation.get('amount')} ({obligation.get('frequency')})")

        # Operations Analysis
        if state.get("operations"):
            parts.append("\n## Operations Analysis\n")
            parts.append(state["operations"])

        # Recommendations
        if config.include_recommendations:
            parts.append("\n## Recommendations\n")
            recommendations = ReportGenerator._generate_recommendations(state, config)
            parts.append(recommendations)

        # Raw Analysis (optional)
        if config.show_raw_analysis and state.get("agent_context"):
            parts.append("\n## Raw Agent Findings\n")
            parts.append("```")
            parts.append(state["agent_context"])
            parts.append("```")

        report = "\n".join(parts)

        # Truncate if needed
        if config.max_length and len(report) > config.max_length:
            report = report[: config.max_length] + "\n\n[Report truncated]"

        return report

    @staticmethod
    def _generate_json(state: AgentState, config: ReportConfig) -> str:
        """Generate JSON format report."""
        report_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "tone": config.tone.value,
                "focus": config.focus.value,
            },
            "summary": ReportGenerator._create_executive_summary(state, config),
            "analysis": {
                "legal": state.get("legal"),
                "compliance": state.get("compliance"),
                "finance": state.get("finance"),
                "operations": state.get("operations"),
            },
            "structured_data": {},
        }

        if config.include_structured:
            if state.get("legal_clauses"):
                report_data["structured_data"]["legal_clauses"] = state["legal_clauses"]
            if state.get("compliance_risks"):
                report_data["structured_data"]["compliance_risks"] = (
                    state["compliance_risks"].get("data", state["compliance_risks"])
                    if isinstance(state["compliance_risks"], dict)
                    else state["compliance_risks"]
                )
            if state.get("finance_risks"):
                report_data["structured_data"]["finance_risks"] = (
                    state["finance_risks"].get("data", state["finance_risks"])
                    if isinstance(state["finance_risks"], dict)
                    else state["finance_risks"]
                )

        if config.include_recommendations:
            report_data["recommendations"] = ReportGenerator._get_recommendations_list(state, config)

        return json.dumps(report_data, indent=2)

    @staticmethod
    def _generate_html(state: AgentState, config: ReportConfig) -> str:
        """Generate HTML format report."""
        html_parts = []

        html_parts.append("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Contract Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1, h2 { color: #333; }
        h1 { border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        h2 { margin-top: 30px; color: #0056b3; }
        .section { margin: 20px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #007bff; }
        .risk-high { color: #dc3545; font-weight: bold; }
        .risk-medium { color: #fd7e14; font-weight: bold; }
        .risk-low { color: #28a745; font-weight: bold; }
        .metadata { color: #666; font-size: 0.9em; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f0f0f0; font-weight: bold; }
    </style>
</head>
<body>
<div class="container">""")

        html_parts.append(f"<h1>Contract Analysis Report</h1>")
        html_parts.append(
            f"""<div class="metadata">
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Tone: {config.tone.value.title()} | Focus: {config.focus.value.title()}</p>
</div>"""
        )

        # Executive Summary
        html_parts.append("<h2>Executive Summary</h2>")
        html_parts.append("<div class='section'>")
        html_parts.append(ReportGenerator._create_executive_summary(state, config))
        html_parts.append("</div>")

        # Analysis sections
        for title, key in [("Legal", "legal"), ("Compliance", "compliance"), ("Finance", "finance"), ("Operations", "operations")]:
            if state.get(key):
                html_parts.append(f"<h2>{title} Analysis</h2>")
                html_parts.append("<div class='section'>")
                html_parts.append(state[key].replace("\n", "<br>"))
                html_parts.append("</div>")

        html_parts.append("</div></body></html>")

        return "\n".join(html_parts)

    @staticmethod
    def _generate_text(state: AgentState, config: ReportConfig) -> str:
        """Generate plain text format report."""
        parts = []

        parts.append("=" * 70)
        parts.append("CONTRACT ANALYSIS REPORT")
        parts.append("=" * 70)
        parts.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        parts.append(f"Tone: {config.tone.value.upper()}")
        parts.append(f"Focus: {config.focus.value.upper()}\n")

        parts.append(ReportGenerator._create_executive_summary(state, config))

        for title, key in [("LEGAL", "legal"), ("COMPLIANCE", "compliance"), ("FINANCE", "finance"), ("OPERATIONS", "operations")]:
            if state.get(key):
                parts.append(f"\n{'-' * 70}")
                parts.append(f"{title} ANALYSIS")
                parts.append(f"{'-' * 70}\n")
                parts.append(state[key])

        if config.include_recommendations:
            parts.append(f"\n{'-' * 70}")
            parts.append("RECOMMENDATIONS")
            parts.append(f"{'-' * 70}\n")
            parts.append(ReportGenerator._generate_recommendations(state, config))

        parts.append(f"\n{'=' * 70}")

        return "\n".join(parts)

    @staticmethod
    def _create_executive_summary(state: AgentState, config: ReportConfig) -> str:
        """Create executive summary based on focus and tone."""
        if config.focus == ReportFocus.RISKS:
            return "This contract presents several areas requiring attention. Legal enforceability concerns, compliance gaps, and financial exposure have been identified. Detailed analysis by domain follows."

        elif config.focus == ReportFocus.OPPORTUNITIES:
            return "This contract provides solid terms with manageable risks. Key opportunities for optimization and value creation have been identified. See detailed analysis for specific recommendations."

        elif config.focus == ReportFocus.COMPLIANCE:
            return "Compliance analysis reveals potential regulatory gaps. Data protection, audit requirements, and policy adherence should be addressed before execution."

        elif config.focus == ReportFocus.FINANCIAL:
            return "Financial exposure analysis shows estimated total exposure and payment obligations. Cost optimization opportunities and penalty clauses require attention."

        else:  # BALANCED
            return "This comprehensive analysis evaluates the contract across legal, compliance, financial, and operational dimensions. See each section for detailed findings."

    @staticmethod
    def _get_recommendations_list(state: AgentState, config: ReportConfig) -> List[str]:
        """Generate list of recommendations."""
        recommendations = []

        if state.get("legal"):
            recommendations.append("Review legal enforceability and liability clauses")

        if state.get("compliance_risks"):
            data = state["compliance_risks"]
            if isinstance(data, dict):
                data = data.get("data", data)
                if data.get("priority_actions"):
                    for action in data.get("priority_actions", []):
                        recommendations.append(action.get("action", "Action item"))

        if state.get("finance_risks"):
            data = state["finance_risks"]
            if isinstance(data, dict):
                data = data.get("data", data)
                if data.get("mitigation_needed"):
                    recommendations.append("Address uncapped liability provisions")

        if state.get("operations"):
            recommendations.append("Validate operational feasibility of SLA commitments")

        return recommendations

    @staticmethod
    def _generate_recommendations(state: AgentState, config: ReportConfig) -> str:
        """Generate detailed recommendations section."""
        recommendations = ReportGenerator._get_recommendations_list(state, config)

        if not recommendations:
            return "No specific recommendations at this time."

        parts = []
        for i, rec in enumerate(recommendations, 1):
            parts.append(f"{i}. {rec}")

        return "\n".join(parts)


def create_report(state: AgentState, tone: str = "executive", format_type: str = "markdown") -> str:
    """
    Convenience function to create a report.

    Args:
        state: AgentState with analysis results
        tone: Report tone (executive, technical, legal, casual)
        format_type: Output format (markdown, json, html, text)

    Returns:
        Formatted report
    """
    tone_enum = ReportTone[tone.upper()]
    format_enum = ReportFormat[format_type.upper()]

    config = ReportConfig(tone=tone_enum, format=format_enum)
    return ReportGenerator.generate(state, config)


__all__ = ["ReportGenerator", "ReportConfig", "ReportTone", "ReportFormat", "ReportFocus", "create_report"]
