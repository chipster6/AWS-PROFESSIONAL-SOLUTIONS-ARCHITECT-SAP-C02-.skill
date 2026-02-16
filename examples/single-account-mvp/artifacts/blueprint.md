# Blueprint: SaaS web + API (single-account MVP)

## Summary

Serverless web + API with managed services and minimal ops. Designed for rapid MVP launch and low fixed costs.

## Constraints and fit

- Primary drivers: speed, simplicity, low ops
- Key constraints: small team, tight budget
- Not a fit when: hard real-time latency, complex hybrid networking

## Reference architecture

- Components: Route 53, ACM, CloudFront, S3 (static web), API Gateway, Lambda, DynamoDB
- Data flows: user -> CloudFront -> S3 and API Gateway -> Lambda -> DynamoDB
- Trust boundaries: internet edge at CloudFront, data boundary at DynamoDB

## Key decisions (with ADR refs)

| Decision | Choice | ADR |
|----------|--------|-----|
| Landing zone | Single-account baseline | docs/02_ARCHITECTURE/ADRs/ADR-0001-single-account-landing-zone-strategy.md |
| Network | No VPC unless required | docs/02_ARCHITECTURE/ADRs/ADR-0002-network-architecture-serverless-no-vpc.md |
| Security baseline | CloudTrail/Config/Security Hub/GuardDuty | docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-logging-and-detections.md |

## Variants

- Cost-optimized: aggressive caching, reduced log retention
- Security-optimized: WAF enabled, stricter headers
- DR-optimized: documented restore runbook

## Cost drivers (map to ADRs)

| Driver | Why it exists | ADR |
|--------|---------------|-----|
| CloudFront egress | public web traffic | docs/02_ARCHITECTURE/ADRs/ADR-0002-network-architecture-serverless-no-vpc.md |
| Log ingestion | CloudTrail/Config/Security Hub | docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-logging-and-detections.md |

## AWS documentation references

- https://aws.amazon.com/documentation-overview/cloudfront/
- https://aws.amazon.com/documentation-overview/api-gateway/
- https://aws.amazon.com/documentation-overview/lambda/
- https://aws.amazon.com/documentation-overview/dynamodb/

