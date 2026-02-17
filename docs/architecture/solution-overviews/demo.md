# Solution Overview

System: demo
Date: 2026-02-16
Owner(s): TBD

## Requirements
- {{requirement_1}}
- {{requirement_2}}

## Constraints
- {{constraint_1}}
- {{constraint_2}}

## Proposed Architecture
{{architecture_summary}}

## Data Flows
{{data_flows}}

## Security Model
{{security_model}}

## Scaling Approach
{{scaling_approach}}

## Disaster Recovery
RTO: {{rto}}
RPO: {{rpo}}
DR pattern: {{dr_pattern}}

## Cost Model
{{cost_model}}

## Operations Model
{{ops_model}}

## Risks
- {{risk_1}}
- {{risk_2}}

## Major Decisions
Use canonical marker syntax exactly:
`MAJOR_DECISION: <category> | <decision_id_or_slug> | <one-line summary>`
Add one `MAJOR_DECISION` line for every major architecture decision that requires ADR mapping.

Examples:
`MAJOR_DECISION: data-store | db-choice | Choose Aurora PostgreSQL over DynamoDB due to relational constraints`
`MAJOR_DECISION: networking | egress-model | Use centralized egress with inspection to reduce exfiltration risk`
