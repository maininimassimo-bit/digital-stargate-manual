# ARB — PR #191 BKL-031 F3 Solution Architecture

| Field | Value |
|---|---|
| Review ID | ARB-PR191-BKL031-F3-SA-AI-001 |
| Review mode | AI-assisted, owner-authorized; not an independent human approval |
| Date | 2026-09-14 |
| Pull request | [#191](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/191) |
| Technical head reviewed | `43a46ac28c30badc40e4cb180ed98924ebcf74a1` |
| Base | `2ffc77917bcd3fc25a3c5657e8f12e62c9284303` |
| Decision | **APPROVED WITH CONDITIONS** |
| Score | **98 / 100** |

## 1. Independence and authorization disclosure

This review was produced by an AI acting in the Architecture Review Board role after explicit repository-owner authorization scoped to PR #191 at technical head `43a46ac28c30badc40e4cb180ed98924ebcf74a1`. It is **not equivalent to an independent human approval**.

The reviewer assessed the proposal without modifying the architecture or validation documents. Publication of this review does not authorize merge, a ruleset waiver, ADR acceptance, provider/library selection, authority records, implementation or runtime activity.

## 2. Reviewed scope and repository truth

The reviewed increment defines the source-neutral F3 design for:

- S08 governed site identity, geodetic position and IANA timezone;
- S09 current setup assignment with approval, validity and conflict semantics;
- S10 ephemeris/lunar request, method and evidence contracts;
- Application ports, Infrastructure adapters/cache, validation and sanitized projection boundaries;
- UTC/time-scale, coordinate frame/epoch/datum/refraction, privacy, licensing and precision gates;
- migration slices F3-A1/A2/A3/B/C and validation cases P01–P10/N21–N66.

Verified state:

- PR open, draft, mergeable and not merged;
- branch two commits ahead and zero behind base;
- 14 changed files, +823/-58, limited to documentation/navigation/governed JSON;
- no schema, fixture, validator, adapter, dependency, external call, deployment or PC/EAGLE change;
- seven exact-head workflows succeeded;
- no existing PR review submissions or review threads;
- repository ruleset collection is empty;
- branch-protection endpoint is inaccessible to the integration with HTTP 403.

## 3. Architecture assessment

The package is consistent with accepted BKL-031 F1/F2 and does not fabricate S08–S10 authority. It preserves F2 availability states, Citation/Provenance and prohibited ranking/readiness/command semantics.

Dependency direction is correct: Domain remains framework-independent; Application owns orchestration and ports; Infrastructure owns storage/provider/cache adapters; Presentation receives only a sanitized read-only projection. Provider selection is correctly deferred to an ADR and scientific validation campaign.

Time, coordinate and scientific semantics are unusually thorough for a pre-implementation package. Facts cannot become `AVAILABLE` before method/data identity, numeric error budget and independent validation are accepted. Network failures, coverage gaps, conflicts and cache mismatch fail closed.

The design preserves the observatory boundary: external calls and non-trivial calculations remain off EAGLE; BKL-032 and local physical interlocks retain separate readiness and Safety authority.

Two non-blocking ambiguities require binding remediation before implementation: a public reference must not expose or enable correlation against the digest of a protected site record, and validity intervals require one canonical endpoint rule.

## 4. Scoring matrix

| Dimension | Score | Evidence-based assessment |
|---|---:|---|
| Program and enterprise alignment | 100 | exact F3 position and predecessor/successor boundaries |
| Authority and source integrity | 99 | no historical or conceptual source is promoted to current authority |
| Domain, time and semantic integrity | 97 | strong normalized contracts; interval endpoint semantics need closure |
| Layer and dependency integrity | 100 | source-neutral ports/adapters and off-EAGLE boundary |
| Safety | 100 | readiness, commands and Safety Authority remain separate |
| Security, privacy and licensing | 94 | exact coordinates are protected; public/internal digest separation is underspecified |
| Operability and resource placement | 99 | topology and budgets appropriately deferred |
| Traceability and continuity | 99 | F1/F2, handoff, roadmap, navigation and validation links reconcile |
| Migration and rollback | 98 | additive slices and fail-closed restoration are explicit |
| Validation evidence | 98 | design plan is complete and technical-head CI is 7/7; runtime/scientific tests correctly remain unexecuted |

Conservative rounded ARB score: **98 / 100**.

## 5. Findings

| Severity | ID | Finding | Required disposition |
|---|---|---|---|
| Blocker | — | None | — |
| Major | — | None | — |
| Minor | ARB-191-MI01 | The design permits a public site revision/digest while exact coordinates and the source record are protected. It does not state whether that value is an opaque public reference, a keyed commitment or the raw content digest of the protected record. A raw deterministic digest can create correlation or low-entropy enumeration risk. | Before F3-B/F3-C, define separate internal `recordDigest` and public `siteEvidenceRef` semantics. Public output must not expose a directly testable digest over protected fields; add negative privacy/correlation tests. |
| Minor | ARB-191-MI02 | `validFromUtc`/`validToUtc` are required but endpoint inclusivity and adjacency are not normative. Boundary instants could produce zero or two current records across implementations. | Before F3-A1/F3-A2 or schema work, define UTC half-open intervals `[validFromUtc, validToUtc)`, explicit unbounded-end representation and boundary/adjacency tests. |
| Observation | ARB-191-O01 | Provider, library, kernel, error budget, EOP and host decisions remain open. | Close through the planned ADR and evidence campaign; do not infer selection from the alternatives table. |
| Observation | ARB-191-O02 | `moonPhaseAngleDeg` uses a declared 0=new/180=full cycle convention. | Preserve a single unambiguous name, direction and wrap convention in the future ADR/schema and adapter tests. |
| Observation | ARB-191-O03 | `main` has no visible repository ruleset and branch protection cannot be verified by the integration. | Recheck before merge; any exception needs an exact-head owner decision. |
| Observation | ARB-191-O04 | Review mode lacks independent human approval. | Retain the disclosure in every acceptance claim. |

## 6. Conditions

1. Transfer ARB-191-MI01 and ARB-191-MI02 as mandatory preconditions to every applicable F3 implementation slice.
2. No S08/S09/S10 fact becomes production `AVAILABLE` before approved authority records, an accepted ADR/error budget and executed validation evidence exist.
3. Provider/library/kernel, licensing, privacy, EOP/leap-second, cache and host decisions remain open until separately accepted.
4. F4 forecast, F5 ranking/consumer, BKL-032 readiness, scheduler, go/no-go, commands and Safety Authority remain out of F3.
5. External calls and non-trivial calculation remain off EAGLE; exact coordinates and protected locators remain outside browser/public artifacts.
6. Review-publication navigation and continuity changes must pass every applicable workflow on their new exact head.
7. Merge and any merge-control exception require separate repository-owner authorization scoped to the final exact head.

## 7. Validation evidence

Verified on technical head `43a46ac28c30badc40e4cb180ed98924ebcf74a1`:

| Workflow | Run | Result |
|---|---:|---|
| Developer Foundation #1398 | 34884610517 | SUCCESS |
| Validate documentation #1035 | 34884610453 | SUCCESS |
| Genera manuale Word #1461 | 34884610210 | SUCCESS |
| Scientific Platform Governance #98 | 34884610226 | SUCCESS |
| BKL-041 F4 Governance #100 | 34884610442 | SUCCESS |
| BKL-046 F4 governance #74 | 34884610400 | SUCCESS |
| BKL-046 F5 governance #59 | 34884610372 | SUCCESS |

Also verified: PR state and branch relation, changed-file scope, F2 predecessor contract, source inventory, generated/canonical roadmap agreement, no PR reviews/threads, empty ruleset collection and branch-protection HTTP 403 limitation.

Not executed or claimed: real site/setup verification, provider/library selection, ADR acceptance, schema/fixture/validator/adapter tests, scientific accuracy campaign, privacy runtime tests, dependency/security scan, runtime/OAT, independent human review, merge or post-merge verification.

## 8. Decision

**APPROVED WITH CONDITIONS** for integration of the F3 Solution Architecture documentation after successful review-publication exact-head CI and separate owner merge-control authorization.

This decision accepts the architecture direction, not an implementation or production capability. ARB-191-MI01 and ARB-191-MI02 remain binding before their applicable implementation slices.
