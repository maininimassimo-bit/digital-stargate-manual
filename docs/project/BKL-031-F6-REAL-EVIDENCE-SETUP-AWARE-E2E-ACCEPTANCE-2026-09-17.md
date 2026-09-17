# BKL-031 F6 — Real-Evidence Setup-Aware E2E Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Capability | BKL-031 F6 |
| Projection | `BKL031_F6_REAL_EVIDENCE_SETUP_AWARE_E2E_PROJECTION` |
| Method | `BKL031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E@1.0` |
| Environment / authority | `EVALUATION` / `NONE` |
| Consumer mode | `READ_ONLY` |
| Reviewed head | `ad7cad8267eaee1e27e7b1373d34f422efd8f088` |
| Pull request | [#275](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/275) |
| Merge commit | `f75303c9575c77f23de777d55c6067bf08bc99f1` |
| Exact-head workflows | 13/13 successful |
| Post-merge workflows | 14/14 successful |
| Provider request budget | `2/2_EXHAUSTED` |
| Runtime effect | None; S10 remains `UNAVAILABLE` |
| Safety effect | None; local physical interlocks remain authoritative |

## Accepted decision

F6 is accepted as a bounded end-to-end integration proof. It demonstrates that already-reconciled real F4-C provider forecast values can flow through the planner together with governed setup authority, registered scientific-session evidence, governed target identities and the accepted F5 explainable ranking mechanics, producing a sanitized read-only portal projection.

F6 performs zero provider requests. The accepted evidence remains bound to F4-C digest `350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5`, the provider budget remains `2/2_EXHAUSTED`, and protected-site coordinates are not used for provider acquisition.

The public setup scenarios remain sanitized. Historical acquisition evidence establishes only `SUPPORTED_BY_HISTORY` / `UNVERIFIED_FOR_SELECTED_SETUP`; it is not yet an optical suitability model. F5 scores remain explicitly `SYNTHETIC_METHOD_VALIDATION_ONLY` and are not reclassified as current-night recommendations.

## Verification

The final reviewed head `ad7cad8267eaee1e27e7b1373d34f422efd8f088` completed all 13 applicable pull-request workflows successfully. The dedicated F6 governance path verified deterministic regeneration from accepted evidence, real forecast-value binding, governed setup/session evidence, privacy allowlisting, request-budget invariants, fail-closed mutations and browser syntax. Developer Foundation and documentation/manual pipelines also passed.

Architecture Review Board returned **APPROVED WITH CONDITIONS** with no Blocker or Major finding. Release Quality returned **CONDITIONALLY READY FOR MERGE** with no waiver. The retained condition was explicit: F6 is valid integration evidence but is not sufficient for BKL-031 closure while fresh runtime forecast supply, real astronomical windows and explicit OTA/camera/filter suitability remain unresolved.

PR #275 was merged with expected-head control as `f75303c9575c77f23de777d55c6067bf08bc99f1`. All 14 applicable push workflows completed successfully on that merge SHA, including F3-C/F4-C/F4-D/F5/F6 governance regressions, Developer Foundation, documentation validation, Word generation and GitHub Pages deployment.

## Retained limitations

- F4-C location is `SYNTHETIC_GENERALIZED`, not the protected observatory site;
- the accepted weather sample proves the E2E data path but is not a fresh runtime feed;
- F5 ranking geometry remains synthetic method-validation evidence;
- setup compatibility remains historical acquisition evidence, not explicit optical suitability;
- no third provider request is authorized and the current validation request budget remains `2/2_EXHAUSTED`;
- no readiness/go-no-go, scheduler, automatic target selection or device command is authorized;
- F6 is not Safety Authority;
- BKL-032 remains the separate owner of readiness/go-no-go decision support;
- S10 production runtime remains `UNAVAILABLE`.

## Transition

F6 acceptance authorizes only the separately governed **F7 fresh forecast supply and runtime boundary** package as the next dependency-ordered gate.

F7 must define and validate a refresh/runtime supply contract for current forecast series at an approved generalized/public location while preserving ADR-011 provider/model/run lineage, freshness/missingness semantics, privacy and request accounting. **F6 acceptance itself authorizes no provider request**; the current validation budget remains `2/2_EXHAUSTED`, so any new provider traffic requires a separate explicit authority/budget decision before execution.

BKL-031 remains `In Progress`. After F7, capability closure is still deferred until a later scientific integration gate replaces synthetic geometry and historical-only compatibility with current astronomical windows plus explicit OTA/camera/filter target suitability and proves the final read-only portal ranking end to end.
