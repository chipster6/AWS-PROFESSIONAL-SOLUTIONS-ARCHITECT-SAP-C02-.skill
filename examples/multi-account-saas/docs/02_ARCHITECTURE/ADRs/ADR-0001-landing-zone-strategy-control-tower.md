# ADR: Landing zone strategy (Control Tower)

- Status: Accepted
- Date: 2026-02-15
- ADR ID: ADR-0001

## Context

Multiple teams and environments require strong guardrails and centralized governance.

## Decision

Use AWS Control Tower to establish a multi-account landing zone.

## Alternatives considered

Custom Organizations setup without Control Tower.

## Consequences

### Positive

Standardized guardrails and simpler account vending.

### Negative / trade-offs

Less flexibility than fully custom setups.

## Well-Architected mapping

- Pillars touched: security, operational_excellence, reliability
- Risks mitigated: inconsistent governance
- Risks introduced: guardrail constraints

## Cost impact

- Drivers: security_services, log_retention
- Estimate linkage: `artifacts/cost-estimate.md`

## Security / compliance evidence

- Evidence sources: Control Tower guardrails, CloudTrail
- Notes: central log archive

## AWS documentation references

- https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html

