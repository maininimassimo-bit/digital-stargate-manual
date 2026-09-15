# BKL-031 F3-A2-D1 — GitHub Authority and First Baseline Draft Assessment

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D1-ASSESS-001 |
| Stato | **FIRST BASELINE APPROVED / RECEIPT MATERIALIZATION CANDIDATE** |
| Data | 15/09/2026 |
| Baseline verificata | `main@1ce08f4cc5458cc7ac68732a02df0d27a359f8d5` |
| Capability | BKL-031 — Observation Planner intelligente |
| Parent | `BKL-031-F3-A2-CONTRACT-001` |
| ADR | ADR-009 |
| Runtime delta | None |
| Data delta | One protected APPROVED baseline and immutable receipt; no assignment |
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

This closes the authority-system/role/source and first-baseline approval portions of `ARB-197-MI01`. It does not close the F3-A1 site-record or assignment gates.

## Evidence selection

The equipment registry supplies two explicit `ACTIVE` projection rows. Both are copied into the candidate without promoting their authority:

1. `QUATTRO200_TOUPTEK294_BIN1`;
2. `C8_QHY695A_BIN1`.

The shared CGX-L and parallel-OTA candidate relation comes from the two registry notes. C8 guiding is null because the source says it must be inventoried. No log, filename, host state or latest-observation heuristic was used.

## Exact candidate

- record: `governance/setup-authority/configuration-baselines/DSG-SETUP-BASELINE-001.approved.json`;
- state: `APPROVED`;
- payload digest: `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`;
- proposed validity: `[2026-09-16T00:00:00Z, +infinity)`;
- classification: `PROTECTED_CONFIGURATION`;
- baseline-reference eligibility: true only inside the approved validity interval;
- current assignment: absent;
- S09: `UNAVAILABLE_CURRENT`.

## Owner definition confirmations

On 15/09/2026 the Repository Owner confirmed through the controlled interaction channel:

- one composite baseline for the two OTAs mounted in parallel on the CGX-L;
- validity start `2026-09-16T00:00:00Z`;
- unresolved C8 guiding, serials and runtime versions remain explicit null/`DA_VALIDARE` exceptions outside the authoritative payload claims.

These confirmations defined the candidate and preserved payload `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`. The Repository Owner then explicitly approved that exact digest and validity through the owner-controlled interaction channel; receipt `DSG-SETUP-BASELINE-001-APPROVAL-001` records the separate approval act.

## Remaining gaps

| Gate | Stato |
|---|---|
| Owner approval/correction of exact payload digest and validity | **CLOSED — APPROVED** |
| Baseline approval receipt | present / exact-digest bound |
| F3-A1 concrete site record | absent |
| CurrentSetupAssignment | absent |
| Assignment approval receipt | absent |
| Machine-readable schema/validator | not implemented |
| Adapter/persistence/public read model | not implemented |
| Runtime/OAT | not executed |
| C8 guiding and runtime/serial details | `DA_VALIDARE` |

## Acceptance and rollback

This package may integrate the protected `APPROVED` envelope and exact-digest receipt. It must not claim current-setup resolution or S09 availability. Rollback retires or reverts the envelope and receipt through reviewed Git history; no runtime, migration or observatory operation exists.
