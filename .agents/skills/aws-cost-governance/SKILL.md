---
name: aws-cost-governance
description: >
  Use when designing AWS cost governance and optimization controls, including tagging and allocation
  policy, commitment strategy, anomaly response, and auditable cost decision workflows.
---

Note: This is the active Codex skills suite; ignore /skills/aws-sap-c02-architect/ (legacy).

# AWS Cost Governance

## Purpose
Create deterministic cost governance decisions that preserve business value while enforcing accountability and predictable spend controls.

## When to use
- The request involves cost allocation, budgeting, cost controls, or FinOps governance.
- The architecture requires commitment strategy guidance (Savings Plans/RI posture).
- The user needs cross-account cost transparency or chargeback/showback model decisions.

## When NOT to use
- The request is pure workload architecture without financial governance scope.
- The request is only migration-wave and DR design.
- The request is only low-level billing mechanics without architecture impact.

## Inputs to request
- Business ownership model (BU/team/app/environment).
- Allocation needs (showback vs chargeback).
- Forecast confidence and usage stability by workload class.
- Optimization constraints (performance, compliance, time-to-delivery).

## Required workflow
Run in strict order:
1. `scripts/init_arch_workflow.py --system <system>`
2. Create/update solution overview with canonical `MAJOR_DECISION` markers.
3. Create required ADRs via `scripts/new_adr.py`.
4. Generate WA review via `scripts/wa_review.py`.
5. Validate artifacts via `scripts/validate_archifacts.py`.
6. Generate decision trace via `scripts/decision_trace.py`.

## Decision workflow
1. Define allocation model and tagging/category schema.
2. Define governance controls (budgets, anomaly detection, ownership SLAs).
3. Define commitment strategy by workload predictability.
4. Define optimization playbook and review cadence.
5. Record major decisions and validate with WA and policy gates.

## Rules & guardrails
- Must create ADRs for: datastore class/engine family choices, sync vs async integration model choices, trust boundary/auth model choices, network topology/segmentation/egress/endpoint choices, RTO/RPO and DR posture choices, region/account/partition strategy choices, and major cost model commitments.
- Must use canonical marker:
  `MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`
- Must define accountable owners for cost categories and anomaly actions.
- Must not recommend commitments without usage-baseline evidence.

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
- `references/cost-allocation-and-tagging.md`
- `references/savings-plans-basics.md`
- `references/cost-optimization-playbook.md`
- `references/finops-governance-model.md`
