# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — FIRST BASELINE OWNER-APPROVED / PR #201 UNDER REVIEW** |
| Repository baseline | `main@1ce08f4cc5458cc7ac68732a02df0d27a359f8d5` |
| Current package | `BKL-031-F3-A2-D2-BASELINE-APPROVAL-PUBLICATION` |
| Runtime delta | None |
| Data delta | Protected APPROVED baseline and immutable receipt; no assignment |
| Infrastructure delta | None |

## 1. Integrated state

PR #199 is merged/post-merge verified 9/9. ADR-009 makes GitHub the setup-authority registry, the Repository Owner the human Approval Authority and the Architecture Office the non-approving custodian. Protected records remain outside `docs/`.

## 2. Exact candidate

`DSG-SETUP-BASELINE-001` represents the owner-approved composite dual-OTA setup and has immutable payload `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`, validity `[2026-09-16T00:00:00Z, +infinity)`, explicit missing-data exceptions and lifecycle `APPROVED`. Receipt `DSG-SETUP-BASELINE-001-APPROVAL-001` binds the human decision to the exact digest.

## 3. Dependency readiness

| Elemento | Stato |
|---|---|
| Authority source/roles | integrated |
| Candidate definition | owner-confirmed |
| Payload digest | independently verified |
| Human exact-digest approval | **complete / exact digest approved** |
| Approval receipt | present / PR #201 |
| F3-A1 site record | absent |
| CurrentSetupAssignment | absent |
| Schema/validator/adapter | not implemented |
| S09 | `UNAVAILABLE_CURRENT` |

## 4. Rollback

Retire or revert the approved envelope and receipt through reviewed Git history; no runtime, migration, credential or observatory impact.
