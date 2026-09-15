# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — AUTHORITY MODEL INTEGRATED / FIRST BASELINE DRAFT** |
| Repository baseline | `main@4e8802c80359efce28d8d75521a1b9cc4cb44b05` |
| Current package | `BKL-031-F3-A2-D1-EXACT-DIGEST-OWNER-GATE` |
| Runtime delta | None |
| Data delta | Protected DRAFT only; no approved authority record |
| Infrastructure delta | None |

## 1. Integrated state

PR #199 is merged/post-merge verified 9/9. ADR-009 makes GitHub the setup-authority registry, the Repository Owner the human Approval Authority and the Architecture Office the non-approving custodian. Protected records remain outside `docs/`.

## 2. Exact candidate

`DSG-SETUP-BASELINE-001` represents the owner-confirmed composite dual-OTA setup and has payload `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`, proposed validity `[2026-09-16T00:00:00Z, +infinity)`, explicit missing-data exceptions and lifecycle `DRAFT`.

## 3. Dependency readiness

| Elemento | Stato |
|---|---|
| Authority source/roles | integrated |
| Candidate definition | owner-confirmed |
| Payload digest | independently verified |
| Human exact-digest approval | **mandatory / pending** |
| Approval receipt | absent |
| F3-A1 site record | absent |
| CurrentSetupAssignment | absent |
| Schema/validator/adapter | not implemented |
| S09 | `UNAVAILABLE_CURRENT` |

## 4. Rollback

Revert PR #199; no runtime, migration, credential or observatory impact.
