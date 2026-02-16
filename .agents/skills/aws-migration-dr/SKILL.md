---
name: aws-migration-dr
description: >
  Use when planning AWS migration strategy and disaster recovery architecture, including
  migration-wave execution, RTO/RPO-driven DR pattern selection, and auditable recovery decisions.
---

Note: This is the active Codex skills suite; ignore /skills/aws-sap-c02-architect/ (legacy).

# AWS Migration and DR

## Purpose
Design migration and disaster recovery strategy with explicit trade-offs, measurable objectives, and auditable artifacts.

## When to use
- The request involves cloud migration strategy selection (7 Rs, wave planning, cutover).
- The request includes DR posture, failover design, or RTO/RPO mapping.
- The architecture needs migration + continuity sequencing.

## When NOT to use
- The request is enterprise governance-only without migration/DR scope.
- The request is purely operations incident handling.
- The request is only cost governance.

## Inputs to request
- Workload inventory and dependency map.
- Migration constraints (downtime, refactor tolerance, compliance).
- Recovery objectives (RTO/RPO) by system tier.
- Cutover windows and rollback tolerance.

## Required workflow
Run in strict order:
1. `scripts/init_arch_workflow.py --system <system>`
2. Create/update solution overview with canonical `MAJOR_DECISION` markers.
3. Create required ADRs via `scripts/new_adr.py`.
4. Generate WA review via `scripts/wa_review.py`.
5. Validate artifacts via `scripts/validate_archifacts.py`.
6. Generate decision trace via `scripts/decision_trace.py`.

## Decision workflow
1. Choose migration strategy per workload segment.
2. Define migration waves, readiness gates, and cutover criteria.
3. Map RTO/RPO to DR strategy (backup/restore, pilot light, warm standby, active-active).
4. Define testing and failback strategy.
5. Record major decisions and validate gates.

## Rules & guardrails
- Must create ADRs for: datastore class/engine family choices, sync vs async integration model choices, trust boundary/auth model choices, network topology/segmentation/egress/endpoint choices, RTO/RPO and DR posture choices, region/account/partition strategy choices, and major cost model commitments.
- Must use canonical marker:
  `MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`
- Must avoid control-plane-heavy failover patterns where data-plane alternatives exist.
- Must include explicit rollback/failback conditions.

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
- `references/migration-strategy-chooser.md`
- `references/rto-rpo-to-dr-chooser.md`
- `references/dr-patterns-and-tradeoffs.md`
- `references/migration-wave-and-cutover.md`
- `references/dr-testing-checklist.md`
