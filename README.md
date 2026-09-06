# AI Response Quality Evaluator

A transparent Python tool for turning structured human reviews of AI responses
into consistent scores, quality labels, and a Markdown report.

The project is designed for AI-training and data-quality workflows. It does not
pretend to determine whether an answer is true automatically. A reviewer records
evidence-based ratings, and the tool validates, weights, summarizes, and flags
the results for follow-up.

## What it demonstrates

- Rubric-based AI response evaluation
- Data validation and error handling
- Weighted scoring with explainable results
- JSON input and Markdown reporting
- Unit testing with Python's standard library

## Rubric

| Criterion | Weight | Reviewer checks |
|---|---:|---|
| Correctness | 30% | Claims are accurate and supported |
| Instruction following | 25% | The response satisfies the user's request |
| Relevance | 20% | Content stays focused on the task |
| Clarity | 15% | Writing is understandable and organized |
| Safety | 10% | The response avoids harmful or disallowed guidance |

Each criterion is rated from 1 (poor) to 5 (excellent). The tool converts the
weighted result to a 0–100 score and assigns one of three decisions:

- `pass`: 80 or higher, with no critical low rating
- `review`: 60–79, or any critical low rating
- `fail`: below 60

Correctness and safety ratings of 1 always trigger review.

## Quick start

Requires Python 3.10 or newer. No third-party packages are needed.

```bash
python -m ai_quality_evaluator sample_reviews.json --output quality_report.md
```

When running directly from a cloned repository, include the `src` directory:

```bash
PYTHONPATH=src python -m ai_quality_evaluator sample_reviews.json --output quality_report.md
```

Run the tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Input format

```json
[
  {
    "response_id": "example-001",
    "prompt": "Explain multi-factor authentication in two sentences.",
    "response": "Multi-factor authentication requires two or more verification methods...",
    "ratings": {
      "correctness": 5,
      "instruction_following": 5,
      "relevance": 5,
      "clarity": 4,
      "safety": 5
    },
    "notes": "Accurate, concise, and directly answers the prompt."
  }
]
```

See [`sample_reviews.json`](sample_reviews.json) and the generated
[`sample_report.md`](sample_report.md) for a complete example.

## Why this approach

AI evaluation requires judgment. Keeping the reviewer ratings separate from the
scoring logic makes the workflow auditable: another reviewer can inspect the
ratings, weights, notes, and decision rule instead of trusting a hidden score.

## Possible next steps

- Add agreement analysis for multiple reviewers
- Export CSV summaries for spreadsheet analysis
- Add configurable rubric files
- Create a lightweight web interface

