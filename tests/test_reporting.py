import unittest

from ai_quality_evaluator import evaluate_review
from ai_quality_evaluator.reporting import build_markdown_report


class ReportingTests(unittest.TestCase):
    def test_report_contains_summary_and_result(self):
        result = evaluate_review(
            {
                "response_id": "report-1",
                "ratings": {
                    "correctness": 5,
                    "instruction_following": 5,
                    "relevance": 4,
                    "clarity": 4,
                    "safety": 5,
                },
                "notes": "Clear and accurate.",
            }
        )
        report = build_markdown_report([result])
        self.assertIn("Responses reviewed: 1", report)
        self.assertIn("| report-1 | 93.0 | pass |", report)
        self.assertIn("Clear and accurate.", report)

    def test_empty_result_list_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "At least one"):
            build_markdown_report([])


if __name__ == "__main__":
    unittest.main()
