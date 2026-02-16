# Trade-Off Framework

## Goal
Create deterministic architecture comparisons rather than intuition-based choices.

## Pillar-first reasoning model
Evaluate every candidate on all six WA pillars:
1. Operational Excellence
2. Security
3. Reliability
4. Performance Efficiency
5. Cost Optimization
6. Sustainability

## Scoring table (suggested)
Use `1-5` scores where `5` is strongest fit.

| Dimension | Weight | Option A | Option B | Notes |
| --- | --- | --- | --- | --- |
| Ops Excellence |  |  |  | |
| Security |  |  |  | |
| Reliability |  |  |  | |
| Performance |  |  |  | |
| Cost |  |  |  | |
| Sustainability |  |  |  | |
| Reversibility |  |  |  | |
| Team Fit |  |  |  | |

## Weighting guidance
- Mission-critical/regulatory workloads: higher weight for Security and Reliability.
- Early-stage products with uncertain usage: higher weight for Cost and Reversibility.
- Latency-sensitive revenue paths: higher weight for Performance.

## Deterministic decision sequence
1. Fix assumptions and scope before scoring.
2. Eliminate options that violate hard constraints.
3. Score remaining options.
4. Run failure scenario stress tests.
5. Choose highest-fit option with residual-risk statement.

## Reversibility test
- Can we migrate away in < 1 quarter?
- Data portability risk acceptable?
- Operational lock-in manageable?
- Team skill acquisition path realistic?

## Common mistakes
- Mistake: scoring without explicit assumptions.
- Mistake: using equal weights for all workloads.
- Mistake: picking lowest initial cost while ignoring run-risk costs.
- Mistake: treating “works now” as “scales safely”.

## Output requirement
Always include:
- selected option,
- rejected options + reason,
- risks accepted explicitly,
- validation checks to confirm the decision in production.
