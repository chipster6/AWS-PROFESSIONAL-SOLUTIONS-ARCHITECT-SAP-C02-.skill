# CAP and Consistency Primer

## Core framing
- Under network partition, distributed designs must trade off consistency and availability.
- Choose consistency level by business consequence, not by technical preference.
- State the read/write contract explicitly for each data category.
- CAP framing is for partitioned distributed systems; use it to clarify failure behavior, not as a slogan.

## Consistency chooser
| Data type / workflow | Suggested consistency | Why |
|---|---|---|
| Financial balances, inventory decrements | Strong | Incorrect reads/writes have direct business impact |
| User feeds, analytics dashboards | Eventual | Freshness lag is often acceptable |
| Config, entitlement, feature flags | Strong or monotonic | Inconsistent reads can create policy/security defects |
| Idempotent event replay state | Eventual with reconciliation | Can be repaired safely |

## Consistency contract checklist
- Read-after-write required? For which workflows?
- Maximum tolerable staleness (seconds/minutes)?
- Conflict resolution strategy (last-write-wins, version check, merge policy)?
- User-visible behavior during stale reads?
- Reconciliation frequency and owner?

## If/Then rules
| If | Then |
|---|---|
| Stale read can violate policy or billing | Enforce strong consistency path |
| Temporary staleness is acceptable | Use eventual consistency + freshness SLO |
| Write availability during partitions is critical | Accept reconciliation complexity explicitly |
| Multiple writers compete on same entity | Add versioning / conflict strategy |

## Consistency mode selection table
| Mode | Use when | Trade-off |
|---|---|---|
| Strong consistency | Financial/security-critical correctness required | Higher latency/availability trade-offs under partition scenarios |
| Eventual consistency | Read freshness lag is acceptable | Must manage stale reads and reconciliation |
| Monotonic/session consistency | User journey must not move backward | Requires session-aware design controls |

## Practical checks
- What is maximum tolerable staleness?
- What happens on conflicting concurrent writes?
- Is read-after-write required for user journey?
- What is repair/reconciliation runbook?

## Anti-patterns
- Global strong-consistency assumption without latency budget analysis.
- Eventual consistency used on entitlement/billing decisions without safeguards.
- Conflict resolution left implicit in application code.

## Acceptance criteria
- Each critical data domain has a declared consistency mode.
- Reconciliation strategy exists for eventually-consistent workflows.
- User-visible behavior for stale/lagging state is defined.
- Test scenarios include partition-like impairment and stale-read handling.

### Example MAJOR_DECISION
`MAJOR_DECISION: consistency | account-balance-read | Use strongly consistent reads for balance updates and withdrawals`
