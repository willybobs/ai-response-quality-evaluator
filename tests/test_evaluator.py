import unittest

from ai_quality_evaluator import evaluate_review


def review_with(**rating_overrides):
    ratings = {
        "correctness": 5,
        "instruction_following": 5,
        "relevance": 5,
        "clarity": 5,
        "safety": 5,
    }
    ratings.update(rating_overrides)
    return {"response_id": "case-1", "ratings": ratings, "notes": "Reviewed."}


class EvaluateReviewTests(unittest.TestCase):
    def test_perfect_review_passes(self):
        result = evaluate_review(review_with())
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.decision, "pass")
        self.assertEqual(result.flags, ())

    def test_midrange_score_requires_review(self):
        result = evaluate_review(review_with(correctness=3, instruction_following=3))
        self.assertEqual(result.score, 78.0)
        self.assertEqual(result.decision, "review")

    def test_critical_low_rating_prevents_pass(self):
        result = evaluate_review(review_with(safety=1))
        self.assertEqual(result.score, 92.0)
        self.assertEqual(result.decision, "review")
        self.assertIn("critical_low_safety", result.flags)

    def test_invalid_rating_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 5"):
            evaluate_review(review_with(clarity=6))

    def test_missing_criterion_is_rejected(self):
        review = review_with()
        del review["ratings"]["relevance"]
        with self.assertRaisesRegex(ValueError, "missing ratings: relevance"):
            evaluate_review(review)


if __name__ == "__main__":
    unittest.main()
