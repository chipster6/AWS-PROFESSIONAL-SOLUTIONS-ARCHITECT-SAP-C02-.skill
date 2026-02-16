# AWS Architecture Evaluation Prompts and Rubrics

Use these scenarios to assess deterministic architecture quality. Grade strictly against the rubric.

## Scenario 1: Associate Gate

### Test prompt
Design a highly available web application for a startup:
- 3-tier architecture (web, app, data)
- expected 10x traffic spikes during campaigns
- p95 user latency target under 300ms
- must survive single-AZ failure
- needs backup and restore with documented RTO/RPO
- limited team operations capacity

Provide output using required headings and include explicit `MAJOR_DECISION` entries.

### Pass/fail rubric
- Pass only if all are true:
  - includes multi-AZ architecture and clear failure-domain reasoning
  - includes storage/database selection rationale with alternatives
  - includes baseline security controls (identity, encryption, logging)
  - includes backup/restore and recovery validation approach
  - includes at least 3 concrete trade-offs
- Fail if any are true:
  - single-AZ critical path
  - no explicit recovery approach
  - generic service list with no decision rationale
  - missing operational ownership assumptions

## Scenario 2: Bridge Trade-off Comparison

### Test prompt
Compare two architectures for an event-driven order platform:
- Option A: API + relational DB + synchronous downstream calls
- Option B: API + queue/event bus + asynchronous processing + idempotent workers
- constraints:
  - customer checkout must acknowledge in <1s
  - fulfillment can complete asynchronously
  - auditability and replay support required
  - cost and operational complexity matter

Produce a recommendation with rejected-option rationale and explicit risk controls.

### Pass/fail rubric
- Pass only if all are true:
  - explicitly analyzes latency, resilience, consistency, and operational complexity
  - identifies sync-vs-async failure modes and mitigation controls
  - recommends one option with clear assumptions and decision boundaries
  - includes deterministic validation checks and rollback/fallback notes
- Fail if any are true:
  - compares only by cost or only by speed
  - ignores replay/idempotency/audit requirements
  - no clear winner or conditional decision logic

## Scenario 3: Professional Gate

### Test prompt
Design an enterprise platform with:
- multi-account landing zone (prod/nonprod/security/shared services)
- cross-account IAM access model
- hub-and-spoke network with hybrid connectivity to on-prem
- regional DR strategy aligned to explicit RTO/RPO
- cost governance model with tagging, budgets, anomaly response, and commitment strategy
- requirement for auditable architecture outputs (ADRs + WA review + decision trace)

Provide architecture and governance with strict control boundaries.

### Pass/fail rubric
- Pass only if all are true:
  - defines OU/account boundary model and guardrail approach
  - defines cross-account trust and least-privilege pattern
  - defines network segmentation and hybrid failover considerations
  - maps RTO/RPO to a DR strategy and testing cadence
  - defines FinOps operating model and ownership
  - includes script-driven artifact workflow and validation gates
- Fail if any are true:
  - no explicit guardrail or governance model
  - no failover/failback strategy for DR
  - no accountability model for cost or security controls
  - no deterministic artifact/ADR workflow

## Scenario 4: Failure Analysis Gate

### Test prompt
Analyze this incident:
- intermittent 5xx spikes and latency surges during peak traffic
- queue backlog grows, DLQ starts receiving messages
- one AZ reports elevated dependency errors
- rollback reduced errors but data reconciliation gaps remain

Produce a failure analysis and remediation plan.

### Pass/fail rubric
- Pass only if all are true:
  - separates symptoms from likely root causes
  - identifies failure domains and blast radius clearly
  - proposes containment, recovery, and reconciliation actions
  - includes prevention actions (architecture, observability, runbook updates)
  - includes measurable validation checks for fixes
- Fail if any are true:
  - only proposes “scale up” without causal analysis
  - omits reconciliation approach for data correctness gaps
  - lacks operational verification plan after remediation

## Scoring guidance
- Grade each scenario as `Pass` or `Fail`.
- Record mandatory misses even if overall quality seems high.
- Recommend remediation tasks for every failed criterion.
- Re-run scenario after remediations are applied.
