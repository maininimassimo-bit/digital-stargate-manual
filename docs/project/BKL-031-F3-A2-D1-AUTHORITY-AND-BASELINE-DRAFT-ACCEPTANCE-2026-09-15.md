# BKL-031 F3-A2-D1 — Authority and Baseline Draft Acceptance

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D1-ACCEPTANCE-001 |
| Stato | **ACCEPTANCE CANDIDATE — PR #199 POST-MERGE VERIFIED / EXACT-DIGEST APPROVAL PENDING** |
| Data | 15/09/2026 |
| Integrated PR | #199 |
| Publication head | `7c124d6f2cb1b6356c7008ac2f70824b5579a262` |
| Merge | `4e8802c80359efce28d8d75521a1b9cc4cb44b05` |
| Review | ARB 99/100; Release Quality Conditionally Ready |
| Runtime / EAGLE | None |

## 1. Accepted increment

PR #199 integrated the owner-authorized GitHub setup-authority model, ADR-009, the protected registry outside `docs/`, the mandatory stop-notification rule and the first exact DRAFT payload.

The Repository Owner confirmed:

- one composite baseline for the parallel Quattro 200P and C8 profiles on CGX-L;
- validity from `2026-09-16T00:00:00Z`;
- explicit null/`DA_VALIDARE` exceptions for C8 guiding, serials and runtime versions.

These choices define the candidate. They do not constitute the separate human approval of its exact digest.

## 2. Exact candidate state

| Elemento | Stato |
|---|---|
| Baseline ID | `DSG-SETUP-BASELINE-001` |
| Payload digest | `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8` |
| Lifecycle | `DRAFT` |
| Resolver eligible | false |
| Approval receipt | absent |
| CurrentSetupAssignment | absent |
| S09 | `UNAVAILABLE_CURRENT` |
| Publication | protected; excluded from Pages |

The digest was independently recomputed and matched. JSON parse and source-lineage checks are verified. Approved-schema validation, physical inventory and runtime OAT are correctly `NOT_EXECUTED`.

## 3. Reviews and CI

ARB AI-assisted: **APPROVED WITH CONDITIONS — 99/100**. Release Quality AI-assisted: **CONDITIONALLY READY FOR MERGE**. These reviews are process-separated and not equivalent to independent human approval.

Exact publication head completed 7/7 PR workflows. Merge `4e8802c80359efce28d8d75521a1b9cc4cb44b05` completed 9/9 post-merge workflows:

| Workflow | Run | Esito |
|---|---:|---|
| Developer Foundation | #1447 | SUCCESS |
| Validate documentation | #1084 | SUCCESS |
| Genera manuale Word | #1510 | SUCCESS |
| Scientific Platform Governance | #147 | SUCCESS |
| BKL-041 F4 Governance | #149 | SUCCESS |
| BKL-046 F4 governance | #123 | SUCCESS |
| BKL-046 F5 governance | #108 | SUCCESS |
| Governed Projection Sync | #60 | SUCCESS |
| Deploy MkDocs artifact to GitHub Pages | #808 | SUCCESS |

## 4. Finding disposition

- `ARB-197-MI01-A`: closed by ADR-009 for authority system, roles, evidence location and separation.
- `ARB-197-MI01-B` / `ARB-199-MI01`: open until exact-digest human approval.
- `ARB-199-MI02`: assigned to schema/validator materialization.
- `ARB-199-MI03`: assigned before S09 activation to F3-A1 site record and separately approved assignment.

No Blocker or Major remains for integration of the DRAFT.

## 5. Next mandatory gate

The Repository Owner must explicitly approve or correct `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8` and its validity. Only after that decision may the custodian create a matching approval receipt and propose a lifecycle transition. Baseline approval must not create or imply a setup assignment.

## 6. Rollback

Revert PR #199. No migration, runtime deployment, credential or observatory operation exists.
