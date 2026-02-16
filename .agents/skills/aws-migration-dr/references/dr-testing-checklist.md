# DR Testing Checklist

## Goal
Prove DR strategy works under real conditions and meets declared objectives.

## Mandatory test scope
1. Data restoration integrity checks.
2. Application functional checks.
3. RTO measurement from event start to service readiness.
4. RPO measurement against last recoverable point.
5. Failback procedure validation.

## Test scenario minimum set
- Regional failure simulation.
- Data corruption recovery scenario.
- Control-plane impairment scenario (limited dependency operations).
- Communication/escalation dry run.

## Test cadence guidance
- Tier 0 workloads: monthly or more frequent.
- Tier 1 workloads: quarterly.
- Tier 2 workloads: semi-annual.

## Evidence required
- Timestamped run logs.
- Measured RTO and RPO outcomes.
- Defect/remediation records with owners.
- Updated runbook deltas.

## Deterministic pass/fail criteria
- Pass when measured RTO and RPO are within target bounds and all critical checks pass.
- Needs Work when recovery succeeds but one or more noncritical controls fail.
- Fail when RTO/RPO misses, integrity checks fail, or failback cannot be executed safely.

## Restore testing controls (AWS Backup aligned)
- Define restore testing plans for in-scope resources.
- Set frequency and start window appropriate to criticality.
- Run post-restore validation checks and record outcomes.
- Track quota/capacity constraints that can delay test execution.

## Anti-patterns
- DR plan exists but never rehearsed.
- Backup success treated as restore success.
- Tests that skip user-facing validation.
- Tests executed without documenting measured timings and outcomes.

## Acceptance criteria
- Critical systems have recent DR test evidence.
- Failures produce remediation items with owners and due dates.
- Runbooks are updated after every meaningful test finding.
- WA reliability pillar review references DR test outputs.

## MAJOR_DECISION examples
- `MAJOR_DECISION: dr-validation | quarterly-dr-drills | Run quarterly end-to-end DR drills with measured RTO/RPO evidence.`
- `MAJOR_DECISION: dr-validation | failback-standard | Require failback rehearsal before production sign-off.`
