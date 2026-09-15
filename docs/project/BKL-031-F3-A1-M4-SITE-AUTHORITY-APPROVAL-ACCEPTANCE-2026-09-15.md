# BKL-031 F3-A1-M4 — Site Authority Approval Acceptance

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-M4-ACCEPTANCE-001 |
| Stato | **ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED** |
| Data | 15/09/2026 |
| Pull request | #204 |
| Reviewed head | `f394ef5c3b5ad089e18fa3c4c431e2fcbd556e38` |
| Merge baseline | `e73b1aa631c41dff97b9e5ededb6d6be02a667d4` |
| Protected values | Omitted by policy |
| Runtime / EAGLE | None |

## 1. Acceptance decision

F3-A1-M4 is accepted after exact-head review, expected-head merge and post-merge verification. The protected Site Authority lifecycle is `APPROVED`; the separately committed owner receipt binds the immutable payload and governed validity. The historical DRAFT remains unchanged.

This public acceptance deliberately omits exact site facts, protected digests, internal identifiers and source locators.

## 2. Quality evidence

| Gate | Esito |
|---|---|
| Executable suite | 59/59 PASS |
| Exact-head workflows | 8/8 SUCCESS |
| ARB | APPROVED WITH CONDITIONS — 98/100 |
| Release Quality | CONDITIONALLY READY |
| Waiver | None |
| Blocker / Major | None |
| Expected-head merge | SUCCESS |
| Post-merge workflows | 10/10 SUCCESS |

The reviews are owner-authorized and AI-assisted; they are not equivalent to independent human approval. The lifecycle approval itself is the separate human owner receipt stored in the protected registry.

## 3. Capability state

- repository-level Site Authority resolution is eligible only for authorized callers within governed validity;
- public projection remains deny-by-default and contains no exact site data;
- no runtime adapter exists, therefore S08 remains `UNAVAILABLE`;
- no separately approved `CurrentSetupAssignment` exists, therefore S09 remains `UNAVAILABLE_CURRENT`;
- no provider, ephemeris computation, forecast, ranking, readiness, command or Safety Authority is introduced.

## 4. Conditions carried forward

| ID | Condition | Required before |
|---|---|---|
| `ARB-204-MI01` | Generalize receipt/schema/validator path binding beyond the first hard-coded record | second site revision or receipt |
| `ARB-204-MI02` | Define repository key, access and deployment boundaries | any runtime adapter |

The owner-attested source is authoritative for this repository record but is not an independent geodetic survey or accuracy certification.

## 5. Successor gate

The dependency-ready successor is `BKL-031-F3-A2-D3 — CurrentSetupAssignment Owner Decision`. It may collect governance decisions only. A future assignment record requires a separate DRAFT materialization, exact-digest approval and lifecycle promotion; runtime remains a later architecture package.

## 6. Rollback

Revert the PR #204 promotion commit through reviewed Git history, removing the APPROVED envelope and receipt while preserving the immutable DRAFT. Repository resolution returns fail-closed. No runtime, device or observatory rollback is required.
