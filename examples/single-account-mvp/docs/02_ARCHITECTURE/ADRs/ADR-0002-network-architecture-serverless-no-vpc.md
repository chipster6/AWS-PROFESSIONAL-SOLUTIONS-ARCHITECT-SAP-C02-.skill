# ADR: Network architecture (serverless, no VPC)

- Status: Accepted
- Date: 2026-02-15
- ADR ID: ADR-0002

## Context

Serverless services can avoid VPC complexity for the MVP.

## Decision

Use public AWS managed service endpoints; avoid VPC unless required.

## Alternatives considered

Private VPC with NAT gateways and endpoints.

## Consequences

### Positive

Lower cost and less operational complexity.

### Negative / trade-offs

Less private connectivity and network segmentation.

## Well-Architected mapping

- Pillars touched: performance_efficiency, cost_optimization
- Risks mitigated: NAT costs and complexity
- Risks introduced: reliance on public endpoints

## Cost impact

- Drivers: nat_gateways, vpc_endpoints
- Estimate linkage: `artifacts/cost-estimate.md`

## Security / compliance evidence

- Evidence sources: CloudFront access logs
- Notes: WAF optional for MVP

## AWS documentation references

- https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html

