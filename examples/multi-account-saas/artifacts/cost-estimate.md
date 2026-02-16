# Cost estimate (v1)

## Pricing as-of

- Timestamp (UTC): 2026-02-15T00:00:00Z
- Tooling: driver-based estimate
- Region(s): us-east-1

## Assumptions

- 5 workload accounts
- centralized logging enabled

## Monthly estimate (USD)

- Low: 1500
- Most likely: 4000
- High: 9000

## Top cost drivers (must map to ADRs)

| Driver | Est. impact | ADR | Notes |
|--------|-------------|-----|-------|
| NAT gateways | High | docs/02_ARCHITECTURE/ADRs/ADR-0002-network-hub-spoke-egress.md | centralized egress |
| Log ingestion | Medium | docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-delegated-admin.md | org trail + config |

## Sensitivity notes

- If traffic doubles: NAT and data transfer costs increase
- If logs increase: retention costs rise
- If data egress increases: cloudfront/egress costs rise

## Cost guardrails

- Budgets + anomaly detection
- Tagging and cost allocation
- Log retention and sampling strategy

## AWS documentation references

- https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html

