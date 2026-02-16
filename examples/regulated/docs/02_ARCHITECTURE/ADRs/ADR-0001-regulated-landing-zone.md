# ADR: Regulated landing zone

- Status: Accepted
- Date: 2026-02-15
- ADR ID: ADR-0001

## Context

Regulated workloads require strong isolation and centralized audit.

## Decision

Use multi-account with dedicated log archive and security accounts.

## Alternatives considered

Single account with logical segregation.

## Consequences

### Positive

Improved auditability and separation of duties.

### Negative / trade-offs

Higher operational overhead.

## Well-Architected mapping

- Pillars touched: security, operational_excellence
- Risks mitigated: audit gaps
- Risks introduced: increased complexity

## Cost impact

- Drivers: log_retention, security_services
- Estimate linkage: `artifacts/cost-estimate.md`

## Security / compliance evidence

- Evidence sources: CloudTrail, Config, Security Hub
- Notes: log archive with restricted access

## AWS documentation references

- https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html
- https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html

