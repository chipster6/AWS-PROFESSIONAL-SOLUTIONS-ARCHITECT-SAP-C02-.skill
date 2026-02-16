# ADR: Network hub-and-spoke egress

- Status: Accepted
- Date: 2026-02-15
- ADR ID: ADR-0002

## Context

Multiple workload accounts need consistent egress and inspection.

## Decision

Use a shared network account with hub-and-spoke routing and centralized egress.

## Alternatives considered

Distributed egress per account.

## Consequences

### Positive

Centralized controls and monitoring.

### Negative / trade-offs

Higher NAT costs and dependency on shared network.

## Well-Architected mapping

- Pillars touched: security, reliability
- Risks mitigated: inconsistent egress controls
- Risks introduced: shared network bottleneck

## Cost impact

- Drivers: nat_gateways, vpc_endpoints
- Estimate linkage: `artifacts/cost-estimate.md`

## Security / compliance evidence

- Evidence sources: VPC Flow Logs, Route Tables
- Notes: review routing changes

## AWS documentation references

- https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
- https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html

