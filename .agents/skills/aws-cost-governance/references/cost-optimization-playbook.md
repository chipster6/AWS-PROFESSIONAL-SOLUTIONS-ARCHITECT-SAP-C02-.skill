# Cost Optimization Playbook

## Goal
Run predictable optimization loops that improve unit economics without breaking reliability or security.

## Optimization hierarchy
1. Eliminate waste (idle, orphaned, duplicate resources).
2. Rightsize overprovisioned resources.
3. Optimize pricing model (on-demand/commitment/spot where suitable).
4. Optimize architecture patterns (data transfer, storage class, decoupling, caching).

## Monthly optimization loop
1. Identify top spend drivers by service/workload.
2. Identify top variance versus prior period and forecast.
3. Prioritize actions by savings potential and risk.
4. Execute low-risk/high-impact actions first.
5. Validate business and performance outcomes.
6. Record results, residual risks, and next actions.

## Deterministic action matrix
| Signal | Action |
|---|---|
| High idle spend | Stop/schedule/delete unused resources |
| Compute consistently underutilized | Rightsize instances/services |
| Spiky batch workloads | Evaluate Spot and queue-based scheduling |
| High cross-AZ/Region transfer | Reassess placement and data path topology |
| Large cold data footprint | Apply lifecycle/archival controls |

## Guardrails before optimization
- Validate impact to SLOs and DR objectives.
- Validate security/compliance controls remain intact.
- Define rollback path for risky changes.
- Notify service owners of cost-impacting changes.

## KPIs to track
- Cost per workload/unit transaction.
- Coverage of allocatable spend.
- Commitment utilization and coverage.
- Waste reduction trend (idle spend over time).
- Forecast variance over time.

## Anti-patterns
- One-time “cost-cut” exercises with no recurring cadence.
- Optimizing only infrastructure metrics, ignoring business outcomes.
- Rightsizing without load and failover validation.
- Cost actions executed without ownership or rollback.

## Acceptance criteria
- Optimization cadence and ownership are defined.
- Top cost drivers have action plans and target dates.
- Results are tracked with before/after evidence.
- WA Cost pillar findings include remediation ownership.

### Example MAJOR_DECISION
`MAJOR_DECISION: optimization | monthly-finops-loop | Run monthly optimization cycle with prioritized actions and measurable KPI impact tracking.`
