# Observability Baseline

## Scope
Use this baseline for associate-level operations architecture. Align with the AWS observability model (metrics, logs, traces) and treat alert quality as a first-class reliability control.

## Minimum telemetry contract
1. Metrics: service-level and resource-level health metrics with clear owners.
2. Logs: centralized collection with retention policy and query strategy.
3. Traces: request path visibility for user-facing and critical internal paths.
4. Synthetics: endpoint/API checks for customer-critical journeys.
5. Ownership: every signal has an owning team and response SLA.

## Practical implementation pattern
- Core platform:
  - Amazon CloudWatch Metrics and Alarms for threshold and anomaly detection.
  - Amazon CloudWatch Logs and Logs Insights for centralized query and triage.
  - AWS X-Ray or ADOT-based tracing for distributed request analysis.
- Multi-account visibility:
  - CloudWatch cross-account observability for centralized operations teams.
  - Standardized account tagging to map alarms to team ownership.

## Required signal tiers
| Tier | Purpose | Typical examples |
|---|---|---|
| Business outcome | Detect user-facing impact quickly | Checkout success rate, order completion latency |
| Service health | Detect internal degradation | API p95/p99 latency, error rate, saturation |
| Dependency health | Detect upstream/downstream faults | DB connection failures, queue lag, retry spikes |
| Platform/safety | Detect control-plane and security risk | Config drift, trail disablement, IAM anomalies |

## Alert design rules
1. Every alert maps to an actionable runbook step.
2. Use composite alarms to reduce noise and alert fatigue.
3. Separate paging alerts from informational alerts.
4. Define clear severity mapping (`SEV-1/2/3`) and response SLA.
5. Review and prune stale alerts every sprint or monthly.

## SLO-oriented signal mapping
- Availability SLO: success-rate metric + synthetic canary checks.
- Latency SLO: p95 and p99 latency alarms per user-critical API.
- Error-budget health: burn-rate alarms for fast and slow windows.
- Dependency SLO: database/cache/network saturation and retry-rate metrics.

## Deterministic alert gating
- A paging alert must include:
  - clear trigger condition,
  - impact statement,
  - owner and escalation target,
  - runbook link.
- If no runbook exists, alert severity is downgraded until runbook is authored.
- Composite alarms should suppress noisy downstream symptom alerts when a root trigger is active.

## Multi-account operations checklist
- [ ] Monitoring account configured and data sharing enabled.
- [ ] Alarm naming standard includes system/environment/severity.
- [ ] Correlation ID included in logs and traces.
- [ ] Log retention classes mapped to compliance and cost controls.
- [ ] Canary tests cover at least one customer-critical path per system.

## Failure modes and anti-patterns
- Anti-pattern: monitoring only CPU and memory.
  - Fix: include business and request-level metrics.
- Anti-pattern: logs without structure.
  - Fix: enforce JSON logs with request ID and tenant/service identifiers.
- Anti-pattern: alert without owner.
  - Fix: each alarm includes owner tag and escalation route.
- Anti-pattern: dashboards as vanity.
  - Fix: dashboard widgets must map to SLOs or incident triage steps.
- Anti-pattern: central logs without cardinality controls.
  - Fix: define structured fields and avoid unbounded labels.

## Acceptance checklist
- [ ] At least one dashboard per critical workload.
- [ ] All paging alarms have runbook links.
- [ ] Logs retained per compliance policy.
- [ ] Trace sampling configured and validated under load.
- [ ] MTTD and MTTR tracked monthly.
- [ ] WA Operational Excellence and Reliability findings include observability remediations.

## MAJOR_DECISION examples
- `MAJOR_DECISION: observability | central-monitoring-account | Use cross-account CloudWatch observability with a dedicated monitoring account.`
- `MAJOR_DECISION: alerting | anomaly-vs-static-thresholds | Use anomaly detection for seasonal traffic metrics and static thresholds for hard limits.`
