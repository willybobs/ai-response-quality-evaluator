"""Rubric-based quality evaluation for human-reviewed AI responses."""

from .evaluator import EvaluationResult, evaluate_review

__all__ = ["EvaluationResult", "evaluate_review"]
