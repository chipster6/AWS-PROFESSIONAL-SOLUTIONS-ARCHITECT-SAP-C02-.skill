# Evaluation Execution Checklist

## Goal
Run architecture evaluations consistently and capture auditable outcomes.

## Pre-run checks
- Confirm scenario(s) to execute: `associate`, `bridge`, `professional`, `failure`, or `all`.
- Confirm whether evaluation is system-scoped (`--system <name>`).
- Confirm notes input source: `--notes`, `--notes-file`, or `--interactive`.

## Execution steps
1. Run `scripts/run_evals.py --scenario <scenario> ...`.
2. Capture prompt output and rubric text for traceability.
3. Record evaluator notes with objective pass/fail evidence.
4. Verify output file exists at `docs/architecture/reviews/EVAL-NOTES-YYYYMMDD.md`.
5. If system-scoped, verify manifest update at `docs/architecture/manifest/<system>.yaml`.

## Grading discipline
- Grade against explicit rubric criteria only.
- Mark mandatory misses even when overall answer quality seems high.
- Tie every failed criterion to a concrete remediation action.
- Re-run scenario after remediation to confirm closure.

## Anti-patterns
- Subjective scoring without rubric evidence.
- Passing scenarios with missing mandatory criteria.
- Running prompts with altered wording without noting the variant.
- Capturing notes outside the canonical reviews path.

## Acceptance criteria
- Evaluation notes file exists with scenario, prompt, rubric, and findings.
- Pass/fail decisions include objective evidence.
- Manifest action log is updated when `--system` is provided.
