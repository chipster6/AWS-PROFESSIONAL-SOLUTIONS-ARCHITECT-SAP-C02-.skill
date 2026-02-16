# AWS Skills Implementation TODO

Use this checklist as the execution tracker. Mark each item with `[x]` as it is completed.

## 1) Scaffolding
- [x] Create `REPO_ROOT/.agents/skills/`.
- [x] Create `REPO_ROOT/.agents/skills/_shared/architecture-workflow/`.
- [x] Create `REPO_ROOT/.agents/skills/_shared/architecture-workflow/templates/`.
- [x] Create `REPO_ROOT/.agents/skills/_shared/architecture-workflow/scripts/`.
- [x] Ensure there is no `SKILL.md` under `_shared/architecture-workflow/`.

## 2) Shared Templates
- [x] Create `adr-short.md`.
- [x] Create `adr-full.md`.
- [x] Create `well-architected-review.md`.
- [x] Create `solution-overview.md`.
- [x] Create `threat-model-lite.md`.
- [x] Create `runbook-baseline.md`.
- [x] Add ADR YAML fields to both ADR templates: `decision_id`, `system`, `category`, `status`, `owners`, `date`, `tags`, `supersedes`, `superseded_by`.
- [x] Add 6 WA pillars, score rubric, and Findings/Remediations to WA template.
- [x] Add canonical marker grammar in templates: `MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`.

## 3) Shared Workflow Scripts
- [x] Implement `_shared/.../init_arch_workflow.py`.
- [x] Implement `_shared/.../new_adr.py`.
- [x] Implement `_shared/.../wa_review.py`.
- [x] Implement `_shared/.../validate_archifacts.py`.
- [x] Implement `_shared/.../decision_trace.py`.
- [x] Set `WORKFLOW_VERSION = "1.0.0"` in each shared script.
- [x] Require CLI args by default in each shared script.
- [x] Allow prompting only with `--interactive`.
- [x] Return non-zero with actionable messages for missing required args.
- [x] Implement deterministic repo-root resolution (`.git/` or `.agents/skills/`).

## 4) Canonical Manifest Rules
- [x] Enforce canonical manifest path: `REPO_ROOT/docs/architecture/manifest/<system>.yaml`.
- [x] Ensure scripts create `REPO_ROOT/docs/architecture/manifest/` if missing.
- [x] Ensure scripts read/write only canonical `manifest_path`.
- [x] Add manifest top-level keys: `system`, `manifest_path`, `repo_root`, `workflow_version`, `last_updated`.
- [x] Add manifest sections: `artifacts`, `adrs`, `wa_reviews`, `validations`, `decision_traces`, `actions`.
- [x] Append `actions` entry on every script run (script, timestamp, inputs, outputs, exit_code, workflow_version).

## 5) Validation and Gate Logic
- [x] Validate WA review has all 6 pillars.
- [x] Validate each WA pillar has a score (`Pass|Needs Work|Fail`).
- [x] Enforce default gate: no `Fail`, max `2` `Needs Work`.
- [x] Support overrides: `--allow-fail-pillars`, `--max-needs-work`.
- [x] Parse only canonical `MAJOR_DECISION` grammar.
- [x] Require ADR mapping for each `MAJOR_DECISION` (`decision_id` or slug).
- [x] Fail predictably with non-zero + actionable errors when validation fails.

## 6) Skill Directories and Content
- [x] Create `aws-systems-fundamentals` with `SKILL.md` + 4 references.
- [x] Create `aws-aws-foundations` with `SKILL.md` + 4 references.
- [x] Create `aws-saa-architecture` with `SKILL.md` + 5 references + 5 wrapper scripts.
- [x] Create `aws-saa-operations` with `SKILL.md` + 4 references + 5 wrapper scripts.
- [x] Create `aws-architectural-reasoning` with `SKILL.md` + 4 references.
- [x] Create `aws-enterprise-architecture` with `SKILL.md` + 5 references + 5 wrappers + `agents/openai.yaml`.
- [x] Create `aws-migration-dr` with `SKILL.md` + 5 references + 5 wrappers + `agents/openai.yaml`.
- [x] Create `aws-cost-governance` with `SKILL.md` + 4 references + 5 wrapper scripts.
- [x] Create `aws-evals` with `SKILL.md` + `references/evals.md` + `scripts/run_evals.py`.

## 7) Wrapper Script Contract (C/D/F/G/H)
- [x] Resolve repo root by upward walk.
- [x] Resolve shared script path in `_shared/architecture-workflow/scripts/`.
- [x] Execute via subprocess: `python3 <shared_script> <args...>`.
- [x] Forward args unchanged.
- [x] Return exact child exit code.
- [x] Emit actionable non-zero errors if root/shared script missing.
- [x] Avoid Python import coupling in wrappers.

## 8) SKILL.md Standardization
- [x] Add valid YAML frontmatter to all 9 skills (`name`, `description: > Use when ...`).
- [x] Include required sections in order for all skills.
- [x] Include required 7 output headings in all skills.
- [x] Keep trigger cues and anti-triggers narrow to avoid misfires.
- [x] Add strict ADR threshold rules to C/D/F/G/H.
- [x] Add strict workflow sequence to C/D/F/G/H.
- [x] Add canonical `MAJOR_DECISION` grammar to C/D/F/G/H.

## 9) Professional Metadata
- [x] Create `aws-enterprise-architecture/agents/openai.yaml`.
- [x] Create `aws-migration-dr/agents/openai.yaml`.
- [x] Set `allow_implicit_invocation: true` for both.
- [x] Add dependency placeholder `aws-documentation-mcp`.
- [x] Ensure no external hostnames/URLs in metadata.

## 10) Evals Skill
- [x] Add 4 scenarios + pass/fail rubrics in `aws-evals/references/evals.md`:
  - [x] Associate gate
  - [x] Bridge trade-off
  - [x] Professional gate
  - [x] Failure analysis
- [x] Implement `aws-evals/scripts/run_evals.py`:
  - [x] Print prompts.
  - [x] Collect notes.
  - [x] Write `docs/architecture/reviews/EVAL-NOTES-YYYYMMDD.md`.
  - [x] Log to manifest when system-scoped.

## 11) Final Verification
- [x] Verify `_shared/architecture-workflow` has no `SKILL.md`.
- [x] Verify all 9 skill folders contain `SKILL.md`.
- [x] Verify each skill has 2–5 non-placeholder references.
- [x] Verify wrappers dispatch to shared scripts and preserve exit codes.
- [x] Verify missing required args produce deterministic non-zero errors.
- [x] Verify all scripts write manifest only to `REPO_ROOT/docs/architecture/manifest/<system>.yaml`.
- [x] Verify ADR filenames follow `ADR-YYYYMMDD-<slug>.md`.
- [x] Verify ADR files contain required YAML metadata.
- [x] Verify validator enforces pillars, scores, gate policy, and MAJOR_DECISION->ADR mapping.
- [x] Verify no extraneous `README`/changelog/install files were created.

---

## Reference Plan (Copy)

### 1) Objective
Create a complete Codex skills implementation under:

`REPO_ROOT/.agents/skills/`

with:
1. 9 modular skills (8 architecture/domain + 1 evals).
2. deterministic, script-enforced architecture workflow.
3. auditable outputs under `REPO_ROOT/docs/architecture/`.
4. shared workflow module to eliminate duplication.
5. strict ADR + Well-Architected gating.

### 2) Skill Inventory (9)
1. `aws-systems-fundamentals`
2. `aws-aws-foundations`
3. `aws-saa-architecture`
4. `aws-saa-operations`
5. `aws-architectural-reasoning`
6. `aws-enterprise-architecture`
7. `aws-migration-dr`
8. `aws-cost-governance`
9. `aws-evals`

### 3) Shared Support Module (Not a Skill)
Create:

`REPO_ROOT/.agents/skills/_shared/architecture-workflow/`

with:
- `templates/`
- `scripts/`

Critical rule:
- Do **not** create `SKILL.md` inside `_shared/architecture-workflow/`.

#### 3.1 Shared templates
1. `adr-short.md`
2. `adr-full.md`
3. `well-architected-review.md`
4. `solution-overview.md`
5. `threat-model-lite.md`
6. `runbook-baseline.md`

#### 3.2 Shared scripts
1. `init_arch_workflow.py`
2. `new_adr.py`
3. `wa_review.py`
4. `validate_archifacts.py`
5. `decision_trace.py`

All shared scripts define:

`WORKFLOW_VERSION = "1.0.0"`

### 4) Per-Skill File Plan

#### 4.1 `aws-systems-fundamentals`
- `SKILL.md`
- `references/failure-domains-and-blast-radius.md`
- `references/stateful-vs-stateless.md`
- `references/sync-vs-async-latency-throughput.md`
- `references/cap-and-consistency-primer.md`

#### 4.2 `aws-aws-foundations`
- `SKILL.md`
- `references/aws-global-infrastructure.md`
- `references/shared-responsibility.md`
- `references/service-taxonomy.md`
- `references/pricing-basics.md`

#### 4.3 `aws-saa-architecture`
- `SKILL.md`
- `references/alb-vs-nlb-matrix.md`
- `references/storage-selection-matrix.md`
- `references/database-selection-matrix.md`
- `references/ha-multi-az-patterns.md`
- `references/security-baseline-checklist.md`
- wrappers in `scripts/`:
  - `init_arch_workflow.py`
  - `new_adr.py`
  - `wa_review.py`
  - `validate_archifacts.py`
  - `decision_trace.py`

#### 4.4 `aws-saa-operations`
- `SKILL.md`
- `references/observability-baseline.md`
- `references/incident-response-checklist.md`
- `references/backup-restore-checklist.md`
- `references/ops-security-checklist.md`
- same 5 wrapper scripts

#### 4.5 `aws-architectural-reasoning`
- `SKILL.md`
- `references/tradeoff-framework.md`
- `references/anti-pattern-catalog.md`
- `references/failure-analysis-checklist.md`
- `references/decision-quality-rubric.md`

#### 4.6 `aws-enterprise-architecture`
- `SKILL.md`
- `agents/openai.yaml`
- `references/multi-account-landing-zone-patterns.md`
- `references/organizations-and-scp-guardrails.md`
- `references/cross-account-iam-patterns.md`
- `references/hub-spoke-and-tgw-patterns.md`
- `references/hybrid-connectivity-overview.md`
- same 5 wrapper scripts

#### 4.7 `aws-migration-dr`
- `SKILL.md`
- `agents/openai.yaml`
- `references/migration-strategy-chooser.md`
- `references/rto-rpo-to-dr-chooser.md`
- `references/dr-patterns-and-tradeoffs.md`
- `references/migration-wave-and-cutover.md`
- `references/dr-testing-checklist.md`
- same 5 wrapper scripts

#### 4.8 `aws-cost-governance`
- `SKILL.md`
- `references/cost-allocation-and-tagging.md`
- `references/savings-plans-basics.md`
- `references/cost-optimization-playbook.md`
- `references/finops-governance-model.md`
- same 5 wrapper scripts

#### 4.9 `aws-evals`
- `SKILL.md`
- `references/evals.md`
- `scripts/run_evals.py`

### 5) SKILL.md Contract (All Skills)
Every `SKILL.md` must start with YAML frontmatter:
- `name: <skill-id>`
- `description: > Use when ...`

Required sections (in order):
1. Purpose
2. When to use
3. When NOT to use
4. Inputs to request
5. Required workflow
6. Decision workflow
7. Rules & guardrails
8. Output format
9. Reference index

Required output headings:
1. Requirements & Assumptions
2. Proposed Architecture
3. Well-Architected Pillar Review (6 pillars)
4. Key Decisions & Trade-offs (link to ADRs if created)
5. Risks / Failure Modes
6. Implementation Notes (services + key configs)
7. Next Steps / Validation Checks (include scripts to run)

Routing guardrail:
- Frontmatter + anti-triggers are intentionally narrow to prevent misfires.

### 6) Architecture-Producing Skill Rules (C/D/F/G/H)

#### 6.1 ADR threshold (must create ADRs for)
1. datastore class/engine family choices
2. sync vs async integration model choices
3. trust boundary/auth model choices
4. network topology/segmentation/egress/endpoint choices
5. RTO/RPO and DR posture choices
6. region/account/partition strategy choices
7. major cost model commitments

#### 6.2 Mandatory script workflow
1. `init_arch_workflow.py`
2. update solution overview
3. `new_adr.py` (all required ADRs)
4. `wa_review.py`
5. `validate_archifacts.py`
6. `decision_trace.py`

#### 6.3 Canonical major decision grammar
Use exactly:

`MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`

Validator parses only this grammar.

### 7) Wrapper Script Contract (C/D/F/G/H)
Each wrapper script:
1. resolves repo root by walking up until `.git/` or `.agents/skills/` exists
2. resolves shared script path under `_shared/architecture-workflow/scripts/`
3. executes shared script via subprocess:

`python3 <shared_script> <args...>`

4. forwards args unchanged
5. returns exact child exit code
6. emits actionable non-zero errors if root/script not found

No Python import coupling in wrappers.

### 8) Canonical Manifest Rules (Pinned)
Canonical manifest file is `<system>.yaml`, always stored at:

`REPO_ROOT/docs/architecture/manifest/<system>.yaml`

All scripts MUST:
1. resolve `REPO_ROOT` first
2. compute:
   - `manifest_dir = REPO_ROOT/docs/architecture/manifest`
   - `manifest_path = manifest_dir/<system>.yaml`
3. create `manifest_dir` if missing
4. read/write only `manifest_path`
5. never write manifest based on current working directory

Required top-level manifest keys:
1. `system`
2. `manifest_path`
3. `repo_root`
4. `workflow_version`
5. `last_updated`

Plus operational sections:
- `artifacts`
- `adrs`
- `wa_reviews`
- `validations`
- `decision_traces`
- `actions`

Each script appends an `actions` entry with:
- script name
- timestamp
- inputs
- outputs
- exit_code
- workflow_version

### 9) Shared Script Specifications

#### 9.1 `init_arch_workflow.py`
Required: `--system`

Creates/ensures:
- `docs/architecture/decisions`
- `docs/architecture/reviews`
- `docs/architecture/diagrams`
- `docs/architecture/threat-models`
- `docs/architecture/runbooks`
- `docs/architecture/solution-overviews`
- `docs/architecture/manifest`
- `docs/architecture/index.md`

Updates manifest action log.

#### 9.2 `new_adr.py`
Required:
- `--system --title --category --status --owners --tags`

Optional:
- `--slug --date --supersedes --superseded-by --template short|full --interactive`

Output:
- `docs/architecture/decisions/ADR-YYYYMMDD-<slug>.md`

Writes ADR YAML metadata header:
- `decision_id`
- `system`
- `category`
- `status`
- `owners`
- `date`
- `tags`
- `supersedes`
- `superseded_by`

Also updates `docs/architecture/index.md` + manifest.

#### 9.3 `wa_review.py`
Required: `--system`
Optional: `--date --interactive`

Output:
- `docs/architecture/reviews/WA-REVIEW-YYYYMMDD-<system>.md`

Must contain:
- all 6 WA pillars
- per-pillar score (`Pass|Needs Work|Fail`)
- findings/remediations
- optional canonical `MAJOR_DECISION:` lines

Updates manifest.

#### 9.4 `validate_archifacts.py`
Required: `--system`
Optional:
- `--max-needs-work <int>` default `2`
- `--allow-fail-pillars` default `false`
- `--interactive`

Validates:
1. solution overview exists
2. WA review exists
3. WA review has all 6 pillars
4. every pillar has score
5. each `MAJOR_DECISION` maps to ADR (`decision_id` or slug)
6. gate policy passes:
   - no Fail unless override
   - Needs Work <= threshold

Failure: non-zero + actionable errors.
Updates manifest with gate config/result/issues.

#### 9.5 `decision_trace.py`
Required: `--system`
Optional: `--date --interactive`

Output:
- `docs/architecture/reviews/DECISION-TRACE-YYYYMMDD-<system>.md`

Maps:
- major decisions -> ADRs -> WA findings/remediations

Updates manifest.

### 10) Template Content Requirements

#### 10.1 ADR templates (`adr-short.md`, `adr-full.md`)
Both include YAML metadata fields listed above and sections:
- Title
- Status
- Context
- Decision
- Alternatives
- Consequences
- Security/Compliance notes
- Cost notes
- Operational notes
- References
- Date
- Owners

#### 10.2 WA review template
Includes:
- all 6 pillars
- checklist/questions per pillar
- score rubric (`Pass|Needs Work|Fail`)
- Findings + Remediations

#### 10.3 Solution overview template
Includes:
- requirements
- constraints
- architecture
- data flows
- security model
- scaling
- DR
- cost model
- ops model
- risks
- canonical `MAJOR_DECISION:` entries as needed

#### 10.4 Threat model + runbook templates
- `threat-model-lite.md`: assets, boundaries, threats, mitigations, residual risk
- `runbook-baseline.md`: ownership, triggers, triage, rollback/recovery, escalation

No external URLs in templates.

### 11) Professional Skill Metadata (F/G)
Create:
- `aws-enterprise-architecture/agents/openai.yaml`
- `aws-migration-dr/agents/openai.yaml`

Include:
- interface metadata
- `allow_implicit_invocation: true`
- dependency placeholder `aws-documentation-mcp`
- no hostnames/URLs

### 12) Evals Skill Requirements
`aws-evals/references/evals.md` includes:
1. Associate gate scenario + pass/fail rubric
2. Bridge trade-off scenario + rubric
3. Professional gate scenario + rubric
4. Failure analysis scenario + rubric

`aws-evals/scripts/run_evals.py`:
- deterministic CLI behavior (interactive only with `--interactive`)
- prints prompts
- captures notes
- writes `docs/architecture/reviews/EVAL-NOTES-YYYYMMDD.md`
- logs to manifest when system-scoped

### 13) Validation / Acceptance Checklist
1. `_shared/architecture-workflow` exists and has no `SKILL.md`.
2. all 9 skills exist with valid `SKILL.md`.
3. each skill has 2–5 non-placeholder references.
4. C/D/F/G/H wrappers dispatch correctly and preserve exit code.
5. shared scripts enforce required args (non-zero on missing args unless `--interactive`).
6. all scripts write manifest only to `REPO_ROOT/docs/architecture/manifest/<system>.yaml`.
7. ADR files have deterministic names + YAML metadata.
8. validator enforces 6 pillars + scores + gate policy + major decision ADR mapping.
9. C/D/F/G/H `SKILL.md` includes strict ADR threshold + strict workflow sequence.
10. no extraneous `README`/changelog/install files.

### 14) Assumptions and Defaults
1. Implementation is created fresh in current repo without deleting unrelated content.
2. L1 skill name remains exactly `aws-aws-foundations`.
3. workflow version starts at `1.0.0`.
4. default gate: no Fail pillars; max 2 Needs Work.
5. major decision parsing is strict and only uses canonical grammar.
