# BKL-031 F5 — Explainable Ranking Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Capability | BKL-031 F5 |
| Method | `BKL031-F5-EXPLAINABLE-RANKING@1.0` |
| Environment / authority | `EVALUATION` / `NONE` |
| Consumer mode | `READ_ONLY` |
| Reviewed head | `dfda963e7e9d088282516200a6bd8bb64dd0dd1d` |
| Pull request | [#273](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/273) |
| Merge commit | `777924e2638430f15bf717fa33dd71057751625a` |
| Exact-head workflows | 6/6 successful |
| Post-merge workflows | 7/7 successful |
| Provider request budget | `2/2_EXHAUSTED` |
| Runtime effect | None; S10 remains `UNAVAILABLE` |
| Safety effect | None; local physical interlocks remain authoritative |

## Accepted decision

F5 is accepted as a bounded deterministic method-validation capability. It provides a versioned four-factor ranking function, a synthetic EVALUATION fixture over governed target identities, a known-answer read-only projection and a fail-closed browser consumer.

The accepted known-answer values are `76.3889` for LDN 1320 and `53.0556` for M 27. These are synthetic method-validation outputs only. They are not evidence that either target is currently observable, preferable, ready, safe or schedulable.

## Verification

The final reviewed head `dfda963e7e9d088282516200a6bd8bb64dd0dd1d` completed all six applicable exact-head workflows successfully. The dedicated F5 workflow verified deterministic regeneration, predecessor F3-C/F4-D boundaries, ten negative/sensitivity cases and browser syntax. Developer Foundation, strict MkDocs/artifact validation and Word generation also passed.

Architecture Review Board returned **APPROVED WITH CONDITIONS** with no Blocker or Major finding. Release Quality returned **CONDITIONALLY READY FOR MERGE** with no waiver. The conditions were expected-head merge, complete post-merge verification and formal acceptance reconciliation before F6.

PR #273 was merged with expected-head control as `777924e2638430f15bf717fa33dd71057751625a`. All seven applicable push workflows completed successfully on that merge SHA, including F5 Governance, F3-C regression, F4-D regression, Developer Foundation, documentation validation, Word generation and GitHub Pages deployment.

## Retained limitations

- factor values in the F5 bounded fixture are synthetic;
- F4-D publishes no forecast value arrays;
- no third provider request is permitted and the request budget remains `2/2_EXHAUSTED`;
- no protected-site provider acquisition is authorized;
- no readiness/go-no-go, scheduler, automatic target selection or device command is authorized;
- F5 is not Safety Authority;
- BKL-032 remains the separate owner of readiness/go-no-go decision support;
- S10 production runtime remains `UNAVAILABLE`.

## Transition

F5 acceptance authorizes only the separately governed **F6 capability closure** package. F6 must reconcile F1–F5, close BKL-031 and preserve all retained limitations. It may not add new planning/runtime behavior.
