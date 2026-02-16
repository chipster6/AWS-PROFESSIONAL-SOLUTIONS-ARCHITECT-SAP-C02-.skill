# RTO/RPO to DR Chooser

## Goal
Map recovery objectives to DR patterns consistently.

## Pattern mapping
| DR Pattern | Typical RPO | Typical RTO | Cost/Complexity |
| --- | --- | --- | --- |
| Backup and restore | Hours (or lower with PITR) | Up to 24h | Low |
| Pilot light | Minutes | Tens of minutes | Medium |
| Warm standby | Seconds | Minutes | Medium-high |
| Multi-region active-active | Near zero | Potentially near zero | High |

## Selection rules
1. If RTO/RPO are relaxed and budget-sensitive: backup/restore.
2. If moderate RTO/RPO and lower ongoing spend needed: pilot light.
3. If fast recovery required with pre-running stack: warm standby.
4. If near-zero downtime/data loss and global availability required: active-active.

## Decision workflow
1. Confirm business impact and contractual/regulatory objectives.
2. Define acceptable RTO and RPO bounds for each critical workflow.
3. Select baseline DR pattern.
4. Validate operational readiness (runbooks, automation, test cadence).
5. Reassess cost versus impact quarterly or after major architecture changes.

## Critical distinctions
- Pilot light requires activation/provisioning before serving traffic.
- Warm standby serves traffic at reduced capacity immediately.
- Active-active requires conflict-aware data model and sync strategy.

## Data-plane rule
- Recovery runbooks should prioritize data-plane operations during failover to minimize control-plane dependency risk.

## Pattern fit cues
| Requirement cue | Strongest pattern fit |
|---|---|
| Cost-sensitive with hours-level recovery tolerance | Backup and restore |
| Moderate recovery speed with controlled cost | Pilot light |
| Fast recovery with pre-running reduced stack | Warm standby |
| Continuous service under regional disruption | Multi-region active-active |

## Anti-patterns
- Using Multi-AZ high availability as a substitute for regional DR.
- Selecting active-active without conflict resolution and operational maturity.
- No documented failback process after DR invocation.

## Acceptance criteria
- RTO/RPO objectives are explicit per critical workflow.
- Selected DR pattern is justified by business impact and cost.
- DR tests include failover and failback validation.
- WA reliability findings reference DR evidence and remediation actions.

## MAJOR_DECISION examples
- `MAJOR_DECISION: dr-posture | payments-warm-standby | Choose warm standby to satisfy sub-10-minute RTO and sub-minute RPO with controlled cost.`
- `MAJOR_DECISION: dr-posture | analytics-backup-restore | Choose backup/restore for non-customer-facing analytics with 8-hour RTO objective.`
