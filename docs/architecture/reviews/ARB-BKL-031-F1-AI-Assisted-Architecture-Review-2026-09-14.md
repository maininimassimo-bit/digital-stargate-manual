# ARB — BKL-031 F1 Source Discovery and Semantic Boundary

| Field | Value |
|---|---|
| Review ID | ARB-BKL031-F1-AI-001 |
| Review mode | AI-assisted, owner-authorized; not an independent human approval |
| Date | 2026-09-14 |
| Pull request | #183 |
| Technical head reviewed | `55b502fb4e47ef92975767ceb444078cae36caf8` |
| Base | `c1440172a0565a99647ed5d6df0cb1a8adb1c8b1` |
| Decision | **APPROVED WITH CONDITIONS** |
| Score | **99 / 100** |

## 1. Independence and authorization disclosure

This review was produced by an AI acting in the Architecture Review Board role after explicit repository-owner authorization limited to PR #183 at technical head `55b502fb4e47ef92975767ceb444078cae36caf8`.

It is AI-assisted and is **not equivalent to an independent human approval**. It does not authorize merge, implementation, provider selection, ranking or any runtime change.

## 2. Reviewed scope

- BKL-031 F1 source-discovery and semantic-boundary contract;
- F1 validation plan;
- program-handoff traceability update;
- Governance Center, Validation Center and MkDocs navigation updates;
- exact-head workflow evidence associated with the technical head.

The changed set contains six documentation/navigation files. No schema, code, generated projection, workflow or runtime file is changed.

## 3. Repository alignment

The proposal is consistent with:

- the BKL-031 program handoff and current roadmap boundary;
- BKL-015 knowledge traceability and BKL-035 target identity/lineage;
- AP-013/AP-014 scientific asset, session and catalog authority;
- BKL-029 SQM semantics;
- the separation of BKL-031 planning advice from BKL-032 readiness;
- the independent local physical Safety Authority.

The source inventory correctly distinguishes governed projections from architecture authorities and explicitly classifies missing current site/setup, ephemeris/lunar and forecast sources as unavailable.

## 4. Scoring matrix

| Dimension | Score | Evidence-based assessment |
|---|---:|---|
| Program and enterprise alignment | 100 | exact match with the F1-only handoff; no capability expansion |
| Source authority and ownership | 97 | exact locators and fact-class precedence are defined; custodians for future/unavailable sources remain a later decision |
| Domain and semantic integrity | 100 | candidate, context, evidence dimension, factor and explanation are separated without hidden score |
| Layer and dependency integrity | 99 | future adapters and computation remain outside presentation/EAGLE; implementation topology is intentionally deferred |
| Safety | 100 | no readiness, command, interlock or Safety Authority coupling |
| Security and privacy | 98 | data minimization, secret handling and raw-locator controls are explicit; future provider terms remain unresolved |
| Freshness, missingness and conflict | 100 | historical/current/forecast separation is fail-closed and conflict-preserving |
| Operability and resource placement | 99 | heavy work is excluded from EAGLE; operational behavior is correctly not claimed in F1 |
| Traceability and documentation | 99 | program handoff, project index, validation index and MkDocs are linked; publication-head evidence remains required |
| Migration and rollback | 99 | documentation-only additive change; repository revert is sufficient |
| Validation evidence | 98 | 20 negative cases are specified and exact-head documentation CI is green; no implementation tests are applicable |

Rounded ARB score: **99 / 100**.

## 5. Findings

| Severity | ID | Finding | Disposition |
|---|---|---|---|
| Blocker | — | None | — |
| Major | — | None | — |
| Minor | — | None | — |
| Observation | ARB-183-O01 | The accepted BKL-035 consumer is bounded to two reconciled targets and the inspected session catalog to 16 sessions; this is not representative evidence for a general planner. | Preserve the bound and do not claim broad target coverage. |
| Observation | ARB-183-O02 | No governed current site record, active-setup validity source, ephemeris/lunar source or forecast source exists on the reviewed baseline. | Keep BKL031-S08–S11 unavailable until separately governed. |
| Observation | ARB-183-O03 | Some source ownership is expressed by capability/component rather than a durable source-custodian record. | Materialize accountable ownership before the corresponding source is implemented. |
| Observation | ARB-183-O04 | Developer Foundation did not trigger because this documentation-only path set is outside its configured filters. | `NOT_TRIGGERED / NOT_APPLICABLE`; the documentation workflow is the applicable build gate. |

## 6. Conditions

1. F2 fixtures must encode BKL031-S07–S11 as unavailable/unknown on this baseline and must not simulate site, active setup, ephemeris, lunar or forecast evidence.
2. Any future site/setup/provider integration requires a separately reviewed source contract covering owner, authority, locator, licensing, precision, privacy, validity/freshness and failure behavior.
3. F2 must not contain numeric weights, score contributions, thresholds, normalization curves, target ordering or readiness semantics.
4. Citation, Provenance, identity conflicts and source-authority classes inherited from BKL-035/AP-014/BKL-029 must remain lossless.
5. Review publication must pass the applicable exact-head workflows before merge is considered.
6. Merge and any transition to F2 require separate repository-owner authorization.

These conditions do not require modification of the reviewed technical package before review publication; they constrain integration and the next increment.

## 7. Safety and security decision

The architecture remains read-only and advisory. It cannot declare the observatory safe/ready, edit a N.I.N.A. sequence, schedule automatically or command dome, mount, camera, power, network or interlocks. The local physical Safety Authority remains independent.

No credential, provider endpoint, external data transfer or heavy EAGLE workload is introduced.

## 8. Validation evidence

Verified on technical head `55b502fb4e47ef92975767ceb444078cae36caf8`:

- Validate documentation (no deploy) run `34819316309`: SUCCESS;
- Genera manuale Word run `34819316244`: SUCCESS;
- BKL-041 F4 Governance run `34819316381`: SUCCESS;
- BKL-046 F4 governance run `34819316255`: SUCCESS;
- BKL-046 F5 governance run `34819316294`: SUCCESS;
- PR mergeability: true;
- changed-file scope: six documentation/navigation files;
- Developer Foundation: `NOT_TRIGGERED / NOT_APPLICABLE` according to its path filters.

Not executed or claimed:

- provider/API validation;
- ephemeris, lunar, forecast or ranking calculation;
- runtime, PC Principale or EAGLE validation;
- human-independent ARB approval;
- merge or post-merge verification.

## 9. ARB decision

**APPROVED WITH CONDITIONS** for F1 documentation integration. The semantic boundary is coherent, fail-closed and aligned with the program decision. This AI-assisted decision is not an independent human approval and does not itself authorize merge or F2 implementation.
