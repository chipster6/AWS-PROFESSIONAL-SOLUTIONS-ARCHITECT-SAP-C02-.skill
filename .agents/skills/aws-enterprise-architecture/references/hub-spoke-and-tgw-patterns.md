# Hub-Spoke and Transit Gateway Patterns

## Goal
Design scalable network topology for many VPCs and on-premises connectivity without mesh sprawl.

## Recommended topology
- Prefer hub-and-spoke over many-to-many mesh.
- Use AWS Transit Gateway as routing hub.
- Attach workload VPCs, inspection VPCs, and hybrid connectivity attachments.

## Topology decision cues
| Signal | Recommendation |
|---|---|
| Growing VPC/account count with peering sprawl | Transit Gateway hub-and-spoke |
| Need centralized inspection and segmentation | Dedicated inspection/shared services attachments |
| Need hybrid and multi-account routing control | TGW with explicit route-domain design |

## Why hub-and-spoke
- Reduces route-table complexity.
- Centralizes policy and traffic control.
- Improves scalability as account/VPC count grows.

## Route segmentation model
1. Isolate prod/non-prod routes.
2. Separate east-west and north-south policy paths.
3. Control shared service reachability explicitly.
4. Log and inspect inter-segment traffic as required.

## Deterministic TGW design checklist
- [ ] Separate route tables for production and non-production traffic.
- [ ] Explicit propagation/association model documented per attachment.
- [ ] East-west and north-south paths are mapped and approved.
- [ ] Inspection/evaluation path is defined for regulated segments.
- [ ] Data transfer and inter-AZ traffic cost assumptions are documented.

## Anti-patterns
- Anti-pattern: unsegmented TGW route tables.
- Anti-pattern: overcomplicated custom routing without ownership.
- Anti-pattern: unmanaged cross-AZ/region traffic cost growth.
- Anti-pattern: many-to-many peering retained after TGW adoption.

## Acceptance criteria
- Route domains align to security and operational boundaries.
- Attachment ownership and change process are documented.
- Failure and failover behavior are tested for critical paths.
- At least one ADR captures topology and segmentation trade-offs.

## MAJOR_DECISION examples
- `MAJOR_DECISION: network-topology | tgw-hub-spoke | Use Transit Gateway hub-spoke topology instead of VPC peering mesh.`
- `MAJOR_DECISION: segmentation | route-table-boundaries | Enforce separate TGW route domains for production and non-production traffic.`
