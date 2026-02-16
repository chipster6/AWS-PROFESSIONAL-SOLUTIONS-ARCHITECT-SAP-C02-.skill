# Incident Response Checklist

## Goal
Provide deterministic steps for handling operational and security incidents with clear escalation, containment, and recovery actions.

## Incident phases
1. Detect: confirm signal quality and classify severity.
2. Analyze: scope blast radius, affected services, and customer impact.
3. Contain: stop further impact.
4. Eradicate: remove root cause or threat vector.
5. Recover: restore service safely.
6. Learn: capture timeline, actions, and prevention tasks.

## Severity model baseline
| Severity | Typical impact | Update cadence |
|---|---|---|
| `SEV-1` | Major customer-facing outage or security compromise | 15 minutes |
| `SEV-2` | Partial degradation with material risk | 30 minutes |
| `SEV-3` | Limited impact with workaround | 60 minutes |

## Playbook minimum fields
- Scenario and trigger.
- Prerequisites (logs, dashboards, query tooling, access roles).
- Communications matrix (incident commander, service owner, security, customer comms).
- Tactical steps per phase.
- Expected outcomes and rollback criteria.
- Recovery validation checks.

## Decision matrix (containment)
- If customer data exposure is suspected:
  - Immediately isolate impacted path, rotate credentials, and involve security lead.
- If availability-only issue with no integrity risk:
  - Prioritize rollback/failover path first, then deep root-cause analysis.
- If scope unknown:
  - Freeze risky changes, enable conservative traffic controls, collect forensic evidence.

## Deterministic command model
1. Assign incident commander.
2. Assign technical lead.
3. Assign communications lead.
4. Assign scribe/timekeeper.
5. Confirm backups for each role.

## Communications contract
1. Declare incident in a single canonical channel.
2. Publish status updates on fixed cadence (for example every 15 minutes for `SEV-1`).
3. Include known impact, current mitigation, and next update time.
4. Capture all commands/actions in timeline notes.
5. Record major decision points with rationale and approver.

## Failure-mode checks
- Are alarms reflecting current user impact or only infrastructure health?
- Did any retry/circuit-breaker settings amplify failure?
- Did recent deployment/config/IAM/SCP changes correlate with onset?
- Are there regional dependencies that prevent failover?

## Recovery exit criteria
- Impacted SLOs are back within target for agreed observation window.
- Temporary bypasses are removed or explicitly accepted with owner/date.
- Data integrity checks complete for affected systems.
- Final communication includes impact, timeline, and next remediations.

## Anti-patterns
- Anti-pattern: treating every page as unique.
  - Fix: map to predefined scenario classes and playbooks.
- Anti-pattern: single responder owns all tracks.
  - Fix: split command, comms, and technical lead roles.
- Anti-pattern: closing incident without recovery proof.
  - Fix: require evidence-based exit criteria.
- Anti-pattern: undefined incident roles at declaration time.
  - Fix: enforce minimum command structure before major actions.

## Acceptance checklist
- [ ] Incident commander and escalation contacts defined.
- [ ] At least top 5 incident scenarios have playbooks.
- [ ] Tabletop test completed in last 90 days.
- [ ] Post-incident review includes remediations with owners/dates.
- [ ] Incident timeline captures major decisions and linked ADRs where needed.

## MAJOR_DECISION examples
- `MAJOR_DECISION: incident-model | sev-classification | Use SEV-1/2/3 incident classes with fixed escalation timers.`
- `MAJOR_DECISION: containment | traffic-isolation-strategy | Route failover traffic via pre-approved controls before deep debugging.`
