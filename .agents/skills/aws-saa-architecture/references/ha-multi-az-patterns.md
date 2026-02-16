# HA Patterns and Multi-AZ

## Baseline
- Run critical request path across at least two AZs.
- For managed relational databases, use Multi-AZ where required by availability posture.
- Treat Multi-AZ as availability/failover control, not read-scaling strategy.
- Design for partial failure first (zonal impairment), then full regional disruption.

## Pattern map
| Layer | Recommended pattern |
|---|---|
| Web/API | Stateless service across multiple AZs behind load balancer |
| Relational DB | Multi-AZ deployment with tested failover expectations |
| Async/event | Durable messaging with retries, DLQ, and idempotent consumers |
| Caching/session | Replicated/distributed cache strategy with degradation plan |
| Control dependencies | Minimize single-point control-path dependencies per AZ |

## If/Then rules
| If | Then |
|---|---|
| DB outage tolerance is low | Enable Multi-AZ and document failover behavior |
| Read scaling needed in addition to HA | Add read replica strategy; do not use standby for read path |
| Recovery objective cannot tolerate restore-only approach | Add warm/hot redundancy and failover drill cadence |
| One AZ failure must not impact SLO | Ensure capacity and healthy targets in remaining AZs |
| Database writes are latency-sensitive | Validate synchronous replication impact against SLO before production |

## Failure-mode checks
- AZ outage simulation: can service maintain critical functionality?
- DB failover test: is reconnection behavior within SLO?
- Backup restore test: does restore path meet RTO/RPO?
- Dependency impairment test: do retries/timeouts protect upstream services?

## HA design checklist
- Stateless tiers can rebalance traffic across AZs without manual intervention.
- Capacity planning includes degraded mode (N-1 AZ scenario).
- Health checks and failure detection thresholds are explicitly tuned.
- Connection retry policy is bounded and jittered.
- Read/write behavior during failover is documented.
- Runbook includes manual override path when automatic failover is insufficient.

## RTO/RPO alignment quick table
| Requirement pattern | Baseline pattern |
|---|---|
| Minutes of downtime acceptable, limited data loss tolerance | Multi-AZ + backups + tested restore |
| Low downtime tolerance with low data loss tolerance | Multi-AZ + automated failover + warm standby |
| Near-zero downtime/data loss objectives | Multi-region active patterns with strict operational discipline |

## Anti-patterns
- Single-AZ stateful tier for production-critical workload.
- Declaring HA without failover test evidence.
- Assuming Multi-AZ standby can serve read traffic by default.
- Relying on retries only without bulkheads/circuit breakers.
- Treating backup existence as equivalent to high availability.

## Acceptance criteria
- HA pattern selected per layer and mapped to workload SLO.
- Failover procedure and expected impact are documented.
- At least one failover/restore validation runbook exists.
- WA reliability pillar findings are captured with remediation owners/dates.

### Example MAJOR_DECISION
`MAJOR_DECISION: reliability | relational-ha-posture | Enable RDS Multi-AZ with quarterly failover validation and documented reconnection policy`
