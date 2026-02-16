# AWS Global Infrastructure

## Baseline concepts
- `Region`: separate geographic area designed for fault isolation from other Regions.
- `Availability Zone (AZ)`: isolated location in a Region with low-latency, high-bandwidth, redundant interconnect to peer AZs.
- `Local Zone`: extension for placing compute/storage near users in metro areas when latency demands it.
- `Wavelength Zone`: edge deployment integrated with 5G carrier networks for ultra-low-latency mobile scenarios.
- `Outposts`: AWS-managed infrastructure footprint on-premises for low-latency/local processing constraints.

## Architecture placement workflow
1. Identify legal/regulatory data residency constraints.
2. Identify user-latency SLO by geography (interactive vs batch vs internal).
3. Select primary region and AZ layout for steady state.
4. Select resiliency posture: single-region multi-AZ, pilot-light, warm standby, or active-active multi-region.
5. Define explicit data replication, failover triggers, and failback strategy.
6. Validate network and data transfer implications before committing.
7. Record all region/AZ decisions as ADRs when they affect DR posture, sovereignty, or cost.

## Region strategy matrix
| Strategy | Best for | Trade-off |
|---|---|---|
| Single region, multi-AZ | Most workloads with regional regulatory constraints | Regional outage still disruptive |
| Primary + DR region (warm/pilot) | Strong resilience with moderate complexity | Higher operational/testing burden |
| Active-active multi-region | Global low latency + highest availability | Highest complexity and consistency challenges |

## Zone type guidance
| Zone type | Use when | Avoid when |
|---|---|---|
| Standard AZ | Default for resilient production workloads | Never place all critical state in one AZ |
| Local Zone | Need lower latency for specific metro users | Using it as replacement for Region-level DR |
| Wavelength Zone | Need ultra-low latency for 5G/mobile edge workloads | Workload cannot tolerate carrier-edge constraints |
| Outposts | On-prem latency/data processing/compliance requires local AWS runtime | Workload can run fully in Region with acceptable latency |

## AZ placement baseline
| Component type | Minimum placement |
|---|---|
| Public ingress and API tier | 2+ AZs |
| Stateful relational data tier | Multi-AZ or equivalent failover pattern |
| Async processing tier | 2+ AZ workers/consumers |
| Shared dependencies (NAT, egress, endpoints) | Redundant path per AZ where possible |

## If/Then rules
| If | Then |
|---|---|
| Regulatory residency is strict | Constrain data plane to approved region(s) |
| p95 latency target requires edge locality | Evaluate Local Zone / edge strategy |
| AZ failure cannot cause outage | Run active components in at least two AZs |
| Regional outage is in threat model | Add second-region recovery design and drill plan |
| Customer base is globally distributed with strict latency targets | Evaluate global front-door + regional data partition strategy |
| Workload uses stateful write-heavy datastore | Validate replication consistency and failover write semantics early |

## Networking and dependency checks
- Confirm inter-AZ traffic assumptions and cost for east-west patterns.
- Confirm inter-region replication lag tolerance and reconciliation behavior.
- Confirm DNS failover model and TTL strategy for cutover.
- Confirm identity and key-management dependencies in each region.

## Deterministic architecture checks
- Define exact failover trigger source (health checks, dependency SLO breach, operator decision).
- Define DNS failover TTL and expected convergence window.
- Define write behavior during failover (read-only window, write queueing, or conflict policy).
- Define rollback/failback criteria after recovery.

## Failure-domain decision table
| Failure scenario | Minimum architecture response | Evidence required |
|---|---|---|
| Single AZ impairment | Service remains available in surviving AZ(s) | AZ game day / simulated failover results |
| Regional service degradation | DR playbook with trigger + operator steps | Runbook + drill evidence |
| Regional hard outage | Secondary region recovery path | RTO/RPO validation record |
| Control-plane impairment | Pre-provisioned recovery primitives | Tested manual procedure |

## Anti-patterns
- “Multi-region” architecture with no data replication/failover contract.
- Stateful production workload in one AZ.
- Cross-region dependencies without latency and cost assessment.
- Regional DR documented but never tested under realistic failure conditions.
- Treating edge zones as full substitutes for regional resiliency architecture.

## Failure-mode prompts
- If one AZ is unavailable, what user journeys remain healthy?
- If region control-plane operations degrade, what operations are blocked?
- If replication lags during incident, what data correctness guarantees remain?
- If DNS cutover fails, what is the manual fallback?

## Acceptance criteria
- Region and AZ strategy documented in solution overview.
- Critical services are AZ-redundant.
- DR region and failover trigger criteria are defined when required.
- Recovery runbook exists with RTO/RPO and test cadence.
- At least one explicit ADR captures region strategy trade-offs.
- Manifest contains artifact links for solution overview, WA review, and decision trace.

### Example MAJOR_DECISION
`MAJOR_DECISION: region-strategy | primary-dr-region | Use us-east-1 primary and us-west-2 DR with asynchronous replication`
