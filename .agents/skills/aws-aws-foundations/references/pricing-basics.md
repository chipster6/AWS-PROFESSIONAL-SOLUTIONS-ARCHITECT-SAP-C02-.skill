# AWS Pricing Basics

## Primary cost drivers
- Compute runtime/instance size or provisioned capacity.
- Storage capacity plus access/retrieval profile.
- Data transfer (inter-AZ, inter-region, internet egress).
- Managed service request units, throughput units, and features.
- Operational telemetry and retention (logs/metrics/traces).
- Resilience overhead (replication, backups, DR readiness capacity).

## Cost driver taxonomy
| Driver class | Examples |
|---|---|
| Baseline capacity | Always-on compute, provisioned database/storage throughput |
| Variable consumption | Requests, invocations, data scanned, data transferred |
| Protection overhead | Backups, replication, DR warm capacity |
| Operations overhead | Logging, metrics, tracing, retention, support services |

## Estimation checklist
- Capture workload shape: baseline, peak, seasonal, growth assumptions.
- Separate one-time migration cost from steady-state run cost.
- Include hidden multipliers: replication, backups, logs, cross-zone traffic.
- Include resilience options (Multi-AZ, DR region) in baseline estimate.
- Produce low/most-likely/high estimate bands with explicit assumptions.

## Estimation workflow
1. Define usage profile (steady-state, peak, burst frequency).
2. Map each architecture component to pricing units.
3. Add resilience and observability overhead.
4. Add data transfer between tiers/regions.
5. Evaluate pricing model fit per component (on-demand vs commitments vs spot where safe).
6. Produce scenario ranges and confidence level.
7. Define post-launch measurement checkpoints to calibrate estimates.

## If/Then rules
| If | Then |
|---|---|
| Usage is spiky and unpredictable | Favor elastic/on-demand posture first |
| Usage is stable and sustained | Evaluate commitments after usage baseline |
| Cross-region architecture selected | Model transfer + replication + failover testing cost |
| Data retention is long-term | Use lifecycle and archival classes by policy |
| Workload is event-driven with low average utilization | Avoid heavy always-on capacity by default |
| Capacity headroom is large due to uncertain growth | Add staged rightsizing milestones and re-estimation cadence |
| Compute or database usage is highly predictable | Model commitment options after baseline stabilization period |
| Data architecture crosses AZ/Region boundaries heavily | Explicitly model transfer and replication costs as first-order drivers |

## Pricing model chooser
| Pattern | First choice | Revisit trigger |
|---|---|---|
| Unknown/new workload with volatile usage | On-demand baseline | After 2-4 weeks of stable usage trend |
| Stable 24x7 baseline demand | Savings Plans / Reserved capacity for baseline + on-demand for burst | Monthly utilization drift >15% |
| Fault-tolerant interruptible batch jobs | Spot for eligible portion + fallback on-demand | Interruption rate degrades SLO |
| Archival data with rare retrieval | Lifecycle to lower-cost storage classes | Retrieval frequency increases |

## Data transfer checklist (frequent miss)
- Inter-AZ traffic between app and database tiers.
- Cross-AZ load balancer behavior and backend placement.
- Cross-Region replication and DR data movement.
- Internet egress and CDN offload assumptions.
- Backup copy and restore data movement patterns.

## Governance baseline
- Tagging policy with mandatory owner, environment, and cost-center tags.
- Budget alerts and anomaly detection per environment.
- Periodic rightsizing review and idle resource cleanup.
- Quarterly commitment review (Savings Plans/RI posture).

## Controls by lifecycle stage
| Stage | Minimum controls |
|---|---|
| Design | Scenario estimate with assumptions and top 3 cost risks |
| Pre-production | Budget thresholds + anomaly detection configured |
| Post-launch (30 days) | Actual vs estimate variance analysis |
| Ongoing | Monthly unit economics review + quarterly commitment review |

## Deterministic estimate quality gate
- Every estimate includes units, rate assumptions, and confidence.
- Every high-cost component has a named owner and optimization action.
- Every architecture output includes one `MAJOR_DECISION` for cost model posture.
- Every post-launch review compares actuals to estimate and records variance causes.

## Anti-patterns
- No scenario ranges (low/most likely/high) in estimates.
- Ignoring transfer and observability costs.
- Commitments purchased before usage pattern stabilizes.
- Treating DR/backup as "free" overhead not included in TCO.
- Estimating only service list prices without workload behavior assumptions.

## Acceptance criteria
- Estimate includes assumptions and confidence level.
- Top three cost drivers are identified with mitigations.
- Cost controls (budget/anomaly/tagging) are documented before launch.
- A calibration plan exists to compare actual spend vs estimate after go-live.
- At least one ADR captures commitment strategy and revisit trigger.
- WA cost pillar includes explicit findings with remediation owners and target dates.

### Example MAJOR_DECISION
`MAJOR_DECISION: cost-model | commitment-strategy | Start on-demand for 30 days, then evaluate Savings Plans using observed baseline`
