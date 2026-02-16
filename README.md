# AWS Professional Solutions Architect Skill Suite

Deterministic, auditable Codex skills for AWS Solutions Architect Associate + Professional style architecture work.

## What is included

- 9 modular skills under `.agents/skills/`
- Shared workflow module under `.agents/skills/_shared/architecture-workflow/`
- Deterministic architecture artifact workflow under `docs/architecture/`
- Scripted outputs for ADRs, Well-Architected reviews, validation, and decision tracing

## Core workflow

For architecture-producing skills, use this sequence:

1. `init_arch_workflow.py`
2. Create/update `docs/architecture/solution-overviews/<system>.md`
3. `new_adr.py` for major decisions
4. `wa_review.py`
5. `validate_archifacts.py`
6. `decision_trace.py`

## Determinism and auditability

- Canonical manifest path:
  - `docs/architecture/manifest/<system>.yaml`
- Strict `MAJOR_DECISION` grammar:
  - `MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`
- Workflow version and action logging in manifest on every script run

## Repository structure

- `.agents/skills/` - active Codex skills suite
- `.agents/skills/_shared/architecture-workflow/` - shared templates and scripts (support module, not a skill)
- `docs/architecture/` - generated architecture artifacts and audits

