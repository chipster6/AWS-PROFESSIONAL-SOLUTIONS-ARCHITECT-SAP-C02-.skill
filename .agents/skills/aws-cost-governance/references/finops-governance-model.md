# FinOps Governance Model

## Goal
Define clear accountability and decision rights for cloud financial management.

## Operating model roles
| Role | Core responsibility |
|---|---|
| Finance/FinOps lead | Policy, reporting, budget controls, commitment approvals |
| Platform team | Shared services cost posture, tagging enforcement, guardrails |
| Application owners | Workload optimization actions, demand forecasting, anomaly response |
| Security/compliance | Ensure optimization does not violate control obligations |

## Decision rights matrix
| Decision type | Primary owner | Consulted parties |
|---|---|---|
| Allocation/tagging policy | FinOps + Platform | App owners, Finance |
| Commitment purchase strategy | FinOps/Finance | Platform, App owners |
| Workload rightsizing | App owner | Platform, SRE |
| Budget/anomaly thresholds | FinOps | App owners, Finance |
| Exception approvals | Governance board | Security, Finance, Platform |

## Governance cadence
- Weekly: anomaly triage and remediation progress.
- Monthly: spend review, forecast variance, action tracking.
- Quarterly: commitment strategy and policy tuning.

## Deterministic policy controls
- Budget thresholds by environment and workload class.
- Anomaly response SLA by severity.
- Required metadata/tagging compliance target.
- Standard exception process with expiry and owner.
- ADR requirement for major cost model commitments.

## Escalation model
| Condition | Escalation path |
|---|---|
| Forecast variance exceeds threshold | App owner -> FinOps lead -> exec sponsor |
| Unowned anomaly persists beyond SLA | FinOps lead -> platform leadership |
| Commitment utilization below target over sustained period | FinOps lead -> architecture and capacity review |

## Anti-patterns
- Cost governance treated as finance-only problem.
- No ownership for shared platform spend.
- Anomalies detected but no response SLA.
- Exception approvals with no expiry date.

## Acceptance criteria
- FinOps operating model documented and approved.
- Decision rights and escalation paths are explicit.
- Governance meetings produce tracked actions.
- Cost policy exceptions are time-bounded and auditable.

### Example MAJOR_DECISION
`MAJOR_DECISION: governance | finops-operating-model | Establish FinOps + platform + app owner shared model with monthly accountability reviews.`
