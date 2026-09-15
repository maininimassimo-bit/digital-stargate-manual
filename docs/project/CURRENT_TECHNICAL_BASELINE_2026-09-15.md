# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — FIRST SETUP BASELINE APPROVED / SITE AUTHORITY UNAVAILABLE** |
| Repository baseline | `main@9932bace989565a10fd8e0d6f4a9c3b2cc057c46` |
| Current package | `BKL-031-F3-A1-M1-SITE-AUTHORITY-OWNER-DECISION` |
| Runtime delta | None |
| Data delta | Protected approved setup baseline and receipt; no site record or assignment |
| Infrastructure delta | None |

## 1. Integrated state

PR #201 is merged/post-merge verified 6/6. The protected GitHub setup-authority registry contains the owner-approved baseline envelope and immutable receipt. The canonical payload was not mutated during lifecycle promotion.

## 2. Exact approved baseline

`DSG-SETUP-BASELINE-001` has payload `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`, validity `[2026-09-16T00:00:00Z, +infinity)` and receipt `DSG-SETUP-BASELINE-001-APPROVAL-001`.

Proposal-time labels inside the immutable payload remain historical assertions. Current lifecycle truth is the envelope plus receipt.

## 3. Dependency readiness

| Elemento | Stato |
|---|---|
| Setup authority source/roles | integrated |
| First setup baseline | APPROVED / post-merge verified |
| F3-A1 normative site contract | accepted with conditions |
| Exact protected site facts | absent / owner input required |
| Site Authority owner/approver/source | decision required |
| Elevation vertical semantics | open — `ARB-193-MI01` |
| Canonical site resolver identity/scope | open — `ARB-193-MI02` |
| Executable validity/privacy tests | not implemented |
| CurrentSetupAssignment | absent |
| S08 / S09 | `UNAVAILABLE` / `UNAVAILABLE_CURRENT` |

## 4. Rollback

The acceptance reconciliation is documentation-only and can be reverted through reviewed Git history. The approved setup baseline remains governed by ADR-009 retirement/revert rules. No runtime, migration, credential or observatory impact exists.
