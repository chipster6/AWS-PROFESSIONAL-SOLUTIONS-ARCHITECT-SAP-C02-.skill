---
name: aws-systems-fundamentals
description: >
  Use when framing core distributed-systems fundamentals before selecting AWS services,
  including failure domains, state management, sync-vs-async trade-offs, and CAP-informed
  consistency decisions.
---

Note: This is the active Codex skills suite; ignore /skills/aws-sap-c02-architect/ (legacy).

# AWS Systems Fundamentals

## Purpose
Establish the baseline systems reasoning needed before cloud-service selection so architecture decisions are defensible and consistent.

## When to use
- The request is still at first-principles level.
- The user needs help reasoning about reliability, latency, consistency, or coupling.
- Service selection would be premature without core system constraints.

## When NOT to use
- The request is explicitly about AWS product/service choices (use `aws-aws-foundations` or higher-layer skills).
- The task is implementation-only without architecture decisions.

## Inputs to request
- Workload type and critical path.
- Availability, latency, throughput, and consistency expectations.
- State model (ephemeral, durable, transactional, event-sourced).
- Failure tolerance and blast-radius constraints.

## Required workflow
1. Identify system invariants and non-negotiables.
2. Map failure domains and likely partial-failure modes.
3. Clarify required consistency behavior and latency budgets.
4. Recommend high-level architectural style constraints before AWS service mapping.

## Decision workflow
1. Define data criticality and acceptable staleness.
2. Decide sync vs async communication boundaries.
3. Decide state ownership and recovery boundaries.
4. Validate CAP trade-offs against business requirements.
5. Produce candidate patterns and explicit risks.

## Rules & guardrails
- Must separate assumptions from verified requirements.
- Must express trade-offs; must not claim all dimensions can be maximized simultaneously.
- Should identify failure handling and fallback behavior explicitly.
- Must not jump to specific AWS services unless requested.

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
- `references/failure-domains-and-blast-radius.md`
- `references/stateful-vs-stateless.md`
- `references/sync-vs-async-latency-throughput.md`
- `references/cap-and-consistency-primer.md`
