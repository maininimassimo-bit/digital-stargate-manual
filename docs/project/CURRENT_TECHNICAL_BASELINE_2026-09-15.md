# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — SETUP BASELINE APPROVED / SITE AUTHORITY DRAFT CANDIDATE INELIGIBLE** |
| Repository baseline | `main@bb11f25192200655427411a46a2e18560a5d9bec` |
| Current package | `BKL-031-F3-A1-M2-SITE-AUTHORITY-DRAFT-MATERIALIZATION` |
| Runtime delta | None |
| Data delta | Protected approved setup baseline; protected site DRAFT candidate and source decision; no assignment |
| Infrastructure delta | None |

## 1. Integrated state

PR #202 is merged/post-merge verified and establishes the current repository baseline. The protected GitHub setup-authority registry continues to contain the approved setup baseline envelope and immutable receipt.

## 2. Exact approved baseline

`DSG-SETUP-BASELINE-001` has payload `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`, validity `[2026-09-16T00:00:00Z, +infinity)` and receipt `DSG-SETUP-BASELINE-001-APPROVAL-001`.

Proposal-time labels inside the immutable payload remain historical assertions. Current lifecycle truth is the envelope plus receipt.

## 3. Dependency readiness

| Elemento | Stato |
|---|---|
| Setup authority source/roles | integrated |
| First setup baseline | APPROVED / post-merge verified |
| F3-A1 normative site contract | accepted with conditions |
| Exact protected site facts | owner-supplied / DRAFT candidate outside Pages |
| Site Authority owner/approver/source | decision complete; exact-digest approval pending |
| Elevation vertical semantics | materialized in schema/validator; ARB review pending |
| Canonical site resolver identity/scope | materialized in schema/validator; ARB review pending |
| Executable validity/privacy tests | 51/51 local PASS; exact-head CI pending |
| CurrentSetupAssignment | absent |
| S08 / S09 | `UNAVAILABLE` / `UNAVAILABLE_CURRENT` |

## 4. Rollback

The F3-A1-M2 DRAFT candidate can be reverted through reviewed Git history. The approved setup baseline remains governed by ADR-009 retirement/revert rules. No runtime, migration, credential or observatory impact exists.
