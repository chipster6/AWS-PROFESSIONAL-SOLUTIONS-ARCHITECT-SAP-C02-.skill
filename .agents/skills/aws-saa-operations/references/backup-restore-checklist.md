# Backup and Restore Checklist

## Goal
Ensure backup integrity and recovery capability meet RTO/RPO targets using repeatable restore testing.

## Baseline controls
1. Identify all data stores and classify by criticality.
2. Define RTO/RPO per system and dataset.
3. Configure backup methods and retention policy.
4. Test restoration periodically and measure completion time.
5. Record results and remediation actions.

## Recovery objective mapping
| Criticality tier | Typical objective posture | Minimum validation |
|---|---|---|
| Tier 0 (mission critical) | Very low RTO/RPO tolerance | Frequent restore testing + app functional validation |
| Tier 1 (important) | Moderate RTO/RPO tolerance | Scheduled restore drills + integrity checks |
| Tier 2 (supporting) | Relaxed objectives | Periodic restore verification |

## Service-specific guidance
- Amazon RDS/Aurora:
  - Enable automated backups and PITR where required.
  - Validate restore from snapshot and PITR paths.
- DynamoDB:
  - Use PITR and validate table restore flows.
- EBS/EFS/S3:
  - Snapshot or versioning/object lock policies aligned to compliance.
- Hybrid servers:
  - Use AWS Backup / AWS Elastic Disaster Recovery where appropriate.

## Restore testing automation baseline
- Use AWS Backup restore testing plans for scheduled recoverability checks.
- Define resource scope and frequency per criticality tier.
- Add validation automation (for example, EventBridge + Lambda verification).
- Capture restore duration and compare against target restore time.

## Test cadence recommendations
- Tier 0 critical: weekly restore drill.
- Tier 1 important: monthly restore drill.
- Tier 2 supporting: quarterly restore drill.

## Restore test workflow
1. Restore into isolated test environment.
2. Validate data completeness, accessibility, and integrity.
3. Measure end-to-end restore + verification time.
4. Compare against RTO/RPO targets.
5. Open remediation actions if objectives are missed.

## Deterministic validation checks
- Recovery point selected by documented rule (latest successful, point-in-time, or policy-based).
- Data integrity query set is versioned and repeatable.
- Application readiness check includes dependencies, not only datastore status.
- Failback path is tested for at least critical systems.
- Evidence artifacts are attached to reviews (timestamps, metrics, pass/fail).

## Anti-patterns
- Anti-pattern: backup success assumed as restore success.
  - Fix: mandatory restore testing with evidence.
- Anti-pattern: restore test without data validation queries.
  - Fix: run deterministic integrity checks.
- Anti-pattern: RTO measured only for restore API completion.
  - Fix: include app/service readiness validation.
- Anti-pattern: restore tests run in shared production-like environments causing risk.
  - Fix: restore into isolated validation environments with controlled access.

## Acceptance checklist
- [ ] Recovery objectives are documented and approved.
- [ ] Restore tests executed with auditable logs.
- [ ] Failures have tracked remediation tickets.
- [ ] Data retention and immutability controls align with policy.
- [ ] WA reliability findings reflect latest restore evidence.

## MAJOR_DECISION examples
- `MAJOR_DECISION: backup-strategy | tiered-restore-cadence | Use weekly/monthly/quarterly restore cadence by business criticality.`
- `MAJOR_DECISION: dr-tooling | drs-vs-native-backups | Use AWS Elastic Disaster Recovery for legacy VM fleet and native backup/PITR for managed data services.`
