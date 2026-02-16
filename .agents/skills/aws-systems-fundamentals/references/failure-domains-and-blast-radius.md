# Failure Domains and Blast Radius

## Core model
- A failure domain is the smallest boundary where a single fault can cause correlated impact.
- Design objective: keep faults local, detect quickly, degrade gracefully, recover predictably.
- Treat control-plane and data-plane failures as separate risk classes.

## Domain mapping checklist
- Compute domain: can one host pool failure take out all request handling?
- Data domain: can one data-store impairment break read and write paths globally?
- Network domain: can one egress, endpoint, or route fault block all traffic classes?
- Control domain: can one IAM/KMS/DNS/config change break all services?
- Operations domain: can one deployment pipeline or runbook defect create systemic outage?

## Domain catalog (starter taxonomy)
| Domain type | Typical example | Containment mechanism |
|---|---|---|
| Zonal | Single AZ dependency outage | Multi-AZ active capacity + health-based routing |
| Regional | Region-wide service impairment | DR region with documented failover trigger |
| Data | Primary datastore write path degraded | Queue buffering, fallback modes, recovery playbook |
| Identity/control | IAM/KMS/config failure | Least-privilege change controls and break-glass runbook |
| Dependency | Third-party API outage | Circuit breaker, bulkheads, graceful degradation |

## If/Then rules
| If | Then |
|---|---|
| One component supports multiple critical capabilities | Split by bounded context or tenant/cell |
| RTO target is less than restore time from backup | Add hot/warm redundancy in independent domain |
| Shared dependency is unavoidable | Add bulkheads, retries with jitter, circuit breaking, fallback mode |
| Regional outage is in risk model | Define cross-region failover contract and test cadence |

## Blast-radius scoring (quick)
| Score | Meaning | Typical action |
|---|---|---|
| 1 | Localized, non-critical impact | Accept with monitoring |
| 2 | Single capability degradation | Add fallback and rollback guardrails |
| 3 | Multi-capability outage in one environment | Partition or isolate data/control paths |
| 4 | Cross-environment or cross-tenant outage | Mandatory architecture redesign before release |

## Deterministic containment checks
- Can one misconfigured policy disable all environments?
- Can one queue/topic outage block unrelated capabilities?
- Can one deployment wave impact all tenants at once?
- Can one credential/key failure halt both read and write paths?
- Can one observability outage blind incident triage?

## Anti-patterns
- Shared singleton database for unrelated critical paths.
- Single message bus/topic without workload isolation.
- Centralized control-plane dependencies without cache/fallback.
- “Backup exists” used as substitute for high availability.

## Failure-mode prompts
- What fails if one AZ is unavailable?
- What fails if write path is healthy but read path is stale?
- What fails if DNS, IAM, or KMS is degraded?
- What is user-facing behavior within first 5 minutes of incident?

## Acceptance criteria
- Workload runs across at least two independent failure domains for critical path.
- Documented degradation behavior exists per critical dependency.
- Recovery sequence is testable without privileged tribal knowledge.
- At least one explicit `MAJOR_DECISION` marker exists for isolation boundary.
- At least one game day scenario validates blast-radius assumptions.

### Example MAJOR_DECISION
`MAJOR_DECISION: reliability | cell-boundary | Partition tenant traffic into independent service cells to contain compute/database faults`
