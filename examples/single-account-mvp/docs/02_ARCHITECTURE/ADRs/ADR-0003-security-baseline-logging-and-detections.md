# ADR: Security baseline logging and detections

- Status: Accepted
- Date: 2026-02-15
- ADR ID: ADR-0003

## Context

Security and audit visibility are required even for MVP.

## Decision

Enable CloudTrail, AWS Config, Security Hub, GuardDuty; enforce least privilege.

## Alternatives considered

Manual logging and ad hoc monitoring.

## Consequences

### Positive

Improved security posture and auditability.

### Negative / trade-offs

Higher log volume costs.

## Well-Architected mapping

- Pillars touched: security, operational_excellence
- Risks mitigated: missing detections
- Risks introduced: cost growth from logs

## Cost impact

- Drivers: log_ingest, security_services
- Estimate linkage: `artifacts/cost-estimate.md`

## Security / compliance evidence

- Evidence sources: CloudTrail, Config, Security Hub, GuardDuty
- Notes: ensure retention policy

## AWS documentation references

- https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html
- https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html
- https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html
- https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html

