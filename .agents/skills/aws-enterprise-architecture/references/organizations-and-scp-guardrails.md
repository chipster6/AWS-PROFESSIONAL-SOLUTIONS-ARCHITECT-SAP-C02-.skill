# Organizations and SCP Guardrails

## Goal
Use SCPs as permission guardrails without breaking critical operations.

## SCP fundamentals
- SCPs define maximum available permissions for member accounts.
- SCPs do not grant permissions directly.
- Effective permissions are intersection of SCPs and IAM/resource policies.
- SCPs do not apply to management account identities.
- SCPs apply to delegated admin member accounts, including account root users.
- SCPs do not restrict service-linked roles.

## Guardrail classes
1. Preventive:
   - deny high-risk actions unless explicit exception.
2. Detective-aligned:
   - enforce controls supporting centralized logging/audit.
3. Segmentation:
   - enforce service/region/account boundary constraints.
4. Data perimeter:
   - constrain data movement paths where required.

## Safe rollout pattern
1. Start in `Policy Staging` OU.
2. Test in a small set of accounts.
3. Verify critical workflows still work.
4. Expand to target OUs incrementally.
5. Avoid root-level attachment until proven.
6. Use IAM service last accessed data and CloudTrail API usage to identify impacted services before tighten/deny changes.

## Deterministic SCP rollout checklist
- [ ] Baseline allow policy present and validated.
- [ ] Impacted service/API inventory documented.
- [ ] Break-glass rollback steps tested in staging OU.
- [ ] Canary accounts selected for first rollout wave.
- [ ] Business-critical workflows revalidated after policy attachment.
- [ ] Rollout decision and evidence logged in ADR/review artifacts.

## Operational rules
- Keep `FullAWSAccess` equivalent allow baseline unless intentionally replaced.
- Document exemption path for exceptional workloads.
- Track policy versioning and change approvals.
- Never detach baseline allow policy without validated replacement.
- Capture rollback procedure for every SCP rollout batch.

## Common policy patterns
| Pattern | Purpose |
|---|---|
| Region restriction | Limit usage to approved regions |
| Sensitive service deny | Block risky services not approved by policy |
| Control-protection deny | Prevent disabling logging/audit/security controls |
| Data movement guardrail | Restrict cross-account or external sharing actions |

## Anti-patterns
- Anti-pattern: immediate org-root deny policy rollout.
- Anti-pattern: SCPs treated as full IAM replacement.
- Anti-pattern: no staged validation or rollback plan.
- Anti-pattern: assuming SCPs affect management-account users.
- Anti-pattern: using SCPs to restrict service-linked roles.

## Acceptance criteria
- SCP objectives and affected scopes are documented before rollout.
- Staged rollout evidence exists for each new deny guardrail.
- Rollback path is tested and accessible.
- Exception handling path is documented and auditable.

## MAJOR_DECISION examples
- `MAJOR_DECISION: guardrails | staged-scp-rollout | Apply SCP changes in Policy Staging OU before production OUs.`
- `MAJOR_DECISION: control-model | ou-level-policies | Prefer OU-level guardrails and minimize per-account policy variance.`
