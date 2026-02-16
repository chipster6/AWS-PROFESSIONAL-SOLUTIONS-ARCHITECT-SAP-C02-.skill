# Anti-Pattern Catalog

## Scope
Use this catalog to reject weak designs early.

## Architecture anti-patterns
1. **Single-region critical dependency with no recovery pattern**
   - Symptom: no tested failover path.
   - Risk: prolonged outage on regional event.
2. **Security afterthought design**
   - Symptom: trust boundaries and IAM are deferred.
   - Risk: privilege sprawl and incident blast radius.
3. **Control-plane dependency in failover**
   - Symptom: recovery plan requires many ad hoc provisioning actions during incident.
   - Risk: missed RTO under stress.
4. **Over-coupled synchronous chains**
   - Symptom: long request path with strict serial dependencies.
   - Risk: cascading latency and failure amplification.
5. **No decision traceability**
   - Symptom: major choices have no ADR or rationale.
   - Risk: drift and repeated re-litigation.

## Organizational anti-patterns
1. **OU/account design mirrors org chart only**
   - Risk: weak policy boundaries and governance drift.
2. **SCP rollout at root without staged testing**
   - Risk: broad service disruption or lockout.
3. **Shared credentials for third-party integrations**
   - Risk: poor attribution and credential leakage.

## Cost anti-patterns
1. **Commitment purchases before usage stability**
2. **No tagging governance for showback/chargeback**
3. **Optimization limited to compute rightsizing only**

## How to use this catalog
1. During option analysis, mark anti-pattern matches.
2. Any “high-risk anti-pattern” requires redesign or strong mitigation.
3. If mitigation is accepted, record as explicit risk.
