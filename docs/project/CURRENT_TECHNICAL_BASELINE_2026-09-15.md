# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — SETUP BASELINE AND SITE AUTHORITY APPROVED / ASSIGNMENT ABSENT** |
| Repository baseline | `main@e73b1aa631c41dff97b9e5ededb6d6be02a667d4` |
| Current package | `BKL-031-F3-A2-D3-CURRENT-SETUP-ASSIGNMENT-OWNER-DECISION` |
| Runtime delta | None |
| Data delta | Protected approved setup baseline and Site Authority; no assignment |
| Infrastructure delta | None |

## 1. Integrated state

PR #204 is merged as `e73b1aa631c41dff97b9e5ededb6d6be02a667d4` and establishes the current verified repository baseline. Exact-head CI passed 8/8 and post-merge workflows passed 10/10. The protected setup and site registries contain their separately approved authority envelopes and immutable receipts.

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
| CurrentSetupAssignment | absent |
| S08 / S09 | `UNAVAILABLE` / `UNAVAILABLE_CURRENT` |
| Runtime adapter | absent; separate package and authorization required |

## 4. Rollback

The F3-A1-M4 promotion can be reverted through reviewed Git history by removing the APPROVED envelope and receipt while retaining the historical DRAFT. Approved authority retirement remains governed by ADR-009. No runtime, migration, credential or observatory impact exists.
