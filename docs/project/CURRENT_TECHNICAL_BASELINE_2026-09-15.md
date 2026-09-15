# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — ASSIGNMENT APPROVAL/PROMOTION REVIEW CANDIDATE** |
| Repository baseline | `main@e99e6b5ff5ea7247ee447a1c6c62dcaa479dee1b` |
| Current package | `BKL-031-F3-A2-D5` in PR #209 |
| Runtime delta | None |
| Data delta | Protected approval receipt and unchanged APPROVED lifecycle envelope candidate |
| Infrastructure delta | None |

## 1. Integrated state

PR #207 is merged as `e99e6b5ff5ea7247ee447a1c6c62dcaa479dee1b` and establishes the current verified repository baseline with 7/7 post-merge workflows. The protected setup and site registries retain their separately approved authority envelopes and immutable receipts; the assignment registry now contains only a DRAFT.

## 2. Approved authority state

The setup baseline and Site Authority are independently approved. Their exact digests, internal identifiers, locators and protected site facts are intentionally omitted from this public baseline. Lifecycle truth is the applicable immutable payload plus its separate approval receipt.

## 3. Dependency readiness

| Elemento | Stato |
|---|---|
| Setup authority source/roles | integrated |
| First setup baseline | APPROVED / post-merge verified |
| F3-A1 normative site contract | accepted with conditions |
| Exact protected site facts | approved authority outside Pages; omitted publicly |
| Site Authority owner/approver/source | complete; receipt and lifecycle post-merge verified |
| Elevation vertical semantics | materialized and validated |
| Canonical site resolver identity/scope | materialized and validated |
| Executable validity/privacy/promotion tests | 59/59 PASS; exact-head and post-merge verified |
| CurrentSetupAssignment | DRAFT integrated; exact-digest owner approval received; APPROVED envelope review candidate |
| Assignment owner decisions | complete; protected evidence integrated |
| Assignment lifecycle validation | implementation head SUCCESS; 65/65 tests |
| S08 / S09 | `UNAVAILABLE` / `UNAVAILABLE_CURRENT` |
| Runtime adapter | absent; separate package and authorization required |

## 4. Rollback

The F3-A1-M4 promotion can be reverted through reviewed Git history by removing the APPROVED envelope and receipt while retaining the historical DRAFT. Approved authority retirement remains governed by ADR-009. No runtime, migration, credential or observatory impact exists.

## F3-A2-D4 baseline delta

PR #207 integrated repository-only protected authority artifacts and a redacted validation workflow. S08 remains unavailable to runtime and S09 remains `UNAVAILABLE_CURRENT`. No runtime, EAGLE, provider, readiness, command or Safety Authority delta is present. Rollback is the reviewed revert of the D4 merge; no operational rollback is required.


## F3-A2-D5 candidate delta

PR #209 adds only protected receipt/promotion artifacts, one closed schema, validator/tests and sanitized documentation. The approved envelope preserves the D4 assignment payload and digest. Repository resolution can become `AVAILABLE` for authorized validated callers after integration, but runtime S09 remains `UNAVAILABLE_CURRENT` because no adapter is introduced.
