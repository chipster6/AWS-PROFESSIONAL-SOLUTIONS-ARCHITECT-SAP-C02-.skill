# Solution Overview

System: system
Date: 2026-02-17
Owner(s): Platform Architecture Team

## Requirements
- Public web application with API backend and persistent transactional data.
- Target availability 99.95%, p95 API latency under 200 ms, and auditable security controls.

## Constraints
- AWS-native managed services preferred.
- Minimize operational overhead while preserving strong data durability and recoverability.

## Proposed Architecture
Internet-facing `Application Load Balancer` routes HTTPS traffic to `ECS Fargate` services in private subnets across 2 AZs. Application services use `Aurora PostgreSQL (Multi-AZ)` for transactional data and `ElastiCache Redis` for low-latency reads/session caching. Static content is stored in `S3` and distributed via `CloudFront`. Secrets are managed in `Secrets Manager` and KMS encryption is enforced.

## Data Flows
1. Client -> CloudFront -> ALB -> ECS API service.
2. API reads/writes Aurora for system-of-record transactions.
3. Hot reads/session tokens are cached in Redis.
4. Logs and metrics flow to CloudWatch; audit logs to CloudTrail.

## Security Model
- Private application/data tiers; only ALB is internet-facing.
- IAM least privilege for task roles.
- TLS in transit, KMS encryption at rest.
- WAF on CloudFront/ALB and GuardDuty enabled.

## Scaling Approach
- ECS service auto scaling on request count and CPU.
- Aurora read replica scaling for read-heavy workloads.
- CloudFront and S3 scale automatically for static content delivery.

## Disaster Recovery
RTO: 60 minutes
RPO: 5 minutes
DR pattern: Warm standby in secondary region with Aurora cross-region replica and infrastructure templates ready for promotion.

## Cost Model
- Fargate for right-sized compute without EC2 fleet management.
- Aurora reserved capacity/Savings Plans for steady baseline load.
- S3 lifecycle policies and CloudWatch log retention controls.

## Operations Model
- CloudWatch dashboards/alarms with on-call runbook.
- Blue/green deployments for API service.
- Backups and quarterly restore tests.

## Risks
- Regional control-plane disruptions can delay failover orchestration.
- Redis cache stampede under sudden traffic spikes if invalidation is misconfigured.

## Major Decisions
MAJOR_DECISION: data-store | db-choice | Choose Aurora PostgreSQL over DynamoDB due to relational transaction and query constraints.
MAJOR_DECISION: integration | async-events | Use SQS for asynchronous order/event processing to decouple write path from downstream tasks.
MAJOR_DECISION: networking | private-subnet-boundary | Keep compute and database in private subnets with ALB-only ingress.
