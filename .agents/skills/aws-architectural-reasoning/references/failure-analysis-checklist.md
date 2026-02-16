# Failure Analysis Checklist

## Goal
Systematically test architecture choices against realistic failure modes.

## Scenario set
1. Dependency latency spike (database, queue, external API).
2. Partial network loss (AZ path impairment, VPN flap, DX outage).
3. Control-plane throttling or temporary unavailability.
4. Credential/secret compromise.
5. Logging/monitoring blind spot.
6. Cost anomaly due to retry storm or runaway scaling.

## Analysis steps
1. Define trigger and detection signal.
2. Identify blast radius.
3. Verify containment controls.
4. Verify recovery path and expected RTO/RPO performance.
5. Capture corrective actions and owner.

## Deterministic questions
- What signal detects this first?
- Who is paged and how fast?
- Which safeguard prevents cross-boundary propagation?
- Can recovery execute with data-plane-first operations?
- What evidence proves the system is healthy after recovery?

## Pass criteria
- Detection occurs within agreed MTTD target.
- Containment keeps blast radius within defined boundary.
- Recovery meets documented RTO/RPO.
- Post-incident artifacts are created and linked.

## Evidence artifacts
- Relevant WA review section,
- runbook steps and timestamps,
- linked ADR or corrective ADR if architecture changed.
