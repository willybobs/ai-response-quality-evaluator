"""Command-line interface for the AI response quality evaluator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .evaluator import evaluate_review
from .reporting import build_markdown_report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Score human-reviewed AI responses with a transparent rubric."
    )
    parser.add_argument("input", type=Path, help="JSON file containing a list of reviews")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("quality_report.md"),
        help="Markdown report path (default: quality_report.md)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError("Input must be a JSON list of reviews")
        results = [evaluate_review(review) for review in raw]
        report = build_markdown_report(results)
        args.output.write_text(report, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1

    print(f"Evaluated {len(results)} responses. Report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

