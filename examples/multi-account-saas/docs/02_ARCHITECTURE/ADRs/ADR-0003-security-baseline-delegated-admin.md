# ADR: Security baseline delegated admin

- Status: Accepted
- Date: 2026-02-15
- ADR ID: ADR-0003

## Context

Security services must be centrally managed across accounts.

## Decision

Enable delegated admin for Security Hub and GuardDuty; org-level CloudTrail/Config.

## Alternatives considered

Per-account unmanaged security services.

## Consequences

### Positive

Consistent detection and visibility.

### Negative / trade-offs

Increased log volume and service costs.

## Well-Architected mapping

- Pillars touched: security, operational_excellence
- Risks mitigated: blind spots
- Risks introduced: cost growth

## Cost impact

- Drivers: log_ingest, security_services
- Estimate linkage: `artifacts/cost-estimate.md`

## Security / compliance evidence

- Evidence sources: Security Hub, GuardDuty, CloudTrail, Config
- Notes: ensure cross-account access

## AWS documentation references

- https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html
- https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html
- https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html
- https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html

