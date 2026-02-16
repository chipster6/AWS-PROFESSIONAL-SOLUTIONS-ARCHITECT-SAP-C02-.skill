# Blueprint: Regulated baseline

## Summary

Multi-account regulated baseline with centralized logging, evidence, and immutability.

## Constraints and fit

- Primary drivers: auditability, evidence, retention
- Key constraints: regulated data and strict controls
- Not a fit when: no compliance requirements

## Reference architecture

- Components: log archive account, security account, workload accounts, centralized audit
- Data flows: workload logs -> log archive with retention policies
- Trust boundaries: account boundaries and log archive boundary

## Key decisions (with ADR refs)

| Decision | Choice | ADR |
|----------|--------|-----|
| Landing zone | Multi-account with log archive | docs/02_ARCHITECTURE/ADRs/ADR-0001-regulated-landing-zone.md |
| Immutability | Object Lock for audit logs | docs/02_ARCHITECTURE/ADRs/ADR-0002-immutability-and-retention.md |
| Network | Private endpoints | docs/02_ARCHITECTURE/ADRs/ADR-0003-network-segmentation-private-endpoints.md |

## Variants

- Cost-optimized: narrower log scopes
- Security-optimized: broader detections and tighter key policies
- DR-optimized: cross-region audit replicas

## Cost drivers (map to ADRs)

| Driver | Why it exists | ADR |
|--------|---------------|-----|
| Log retention | regulatory requirements | docs/02_ARCHITECTURE/ADRs/ADR-0002-immutability-and-retention.md |
| Endpoints | private connectivity | docs/02_ARCHITECTURE/ADRs/ADR-0003-network-segmentation-private-endpoints.md |

## AWS documentation references

- https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html
- https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html

