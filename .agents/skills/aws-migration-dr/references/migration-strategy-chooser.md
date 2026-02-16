# Migration Strategy Chooser

## Goal
Select deterministic migration approaches per workload using the 7 Rs with explicit constraints.

## 7 Rs quick chooser
1. **Retire**: no business value or low utilization zombie apps.
2. **Retain**: unresolved dependencies/compliance blockers/high migration risk.
3. **Rehost**: fastest lift-and-shift with minimal change.
4. **Relocate**: move platform/location with minimal app change.
5. **Repurchase**: SaaS replacement yields better value.
6. **Replatform**: moderate optimization to managed/serverless/container models.
7. **Refactor**: deep architecture change for strategic outcomes.

## Deterministic strategy selection inputs
- Business criticality and acceptable downtime during cutover.
- Application dependency complexity and unknowns.
- Compliance/security constraints that block direct migration.
- Team capacity for code change versus infrastructure move.
- Post-migration optimization goals and timeline.

## Large migration guidance
- For broad portfolio waves, prefer rehost/relocate/replatform first.
- Defer large-scale refactor until post-migration stabilization unless strict business driver exists.

## Decision matrix
| Condition | Recommended Strategy |
| --- | --- |
| Tight timeline, low change tolerance | Rehost / Relocate |
| Need managed-service cost/ops gains with moderate change | Replatform |
| Legacy app with no future value | Retire |
| Strong product pressure for cloud-native redesign | Refactor |
| Vendor SaaS offers better fit | Repurchase |

## Risk/cost trade-off cues
| Strategy | Change risk | Speed | Typical near-term cost impact |
|---|---|---|---|
| Rehost | Low-medium | Fast | Often neutral to slightly improved |
| Replatform | Medium | Medium | Often improved ops/cost profile |
| Refactor | High | Slow | Delayed payoff, highest upfront effort |
| Repurchase | Medium | Medium-fast | Can reduce ops burden, licensing trade-offs |
| Retain | Low immediate | N/A | Defers migration value realization |
| Retire | Medium (business/process) | Medium | Cost reduction when executed cleanly |

## Anti-patterns
- Choosing one strategy for all workloads.
- Refactor-first for entire portfolio without capacity.
- Ignoring dependency chains in wave design.
- Selecting strategy before validating compliance and data constraints.

## Acceptance criteria
- Every workload has a documented strategy and rationale.
- Dependencies and blockers are recorded before wave assignment.
- At least one rejected strategy is documented for critical workloads.
- `MAJOR_DECISION` markers and ADRs exist for high-impact strategy choices.

## MAJOR_DECISION examples
- `MAJOR_DECISION: migration-strategy | crm-replatform | Replatform CRM to managed database/service tier due to ops burden and moderate code impact.`
- `MAJOR_DECISION: migration-strategy | legacy-batch-retire | Retire low-value legacy batch system with no inbound usage for 90+ days.`
