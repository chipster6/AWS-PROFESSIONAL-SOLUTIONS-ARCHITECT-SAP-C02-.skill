# Cost estimate (v1)

## Pricing as-of

- Timestamp (UTC): 2026-02-15T00:00:00Z
- Tooling: driver-based estimate
- Region(s): us-east-1

## Assumptions

- 3 workload accounts
- 1-7 year log retention

## Monthly estimate (USD)

- Low: 2500
- Most likely: 6000
- High: 12000

## Top cost drivers (must map to ADRs)

| Driver | Est. impact | ADR | Notes |
|--------|-------------|-----|-------|
| Log retention | High | docs/02_ARCHITECTURE/ADRs/ADR-0002-immutability-and-retention.md | Object Lock + long retention |
| Endpoints | Medium | docs/02_ARCHITECTURE/ADRs/ADR-0003-network-segmentation-private-endpoints.md | Private connectivity |

## Sensitivity notes

- If logs increase: retention costs rise sharply
- If data egress increases: egress costs rise
- If evidence scope expands: storage costs rise

## Cost guardrails

- Budgets + anomaly detection
- Tagging and cost allocation
- Log retention and sampling strategy

## AWS documentation references

- https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html

