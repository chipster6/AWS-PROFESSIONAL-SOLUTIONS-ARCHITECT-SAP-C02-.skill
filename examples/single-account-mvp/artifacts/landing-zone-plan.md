# Landing zone plan (v1)

## Account strategy (single vs multi)

- Current state: single account
- Target state: single account (org-ready)
- Rationale (ADR): docs/02_ARCHITECTURE/ADRs/ADR-0001-single-account-landing-zone-strategy.md
- Landing zone tooling (if multi-account): N/A

## Identity and access

- Identity provider / IAM Identity Center: IAM Identity Center (future)
- Admin/break-glass model: 2 break-glass users with MFA
- Permission boundaries / guardrails: least privilege IAM

## Networking

- Topology: no VPC unless required
- Egress strategy: managed services public endpoints
- Private connectivity: N/A
- ADR: docs/02_ARCHITECTURE/ADRs/ADR-0002-network-architecture-serverless-no-vpc.md

## Logging and security baseline

- CloudTrail strategy: enabled, management events
- AWS Config strategy: enabled, all resources
- Security Hub/GuardDuty: enabled
- Key management: KMS for logs and data
- ADR: docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-logging-and-detections.md

## Environment strategy

- Environments (dev/stage/prod): prod only (documented gap)
- Promotions and change control: manual approvals

## Implementation phases

1. Plan review + approvals (record in audit log)
2. Bootstrap (state, IAM roles, key policies)
3. Baseline services
4. Workload foundations

## AWS documentation references

- https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html
- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html

