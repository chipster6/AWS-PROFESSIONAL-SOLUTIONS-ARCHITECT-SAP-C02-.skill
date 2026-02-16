# Savings Plans Strategy Basics

## Goal
Apply commitment discounts safely using usage evidence and predictable review cycles.

## Savings Plans types (core)
| Type | Strength | Constraint |
|---|---|---|
| Compute Savings Plans | Broad flexibility across eligible compute usage | Lower max discount than most constrained options |
| EC2 Instance Savings Plans | Deeper discount for specific instance families/regions | Less flexibility |
| Database/SageMaker variants | Service-specific commitment optimization | Scope-limited applicability |

## Deterministic purchase workflow
1. Establish baseline on-demand usage over a defined lookback period.
2. Segment usage into stable baseline and variable burst.
3. Apply commitments to stable baseline first.
4. Keep burst and uncertain usage on-demand (or other appropriate model).
5. Review utilization and coverage on a fixed cadence.

## If/Then rules
| If | Then |
|---|---|
| Usage pattern is new or volatile | Delay major commitments |
| Usage is stable and persistent | Commit baseline with Savings Plans |
| Multi-account organization with centralized finance | Evaluate payer-level recommendations |
| Teams require independent budget ownership | Consider account-level or hybrid commitment strategy |

## Review and governance cadence
- Weekly: utilization and coverage drift check.
- Monthly: recommendation review and purchase candidates.
- Quarterly: strategy reset against architecture and demand changes.

## Risk controls
- Do not commit 100% of observed baseline unless risk tolerance explicitly allows.
- Document commitment owner and approval path.
- Track opportunity cost and overcommitment risk.
- Record rationale when rejecting recommendation outputs.

## Anti-patterns
- Purchasing commitments before baseline usage stabilizes.
- Treating recommendation output as auto-approval.
- Ignoring cross-account sharing and ownership implications.
- No plan to handle architecture shifts that reduce committed usage.

## Acceptance criteria
- Commitment decisions are evidence-based and documented.
- Utilization/coverage thresholds and alerts are defined.
- Purchase and review ownership is explicit.
- ADR captures commitment posture and revisit triggers.

### Example MAJOR_DECISION
`MAJOR_DECISION: cost-model | savings-plan-strategy | Commit only stable 60-80% baseline usage and review monthly for incremental purchases.`
