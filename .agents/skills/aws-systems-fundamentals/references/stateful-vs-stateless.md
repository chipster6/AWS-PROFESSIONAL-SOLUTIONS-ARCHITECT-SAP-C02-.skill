# Stateful vs Stateless

## Decision objective
Choose where state lives so scaling, recovery, and consistency are explicit instead of accidental.

## Quick chooser
| Requirement | Recommended model |
|---|---|
| Rapid horizontal scale with frequent instance churn | Stateless compute + externalized state |
| Strict transactions across entities | Stateful relational layer with explicit boundaries |
| Shared mutable files across many nodes | Shared file system or object pattern, not local disk |
| Per-request personalization/session continuity | Token/session store, avoid instance affinity by default |

## State boundary inventory
| State type | Recommended placement | Notes |
|---|---|---|
| Session/auth context | External session/token store | Do not bind correctness to one compute instance |
| Transaction records | Durable transactional datastore | Define consistency and recovery guarantees |
| Derived/cache data | Cache or recomputable store | Must be rebuildable from source-of-truth |
| Files/artifacts | Shared file/object services | Avoid local ephemeral dependency for durable needs |

## If/Then rules
| If | Then |
|---|---|
| Request path must survive host replacement | Keep app tier stateless |
| State update requires ACID across multiple records | Use transactional store and capture decision as ADR |
| Data can be recomputed from event log | Prefer append/event model with idempotent processors |
| Session affinity appears required for correctness | Re-evaluate design; persistence should not depend on one node |

## Deterministic design checks
- Explicitly identify source-of-truth per data entity.
- Define write ownership for each state boundary.
- Define replay/idempotency behavior for asynchronous updates.
- Define recovery procedure for each mutable state class.
- Define data retention and deletion policy for each state class.

## Guardrails
- Keep source-of-truth state in durable managed services.
- Make ownership clear: one service owns writes for a state boundary.
- Define idempotency strategy for retries and asynchronous handlers.
- Ensure state transitions are logged and reconstructable.

## Anti-patterns
- App memory treated as durable source-of-truth.
- Stateful workloads auto-scaled without state migration contract.
- Cache invalidation policy undocumented but relied on for correctness.
- Sticky sessions used to hide missing shared state design.

## Acceptance criteria
- Stateless tiers can restart without data loss.
- Stateful tier backup/restore RTO/RPO is documented and tested.
- All mutable state has explicit owner and consistency expectation.
- Failure of one compute node does not invalidate user workflow.
- State transition auditability is available for high-risk workflows.

### Example MAJOR_DECISION
`MAJOR_DECISION: data-store | session-model | Move session state from instance memory to managed datastore for stateless scaling`
