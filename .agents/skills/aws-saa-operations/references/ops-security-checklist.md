# Operations Security Checklist

## Goal
Operationalize detective and preventive controls so incidents are detected quickly and high-risk actions are auditable.

## Logging and audit baseline
1. Enable organization-level CloudTrail with multi-Region coverage.
2. Send CloudTrail events to centralized log storage and monitoring.
3. Enable CloudTrail log file validation.
4. Protect log buckets from public access and unauthorized modification.
5. Use a dedicated log archive account and bucket separation of duties.
6. Enable SSE-KMS encryption for CloudTrail logs.

## Account and identity baseline
- [ ] Root user credentials secured and not used for routine actions.
- [ ] MFA enforced for privileged human access.
- [ ] Privileged access is time-bounded and auditable.
- [ ] Federation/SSO is the default for workforce identities.

## Threat detection baseline
- Enable Amazon GuardDuty in all in-scope Regions.
- Aggregate findings centrally and route high-severity findings to on-call.
- Enable Security Hub controls and track drift/remediation.

## Control checks
- IAM and privileged access:
  - No routine use of root credentials.
  - MFA and just-in-time elevated access.
- Encryption and secrets:
  - KMS-backed encryption for critical data paths.
  - Key rotation and secret rotation policies.
- Change safety:
  - Production changes require approvals and rollback plan.

## Deterministic detection coverage
- [ ] Alert on disabling/degrading logging or security services.
- [ ] Alert on policy changes to IAM/KMS/Organizations/network guardrails.
- [ ] Alert on anomalous root/privileged access patterns.
- [ ] Alert on critical finding states that exceed SLA without assignment.

## Operational detection rules
- Alert on high-risk API actions (IAM, KMS, Organizations, networking).
- Alert on failed console sign-ins and unusual geolocation patterns.
- Alert on disabled logging or tampering attempts.
- Add AWS Config controls for trail coverage, CloudWatch Logs integration, and encryption posture.

## Incident-readiness checks
- [ ] Security incident playbooks exist for credential compromise, data exposure, and unauthorized change.
- [ ] Evidence retention windows meet legal/compliance requirements.
- [ ] Quarterly security runbook drills completed with tracked actions.

## Anti-patterns
- Anti-pattern: enabling controls but not routing findings to owners.
  - Fix: owner mapping and SLA-based triage.
- Anti-pattern: relying on one control plane for detection.
  - Fix: combine CloudTrail, GuardDuty, and Security Hub evidence.
- Anti-pattern: no evidence retention policy.
  - Fix: immutable retention with legal/compliance-aligned durations.
- Anti-pattern: overreliance on one detection source.
  - Fix: correlate CloudTrail, GuardDuty, Security Hub, and Config.

## Acceptance checklist
- [ ] CloudTrail and log integrity enabled.
- [ ] GuardDuty + Security Hub enabled and monitored.
- [ ] Critical findings triaged within SLA.
- [ ] Security runbooks tested quarterly.
- [ ] WA security and operational excellence pillars include current control status.

## MAJOR_DECISION examples
- `MAJOR_DECISION: security-ops | org-level-detection-stack | Use org trail + centralized CloudWatch + GuardDuty/Security Hub aggregation.`
- `MAJOR_DECISION: evidence-retention | immutable-log-retention | Use immutable log retention for security/audit trails.`
