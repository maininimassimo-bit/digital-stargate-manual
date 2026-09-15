# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — F3-A2-D1 AUTHORITY DECISION / DRAFT ONLY** |
| Repository baseline | `main@687f966fa544f7c4b31eaa29433cfa8ab48e52fe` |
| Working branch | `docs/bkl-031-f3-a2-d1-authority-baseline-draft` |
| Current package | `BKL-031-F3-A2-D1` |
| Runtime delta | None |
| Data delta | Protected DRAFT only; no approved authority record |
| Infrastructure delta | None |

## 1. Integrated foundation

F3-A2 contract and acceptance are post-merge verified through PR #198. ADR-009 records the newly owner-authorized GitHub authority model; the target registry is `governance/setup-authority/`, outside Pages.

## 2. Candidate state

`DSG-SETUP-BASELINE-001` contains two projection-sourced configuration profiles and payload digest `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`. Its lifecycle is `DRAFT`, `eligibleForResolution=false`, with no approval evidence. The validity start `2026-09-16T00:00:00Z` is proposed for owner decision.

## 3. Authority and separation

The Repository Owner is baseline/assignment owner and human Approval Authority. The Digital StarGate Architecture Office is custodian only. Baseline and assignment approvals remain distinct; no assistant review or CI result can replace owner approval.

## 4. Dependency readiness

| Elemento | Stato |
|---|---|
| GitHub authority source/roles | owner-authorized via ADR-009 |
| First payload | DRAFT / exact digest available |
| First baseline approval | **mandatory owner decision pending** |
| F3-A1 concrete site record | absent |
| CurrentSetupAssignment | absent |
| Schema/validator/adapter | not implemented |
| S09 | `UNAVAILABLE_CURRENT` |
| F3-A3/B/C | not promoted |

## 5. Rollback

Revert ADR-009 and the protected DRAFT files. No migration, deployment, credential or observatory operation exists.
