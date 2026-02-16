# ADR: Immutability and retention

- Status: Accepted
- Date: 2026-02-15
- ADR ID: ADR-0002

## Context

Audit logs must be immutable and retained for years.

## Decision

Enable Object Lock on log archive buckets with long retention.

## Alternatives considered

Standard versioning without Object Lock.

## Consequences

### Positive

Tamper resistance and compliance alignment.

### Negative / trade-offs

Higher storage costs.

## Well-Architected mapping

- Pillars touched: security, reliability
- Risks mitigated: evidence tampering
- Risks introduced: cost growth

## Cost impact

- Drivers: log_retention, object_lock
- Estimate linkage: `artifacts/cost-estimate.md`

## Security / compliance evidence

- Evidence sources: S3 Object Lock settings
- Notes: retention periods documented

## AWS documentation references

- https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html

