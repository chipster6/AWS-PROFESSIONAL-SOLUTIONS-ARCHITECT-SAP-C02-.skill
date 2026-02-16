---
name: aws-aws-foundations
description: >
  Use when mapping workload requirements to AWS foundation concepts, including global
  infrastructure, shared responsibility boundaries, service families, and pricing model basics.
---

Note: This is the active Codex skills suite; ignore /skills/aws-sap-c02-architect/ (legacy).

# AWS Foundations

## Purpose
Translate system requirements into AWS foundational design choices before deep architecture specialization.

## When to use
- The user asks for baseline AWS architecture direction.
- Region/AZ/account placement, security ownership, or cost model basics are unclear.
- The design needs service-family selection guidance.

## When NOT to use
- The request is only first-principles systems reasoning (use `aws-systems-fundamentals`).
- The request is advanced multi-account governance, migration/DR, or cost-governance specialization.

## Inputs to request
- Region and data residency constraints.
- Compliance and security ownership requirements.
- Expected traffic pattern and workload profile.
- Budget sensitivity and cost observability expectations.

## Required workflow
1. Confirm global infrastructure assumptions (region/AZ scope).
2. Clarify shared responsibility boundaries.
3. Map workload components to AWS service taxonomy.
4. Document baseline pricing drivers and guardrails.

## Decision workflow
1. Choose candidate region strategy.
2. Choose compute/storage/database service families.
3. Validate identity, logging, and encryption baseline.
4. Identify cost drivers and expected spend shape.
5. Record trade-offs and unresolved decisions.

## Rules & guardrails
- Must separate AWS-managed responsibility from customer responsibility.
- Must state service-family alternatives and selection rationale.
- Should call out known quota/limit considerations.
- Must not claim exact cost without explicit assumptions.

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
- `references/aws-global-infrastructure.md`
- `references/shared-responsibility.md`
- `references/service-taxonomy.md`
- `references/pricing-basics.md`
