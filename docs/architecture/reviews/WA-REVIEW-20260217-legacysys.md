# Well-Architected Review

System: legacysys
Date: 2026-02-17
Reviewer(s): TBD

Scoring rubric per pillar:
- Pass: controls are implemented and verified.
- Needs Work: controls are partially implemented or unverified.
- Fail: critical control gaps or unacceptable risk remain.

## Operational Excellence
Score: Pass | Needs Work | Fail
Checklist:
- [ ] Ownership and on-call model is documented.
- [ ] Runbooks exist for critical incidents.
- [ ] Deployment and rollback procedures are tested.
Findings + Remediations:
- Finding:
  Remediation:

## Security
Score: Pass | Needs Work | Fail
Checklist:
- [ ] Least privilege IAM boundaries are defined.
- [ ] Encryption at rest and in transit is enforced.
- [ ] Logging and detection controls are enabled.
Findings + Remediations:
- Finding:
  Remediation:

## Reliability
Score: Pass | Needs Work | Fail
Checklist:
- [ ] Failure domains and blast radius are addressed.
- [ ] Backup and restore procedures are tested.
- [ ] RTO/RPO targets are documented and validated.
Findings + Remediations:
- Finding:
  Remediation:

## Performance Efficiency
Score: Pass | Needs Work | Fail
Checklist:
- [ ] Capacity/scaling model is documented.
- [ ] Bottlenecks and quotas are identified.
- [ ] Load/performance tests are planned or completed.
Findings + Remediations:
- Finding:
  Remediation:

## Cost Optimization
Score: Pass | Needs Work | Fail
Checklist:
- [ ] Cost drivers and allocation tags are defined.
- [ ] Rightsizing and commitment strategy are documented.
- [ ] Cost anomaly detection and budgets are configured.
Findings + Remediations:
- Finding:
  Remediation:

## Sustainability
Score: Pass | Needs Work | Fail
Checklist:
- [ ] Architecture choices include efficiency goals.
- [ ] Data retention/lifecycle policies are defined.
- [ ] Workload scheduling and scaling reduce waste.
Findings + Remediations:
- Finding:
  Remediation:

## Major Decisions
Use canonical marker syntax exactly:
`MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`

Example:
`MAJOR_DECISION: data-store | db-choice | Choose Aurora PostgreSQL over DynamoDB due to relational constraints`
