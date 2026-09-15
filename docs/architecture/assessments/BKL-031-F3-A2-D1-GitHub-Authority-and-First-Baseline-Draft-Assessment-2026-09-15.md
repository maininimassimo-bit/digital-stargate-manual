# BKL-031 F3-A2-D1 — GitHub Authority and First Baseline Draft Assessment

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D1-ASSESS-001 |
| Stato | **OWNER-AUTHORIZED AUTHORITY DECISION / REVIEW CANDIDATE** |
| Data | 15/09/2026 |
| Baseline verificata | `main@687f966fa544f7c4b31eaa29433cfa8ab48e52fe` |
| Capability | BKL-031 — Observation Planner intelligente |
| Parent | `BKL-031-F3-A2-CONTRACT-001` |
| ADR | ADR-009 |
| Runtime delta | None |
| Data delta | One protected DRAFT record; no approved baseline or assignment |
| PC Principale / EAGLE | Nessuna attività richiesta |

## Outcome

The repository now has a deterministic target model for setup authority:

| Elemento | Decisione |
|---|---|
| Authority system | GitHub repository, protected registry outside `docs/` |
| Baseline owner | `github:user:maininimassimo-bit` |
| Baseline custodian | `role:digital-stargate-architecture-office` |
| Baseline Approval Authority | `github:user:maininimassimo-bit` |
| Assignment owner | `github:user:maininimassimo-bit` |
| Assignment custodian | `role:digital-stargate-architecture-office` |
| Assignment Approval Authority | `github:user:maininimassimo-bit` |
| Separation | baseline and assignment approvals are distinct; custodian cannot approve |
| Publication | deny-by-default; registry excluded from Pages |
| Digest | `DSG-F3A2-CANONICAL-JSON-SHA256-1` |

This closes the authority-system/role/source part of `ARB-197-MI01`. It does not close the mandatory first-baseline approval or assignment gates.

## Evidence selection

The equipment registry supplies two explicit `ACTIVE` projection rows. Both are copied into the candidate without promoting their authority:

1. `QUATTRO200_TOUPTEK294_BIN1`;
2. `C8_QHY695A_BIN1`.

The shared CGX-L and parallel-OTA candidate relation comes from the two registry notes. C8 guiding is null because the source says it must be inventoried. No log, filename, host state or latest-observation heuristic was used.

## Exact candidate

- record: `governance/setup-authority/configuration-baselines/DSG-SETUP-BASELINE-001.draft.json`;
- state: `DRAFT`;
- payload digest: `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`;
- proposed validity: `[2026-09-16T00:00:00Z, +infinity)`;
- classification: `PROTECTED_CONFIGURATION`;
- resolver eligibility: false;
- current assignment: absent;
- S09: `UNAVAILABLE_CURRENT`.

## Owner definition confirmations

On 15/09/2026 the Repository Owner confirmed through the controlled interaction channel:

- one composite baseline for the two OTAs mounted in parallel on the CGX-L;
- validity start `2026-09-16T00:00:00Z`;
- unresolved C8 guiding, serials and runtime versions remain explicit null/`DA_VALIDARE` exceptions outside the authoritative payload claims.

These confirmations define the candidate and preserve payload `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`. They are not the separate final approval of that exact digest.

## Remaining gaps

| Gate | Stato |
|---|---|
| Owner approval/correction of exact payload digest and validity | **MANDATORY — OPEN** |
| Baseline approval receipt | absent |
| F3-A1 concrete site record | absent |
| CurrentSetupAssignment | absent |
| Assignment approval receipt | absent |
| Machine-readable schema/validator | not implemented |
| Adapter/persistence/public read model | not implemented |
| Runtime/OAT | not executed |
| C8 guiding and runtime/serial details | `DA_VALIDARE` |

## Acceptance and rollback

This package may integrate as an authority decision plus protected DRAFT only. It must not claim baseline approval or S09 availability. Rollback is a repository revert; no runtime, migration or observatory operation exists.
