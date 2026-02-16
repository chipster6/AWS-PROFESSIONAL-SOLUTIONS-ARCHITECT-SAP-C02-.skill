# Shared Responsibility Model

## Principle
Security and compliance are shared:
- AWS secures the infrastructure **of** the cloud.
- Customers secure identity, data, configuration, and workload behavior **in** the cloud.
- Responsibility depth changes with abstraction (IaaS -> managed service -> serverless), but customer responsibility never becomes zero.

## Why this matters in architecture reviews
- Most security incidents in cloud workloads are customer-configuration failures, not cloud provider datacenter failures.
- Architecture decisions must assign control ownership explicitly, not implicitly.

## Control ownership map
| Control area | AWS | Customer |
|---|---|---|
| Physical/datacenter security | Yes | No |
| Hypervisor/core service infrastructure | Yes | No |
| IAM policy design and least privilege | No | Yes |
| Data classification and encryption choices | No | Yes |
| Guest OS and app patching (IaaS) | No | Yes |
| Shared controls (patch/config awareness) | Partial | Partial |

## Service-model implications
| Service type | Customer burden | Typical missed responsibility |
|---|---|---|
| IaaS-style compute | Highest (OS, middleware, app hardening) | Patch/vulnerability ownership not assigned |
| Managed PaaS-style data services | Reduced infra burden; config/data/IAM still customer-owned | Assuming managed service implies secure-by-default configuration |
| Serverless managed services | Lower ops burden; policy/data/integration security still customer-owned | Over-permissive IAM and weak event trust boundaries |

## Control ownership by architecture layer
| Layer | AWS manages | Customer manages |
|---|---|---|
| Facility/physical | Site and hardware controls | N/A |
| Service substrate | Core service operation and resilience | Service configuration and exposure model |
| Identity | IAM service availability | Principal model, MFA, least privilege, break-glass controls |
| Data | Durability primitives | Classification, encryption choices, key policies, retention |
| Runtime | Managed runtime where applicable | Code security, dependency risk, secrets handling |
| Detection/response | Logging service availability | Alerting, triage, escalation, incident execution |

## Control classes for planning
| Control class | Description | Typical owner |
|---|---|---|
| Inherited controls | Fully provided by AWS platform | AWS |
| Shared controls | Split responsibilities by layer/service | AWS + Customer |
| Customer controls | Workload-specific policy/config/process | Customer |

## If/Then ownership rules
| If | Then |
|---|---|
| Workload runs on customer-managed OS/runtime | Customer owns patch/hardening and vulnerability response |
| Managed data service is used | Customer still owns access policy, encryption posture, and data governance |
| Team consumes logs but no one owns alert response | Assign explicit detection/response owner before production |
| Multiple teams deploy into same account | Define preventive guardrails and delegated permissions model |
| Break-glass access is required | Enforce time-bounded access and auditable approvals |

## Deterministic ownership gate
- Every critical control has one named owner role.
- Every shared control is written as `AWS:<scope> | Customer:<scope>`.
- Every control with a response SLA includes alert source, triage owner, and escalation path.
- Every compliance control maps to evidence artifacts and retention location.

## Checklist
- Define identity boundary and separation of duties.
- Define logging/auditing ownership and retention.
- Define encryption/key-management ownership.
- Define patching ownership for each workload component.
- Define incident response roles across platform and app teams.
- Define evidence collection path for compliance controls.
- Define break-glass procedure and approval/audit workflow.

## RACI starter matrix
| Area | Platform team | App team | Security/GRC |
|---|---|---|---|
| IAM guardrails and SCP-style controls | A/R | C | C |
| Service-role least privilege | C | A/R | C |
| Key policy and encryption standards | R | C | A |
| Detection rules and triage SLA | R | C | A |
| Compliance reporting evidence | C | C | A/R |

## Anti-patterns
- Assuming managed service means no customer security tasks.
- No named owner for IAM policy lifecycle.
- Compliance evidence expected without telemetry ownership.
- Shared control areas treated as "someone else's problem."
- Break-glass admin access with no audit trail or expiry.

## Acceptance criteria
- RACI exists for security controls by component.
- Shared controls are explicitly split between platform and app teams.
- Workload design includes evidence collection paths for audits.
- Incident runbook references control owners and escalation sequence.
- At least one ADR captures identity/control boundary decisions.
- WA security pillar review includes ownership findings/remediations.

### Example MAJOR_DECISION
`MAJOR_DECISION: security-model | iam-ownership-split | Central platform owns guardrails; app teams own least-privilege service roles`
