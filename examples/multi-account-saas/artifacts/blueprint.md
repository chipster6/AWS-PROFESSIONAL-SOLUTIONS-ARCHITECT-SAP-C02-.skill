# Blueprint: SaaS web + API (multi-account)

## Summary

Multi-account SaaS with shared services and centralized security/logging.

## Constraints and fit

- Primary drivers: governance, isolation, auditability
- Key constraints: multiple environments and teams
- Not a fit when: single team MVP with no compliance needs

## Reference architecture

- Components: Control Tower, Organizations, shared services, workload accounts
- Data flows: user traffic enters per workload account; centralized logging and security
- Trust boundaries: account boundaries and shared services boundaries

## Key decisions (with ADR refs)

| Decision | Choice | ADR |
|----------|--------|-----|
| Landing zone | Control Tower | docs/02_ARCHITECTURE/ADRs/ADR-0001-landing-zone-strategy-control-tower.md |
| Network | Hub-and-spoke | docs/02_ARCHITECTURE/ADRs/ADR-0002-network-hub-spoke-egress.md |
| Security baseline | Delegated admin + org trail | docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-delegated-admin.md |

## Variants

- Cost-optimized: minimize NAT usage with endpoints
- Security-optimized: stricter SCPs and key policies
- DR-optimized: multi-region for critical services

## Cost drivers (map to ADRs)

| Driver | Why it exists | ADR |
|--------|---------------|-----|
| NAT gateway | centralized egress | docs/02_ARCHITECTURE/ADRs/ADR-0002-network-hub-spoke-egress.md |
| Log ingestion | org CloudTrail/Config | docs/02_ARCHITECTURE/ADRs/ADR-0003-security-baseline-delegated-admin.md |

## AWS documentation references

- https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html
- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html

