---
name: aws-evals
description: >
  Use when validating AWS architecture guidance quality through deterministic evaluation prompts and pass/fail rubrics
  for associate, trade-off, professional, and failure-analysis scenarios.
---

Note: This is the active Codex skills suite; ignore /skills/aws-sap-c02-architect/ (legacy).

# AWS Evaluations

## Purpose
Provide a repeatable, auditable way to evaluate whether architecture outputs meet the expected quality bar for AWS Solutions Architect Associate + Professional style reasoning.

## When to use
- You need to test architecture quality before relying on outputs.
- You want deterministic prompt packs and clear grading criteria.
- You need evaluation notes captured under `docs/architecture/reviews/`.

## When NOT to use
- You are actively designing a solution (use architecture-producing skills first).
- You need only one-off brainstorming without formal scoring.
- You are debugging implementation code.

## Inputs to request
- Target system name (if evaluation is system-scoped).
- Scenario(s) to run: `associate`, `bridge`, `professional`, `failure`, or `all`.
- Evaluation notes source (`--notes`, `--notes-file`, or `--interactive`).
- Any domain constraints to apply during grading.

## Required workflow
1. Review scenarios and rubric in `references/evals.md`.
2. Run `scripts/run_evals.py --scenario <scenario> ...`.
3. Save evaluation notes to `docs/architecture/reviews/EVAL-NOTES-YYYYMMDD.md`.
4. If `--system` is used, ensure manifest is updated at `docs/architecture/manifest/<system>.yaml`.

## Decision workflow
1. Choose scenario(s) based on maturity gate needed.
2. Run prompts exactly as written to reduce evaluator drift.
3. Grade using explicit pass/fail rubric criteria only.
4. Record findings, misses, and remediation actions.
5. Link severe misses to ADR or architecture review follow-up actions.

## Rules & guardrails
- Must use scenario prompts and rubrics as written unless a documented variant is required.
- Must record objective evidence for each pass/fail decision.
- Must not pass a scenario with missing mandatory criteria.
- Should run all four scenarios for major architecture milestones.

## Output format
Use this exact structure:
1. Requirements & Assumptions
2. Proposed Architecture
3. Well-Architected Pillar Review (6 pillars)
4. Key Decisions & Trade-offs (link to ADRs if created)
5. Risks / Failure Modes
6. Implementation Notes (services + key configs)
7. Next Steps / Validation Checks (include scripts to run)

## Reference index
- `references/evals.md`
