# ALB vs NLB Decision Matrix

## Core capability differences
| Requirement | ALB | NLB |
|---|---|---|
| OSI layer | Layer 7 (HTTP/HTTPS/gRPC app-aware routing) | Layer 4 (TCP/UDP/TLS/QUIC flow routing) |
| Routing semantics | Host/path/header/query/method-based | Flow-hash based, protocol/port oriented |
| Static IP need | Not native static IP design goal | Supports static IP behavior per AZ node (EIP option for internet-facing) |
| Auth and app controls | Strong fit for app-level routing/auth patterns | Typically handled downstream |
| Very high L4 throughput/low overhead | Possible but not primary | Primary fit |
| Source IP and long-lived connections | Depends on pattern/target type | Strong fit for source-IP aware L4 patterns |

## If/Then rules
| If | Then |
|---|---|
| Routing decisions depend on URL/host/header | Prefer ALB |
| Protocol is TCP/UDP and app-level routing not needed | Prefer NLB |
| You need one endpoint for mixed app-routing microservices | Prefer ALB with target groups/rules |
| You need static network behavior and high-volume L4 | Prefer NLB |
| You need gRPC/HTTP microservice routing and app-aware controls | Prefer ALB |
| You need to preserve strict transport behavior for non-HTTP protocols | Prefer NLB |

## Decision threshold cues
| Signal | Bias |
|---|---|
| HTTP-specific routing requirements are present | ALB |
| Pure TCP/UDP traffic with no app-layer routing | NLB |
| Need to terminate and inspect HTTP for route decisions | ALB |
| Workload dominated by connection-heavy L4 traffic | NLB |

## Operational considerations
- ALB:
  - Listener rules and target-group health checks at app layer.
  - Validate rule priority conflicts and fallback rule behavior.
- NLB:
  - Ensure healthy targets exist in every enabled AZ.
  - Understand cross-zone behavior and DNS implications.
  - Validate client behavior when AZ subnet IPs are removed from DNS.
- Both:
  - Deploy across multiple AZs.
  - Tune health checks with realistic failure detection and recovery time.
  - Validate failover and connection draining expectations before production.

## Security and resilience checklist
- Confirm TLS strategy (terminate at load balancer vs pass-through).
- Confirm WAF placement for internet-facing HTTP endpoints.
- Confirm logging/metrics coverage and alert thresholds.
- Confirm DDoS and rate-limiting strategy at ingress boundary.
- Confirm runbook for degraded target group or AZ isolation.

## Anti-patterns
- Using NLB while needing host/path/header routing logic.
- Using ALB for pure L4 workloads requiring static network semantics.
- Enabling multi-AZ load balancing without healthy targets in each zone.
- Routing security-sensitive auth traffic through a path without app-layer controls.
- Assuming DNS clients always honor TTL during zonal failover.

## Acceptance criteria
- Chosen load balancer aligns with traffic protocol and routing needs.
- Listener/target-group design and health check strategy are documented.
- Cross-zone behavior and AZ-level failure expectations are explicit.
- At least one ADR records ingress trade-offs (protocol, security, cost, operations).

### Example MAJOR_DECISION
`MAJOR_DECISION: networking | public-ingress-lb | Choose ALB for host/path routing and WAF-integrated web ingress`
