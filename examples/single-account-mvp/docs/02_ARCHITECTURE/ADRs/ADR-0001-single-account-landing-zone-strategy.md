# ADR: Single-account landing zone strategy

- Status: Accepted
- Date: 2026-02-15
- ADR ID: ADR-0001

## Context

Small team and MVP timeline require minimal operational overhead.

## Decision

Use a single AWS account with org-ready controls and documented migration path.

## Alternatives considered

Multi-account landing zone with Control Tower.

## Consequences

### Positive

Faster launch, fewer moving parts.

### Negative / trade-offs

Less strong isolation between environments.

## Well-Architected mapping

- Pillars touched: security, operational_excellence, cost_optimization
- Risks mitigated: overhead and complexity
- Risks introduced: isolation gaps

## Cost impact

- Drivers: log_retention
- Estimate linkage: `artifacts/cost-estimate.md`

## Security / compliance evidence

- Evidence sources: CloudTrail, Config
- Notes: centralized logging required

## AWS documentation references

- https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html
- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html

