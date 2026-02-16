# Well-Architected Review

System: sample-system
Date: 2026-02-16
Reviewer(s): architecture-team

## Operational Excellence
Score: Needs Work
Checklist:
- [x] Ownership and on-call model is documented.
- [ ] Runbooks exist for critical incidents.

## Security
Score: Fail
Checklist:
- [x] Least privilege IAM boundaries are defined.
- [ ] Encryption controls are complete.

## Reliability
Score: Needs Work
Checklist:
- [x] Backup strategy exists.
- [ ] Restore validation is scheduled.

## Performance Efficiency
Score: Pass
Checklist:
- [x] Capacity/scaling model documented.

## Cost Optimization
Score: Needs Work
Checklist:
- [x] Cost drivers identified.
- [ ] Commitment strategy finalized.

## Sustainability
Score: Pass
Checklist:
- [x] Lifecycle policies defined.

## Findings + Remediations
- Finding: Encryption coverage gaps remain in one data path.
  Remediation: Complete encryption enforcement and add automated checks.

## Major Decisions
MAJOR_DECISION: networking | net-boundary | Centralized egress and inspection model for outbound traffic
