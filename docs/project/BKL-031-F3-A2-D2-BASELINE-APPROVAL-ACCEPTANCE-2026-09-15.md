# BKL-031 F3-A2-D2 — Baseline Approval Acceptance

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D2-ACCEPTANCE-001 |
| Stato | **ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED** |
| Data | 15/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento | F3-A2-D2 — Approval Receipt and Lifecycle Promotion |
| Pull request | #201 |
| Reviewed head | `e12aad1c3ea5f817e78759020a2b4621d094bcc4` |
| Merge commit | `9932bace989565a10fd8e0d6f4a9c3b2cc057c46` |
| Runtime / EAGLE | None |
| Successore | F3-A1-M1 — owner decision required |

## 1. Decisione

F3-A2-D2 is accepted with conditions as the protected publication of the Repository Owner's exact-digest approval. The package promotes only the lifecycle envelope of `DSG-SETUP-BASELINE-001` to `APPROVED` and adds immutable receipt `DSG-SETUP-BASELINE-001-APPROVAL-001`.

The canonical payload remains unchanged at `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`, valid from `2026-09-16T00:00:00Z`.

## 2. Review and merge evidence

| Evidenza | Esito |
|---|---|
| ARB AI-assisted on exact head | APPROVED WITH CONDITIONS — 99/100 |
| Release Quality AI-assisted | CONDITIONALLY READY FOR MERGE |
| Exact-head workflows | 4/4 SUCCESS |
| Review threads | none |
| Merge commit | `9932bace989565a10fd8e0d6f4a9c3b2cc057c46` |
| Post-merge workflows | 6/6 SUCCESS |
| Rulesets endpoint | empty list |
| Classic branch-protection endpoint | not readable by integration; no claim inferred |
| Merge-control evidence | recorded on PR #201 under `W-DSG-AEM-RULESET-001` |

The reviews are AI-assisted, process-separated and not equivalent to independent human approval.

## 3. Post-merge verification

| Workflow | Run | Esito |
|---|---:|---|
| Scientific Platform Governance | #157 / `34983360136` | SUCCESS |
| Genera manuale Word | #1521 / `34983360056` | SUCCESS |
| Governed Projection Sync | #64 / `34983359838` | SUCCESS |
| Validate documentation | #1095 / `34983360003` | SUCCESS |
| Deploy MkDocs artifact to GitHub Pages | #810 / `34983359856` | SUCCESS |
| Developer Foundation | #1458 / `34983360148` | SUCCESS |

Evidence is valid only for the exact merge SHA.

## 4. Findings and conditions

- `ARB-201-MI01`: proposal-time payload labels remain historical assertions because the approved digest is immutable; lifecycle truth is the envelope plus receipt.
- `ARB-201-MI02`: approved schema/validator remains mandatory before F3-B/runtime resolution.
- `ARB-201-MI03`: F3-A1 concrete site record and separately approved `CurrentSetupAssignment` remain mandatory before S09.
- no Blocker or Major is open for F3-A2-D2 acceptance.

## 5. Preserved boundaries

- approved baseline is eligible only within its validity interval;
- no baseline approval creates or implies a site record or assignment;
- S08 remains `UNAVAILABLE`; S09 remains `UNAVAILABLE_CURRENT`;
- the protected registry remains outside Pages;
- no public exact coordinates, schema, validator, adapter, runtime, EAGLE operation, readiness, go/no-go or Safety Authority is introduced.

## 6. Rollback

Retire or revert the approved envelope and receipt through reviewed Git history. The acceptance reconciliation itself is documentation-only. No migration, credential, runtime or observatory rollback is required.

## 7. Successor decision

F3-A1-M1 Site Authority Materialization Decision is selected as the next dependency-ordered gate. Materialization cannot begin until the owner explicitly determines the protected authority and exact site facts listed in `BKL-031-F3-A1-M1-PROGRAM-001`.
