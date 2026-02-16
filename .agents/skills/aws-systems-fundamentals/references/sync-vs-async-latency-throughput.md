# Sync vs Async: Latency and Throughput

## Decision matrix
| Signal | Prefer sync | Prefer async |
|---|---|---|
| User needs immediate confirmed result | Yes | Only if callback/polling UX is acceptable |
| Downstream dependency is unstable or slow | No | Yes |
| High burst or queueable workload | No | Yes |
| Strict request ordering and low staleness tolerance | Yes | Possible with ordering controls |
| Large fan-out processing | No | Yes |

## Threshold cues (starter defaults)
- End-user p95 latency target under 300ms: minimize synchronous hop count.
- Downstream p95 above 200ms: strongly consider decoupling with queue/event.
- Retry budget >2 for critical path: move expensive retries off sync path.
- End-user flow can tolerate delayed completion: return accepted status and process async.

## If/Then rules
| If | Then |
|---|---|
| A dependency can fail independently | Put circuit breaker and fallback around sync calls |
| Work can complete after user response | Shift to async and return accepted status |
| At-least-once delivery is used | Require idempotency key and dedupe strategy |
| Async path drives user-visible state | Add status model, timeout policy, and reconciliation |

## Delivery semantics checklist
| Requirement | Control |
|---|---|
| Duplicate processing is unacceptable | Idempotency key + dedupe store |
| Ordered processing required | Partition key and explicit ordering strategy |
| Exactly-once business outcome desired | At-least-once delivery + idempotent state transitions |
| User-visible completion certainty required | Status query endpoint or callback contract |

## Failure handling baseline
- Sync path:
  - timeout budget per hop,
  - bounded retries with jitter,
  - fallback response contract.
- Async path:
  - dead-letter queue policy,
  - replay controls,
  - poison message handling,
  - idempotent consumers.

## Deterministic latency budgeting
- Define end-to-end p95 and p99 objectives.
- Allocate per-hop timeout and retry budgets.
- Identify noncritical work moved off request path.
- Define stale-state UX behavior for async completion lag.
- Define alert thresholds for queue lag and DLQ depth.

## Anti-patterns
- Chained synchronous calls across multiple unreliable dependencies.
- Async adoption without observability, retry, or DLQ policies.
- “Exactly once” assumed without explicit mechanism.
- User experience that hides eventual consistency delays.

## Acceptance criteria
- Critical path has explicit latency/error budget and dependency count.
- Async flows define delivery semantics and recovery actions.
- Retries do not create duplicate side effects.
- Operational dashboards expose sync latency and async backlog separately.
- At least one ADR records integration style choice for each critical workflow.

### Example MAJOR_DECISION
`MAJOR_DECISION: integration-style | order-processing-flow | Move payment settlement to async workflow with idempotent processor and DLQ`
