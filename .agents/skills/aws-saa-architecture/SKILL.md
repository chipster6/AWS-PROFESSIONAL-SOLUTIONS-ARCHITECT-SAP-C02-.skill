---
name: aws-saa-architecture
description: >
  Use when designing AWS solution architectures at associate level and producing deterministic,
  auditable outputs under docs/architecture using shared workflow scripts and ADR-linked decisions.
---

Note: This is the active Codex skills suite; ignore /skills/aws-sap-c02-architect/ (legacy).

# AWS SAA Architecture

## Purpose
Produce AWS architecture designs with repeatable artifacts, explicit trade-offs, and decision traceability.

## When to use
- The request is architecture design for an AWS workload.
- The user needs service-selection matrices and HA/security baseline decisions.
- The user expects architecture artifacts and ADR-backed rationale.

## When NOT to use
- The request is only operations/runbook incident handling (use `aws-saa-operations`).
- The request is only enterprise governance, migration/DR specialization, or cost governance specialization.
- The request is pure systems theory without AWS mapping.

## Inputs to request
- Functional requirements and NFRs (availability, latency, throughput, RTO/RPO).
- Security/compliance constraints and data classification.
- Region/account constraints and traffic profile.
- Budget and cost sensitivity assumptions.

## Required workflow
Run in strict order:
1. `scripts/init_arch_workflow.py --system <system>`
2. Create/update solution overview with canonical `MAJOR_DECISION` lines.
3. Create required ADRs via `scripts/new_adr.py`.
4. Generate WA review via `scripts/wa_review.py`.
5. Validate via `scripts/validate_archifacts.py`.
6. Generate decision trace via `scripts/decision_trace.py`.

## Decision workflow
1. Select candidate compute, storage, and database patterns.
2. Evaluate load balancing, network, and security boundaries.
3. Evaluate HA and recovery posture.
4. Record major decisions as ADRs.
5. Validate against WA pillars and gate results.

## Rules & guardrails
- Must create ADRs for: datastore class/engine family choices, sync vs async integration model choices, trust boundary/auth model choices, network topology/segmentation/egress/endpoint choices, RTO/RPO and DR posture choices, region/account/partition strategy choices, and major cost model commitments.
- Must use canonical marker grammar:
  `MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`
- Must ensure all architecture outputs live under `docs/architecture/`.
- Must not bypass validation before reporting recommendations.

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
- `references/alb-vs-nlb-matrix.md`
- `references/storage-selection-matrix.md`
- `references/database-selection-matrix.md`
- `references/ha-multi-az-patterns.md`
- `references/security-baseline-checklist.md`
