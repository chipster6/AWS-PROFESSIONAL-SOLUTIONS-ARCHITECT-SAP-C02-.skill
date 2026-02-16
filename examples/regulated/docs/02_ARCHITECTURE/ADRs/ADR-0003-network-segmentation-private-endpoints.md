# ADR: Network segmentation and private endpoints

- Status: Accepted
- Date: 2026-02-15
- ADR ID: ADR-0003

## Context

Regulated data must avoid public egress where possible.

## Decision

Use private subnets and VPC endpoints for service access.

## Alternatives considered

Public endpoints with strict security groups.

## Consequences

### Positive

Reduced exposure and better control.

### Negative / trade-offs

Endpoint and NAT costs.

## Well-Architected mapping

- Pillars touched: security, performance_efficiency
- Risks mitigated: exposure to public internet
- Risks introduced: cost and complexity

## Cost impact

- Drivers: vpc_endpoints, nat_gateways
- Estimate linkage: `artifacts/cost-estimate.md`

## Security / compliance evidence

- Evidence sources: VPC endpoint policies, Flow Logs
- Notes: change control for routes

## AWS documentation references

- https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
- https://docs.aws.amazon.com/vpc/latest/userguide/privatelink/what-is-privatelink.html

