---
name: aws-enterprise-architecture
description: >
  Use when designing enterprise-scale AWS architectures with multi-account governance,
  organizational guardrails, cross-account security patterns, and advanced hybrid networking.
---

Note: This is the active Codex skills suite; ignore /skills/aws-sap-c02-architect/ (legacy).

# AWS Enterprise Architecture

## Purpose
Design auditable enterprise AWS architectures spanning governance, multi-account structures, and hybrid connectivity.

## When to use
- The request requires organization-level architecture (multiple accounts/OUs).
- The request includes control tower/landing zone/SCP guardrails.
- The request includes hub-spoke networking, TGW, DX, VPN, or hybrid boundaries.

## When NOT to use
- Single-account workload design only.
- Pure migration-wave or DR-pattern planning (use `aws-migration-dr`).
- Cost-only governance strategy (use `aws-cost-governance`).

## Inputs to request
- Business units and workload segmentation requirements.
- Compliance/control requirements (least privilege, data perimeter, audit).
- Network topology constraints and on-prem connectivity needs.
- Regional resilience and sovereignty constraints.

## Required workflow
Run in strict order:
1. `scripts/init_arch_workflow.py --system <system>`
2. Create/update solution overview with canonical `MAJOR_DECISION` markers.
3. Create required ADRs via `scripts/new_adr.py`.
4. Generate WA review via `scripts/wa_review.py`.
5. Validate artifacts via `scripts/validate_archifacts.py`.
6. Generate decision trace via `scripts/decision_trace.py`.

## Decision workflow
1. Define OU/account segmentation and control boundaries.
2. Define SCP and delegated admin guardrail model.
3. Define cross-account IAM and access patterns.
4. Define hybrid networking topology and resilience model.
5. Record major decisions and validate against WA gates.

## Rules & guardrails
- Must create ADRs for: datastore class/engine family choices, sync vs async integration model choices, trust boundary/auth model choices, network topology/segmentation/egress/endpoint choices, RTO/RPO and DR posture choices, region/account/partition strategy choices, and major cost model commitments.
- Must use canonical marker:
  `MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`
- Must stage policy rollout strategy (no root-level blast changes first).
- Must explicitly identify break-glass and audit ownership.

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
- `references/multi-account-landing-zone-patterns.md`
- `references/organizations-and-scp-guardrails.md`
- `references/cross-account-iam-patterns.md`
- `references/hub-spoke-and-tgw-patterns.md`
- `references/hybrid-connectivity-overview.md`
