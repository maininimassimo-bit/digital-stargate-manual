# Architecture Review Board — PR #193 BKL-031 F3-A1 Site Authority Contract

| Field | Value |
|---|---|
| Review ID | ARB-PR193-BKL031-F3A1-SITE-AUTHORITY-AI-001 |
| Review mode | AI-assisted, owner-authorized; not an independent human approval |
| Date | 2026-09-15 |
| Pull request | [#193](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/193) |
| Technical head reviewed | `8bc4c8ed131bce0580ff95905b130b191605e2e7` |
| Base | `21524c687a1fa6a9d840a3951c7ef4fe298f9c3c` |
| Decision | **APPROVED WITH CONDITIONS** |
| Score | **96 / 100** |

## 1. Independence and authorization disclosure

This assessment was produced by an AI acting in the Architecture Review Board role after explicit repository-owner authorization limited to PR #193 and exact head `8bc4c8ed131bce0580ff95905b130b191605e2e7`. It is not equivalent to an independent human approval.

The same AI context assisted preparation of the proposal. Independence is therefore process separation only, not human or organizational independence. The package was not repaired while under review. Publication of this report does not authorize merge, schema, fixtures, real site values, provider selection, F3-A2/A3/B/C, runtime, EAGLE activity or Safety Authority.

## 2. Verified repository truth

- PR #193 is open, draft, mergeable and not merged;
- reviewed head is two commits ahead and zero behind `main@21524c687a1fa6a9d840a3951c7ef4fe298f9c3c`;
- scope is 16 files, +634/-55;
- technical-head workflows are 7/7 SUCCESS;
- no GitHub review submissions or review threads existed at assessment time;
- repository ruleset collection is empty;
- `main` branch-protection detail is not readable by the integration (HTTP 403);
- no executable, dependency, provider, credential, real coordinate, deployment or runtime change exists.

## 3. Architecture assessment

The proposal is consistent with the accepted F3 source-neutral architecture and preserves S08 as `UNAVAILABLE`. It separates Domain value objects, an Application port and future Infrastructure responsibilities. Missingness, invalidity, gaps and overlaps fail closed; no “latest wins” rule is allowed.

The half-open rule is normative and deterministic:

- finite interval: `validFromUtc <= t && t < validToUtc`;
- unbounded interval: `validFromUtc <= t` with explicit `UNBOUNDED` mode;
- adjacent intervals `[a,b)` and `[b,c)` do not overlap;
- at `t=b` only the second interval is eligible;
- overlapping approved records return `CONFLICTED`.

The protected internal aggregate is separated from a sanitized public reference. Public IDs and digests may not be derived from internal identifiers, internal digests, exact coordinates or source locators. This is a sound design treatment of `ARB-191-MI01`, but enforcement remains a future implementation gate.

## 4. Scoring matrix

| Dimension | Score | Evidence-based assessment |
|---|---:|---|
| Program and enterprise alignment | 97 | F3-A1 is dependency-ordered and BKL-031 remains active |
| Domain and layer integrity | 96 | Domain/Application/Infrastructure responsibilities are separated |
| Contract determinism | 94 | temporal resolution is deterministic; authority identity needs clarification |
| Time and validity semantics | 99 | half-open, adjacency, gap, overlap and unbounded rules are explicit |
| Scientific/geodetic semantics | 92 | WGS84 and ranges are stated; vertical reference remains undefined |
| Security and privacy | 97 | protected aggregate and allowlisted public boundary are explicit |
| Safety | 100 | no readiness, command, remediation or Safety Authority is introduced |
| Observability and operability | 95 | future metrics and redaction rules are bounded and non-sensitive |
| Migration and rollback | 96 | future sequence and documentation-only rollback are explicit |
| Traceability and evidence | 94 | exact SHA and 7/7 CI are verified; implementation tests are intentionally not executed |

Conservative rounded ARB score: **96 / 100**.

## 5. Findings

### Blocker

None.

### Major

None.

### Minor

#### ARB-193-MI01 — Vertical coordinate semantics are incomplete

`elevationM` is finite and WGS84 is named, but the contract does not state whether elevation is ellipsoidal height, orthometric height, or another vertical reference. Its operational range is also deferred. This ambiguity can alter future topocentric calculations.

Required disposition before F3-B materialization:

1. define unit and vertical reference explicitly;
2. define accepted range and normalization/rejection behavior;
3. add positive and negative executable cases for the selected semantics.

#### ARB-193-MI02 — Resolver identity and authority scope need one canonical rule

The resolution narrative names `observatoryId`, while `SiteAuthorityPort` receives `observatoryRef`; overlap is described for the “same authority”, but no canonical authority identity/scope is defined. The design remains safe because no implementation exists, but future candidate selection must not rely on an implicit mapping.

Required disposition before F3-B materialization:

1. define the canonical protected identity used for lookup;
2. define how an external/opaque reference maps to it under authorization;
3. define the authority/tenant scope used to build the candidate set;
4. add cross-authority and ambiguous-reference negative tests.

### Observations

- ARB-193-O01 — `timezoneIana` is correctly excluded from validity calculations; future reproducibility evidence should record the tzdb version used for display conversion.
- ARB-193-O02 — The public digest boundary is sound, but algorithm and canonicalization remain intentionally open for F3-B.
- ARB-193-O03 — F3-A1 validation cases are specifications, not executed evidence.
- ARB-193-O04 — The review-publication head requires fresh CI before merge consideration.
- ARB-193-O05 — Independent human review was not executed.

## 6. Prior-condition disposition

| Condition | Disposition on reviewed head |
|---|---|
| `ARB-191-MI02` | **SATISFIED AT NORMATIVE DESIGN LEVEL / EXECUTABLE GATE OPEN** — half-open, unbounded and adjacency rules are defined; executable tests remain mandatory before materialization |
| `ARB-191-MI01` | **PARTIALLY ADDRESSED / OPEN** — internal/public separation is defined; enforcement and leak tests remain mandatory before F3-B/F3-C |

No unexecuted validation is approved as passed.

## 7. Validation evidence

| Workflow | Run | Result |
|---|---:|---|
| Developer Foundation #1415 | 34946243499 | SUCCESS |
| Validate documentation #1052 | 34946243567 | SUCCESS |
| Genera manuale Word #1478 | 34946243496 | SUCCESS |
| Scientific Platform Governance #115 | 34946243342 | SUCCESS |
| BKL-041 F4 Governance #117 | 34946243481 | SUCCESS |
| BKL-046 F4 governance #91 | 34946243351 | SUCCESS |
| BKL-046 F5 governance #76 | 34946243522 | SUCCESS |

Not executed or claimed: F3-A1 executable contract tests, privacy leak tests, schema/fixture validation, runtime/OAT, scientific accuracy campaign, real site approval, PC/EAGLE activity, independent human review, merge or post-merge publication.

## 8. Decision and conditions

**APPROVED WITH CONDITIONS — 96/100.**

The documentation-only contract may proceed to merge consideration after:

1. publication of this report and the paired Release Quality report;
2. successful exact-head CI on the review-publication head;
3. separate owner authorization for merge and ruleset treatment.

`ARB-193-MI01` and `ARB-193-MI02` do not block integration of the documentation-only contract, but they are mandatory gates before F3-B materialization. `ARB-191-MI01` remains open for executable enforcement. No implementation or runtime readiness is asserted.

