# Hybrid Connectivity Overview

## Goal
Provide resilient, policy-driven connectivity between on-premises networks and AWS.

## Connectivity options
1. AWS Direct Connect:
   - primary private connectivity with predictable performance.
2. AWS Site-to-Site VPN:
   - secure tunnel connectivity, often used as backup or for lower-throughput paths.
3. Combined DX + VPN:
   - DX primary with VPN backup on TGW for resilience.

## Connectivity selection matrix
| Requirement | Preferred approach |
|---|---|
| Predictable throughput/latency for critical workloads | Direct Connect primary |
| Fast setup with moderate throughput | Site-to-Site VPN |
| Higher resilience without single-link dependency | DX primary + VPN backup |
| Highest resilience posture | Multiple DX paths across facilities + VPN backup |

## Resilience guidance
- For highest resiliency, use multiple DX connections at multiple locations and devices.
- Use dual VPN tunnels across distinct AZ endpoints.
- Use dynamic routing (BGP) for automated reroute.
- Consider multi-region redundancy when required by business objectives.
- Resiliency target guidance:
  - Maximum resiliency (target SLA 99.99%): redundant DX connections across multiple sites and DX locations.
  - High resiliency (target SLA 99.9%): two independent connections across multiple locations.
- If using DX + VPN backup on TGW, validate ECMP behavior and throughput assumptions per tunnel.

## Deterministic routing and failover controls
- Define BGP preference and failover policy explicitly.
- Test failover on link down, device down, and route withdrawal scenarios.
- Validate traffic symmetry requirements for stateful middleboxes.
- Document failback criteria and post-failover verification checks.

## Cost and risk considerations
- DX provides stability but requires circuit planning and lead time.
- VPN adds resilience but has tunnel throughput constraints.
- Hub routing can increase transfer charges if traffic patterns are not optimized.

## Operational checklist
- [ ] Connectivity SLA target defined.
- [ ] Failure and failback test cadence defined.
- [ ] Routing policy ownership defined.
- [ ] Hybrid incident runbook validated.
- [ ] ISP diversity validated for VPN internet paths.
- [ ] BGP failover behavior tested under link/device failure scenarios.
- [ ] Failback test evidence captured at least quarterly for critical systems.

## Anti-patterns
- Single physical path for business-critical hybrid connectivity.
- Unverified assumptions about VPN throughput during failover.
- No documented routing ownership for BGP policy changes.

## MAJOR_DECISION examples
- `MAJOR_DECISION: hybrid-connectivity | dx-plus-vpn-backup | Use Direct Connect as primary with TGW-terminated VPN backup for failover.`
- `MAJOR_DECISION: resiliency | multi-location-dx | Deploy redundant DX paths across multiple facilities and devices.`
