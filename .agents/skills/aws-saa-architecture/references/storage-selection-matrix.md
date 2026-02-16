# S3 vs EBS vs EFS

## Primary fit
| Requirement | S3 (object) | EBS (block) | EFS (file) |
|---|---|---|---|
| API/object access pattern | Strong fit | No | No |
| Single-host attached low-latency block | No | Strong fit | No |
| Shared filesystem across many clients | No | No | Strong fit |
| Archival/lifecycle tiering | Strong fit | Limited | Limited |
| Traditional file semantics (NFS) | No | No | Strong fit |

## If/Then rules
| If | Then |
|---|---|
| Workload reads/writes objects through API and needs broad durability | Prefer S3 |
| One compute host needs dedicated low-latency block volume | Prefer EBS |
| Many compute clients require concurrent shared file access | Prefer EFS |
| You need lifecycle-based cost tiering and object analytics | Prefer S3 |
| You need boot volume or transactional block IO attached to instance | Prefer EBS |
| You need POSIX-like shared files with elastic growth | Prefer EFS |

## Performance and behavior cues
- S3: strong consistency for object operations and high request parallelism.
- EBS: single-instance block semantics, ideal for OS disks and transactional stores.
- EFS: distributed shared file semantics with aggregate throughput across many clients.

## Deterministic selection table
| Decision input | S3 | EBS | EFS |
|---|---|---|---|
| Access protocol | Object API | Block device | NFS file |
| Typical sharing model | Many clients via API | Single attached host (multi-attach limited patterns) | Many clients shared file tree |
| Latency profile | Millisecond object access | Low-latency block IO | File-level latency with shared semantics |
| Cost optimization mode | Storage classes + lifecycle | Volume type tuning + snapshots | Throughput mode + lifecycle/IA where applicable |
| Archival strategy | Native lifecycle to Glacier classes | Snapshot/archive patterns | Lifecycle for less-frequent file access |

## Service-specific sizing cues
- S3:
  - Choose storage class by access frequency and retrieval tolerance.
  - Use Intelligent-Tiering for unknown/changing access patterns.
- EBS:
  - `gp3` default for general SSD workloads.
  - `io2` when sustained high IOPS/low latency consistency is required.
  - `st1`/`sc1` only for throughput-oriented or cold HDD use cases (not boot volumes).
- EFS:
  - Prefer General Purpose mode for most workloads.
  - Use Elastic throughput for spiky/unpredictable patterns; Provisioned when known throughput floor is required.

## Anti-patterns
- EBS chosen for many-writer shared file access.
- EFS used for object API-native workflows.
- S3 used where POSIX-like shared file behavior is mandatory.
- Single service forced for all data patterns to reduce “tool sprawl.”
- Ignoring throughput mode/volume type tuning during design.

## Acceptance criteria
- Storage choice matches access protocol (object vs block vs file).
- Throughput/latency expectations are documented with workload profile.
- Data durability/availability and lifecycle posture are explicit.
- Backup and restore path is documented and tested for the chosen storage type(s).
- At least one ADR captures storage family selection and rejected alternatives.

### Example MAJOR_DECISION
`MAJOR_DECISION: data-store | media-storage-model | Store media assets in S3 and reserve EFS for shared render workspace`
