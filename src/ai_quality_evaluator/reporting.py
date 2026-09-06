"""Markdown reporting for evaluated AI response reviews."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from .evaluator import EvaluationResult, RUBRIC_WEIGHTS


def build_markdown_report(results: Iterable[EvaluationResult]) -> str:
    items = list(results)
    if not items:
        raise ValueError("At least one evaluation result is required")

    counts = Counter(item.decision for item in items)
    average = round(sum(item.score for item in items) / len(items), 1)
    lines = [
        "# AI Response Quality Report",
        "",
        "## Summary",
        "",
        f"- Responses reviewed: {len(items)}",
        f"- Average score: {average}/100",
        f"- Pass: {counts['pass']}",
        f"- Review: {counts['review']}",
        f"- Fail: {counts['fail']}",
        "",
        "## Results",
        "",
        "| Response ID | Score | Decision | Flags |",
        "|---|---:|---|---|",
    ]
    for item in items:
        flags = ", ".join(item.flags) if item.flags else "—"
        lines.append(f"| {item.response_id} | {item.score:.1f} | {item.decision} | {flags} |")

    lines.extend(["", "## Detailed reviews", ""])
    for item in items:
        lines.extend(
            [
                f"### {item.response_id}",
                "",
                f"**Decision:** {item.decision}  ",
                f"**Score:** {item.score:.1f}/100",
                "",
                "| Criterion | Weight | Rating |",
                "|---|---:|---:|",
            ]
        )
        for criterion, weight in RUBRIC_WEIGHTS.items():
            label = criterion.replace("_", " ").title()
            lines.append(f"| {label} | {weight:.0%} | {item.ratings[criterion]}/5 |")
        lines.extend(["", f"**Reviewer notes:** {item.notes or 'None provided.'}", ""])

    return "\n".join(lines).rstrip() + "\n"

