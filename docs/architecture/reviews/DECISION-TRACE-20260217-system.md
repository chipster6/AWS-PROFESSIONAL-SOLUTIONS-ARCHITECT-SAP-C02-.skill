# Decision Trace
System: system
Date: 2026-02-17

## Decision to ADR Mapping
- Category: data-store
  Key: db-choice
  Summary: Choose Aurora PostgreSQL over DynamoDB due to relational transaction and query constraints.
  ADR: /Users/cody/Documents/Skills/SAP-C02-AWS-SOLUTION-ARCHITECT-PROFESSIONAL/docs/architecture/decisions/ADR-20260216-db-choice.md
- Category: integration
  Key: async-events
  Summary: Use SQS for asynchronous order/event processing to decouple write path from downstream tasks.
  ADR: /Users/cody/Documents/Skills/SAP-C02-AWS-SOLUTION-ARCHITECT-PROFESSIONAL/docs/architecture/decisions/ADR-20260217-async-events.md
- Category: networking
  Key: private-subnet-boundary
  Summary: Keep compute and database in private subnets with ALB-only ingress.
  ADR: /Users/cody/Documents/Skills/SAP-C02-AWS-SOLUTION-ARCHITECT-PROFESSIONAL/docs/architecture/decisions/ADR-20260217-private-subnet-boundary.md
- Category: data-store
  Key: db-choice
  Summary: Choose Aurora PostgreSQL over DynamoDB due to relational transaction and query constraints.
  ADR: /Users/cody/Documents/Skills/SAP-C02-AWS-SOLUTION-ARCHITECT-PROFESSIONAL/docs/architecture/decisions/ADR-20260216-db-choice.md
- Category: integration
  Key: async-events
  Summary: Use SQS for asynchronous order/event processing to decouple write path from downstream tasks.
  ADR: /Users/cody/Documents/Skills/SAP-C02-AWS-SOLUTION-ARCHITECT-PROFESSIONAL/docs/architecture/decisions/ADR-20260217-async-events.md
- Category: networking
  Key: private-subnet-boundary
  Summary: Keep compute and database in private subnets with ALB-only ingress.
  ADR: /Users/cody/Documents/Skills/SAP-C02-AWS-SOLUTION-ARCHITECT-PROFESSIONAL/docs/architecture/decisions/ADR-20260217-private-subnet-boundary.md
