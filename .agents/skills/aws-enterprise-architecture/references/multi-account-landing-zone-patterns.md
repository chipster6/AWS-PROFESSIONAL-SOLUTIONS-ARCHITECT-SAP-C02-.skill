# Multi-Account Landing Zone Patterns

## Goal
Establish clear account boundaries, policy inheritance, and lifecycle separation for enterprise AWS environments.

## Baseline OU model
1. Foundational OUs:
   - `Security` (log archive, security tooling, break-glass).
   - `Infrastructure` (network/shared platform services).
2. Workload OUs:
   - `SDLC` / non-production.
   - `Prod` / production.
3. Support OUs:
   - `Sandbox`, `Policy Staging`, `Suspended`, `Exceptions` as needed.

## Foundational account set
| Account purpose | Typical placement |
|---|---|
| Management/governance | Root-level governance scope |
| Log archive | Security OU |
| Security tooling | Security OU |
| Shared networking | Infrastructure OU |
| Shared platform services | Infrastructure OU |
| Workload accounts | Workloads OU (`Prod`, `NonProd`) |

## Design rules
- Organize OUs by control boundary and function, not corporate org chart.
- Separate production from non-production accounts.
- Apply broad controls at OU level; use account-level exceptions sparingly.
- Keep policy staging OU for safe policy rollout testing.

## Deterministic account boundary triggers
Create a separate account when one or more of these are true:
- Different data classification or regulatory controls are required.
- Different operational ownership or deployment lifecycle is required.
- Workload failure blast radius must be isolated.
- Independent quota or billing ownership is needed.
- Exception controls would otherwise weaken shared guardrails.

## Account boundary heuristics
- Separate accounts when:
  - blast radius must be isolated,
  - quota boundaries are needed,
  - compliance controls differ,
  - ownership/lifecycle differs.

## Anti-patterns
- Anti-pattern: one large “shared everything” account.
- Anti-pattern: OU hierarchy mirrors reporting lines instead of control needs.
- Anti-pattern: production dependencies on SDLC accounts.
- Anti-pattern: no designated exception OU for temporary policy deviations.
- Anti-pattern: shared IAM admin access model across unrelated workload accounts.

## Acceptance criteria
- OU hierarchy is documented with purpose and control boundaries.
- Foundational accounts are separated from workload accounts.
- Production and non-production workloads are isolated.
- Policy staging path exists for controlled rollout.
- At least one ADR records account boundary rationale for each critical domain.

## MAJOR_DECISION examples
- `MAJOR_DECISION: account-strategy | workload-ou-model | Use Security/Infrastructure foundational OUs and split Workloads into SDLC + Prod OUs.`
- `MAJOR_DECISION: governance | policy-staging-ou | Enforce staged SCP rollout through a dedicated Policy Staging OU before broad attachment.`
