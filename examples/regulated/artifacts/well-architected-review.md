# Well-Architected review (v1)

## Scope

- Workload: Regulated system
- Environments: prod
- Regions: us-east-1

## Findings and recommendations (ADR-aware)

### Operational Excellence

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| Limited runbooks | P2 | Define runbooks for incident response and recovery (placeholder) | Ops | docs/02_ARCHITECTURE/ADRs/ADR-0001-regulated-landing-zone.md |

### Security

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| Evidence gaps | P0 | Enforce immutable log storage with Object Lock | SecOps | docs/02_ARCHITECTURE/ADRs/ADR-0002-immutability-and-retention.md |

### Reliability

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| Recovery not tested | P1 | Run quarterly restore tests | Ops | docs/02_ARCHITECTURE/ADRs/ADR-0001-regulated-landing-zone.md |

### Performance Efficiency

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| Capacity unknown | P2 | Review performance baselines and scale limits (placeholder) | Ops | docs/02_ARCHITECTURE/ADRs/ADR-0001-regulated-landing-zone.md |

### Cost Optimization

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| Cost drift | P2 | Implement budgets and review spend monthly (placeholder) | FinOps | docs/02_ARCHITECTURE/ADRs/ADR-0001-regulated-landing-zone.md |

### Sustainability

| Risk | Priority | Recommendation | Owner | adr_ref |
|------|----------|----------------|-------|---------|
| No sustainability review | P3 | Add quarterly sustainability review (placeholder) | Ops | docs/02_ARCHITECTURE/ADRs/ADR-0001-regulated-landing-zone.md |

## AWS documentation references

- https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html
