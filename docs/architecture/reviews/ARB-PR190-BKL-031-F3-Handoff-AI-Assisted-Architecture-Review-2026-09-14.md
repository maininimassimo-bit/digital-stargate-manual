# ARB — PR #190 BKL-031 F3 Governed Site/Setup and Ephemeris/Lunar Handoff

| Field | Value |
|---|---|
| Review ID | ARB-PR190-BKL031-F3-HANDOFF-AI-001 |
| Review mode | AI-assisted, owner-authorized; not an independent human approval |
| Date | 2026-09-14 |
| Pull request | [#190](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/190) |
| Technical head reviewed | `5706924c07c3a9fb9d04897c0aaaec4257d514d0` |
| Base | `4d5526c2fa2af10aeddace4f26c33fc95b7eaa57` |
| Decision | **APPROVED WITH CONDITIONS** |
| Score | **99 / 100** |

## 1. Independence and authorization disclosure

This review was produced by an AI acting in the Architecture Review Board role after explicit repository-owner authorization limited to PR #190 at technical head `5706924c07c3a9fb9d04897c0aaaec4257d514d0`. It is **not equivalent to an independent human approval**.

The review covers only the F3 handoff and governance reconciliation. It does not authorize merge, a ruleset waiver, the F3 Solution Architecture package, provider selection, implementation or runtime activity.

## 2. Reviewed scope

- promotion of BKL-031 F3 only as the governed successor handoff after accepted/post-merge-verified F1/F2;
- S08 authoritative site/timezone, S09 current setup assignment/validity and S10 ephemeris/lunar source/method boundary;
- proposed F3-A/F3-B/F3-C sequence without authorization to execute it;
- reconciliation of bootstrap, backlog, baseline, enterprise context, handover, knowledge map, navigation and roadmap projections;
- preservation of F4 forecast, F5 ranking/consumer, BKL-032 readiness and local physical Safety Authority as separate scopes.

The technical head changes 13 documentation/navigation/governed JSON files (+221/-38), is two commits ahead and zero behind the base, and introduces no executable code, schema, fixture, validator, provider, credential, deployment or PC Principale/EAGLE change.

## 3. Architecture assessment

The handoff is consistent with the accepted F1 inventory and F2 machine-readable context. It does not fabricate current evidence: S08-S10 remain unavailable until a separately approved package establishes authority and source contracts. S07 stays unavailable/current-unknown and S11 remains deferred to F4.

The future package is correctly required to cover stable site identity, IANA timezone, UTC/time-scale semantics, frame/epoch and precision, setup validity/conflict handling, source method/version, licensing/privacy, freshness/caching, deterministic fail-closed behavior and Citation/Provenance preservation.

Dependency direction is sound: Application ports and Infrastructure adapters may be proposed without introducing Infrastructure dependencies into Domain. Non-trivial calculation and external calls remain outside EAGLE.

The boundary is advisory and read-only. Weights, scores, ranking, target ordering, readiness, scheduling, go/no-go, device commands and Safety Authority are prohibited. An ADR is correctly deferred until verified alternatives support a consequential provider/library choice.

## 4. Scoring matrix

| Dimension | Score | Evidence-based assessment |
|---|---:|---|
| Program and enterprise alignment | 100 | F3 follows the accepted dependency sequence |
| Authority and source-of-truth integrity | 100 | unavailable sources are preserved; canonical roadmap remains authority |
| Domain and semantic integrity | 100 | context, evidence, provenance and fail-closed states remain lossless |
| Scope control | 100 | F4/F5/BKL-032/runtime/commands/Safety are excluded |
| Dependency and layer integrity | 99 | direction is explicit; concrete topology is intentionally deferred |
| Safety | 100 | physical interlocks remain independent |
| Security, privacy and licensing | 98 | obligations are explicit; future provider decision remains open |
| Operability and resource placement | 100 | repository-only; non-trivial work remains off EAGLE |
| Traceability and continuity | 99 | predecessor, capability and continuity links are reconciled |
| Migration and rollback | 99 | additive documentation package; implementation migration is deferred |
| Validation evidence | 99 | seven technical-head workflows succeeded; publication head remains pending |

Conservative rounded ARB score: **99 / 100**.

## 5. Findings

| Severity | ID | Finding | Disposition |
|---|---|---|---|
| Blocker | — | None | — |
| Major | — | None | — |
| Minor | — | None | — |
| Observation | ARB-190-O01 | S08-S10 have no approved authority or source. | Preserve unavailable states until reviewed contracts are accepted. |
| Observation | ARB-190-O02 | F3 implementation artifacts are intentionally absent. | Do not treat handoff CI as implementation evidence. |
| Observation | ARB-190-O03 | Repository ruleset discovery returned an empty list. | Recheck controls; any exception requires exact-head owner authorization. |
| Observation | ARB-190-O04 | Branch-protection endpoint was inaccessible to the integration. | Record the limitation; do not infer protection. |
| Observation | ARB-190-O05 | Review mode lacks independent human approval. | Retain the disclosure. |

## 6. Conditions

1. S08-S10 remain unavailable until F3 defines owner, authority, locator, sensitivity, licensing, retention, update and failure semantics.
2. Site time uses a governed IANA timezone and explicit UTC/time-scale rules; fixed offsets cannot substitute.
3. Current setup requires stable identity, effective interval and deterministic conflict handling; historical recency cannot assert current state.
4. Ephemeris/lunar facts preserve method/version, inputs, frame/epoch, time scale, precision, issue/validity and stale-cache behavior.
5. F3 does not introduce forecast/F4, ranking/F5, readiness/BKL-032, scheduler, go/no-go, command, remediation or Safety Authority.
6. External calls and non-trivial calculation remain off EAGLE; no credential, local host or raw operational path enters public artifacts.
7. Review/navigation publication must pass all workflows on its new exact head.
8. Merge and any merge-control exception require separate owner authorization for the final exact head.
9. The F3 Solution Architecture package and implementation require separate later authorizations.

## 7. Validation evidence

Verified on technical head `5706924c07c3a9fb9d04897c0aaaec4257d514d0`:

- Developer Foundation #1395 (`34880297304`): SUCCESS;
- Validate documentation #1032 (`34880297317`): SUCCESS;
- Genera manuale Word #1458 (`34880297336`): SUCCESS;
- Scientific Platform Governance #95 (`34880297300`): SUCCESS;
- BKL-041 F4 Governance #97 (`34880297301`): SUCCESS;
- BKL-046 F4 governance #71 (`34880297318`): SUCCESS;
- BKL-046 F5 governance #56 (`34880297350`): SUCCESS;
- PR open, draft, mergeable and not merged;
- branch two commits ahead, zero behind;
- canonical roadmap and generated projections agree;
- repository rulesets: `[]`; branch-protection query: HTTP 403 to the integration.

Not executed or claimed: provider/library choice, ADR acceptance, F3 schema/fixture/validator/adapter tests, ephemeris/lunar scientific validation, runtime/OAT, independent human review, merge or post-merge verification.

## 8. ARB decision

**APPROVED WITH CONDITIONS** for integration of the BKL-031 F3 handoff. The package is coherent, dependency-ordered, fail-closed and non-implementing. This AI-assisted decision does not authorize merge, waiver, F3 design or implementation.
