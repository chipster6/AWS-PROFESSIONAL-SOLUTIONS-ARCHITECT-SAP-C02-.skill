# Landing zone plan (v1)

## Account strategy (single vs multi)

- Current state: multi-account target
- Target state: management, log archive, security, shared services, workloads
- Rationale (ADR): docs/02_ARCHITECTURE/ADRs/ADR-0001-landing-zone-strategy-control-tower.md
- Landing zone tooling (if multi-account): Control Tower

## Identity and access

- Identity provider / IAM Identity Center: Identity Center with external IdP
- Admin/break-glass model: break-glass in management and security accounts
- Permission boundaries / guardrails: SCPs and boundaries

## Networking

- Topology: hub-and-spoke with shared network account
- Egress strategy: centralized egress with endpoints
- Private connectivity: optional DX/VPN
- ADR: docs/02_ARCHITECTURE/ADRs/ADR-0002-network-hub-spoke-egress.md

## Logging and security baseline

- CloudTrail strategy: org trail to log archive
- AWS Config strategy: org aggregator
- Security Hub/GuardDuty: delegated admin
- Key management: CMKs per account
- ADR: docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-delegated-admin.md

## Environment strategy

- Environments (dev/stage/prod): separate accounts
- Promotions and change control: gated via CI

## Implementation phases

1. Plan review + approvals (record in audit log)
2. Bootstrap (state, IAM roles, key policies)
3. Baseline services
4. Workload foundations

## AWS documentation references

- https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html
- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html

