# Well-Architected Review

System: system
Date: 2026-02-17
Reviewer(s): Platform Architecture Team

Scoring rubric per pillar:
- Pass: controls are implemented and verified.
- Needs Work: controls are partially implemented or unverified.
- Fail: critical control gaps or unacceptable risk remain.

## Operational Excellence
Score: Pass
Checklist:
- [x] Ownership and on-call model is documented.
- [x] Runbooks exist for critical incidents.
- [x] Deployment and rollback procedures are tested.
Findings + Remediations:
- Finding: Restore tests need quarterly evidence capture.
  Remediation: Add restore test evidence checklist to runbook cadence.

## Security
Score: Pass
Checklist:
- [x] Least privilege IAM boundaries are defined.
- [x] Encryption at rest and in transit is enforced.
- [x] Logging and detection controls are enabled.
Findings + Remediations:
- Finding: WAF tuning for false positives is not finalized.
  Remediation: Add managed rule override review every sprint.

## Reliability
Score: Needs Work
Checklist:
- [x] Failure domains and blast radius are addressed.
- [ ] Backup and restore procedures are tested.
- [x] RTO/RPO targets are documented and validated.
Findings + Remediations:
- Finding: Full-region failover drill not yet completed.
  Remediation: Execute biannual DR game day with documented outcomes.

## Performance Efficiency
Score: Pass
Checklist:
- [x] Capacity/scaling model is documented.
- [x] Bottlenecks and quotas are identified.
- [x] Load/performance tests are planned or completed.
Findings + Remediations:
- Finding: None critical.
  Remediation: Continue periodic load profile validation.

## Cost Optimization
Score: Needs Work
Checklist:
- [x] Cost drivers and allocation tags are defined.
- [ ] Rightsizing and commitment strategy are documented.
- [x] Cost anomaly detection and budgets are configured.
Findings + Remediations:
- Finding: Savings Plan coverage model not baselined yet.
  Remediation: Produce 12-month commitment plan and monthly variance review.

## Sustainability
Score: Pass
Checklist:
- [x] Architecture choices include efficiency goals.
- [x] Data retention/lifecycle policies are defined.
- [x] Workload scheduling and scaling reduce waste.
Findings + Remediations:
- Finding: None critical.
  Remediation: Track utilization trends and lifecycle effectiveness.

## Major Decisions
MAJOR_DECISION: data-store | db-choice | Choose Aurora PostgreSQL over DynamoDB due to relational transaction and query constraints.
MAJOR_DECISION: integration | async-events | Use SQS for asynchronous order/event processing to decouple write path from downstream tasks.
MAJOR_DECISION: networking | private-subnet-boundary | Keep compute and database in private subnets with ALB-only ingress.
