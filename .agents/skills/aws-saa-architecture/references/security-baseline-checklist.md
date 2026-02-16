# Security Baseline Checklist

## Design principles baseline
- [ ] Strong identity foundation (least privilege, separation of duties, no long-lived static creds by default).
- [ ] Traceability (monitor, alert, audit actions and config changes).
- [ ] Security at all layers (edge, network, compute, application, code).
- [ ] Security controls as code and version-controlled.
- [ ] Data protected in transit and at rest.
- [ ] Incident response preparedness with drills and automation.

## Implementation checklist
- [ ] IAM role model documented for human and workload identities.
- [ ] Encryption keys and ownership model documented.
- [ ] Logs/metrics/events routed to centralized retention and analysis path.
- [ ] Secrets management in place (no plaintext secrets in code/config).
- [ ] Network segmentation and ingress/egress policies documented.
- [ ] Security findings triage ownership and SLA defined.

## Identity and access hard requirements
- [ ] Root account protections enforced and break-glass process documented.
- [ ] Human access uses federation/SSO and MFA.
- [ ] Workload access uses roles and temporary credentials.
- [ ] High-risk permissions use approval boundaries and audit trails.

## Data protection hard requirements
- [ ] Data classification tags map to encryption and retention policy.
- [ ] Customer-managed key ownership model is documented where required.
- [ ] Backup encryption and restore authorization paths are tested.
- [ ] Secrets are rotated and never persisted in plaintext artifacts.

## Detection and response hard requirements
- [ ] API activity and configuration changes are centrally logged.
- [ ] Findings triage SLA has owner, severity mapping, and escalation path.
- [ ] Incident runbook includes communication and containment steps.
- [ ] Recovery exercises include one realistic security incident scenario.

## If/Then controls
| If | Then |
|---|---|
| Workload handles regulated/sensitive data | Enforce stronger key, access, and audit controls |
| Human direct data access is needed | Implement controlled break-glass and audit trail |
| Public ingress exists | Add layered controls (WAF/rate-limit/authN boundary) |
| Multi-account setup | Define preventive guardrails and detective controls |
| Third-party access is required | Enforce explicit trust boundaries, scoped roles, and expiry |
| Event-driven integrations cross trust boundaries | Validate producer/consumer authorization and replay protections |

## Deterministic review gate
- Each control maps to one owner role and one validation method.
- Findings are classified as `Pass`, `Needs Work`, or `Fail` in WA review.
- No production launch if critical identity or logging controls are unowned.
- Every `MAJOR_DECISION` touching trust boundaries has an ADR.

## Anti-patterns
- Wildcard IAM privileges in production paths.
- Encryption assumed but key policy/rotation ownership undefined.
- Security events logged but no owner/runbook to respond.
- Architecture decisions made without ADR traceability.

## Acceptance criteria
- Security baseline mapped to all six WA pillars (not security-only view).
- Critical controls have owners and validation cadence.
- Major security decisions are captured as ADRs with explicit trade-offs.
- Security findings include remediation owners and target completion dates.

### Example MAJOR_DECISION
`MAJOR_DECISION: security-model | workload-identity-baseline | Enforce workload IAM roles only, eliminate static credentials from runtime`
