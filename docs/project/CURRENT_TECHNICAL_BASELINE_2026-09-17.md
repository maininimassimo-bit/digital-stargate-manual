# Digital StarGate — Current Technical Baseline 17/09/2026

| Campo | Valore |
|---|---|
| Stato | Current governed baseline |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Baseline implementation merge | `20669f7164460297d7318fc3b5874e4bc7f4bcde` |
| Acceptance reconciliation merge | `84d1b889a6c739c9e5d053e1f073fe1d87b8c5d4` |
| Current package | BKL-032 |
| Current next gate | BKL-032 Session Readiness / Go-No-Go Decision Support |

## Observation Planner baseline

F3–F9 sono Accepted/Post-Merge Verified. F9 chiude la pipeline repeatable: forecast MeteoHub corrente di Manciano, geometria astronomica della notte, suitability esplicita setup-target e ranking/finestre advisory nel portale. Il metodo resta `EVALUATION/NONE/READ_ONLY` e non è un readiness/safety engine.

## Authority baseline

- Site Authority: protected GitHub-governed record; coordinate esatte non pubblicabili.
- Setup Authority: approved GitHub-governed assignment/baseline.
- Ephemeris/lunar method: ADR-010 accepted repository authority.
- Forecast source/run lineage: ADR-011 accepted repository authority.
- Session Readiness / Go-No-Go: BKL-032, non BKL-031.
- Safety Authority: local physical interlocks.
- S10 production runtime: `UNAVAILABLE`.

## Provider/request baseline

- F4-C generalized validation budget: `2/2_EXHAUSTED`.
- F7 protected-site one-shot budget: `1/1_EXHAUSTED`.
- F8 provider requests: 0.
- Recurring provider traffic: **NOT AUTHORIZED** by F8 acceptance; requires separate authority/budget/service decision.

## F8 verified implementation

PR #279 exact reviewed head `3f05693482208df2b56b66dcb71162589880e72b`: 9/9 PR workflows SUCCESS; ARB APPROVED WITH CONDITIONS with no Blocker/Major and no waiver; Release Quality CONDITIONALLY READY with no waiver. Expected-head merge `20669f7164460297d7318fc3b5874e4bc7f4bcde`: 10/10 applicable push workflows SUCCESS.

## F8 acceptance reconciliation verification

PR #280 exact reviewed head `bca410dcde804483052beded16c29a9f58f43872`: 17/17 PR workflows SUCCESS after closure of the Knowledge Map continuity finding; ARB re-review APPROVED WITH CONDITIONS; Release Quality READY FOR MERGE. Expected-head merge `84d1b889a6c739c9e5d053e1f073fe1d87b8c5d4`: **19/19 applicable push workflows SUCCESS**. The GitHub Pages workflow completed build, published-site integrity, artifact upload and deployment successfully. A separate external HTTP/browser validation could not be completed from the available web environment and is therefore not claimed.

## Open closure gap

BKL-031 is not closed. F9 must prove repeatable/current-night operation of the complete advisory chain — governed fresh forecast, current astronomy, explicit setup suitability, explainable target ordering and best windows — while preserving privacy, fail-closed freshness/missingness and all authority separations.
