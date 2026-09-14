# ARB — PR #188 BKL-031 F2 Remediation Re-Review

| Field | Value |
|---|---|
| Review ID | ARB-PR188-BKL031-F2-AI-002 |
| Review mode | AI-assisted, owner-authorized; not an independent human approval |
| Date | 2026-09-14 |
| Pull request | #188 |
| Exact remediation head reviewed | `d21d57905b2669ccd572563449a523c1795bdcc2` |
| Base | `f6c4b253a56406c930f009af0658b46a12bc088a` |
| Previous ARB decision | Rework Required — 90/100 |
| Decision | **REWORK REQUIRED** |
| Score | **97 / 100** |

## 1. Independence and authorization disclosure

This re-review was produced by an AI acting in the Architecture Review Board role after explicit repository-owner authorization for the remediation exact head `d21d57905b2669ccd572563449a523c1795bdcc2`.

It is AI-assisted and is **not equivalent to an independent human approval**. It does not authorize repair, merge, waiver, BKL-031 F3, providers, ranking or runtime activity. The reviewer did not modify the proposal while assessing it.

## 2. Reviewed scope and repository truth

The re-review examined the five-file remediation delta and the complete F2 package:

- normative validator, test suite and JSON Schema;
- bounded M 27 fixture and repository sources S01–S11;
- architecture and validation evidence;
- the previous ARB M-01–M-04 criteria;
- exact-head workflow results and PR governance state.

Verified repository state:

- `main`: `f6c4b253a56406c930f009af0658b46a12bc088a`;
- PR #188: open, draft, mergeable, not merged;
- remediation head: five commits ahead / zero behind, 15 changed files;
- repository rulesets: none;
- exact-head workflows: 7/7 SUCCESS;
- Developer Foundation: normative fixture PASS and Node suite 36/36 PASS.

## 3. Previous-finding disposition

| Previous finding | Disposition | Evidence |
|---|---|---|
| M-01 validator totality | **Closed** | type-safe traversal, stage guards, four structural regressions and a 250-case malformed-JSON probe with zero throws |
| M-02 exact Citation/Provenance binding | **Closed with one M-04 exception** | source-field comparisons and exact input/output/Citation-set checks reject the reviewed SQM, identity, session and output-ref mutations |
| M-03 semantic smuggling | **Closed** | per-dimension vocabulary, unit/source/kind restrictions and prohibited semantic/value scan; dedicated regressions pass |
| M-04 coordinate authority/conflict | **Partially closed** | S02 ranges, triplet, value match and conflicts are enforced; the S04 path remains unsound |

The remediation materially improves the contract. The remaining decision blocker is narrower than the original M-04 but is executable and source-authority relevant.

## 4. Scoring matrix

| Dimension | Score | Evidence-based assessment |
|---|---:|---|
| Program and enterprise alignment | 100 | F2 scope and BKL-031/BKL-032 separation remain intact |
| Source authority and ownership | 91 | S02 binding is governed; S04 can still attest fields absent from the cited artifact |
| Domain and semantic integrity | 98 | closed fact vocabulary and operational-semantic rejection are effective |
| Layer and dependency integrity | 100 | repository/CI only; no runtime or EAGLE dependency |
| Safety | 100 | no command, readiness or Safety Authority path |
| Security and privacy | 96 | locator controls remain strong; direct S04 treatment must respect its S03-only registry rule |
| Freshness, missingness and conflict | 96 | state handling is strong; S04 coordinate authority remains incomplete |
| Contract integrity and fail-closed behavior | 90 | arbitrary malformed JSON is total, but one unsupported S04 fact path fails open |
| Traceability and documentation | 98 | review, validation and architecture records are coherent |
| Migration and rollback | 100 | additive repository change; revert-only rollback |
| Validation evidence | 96 | 36/36 and 7/7 are verified; the independent S04 probe exposes a missing regression |

Rounded ARB score: **97 / 100**.

## 5. Findings

### Blocker

None.

### Major

**M-R1 — Coordinate facts can cite S04 even though the cited S04 artifact contains no coordinate fields.**

The remediation allows `TARGET_RA_DEG`, `TARGET_DEC_DEG` and `COORDINATE_EPOCH` to use either S02 or S04. For S04, Citation resolution verifies only that the path equals a catalogued `sourceMetricsPath` and that the session identifier exists. Coordinate values are then compared against S02 metadata, not against the cited S04 artifact.

Repository evidence for session `2026-08-14_2026-08-15` shows that the cited S04 file `normalized/session-metrics.json` contains operational aggregate sections but no `ra_deg`, `dec_deg` or `coordinate_epoch` fields. The S04 registry also states `RESOLVE_ONLY_THROUGH_BKL031_S03`, while the accepted coordinate Provenance probe can reference S04 directly.

An independently constructed, internally consistent payload declared all three coordinate facts as S04, cited that normalized file and used S02 coordinate values. The validator returned **zero errors**.

Impact:

- Provenance can claim a source that does not contain the published fact;
- exact fact-to-source-field binding is bypassed for the S04 branch;
- the residual path violates the intended M-02 and M-04 closure criteria.

Required disposition:

1. for the bounded F2 baseline, remove S04 from coordinate fact source classes and reject direct S04 coordinate Citations; or
2. materialize governed RA/Dec/epoch fields in S04, load and compare those exact fields, require the registered S03 resolution chain and reconcile any S02/S04 disagreement as `CONFLICTED`;
3. add a regression proving that the current S04 artifact cannot substantiate coordinate facts;
4. rerun the complete suite and exact-head workflows.

### Minor

None.

### Observations

- O-01 — M-01 totality is substantiated by deterministic structural regressions and exploratory mutation coverage.
- O-02 — M-03 is closed without introducing ranking, readiness or Safety authority.
- O-03 — The published fixture remains bounded and exposes no S02/S04 coordinate fact.
- O-04 — The S02 positive, wrong-source, range, mismatch and conflict regressions all pass.
- O-05 — No `main` ruleset exists; this re-review grants no merge-control waiver.

## 6. Executed validation evidence

Exact-head GitHub Actions on `d21d57905b2669ccd572563449a523c1795bdcc2`:

- Developer Foundation #1387 — SUCCESS;
- Validate documentation #1024 — SUCCESS;
- Genera manuale Word #1450 — SUCCESS;
- Scientific Platform Governance #87 — SUCCESS;
- BKL-041 F4 Governance #89 — SUCCESS;
- BKL-046 F4 governance #63 — SUCCESS;
- BKL-046 F5 governance #48 — SUCCESS.

Developer Foundation logs verify:

- F2 normative fixture: PASS;
- Node suite: 36 tests, 36 pass, 0 fail;
- remediation cases M-01 through M-04: PASS as currently encoded.

Independent review probes:

- 250 malformed JSON variants: non-empty deterministic errors, zero throws;
- original mismatched SQM, identity, session, Provenance-output and readiness mutations: rejected;
- exact S02 coordinate triplet: accepted;
- wrong source, range, S02 mismatch and S02 conflict cases: rejected;
- S04 coordinate claim against an artifact with no coordinate fields: **accepted with zero errors**.

Not executed or claimed:

- provider/API, ephemeris, lunar or forecast validation;
- ranking effectiveness or target ordering;
- portal consumer or PC Principale/EAGLE runtime OAT;
- independent human review;
- repair, merge or post-merge validation.

## 7. Re-review criteria

A further exact-head ARB review is required after M-R1 is resolved without expanding F2 scope. The minimum bounded correction is to reject S04 as a coordinate fact source until an explicit coordinate-bearing normalized projection exists. The new exact head must retain 36/36 coverage, add the S04-negative regression and produce green applicable workflows.

## 8. Decision

**REWORK REQUIRED.** PR #188 must not merge at exact remediation head `d21d57905b2669ccd572563449a523c1795bdcc2`.

M-01 and M-03 are closed, M-02 is closed for the currently source-backed fixture facts, and most of M-04 is closed. The remaining S04 source-attestation bypass is a Major contract-integrity finding. Its repair requires separate owner authorization.
