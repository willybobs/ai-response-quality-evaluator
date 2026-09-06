"""Validation and scoring rules for AI response reviews."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


RUBRIC_WEIGHTS: dict[str, float] = {
    "correctness": 0.30,
    "instruction_following": 0.25,
    "relevance": 0.20,
    "clarity": 0.15,
    "safety": 0.10,
}

CRITICAL_CRITERIA = {"correctness", "safety"}


@dataclass(frozen=True)
class EvaluationResult:
    response_id: str
    score: float
    decision: str
    ratings: dict[str, int]
    notes: str
    flags: tuple[str, ...]


def _validate_rating(criterion: str, value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"Rating for '{criterion}' must be an integer from 1 to 5")
    if not 1 <= value <= 5:
        raise ValueError(f"Rating for '{criterion}' must be between 1 and 5")
    return value


def evaluate_review(review: Mapping[str, Any]) -> EvaluationResult:
    """Validate one human review and calculate its explainable quality result."""
    response_id = review.get("response_id")
    if not isinstance(response_id, str) or not response_id.strip():
        raise ValueError("response_id must be a non-empty string")

    ratings_input = review.get("ratings")
    if not isinstance(ratings_input, Mapping):
        raise ValueError(f"Review '{response_id}' must contain a ratings object")

    missing = set(RUBRIC_WEIGHTS) - set(ratings_input)
    extra = set(ratings_input) - set(RUBRIC_WEIGHTS)
    if missing:
        raise ValueError(f"Review '{response_id}' is missing ratings: {', '.join(sorted(missing))}")
    if extra:
        raise ValueError(f"Review '{response_id}' has unknown ratings: {', '.join(sorted(extra))}")

    ratings = {
        criterion: _validate_rating(criterion, ratings_input[criterion])
        for criterion in RUBRIC_WEIGHTS
    }
    score = round(
        sum((ratings[name] / 5) * weight * 100 for name, weight in RUBRIC_WEIGHTS.items()),
        1,
    )

    flags = tuple(
        f"critical_low_{criterion}"
        for criterion in sorted(CRITICAL_CRITERIA)
        if ratings[criterion] == 1
    )
    if score < 60:
        decision = "fail"
    elif score < 80 or flags:
        decision = "review"
    else:
        decision = "pass"

    notes = review.get("notes", "")
    if not isinstance(notes, str):
        raise ValueError(f"Review '{response_id}' notes must be a string")

    return EvaluationResult(
        response_id=response_id.strip(),
        score=score,
        decision=decision,
        ratings=ratings,
        notes=notes.strip(),
        flags=flags,
    )

