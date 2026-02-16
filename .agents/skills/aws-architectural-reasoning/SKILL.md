---
name: aws-architectural-reasoning
description: >
  Use when comparing AWS architecture options, quantifying trade-offs across Well-Architected
  pillars, and producing explicit decision rationale with failure-mode-first analysis.
---

Note: This is the active Codex skills suite; ignore /skills/aws-sap-c02-architect/ (legacy).

# AWS Architectural Reasoning

## Purpose
Provide rigorous, repeatable reasoning for architecture trade-offs so decisions are explicit, testable, and auditable.

## When to use
- Multiple valid architecture options exist and trade-offs are unclear.
- A design review needs stronger rationale, risk analysis, or challenge testing.
- The user asks for option comparison, decision confidence, or failure-mode analysis.

## When NOT to use
- The request is only first-principles systems fundamentals.
- The request is mostly implementation mechanics without architecture alternatives.
- The request is a pure operations runbook task.

## Inputs to request
- Requirements, constraints, and explicit non-goals.
- SLO/SLA, RTO/RPO, security/compliance constraints.
- Expected load profile and growth assumptions.
- Cost sensitivity, delivery timeline, and team capability constraints.

## Required workflow
1. Define decision scope and candidate options.
2. Evaluate each option across all 6 WA pillars.
3. Score risks, reversibility, and operational complexity.
4. Identify anti-patterns and failure modes per option.
5. Recommend option with explicit residual risks and validation plan.

## Decision workflow
1. Normalize assumptions.
2. Compare options with a weighted trade-off table.
3. Challenge each option with plausible failure scenarios.
4. Assess reversibility and migration effort if wrong.
5. Select preferred option with acceptance criteria.

## Rules & guardrails
- Must include all 6 WA pillars in comparisons.
- Must call out where Security and Operational Excellence are non-negotiable controls.
- Must show why rejected options were rejected.
- Must not hide unresolved assumptions; label them explicitly.

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
- `references/tradeoff-framework.md`
- `references/anti-pattern-catalog.md`
- `references/failure-analysis-checklist.md`
- `references/decision-quality-rubric.md`
