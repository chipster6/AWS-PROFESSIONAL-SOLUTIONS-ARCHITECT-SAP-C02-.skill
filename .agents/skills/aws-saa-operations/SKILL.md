---
name: aws-saa-operations
description: >
  Use when defining AWS operational architecture at associate level, including observability,
  incident response, backup/restore readiness, and deterministic architecture workflow execution
  with ADR-linked validation outputs.
---

Note: This is the active Codex skills suite; ignore /skills/aws-sap-c02-architect/ (legacy).

# AWS SAA Operations

## Purpose
Design and validate an operational baseline for AWS workloads so reliability, recoverability, and incident handling are explicit and testable.

## When to use
- The request focuses on run reliability, monitoring, incident handling, or operational readiness.
- The architecture exists but operational controls and runbooks are incomplete.
- The user wants deterministic validation for operations-related architecture artifacts.

## When NOT to use
- The request is greenfield architecture service selection only (use `aws-saa-architecture`).
- The request is enterprise governance, migration/DR specialization, or cost governance specialization.
- The request is only foundational AWS concepts.

## Inputs to request
- SLO/SLA targets and error budget.
- On-call model and escalation expectations.
- Recovery targets (RTO/RPO) and backup compliance constraints.
- Critical dependencies and business impact tiers.

## Required workflow
Run in strict order:
1. `scripts/init_arch_workflow.py --system <system>`
2. Create/update solution overview including operations assumptions and `MAJOR_DECISION` markers.
3. Create operational ADRs via `scripts/new_adr.py`.
4. Generate WA review via `scripts/wa_review.py`.
5. Run `scripts/validate_archifacts.py`.
6. Run `scripts/decision_trace.py`.

## Decision workflow
1. Define observability model (signals, SLOs, alerts, dashboards).
2. Define incident handling workflow and ownership.
3. Define backup/restore and continuity controls.
4. Record major operational decisions as ADRs.
5. Validate with WA pillar checks and gate outputs.

## Rules & guardrails
- Must create ADRs for: datastore class/engine family choices, sync vs async integration model choices, trust boundary/auth model choices, network topology/segmentation/egress/endpoint choices, RTO/RPO and DR posture choices, region/account/partition strategy choices, and major cost model commitments.
- Must include explicit alert ownership and escalation paths.
- Must define recovery procedures and test cadence.
- Must use canonical marker grammar:
  `MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`
- Must execute validation before final recommendations.
- Must not claim operational readiness without runbook evidence.

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
- `references/observability-baseline.md`
- `references/incident-response-checklist.md`
- `references/backup-restore-checklist.md`
- `references/ops-security-checklist.md`
