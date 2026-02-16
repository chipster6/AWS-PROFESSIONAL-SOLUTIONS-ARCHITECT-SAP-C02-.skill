# Cost Allocation and Tagging Governance

## Goal
Create deterministic, auditable cost ownership by mapping spend to accountable business entities.

## Allocation model options
| Model | Best for | Trade-off |
|---|---|---|
| Account-based | Clear account-to-team ownership | Coarse granularity inside shared accounts |
| Tag-based | Fine-grained showback/chargeback | Requires strong tag hygiene and enforcement |
| Cost Categories | Aggregating accounts/tags into business views | Adds governance and mapping maintenance |

## Mandatory tagging baseline
- `owner`
- `environment`
- `application`
- `cost-center` (or equivalent finance key)
- `data-classification` (where relevant)

## Deterministic tagging controls
- Enforce tag policies centrally (where supported).
- Define required tags for all production resources.
- Define exception path and expiration for temporary tag gaps.
- Activate cost allocation tags in billing/cost management.
- Validate tag coverage weekly and track remediation ownership.

## Showback vs chargeback chooser
| If | Then |
|---|---|
| Organization is early in cloud financial maturity | Start with showback |
| Internal billing process is established and accepted | Move to chargeback |
| Shared platforms produce mixed spend | Use blended model with clear allocation keys |

## Cost visibility checklist
- [ ] Cost Explorer views exist by account, tag, and cost category.
- [ ] CUR is enabled and accessible for analysis workflows.
- [ ] Unallocatable spend is tracked and reduced over time.
- [ ] Resource tagging drift has owner and SLA.

## Anti-patterns
- Tags defined but not activated for cost allocation.
- Shared account with no tag enforcement and no unallocatable tracking.
- Sensitive data included in tag values.
- Cost allocation model changed without finance/stakeholder alignment.

## Acceptance criteria
- At least 90%+ of in-scope production spend is allocatable (target defined by org).
- Tag and cost category policies are documented and enforced.
- Monthly report includes unallocatable spend and remediation status.
- At least one ADR captures allocation model and governance ownership.

### Example MAJOR_DECISION
`MAJOR_DECISION: cost-model | allocation-basis | Use account+tag hybrid allocation model with mandatory owner/environment/application/cost-center tags.`
