# Migration Wave and Cutover

## Goal
Execute migration in controlled waves with deterministic readiness and rollback gates.

## Wave planning baseline
1. Group workloads by dependency and blast radius.
2. Keep wave scope small enough for controlled rollback.
3. Maintain forward pipeline buffer (future waves planned ahead).
4. Define ownership: portfolio planning, migration execution, hypercare.

## Wave construction rules
- Keep each wave inside a clearly understood dependency boundary.
- Include at least one low-risk proving workload before high-criticality workloads.
- Reserve rollback capacity before cutover begins.
- Do not mix unrelated critical systems in one wave unless rollback coupling is accepted.

## Cutover readiness gates
- Data replication healthy.
- Test launch completed and accepted.
- Launch settings validated (network, instance type, security controls).
- Change freeze window agreed.
- Business and ops stakeholders on bridge.
- Security/compliance validation completed for target environment.

## Cutover flow
1. Launch cutover instances.
2. Perform acceptance tests on target.
3. Switch traffic.
4. Finalize cutover only after validation.
5. Archive/decommission source per policy.

## Deterministic cutover checkpoints
| Checkpoint | Required evidence |
|---|---|
| Pre-cutover | Replication status, acceptance test pass, rollback readiness |
| During cutover | Traffic shift logs, health checks, error/latency metrics |
| Post-cutover | Business validation signoff, data integrity checks, incident-free hold window |

## Rollback conditions
- Critical acceptance test failure.
- Data integrity mismatch.
- Performance/SLA breach during hypercare.
- Security/compliance validation failure.

## Hypercare minimums
- Enhanced monitoring window (for example 24-72 hours depending on criticality).
- On-call escalation map for migration-induced defects.
- Daily review of error rates, latency, and business KPIs.
- Exit criteria for returning to standard operations.

## MAJOR_DECISION examples
- `MAJOR_DECISION: migration-execution | wave-size-limit | Limit production wave to dependency-safe cohort with rollback in <2 hours.`
- `MAJOR_DECISION: cutover | staged-traffic-shift | Use progressive traffic shift with stop/go checkpoints and explicit rollback trigger.`
