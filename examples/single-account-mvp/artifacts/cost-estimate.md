# Cost estimate (v1)

## Pricing as-of

- Timestamp (UTC): 2026-02-15T00:00:00Z
- Tooling: driver-based estimate
- Region(s): us-east-1

## Assumptions

- 1M requests/month to API
- 500 GB/month data egress

## Monthly estimate (USD)

- Low: 150
- Most likely: 450
- High: 1200

## Top cost drivers (must map to ADRs)

| Driver | Est. impact | ADR | Notes |
|--------|-------------|-----|-------|
| CloudFront egress | High | docs/02_ARCHITECTURE/ADRs/ADR-0002-network-architecture-serverless-no-vpc.md | 500 GB/month |
| Log ingestion | Medium | docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-logging-and-detections.md | CloudTrail/Config/Security Hub |

## Sensitivity notes

- If traffic doubles: costs increase proportionally for API and egress
- If logs increase: retention costs rise
- If data egress increases: CloudFront costs rise

## Cost guardrails

- Budgets + anomaly detection
- Tagging and cost allocation
- Log retention and sampling strategy

## AWS documentation references

- https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html

