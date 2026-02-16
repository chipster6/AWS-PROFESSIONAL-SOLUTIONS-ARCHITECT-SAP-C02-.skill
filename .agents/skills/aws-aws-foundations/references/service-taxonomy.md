# AWS Service Taxonomy

## Purpose
Use this as a first-pass decomposition map so architecture drafts do not miss core service families (runtime, data, security, networking, operations, and governance).

## Category Coverage (AWS docs aligned)
AWS service groupings commonly include Analytics, Application Integration, Compute, Containers, Databases, Developer Tools, Front-end/Mobile, IoT, Machine Learning/AI, Management and Governance, Media, Migration and Transfer, Networking and Content Delivery, Security/Identity/Compliance, and Storage.

## Compute Family
- VM compute: `EC2`, `Auto Scaling`, `Launch Templates`, `EC2 Image Builder`.
- Container compute: `ECS`, `EKS`, `ECR`, `Fargate`.
- Serverless compute: `Lambda`, `App Runner`, `Batch`, `Elastic Beanstalk` (managed platform model).
- Workflow/coordination compute: `Step Functions` (stateful orchestration for serverless/service workflows).
- Hybrid/edge compute placement: `Outposts`, `Local Zones`, `Wavelength Zones`, `Snow Family`.

## Storage Family
- Object storage: `S3` and storage classes (`Standard`, `Intelligent-Tiering`, `Standard-IA`, `One Zone-IA`, Glacier classes).
- Block storage: `EBS` (`gp3`, `io2`, `st1`, `sc1`) + snapshots.
- Shared file storage: `EFS`; specialized managed file systems via `FSx` (`Windows`, `Lustre`, `NetApp ONTAP`, `OpenZFS`).
- Hybrid transfer and edge storage: `DataSync`, `Storage Gateway`, `Transfer Family`, `Snow Family`.
- Backup and data protection: `AWS Backup`.

## Database and Data Stores
- Relational OLTP: `RDS`, `Aurora`.
- Key-value/document at scale: `DynamoDB`, `DocumentDB`.
- In-memory/cache: `ElastiCache`, `MemoryDB`.
- Graph/time-series/ledger/specialized: `Neptune`, `Timestream`, `QLDB`.
- Search/near-real-time analytics: `OpenSearch Service`.
- Warehouse/lake analytics: `Redshift`, `Athena`.

## Networking and Content Delivery
- Core network primitives: `VPC`, subnets, route tables, NACLs, security groups.
- Ingress and traffic distribution: `ALB`, `NLB`, `GWLB`, `Route 53`, `Global Accelerator`.
- Content and edge acceleration: `CloudFront`.
- Private service connectivity: `PrivateLink`, VPC endpoints.
- Hybrid connectivity: `Direct Connect`, `Site-to-Site VPN`, `Transit Gateway`.

## Security, Identity, and Compliance
- Identity and access: `IAM`, `IAM Identity Center`, `STS`, `Organizations` + SCP guardrails.
- Key/secrets/certificate controls: `KMS`, `Secrets Manager`, `SSM Parameter Store`, `ACM`.
- Detection and posture: `GuardDuty`, `Security Hub`, `Detective`, `Inspector`, `Macie`.
- Audit and governance telemetry: `CloudTrail`, `Config`, `Access Analyzer`, `Audit Manager`.
- Edge and network protection: `WAF`, `Shield`, `Network Firewall`.

## Integration, Messaging, and Eventing
- Event routing and buses: `EventBridge`.
- Queue and pub/sub: `SQS`, `SNS`.
- Streaming: `Kinesis` family, `MSK`.
- Workflow orchestration: `Step Functions`.
- Protocol broker legacy integration: `Amazon MQ`.

## Management, Operations, and Developer Platform
- Monitoring and telemetry: `CloudWatch`, `CloudWatch Logs`, `X-Ray`.
- Operations and incident tooling: `Systems Manager`, `Incident Manager` (where adopted), `AWS Health`.
- IaC and platform governance: `CloudFormation`, `CDK`, `Service Catalog`, `Control Tower`.
- CI/CD and developer services: `CodeBuild`, `CodeDeploy`, `CodePipeline`, `CodeArtifact`.
- FinOps and billing visibility: `Cost Explorer`, `Budgets`, `CUR`, `Cost Anomaly Detection`, `Billing Conductor`.

## Analytics and AI/ML
- ETL/data prep: `Glue`.
- BI/reporting: `QuickSight`.
- Data lake patterns: `S3` + `Lake Formation` + `Athena/Redshift`.
- ML platform: `SageMaker`.
- Generative AI foundation services: `Bedrock`.

## Application/API and End-User Services
- API layer: `API Gateway`, `AppSync`.
- App auth/user management: `Cognito`.
- Front-end hosting and app workflows: `Amplify`.

## Deterministic Selection Workflow
1. Classify each workload component by responsibility: ingress, compute, state, async integration, control plane, observability, governance.
2. Map each component to one primary service family and one fallback family.
3. Record exclusion rationale for at least one rejected alternative per critical component.
4. Add one `MAJOR_DECISION` line for each family choice that materially affects availability, security, or cost.

## Service Family Selection Triggers
| Requirement signal | Service family bias | Typical ADR category |
|---|---|---|
| HTTP host/path/header routing | `ALB`/`API Gateway` | `networking` |
| High-throughput TCP/UDP, static IP, L4 behavior | `NLB` | `networking` |
| Global object durability + lifecycle economics | `S3` | `data-store` |
| Single-host low-latency block IO | `EBS` | `data-store` |
| Shared POSIX/NFS semantics across many clients | `EFS`/`FSx` | `data-store` |
| Known key access, massive horizontal scale | `DynamoDB` | `data-store` |
| Complex relational joins and ACID transactions | `RDS`/`Aurora` | `data-store` |
| Decoupled workflows and fan-out integration | `EventBridge` + `SQS`/`SNS` | `integration-style` |
| Strict multi-account governance | `Organizations` + SCP + centralized logging | `security-model` |

## Anti-patterns
- Selecting by team familiarity alone without matching protocol/access pattern.
- Mixing unrelated workloads into a single shared datastore or queue “for simplicity.”
- Ignoring service limits, throughput modes, and connection behavior during initial selection.
- Omitting security and operations services from architecture decomposition.

## Acceptance Criteria
- Every major architecture component is mapped to a service family and explicit rationale.
- At least one rejected alternative is documented for each critical component.
- Security, operations, and cost services are included in the architecture baseline.
- `MAJOR_DECISION` markers exist for all high-impact family choices.

## Family selection matrix
| Requirement signal | Service family bias |
|---|---|
| Unpredictable burst, short-lived compute | Serverless compute |
| Stateful OS/runtime control required | VM/container compute |
| Shared file semantics across many clients | EFS/FSx |
| Object-scale durability and lifecycle economics | S3 |
| Complex SQL and transactional joins | RDS/Aurora |
| Massive key-based throughput and low-latency API | DynamoDB |
| Decoupled event-driven architecture | EventBridge/SQS/SNS/Step Functions |
| Global user latency optimization | CloudFront/Global Accelerator/Route 53 |

## If/Then routing rules
| If | Then |
|---|---|
| Application needs L7 routing/auth patterns | Bias to ALB + API Gateway as applicable |
| Requires private service-to-service access across accounts/VPCs | Evaluate PrivateLink and endpoint strategy |
| Needs strong preventive governance across accounts | Use Organizations + SCP baseline |
| Workload depends on asynchronous fan-out | Use events/queues and idempotent consumers |

## Anti-patterns
- Choosing services by team familiarity rather than access pattern constraints.
- Over-consolidating unrelated workloads into one data store or one queue.
- Skipping foundational controls (IAM/KMS/logging) in early architecture drafts.
- Assuming managed service means no operational responsibility.

## Acceptance criteria
- Every major component maps to a service family with rationale.
- At least one alternative per critical component is documented and rejected explicitly.
- Security, observability, and cost controls are selected alongside core runtime services.
