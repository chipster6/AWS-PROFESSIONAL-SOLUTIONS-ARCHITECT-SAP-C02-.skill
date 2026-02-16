# DR Patterns and Trade-Offs

## Backup and Restore
- Strengths: lowest steady-state cost, simple baseline.
- Weaknesses: longer recovery window, restore orchestration required.
- Best for: non-critical systems or strict budget constraints.

## Pilot Light
- Strengths: lower cost than warm standby, better RTO/RPO than pure restore.
- Weaknesses: additional activation steps at failover.
- Best for: systems needing moderate recovery speed.

## Warm Standby
- Strengths: quick scale-up and lower recovery latency.
- Weaknesses: higher ongoing cost and operational overhead.
- Best for: business-critical systems with tight recovery targets.

## Multi-Site Active-Active
- Strengths: highest availability and continuity posture.
- Weaknesses: highest complexity (data consistency/conflict handling).
- Best for: ultra-critical workloads where disruption cost is extreme.

## Pattern comparison
| Pattern | Operational burden | Automation expectation | Testing intensity |
|---|---|---|---|
| Backup and restore | Low-medium | Moderate | Medium |
| Pilot light | Medium | High | Medium-high |
| Warm standby | Medium-high | High | High |
| Multi-site active-active | High | Very high | Very high |

## Cost vs Risk guidance
- Do not overbuild DR posture beyond business impact tolerance.
- Do not underbuild where regulatory or contractual objectives require tighter posture.

## Deterministic selection checks
- Is data replication approach defined and monitored?
- Is failover trigger model explicit (manual vs automated)?
- Is failback procedure documented and rehearsed?
- Are dependencies and third-party integrations included in recovery design?
- Is traffic rerouting strategy tested under realistic fault conditions?

## Common anti-patterns
- No failback plan after failover.
- No periodic DR test evidence.
- Treating multi-AZ high availability as full regional DR strategy.
- Automating failover without false-positive protections.

## Acceptance criteria
- Pattern choice is tied to explicit RTO/RPO and business impact.
- Recovery runbook includes trigger, failover, validation, and failback steps.
- Test evidence exists and is recent for critical workloads.
- ADR captures DR strategy trade-offs and residual risks.

## MAJOR_DECISION examples
- `MAJOR_DECISION: dr-architecture | region-failover-model | Implement active-passive regional failover with warm standby and automated traffic reroute.`
- `MAJOR_DECISION: dr-architecture | data-replication-strategy | Use continuous replication plus point-in-time recovery to mitigate corruption risk.`
