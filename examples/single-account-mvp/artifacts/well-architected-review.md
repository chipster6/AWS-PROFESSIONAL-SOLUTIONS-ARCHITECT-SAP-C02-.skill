# Well-Architected review (v1)

## Scope

- Workload: MVP Web API
- Environments: prod
- Regions: us-east-1

## Findings and recommendations (ADR-aware)

### Operational Excellence

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| Low runbook coverage | P1 | Add runbooks for API errors and Lambda timeouts | Team | docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-logging-and-detections.md |

### Security

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| Missing baseline detections | P0 | Enable Security Hub + GuardDuty + Config | Team | docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-logging-and-detections.md |

### Reliability

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| No documented recovery | P1 | Define restore procedure for DynamoDB | Team | docs/02_ARCHITECTURE/ADRs/ADR-0001-single-account-landing-zone-strategy.md |

### Performance Efficiency

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| Cold start risk | P2 | Size Lambda memory and keep warm if needed | Team | docs/02_ARCHITECTURE/ADRs/ADR-0002-network-architecture-serverless-no-vpc.md |

### Cost Optimization

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| Excess logs | P1 | Org policy: set log retention to 30-90 days | Team | docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-logging-and-detections.md |

### Sustainability

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| None | P3 | Review quarterly | Team | docs/02_ARCHITECTURE/ADRs/ADR-0001-single-account-landing-zone-strategy.md |

## AWS documentation references

- https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html
