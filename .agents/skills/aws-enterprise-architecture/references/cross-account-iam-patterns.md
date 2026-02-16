# Cross-Account IAM Patterns

## Goal
Provide secure, auditable cross-account access using temporary credentials and least privilege.

## Preferred pattern
1. Resource owner account defines IAM role.
2. Trust policy allows specific external principal/account.
3. Require `ExternalId` condition for third-party access.
4. Permission policy remains controlled by resource owner.
5. Access is short-lived via role assumption.
6. External ID generation and mapping process is auditable and tenant-unique.

## Deterministic trust policy baseline
- Trust policy principal is explicit (no wildcard principals).
- Third-party integrations require `ExternalId` where applicable.
- Session duration is bounded by operational need.
- Access is revoked by role policy or trust policy change, not key rotation.

## Role design checklist
- [ ] Explicit principal scoping (account/role ARN).
- [ ] External ID uniqueness for each third-party tenant.
- [ ] Session duration aligned with least privilege.
- [ ] CloudTrail visibility for assume-role events.
- [ ] Revocation procedure documented.
- [ ] Trust policy addresses confused deputy risk.
- [ ] Setup is automated (CloudFormation or equivalent) and drift-monitored.

## Pattern chooser
| Scenario | Recommended pattern |
|---|---|
| Central audit account reading member accounts | Read-only audit role in member accounts |
| Shared operations across workload accounts | Least-privilege ops role with scoped services/resources |
| Third-party platform integration | Dedicated per-tenant role + unique external ID |
| CI/CD deployment across accounts | Pipeline execution role with tightly scoped deploy permissions |

## Common usage patterns
- Central security account read-only audit roles.
- Shared services account operational roles.
- Third-party monitoring/integration roles with strict scope.

## Anti-patterns
- Anti-pattern: long-term access keys for external parties.
- Anti-pattern: default trust policy with no conditions.
- Anti-pattern: reused external IDs across customers.
- Anti-pattern: manual one-off role setup with no repeatable audit trail.
- Anti-pattern: non-revocable integration path without tested disable procedure.

## Acceptance criteria
- All cross-account access uses role assumption and temporary credentials.
- Trust policies have explicit principals and required conditions.
- Assume-role events are visible and monitored.
- Revocation is tested and documented.

## MAJOR_DECISION examples
- `MAJOR_DECISION: trust-boundary | cross-account-role-model | Use role assumption with external IDs for all third-party cross-account access.`
- `MAJOR_DECISION: access-governance | owner-managed-permissions | Keep permission policies in resource-owner account, not third-party-managed.`
