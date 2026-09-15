# BKL-031 F3-A2-D3 — CurrentSetupAssignment Owner Decision

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D3-DECISION-001 |
| Stato | **OWNER DECISIONS COMPLETE / REPOSITORY INTEGRATION CANDIDATE** |
| Data | 15/09/2026 |
| Baseline | `main@d5f403bbe6a39731213c372cb22296324d10b03d` |
| Protected evidence | Outside `docs/`; exact references omitted |
| Runtime / EAGLE | None |

## 1. Decision

The Repository Owner selected the protected GitHub registry outside `docs/` as the future `CurrentSetupAssignment` source authority. The Repository Owner is the assignment owner and human Assignment Approval Authority; the Digital StarGate Architecture Office is the non-approving custodian.

The validity policy is half-open, starts when the already approved setup baseline becomes effective and has no end date. The protected evidence binds the exact approved baseline and Site Authority references without reproducing them publicly.

## 2. Authorized repository effect

This package may add only immutable protected owner-decision evidence and update governance continuity. It does not create an assignment payload, schema, canonical digest, approval receipt, lifecycle promotion, adapter, persistence or runtime API. Decision evidence is not an assignment authority record and cannot be resolved by S09.

## 3. Capability state

- setup baseline: independently APPROVED;
- Site Authority: independently APPROVED;
- assignment source/role/validity decisions: complete;
- `CurrentSetupAssignment`: absent;
- S08: `UNAVAILABLE` because no runtime adapter exists;
- S09: `UNAVAILABLE_CURRENT` because no approved assignment exists.

## 4. Privacy and safety

No exact site fact, internal assignment/site/baseline identifier, digest or locator is published. No provider, forecast, ranking, readiness, command, EAGLE workload or Safety Authority change is introduced. Physical/local interlocks remain authoritative.

## 5. Next gate

After this decision evidence is integrated and post-merge verified, `BKL-031-F3-A2-D4` may prepare a protected resolver-ineligible DRAFT with schema, canonicalization, validator and executable tests. Exact-digest human approval and lifecycle promotion remain later, separate gates.

## 6. Rollback

Revert the protected decision evidence and continuity updates through reviewed Git history. Approved site and baseline authorities remain unchanged; assignment resolution remains unavailable.
