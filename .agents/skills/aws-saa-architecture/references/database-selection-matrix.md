# RDS/Aurora vs DynamoDB

## Decision matrix
| Requirement | RDS/Aurora | DynamoDB |
|---|---|---|
| Complex SQL, joins, relational constraints | Strong fit | Not primary |
| Full ACID across complex multi-entity operations | Strong fit | Limited pattern-dependent |
| Known key-based access at large scale | Possible | Strong fit |
| Serverless burst with minimal connection management | Requires proxy/connection strategy | Strong fit |
| Flexible ad hoc query evolution | Strong fit | Requires access-pattern-first design |

## If/Then rules
| If | Then |
|---|---|
| Access patterns are stable and key-centric | Prefer DynamoDB |
| Query model requires complex joins and ad hoc analytics queries | Prefer RDS/Aurora |
| Lambda-heavy workload with cold-start sensitivity and burst concurrency | Bias toward DynamoDB unless relational requirements dominate |
| Need strict relational transactions and schema constraints | Prefer RDS/Aurora |

## Deeper trade-off table
| Factor | RDS/Aurora | DynamoDB |
|---|---|---|
| Connection model | Traditional DB connections; pooling/proxy often required | HTTP API model; no connection pooling burden |
| Transaction model | Strong ACID relational transactions | Item-centric model, transactions available with design constraints |
| Query model | SQL joins, aggregates, flexible relational queries | Primary-key and index-driven access patterns |
| Scaling posture | Vertical + read replica / cluster scaling model | Horizontal partition-based scaling model |
| Cost shape | Instance/cluster runtime + storage | Request/capacity + storage; aligns with spiky serverless patterns |
| Schema evolution | Structured relational schema governance | Flexible item model with access-pattern discipline |

## Deterministic chooser
| Requirement cue | Preferred default |
|---|---|
| Known key-based reads/writes at very high scale | DynamoDB |
| Complex joins and relational integrity constraints | RDS/Aurora |
| Burst-heavy Lambda workload with intermittent traffic | DynamoDB |
| Existing relational workload with SQL/reporting dependencies | RDS/Aurora |
| Need to avoid connection scaling bottlenecks quickly | DynamoDB or RDS with proxy strategy |

## Operational trade-offs
- RDS/Aurora:
  - manage connection limits and pooling (often proxy-assisted),
  - instance-based capacity posture.
- DynamoDB:
  - key/index model must be intentional,
  - scaling aligns well with request-driven/serverless patterns.

## Consistency and correctness checklist
- Define read consistency mode needed per critical workflow.
- Define transaction boundary and idempotency strategy.
- Define concurrency control and conflict handling behavior.
- Define backup/restore and data-repair plan.
- Define migration/cutover rollback path.

## Anti-patterns
- Relational workload forced into NoSQL without redesign and access-pattern validation.
- Lambda-to-relational design without connection management strategy.
- Choosing relational by default when access patterns are simple key-value.
- Selecting DynamoDB before query/access patterns are modeled.
- Selecting RDS/Aurora without testing connection behavior under burst load.

## Acceptance criteria
- Query/access patterns are documented before final database choice.
- Consistency/transaction requirements are mapped to service capabilities.
- Scalability and operational burden are explicitly compared.
- At least one ADR links database choice to consistency, scale, and cost trade-offs.

### Example MAJOR_DECISION
`MAJOR_DECISION: data-store | order-db-choice | Choose Aurora PostgreSQL for transactional order workflow with relational constraints`
