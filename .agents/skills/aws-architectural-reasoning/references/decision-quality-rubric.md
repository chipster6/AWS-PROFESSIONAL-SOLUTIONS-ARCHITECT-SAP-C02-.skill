# Decision Quality Rubric

## Scoring model
Rate each category `Pass`, `Needs Work`, or `Fail`.

1. **Requirements clarity**
   - Pass: assumptions and constraints are explicit and testable.
2. **Option quality**
   - Pass: at least two viable alternatives are compared.
3. **Pillar completeness**
   - Pass: all 6 WA pillars are addressed with concrete implications.
4. **Risk honesty**
   - Pass: residual risks are explicit, not hidden.
5. **Reversibility**
   - Pass: rollback/migration path is described and feasible.
6. **Auditability**
   - Pass: decision trace to ADR/WA/reviews is complete.

## Gate recommendation
- Recommended acceptance:
  - No `Fail` categories.
  - At most two `Needs Work` categories.

## Red flags
- Decision based only on “team familiarity”.
- No quantified load, latency, or recovery assumptions.
- Rejected options missing rationale.
- No failure-mode stress test evidence.

## Improvement loop
1. Fix failed categories first.
2. Re-run comparison table.
3. Update ADR/WA artifacts.
4. Re-score before approval.
