# BKL-031 F4-D — Sanitized Forecast Projection and Portal

| Field | Value |
|---|---|
| Identifier | `BKL-031-F4-D-PROJECTION-001` |
| Status | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Predecessor | F4-C reconciliation merged in PR #270; post-merge workflows verified |
| Source evidence | `BKL031-F4C-EVIDENCE-35214129960` |
| Environment / authority | `EVALUATION` / `NONE` |
| Pull request | #271 |
| Exact reviewed head | `f6aa9c5dffbc172d554872f9072029f56d1195ec` |
| Merge commit | `8f948ba9593dc2bfde291d2658fe92eafd4cce28` |
| Post-merge verification | 7/7 applicable push workflows successful |
| Runtime effect | None; S10 remains `UNAVAILABLE` |
| Safety effect | None |

## Scope

F4-D materializes a public, sanitized, read-only forecast projection from the already reconciled F4-C repository evidence. It performs no provider request and does not reconstruct, refresh, interpolate, rank or otherwise reinterpret the source series. The source request budget is exhausted and no third provider request is authorized.

The projection is deliberately metadata-only. It exposes the exact model identity, exact model run, validity envelope, supported-variable availability, the one excluded instant, the zero-imputation result and required attribution. It does not expose the generalized coordinates or forecast value arrays even though the F4-A contract permits normalized public values. This narrower publication choice reduces accidental operational interpretation while still proving end-to-end forecast lineage and portal integration.

## Repository truth carried forward

F4-C source evidence records:

- workflow run `35214129960`;
- exact model `italia_meteo_arpae_icon_2i` delivered through `OPEN_METEO_SINGLE_RUNS`;
- run initialization `2026-09-17T00:00:00Z`;
- 72 raw hourly instants, 71 complete accepted instants and one excluded instant;
- excluded instant `2026-09-17T00:00:00Z` because `precipitation` is missing;
- `DROP_INCOMPLETE_INSTANT_NO_IMPUTATION` with zero imputed values;
- validity `[2026-09-17T01:00:00Z, 2026-09-20T00:00:00Z)`;
- `visibility` unavailable for the selected ICON-2I source;
- evidence digest `350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5`;
- further provider requests unauthorized.

## Governed artifacts

| Artifact | Purpose |
|---|---|
| `schemas/observation-planner-forecast-projection-f4d.schema.json` | closed public projection schema |
| `docs/data/observation-planner-forecast-f4d-projection.json` | sanitized projection derived only from F4-C evidence |
| `.github/scripts/verify-observation-planner-forecast-f4d.mjs` | deterministic lineage/privacy/authority verifier |
| `.github/workflows/bkl-031-f4-d-governance.yml` | exact-head and post-merge F4-D governance gate |
| `docs/javascripts/observation-planner.js` | fail-closed read-only browser consumer |
| `docs/observation-planner/index.md` | public Observation Planner integration |

## Public contract

The projection publishes only:

1. projection identity and `EVALUATION/NONE/READ_ONLY` authority state;
2. source evidence identity, workflow run and evidence digest;
3. raw/accepted/excluded/imputed counts;
4. provider/upstream/model/delivery interface and exact run initialization;
5. half-open validity and hourly cadence;
6. the ten supported variables with units and `AVAILABLE` state;
7. `visibility` explicitly as `UNAVAILABLE` with no unit or fallback;
8. the one excluded instant and missing `precipitation` reason;
9. normalization policy, attribution, citations and explicit limitations.

It does not publish forecast value arrays in F4-D.

## Privacy and authority boundary

The verifier and browser consumer reject publication of:

- latitude, longitude, elevation or returned-grid coordinates;
- raw response digest, artifact identifiers, request/site references or raw locators;
- forecast instant arrays or forecast value series;
- score, rank, ranking, readiness, go/no-go, safety state or scheduler output;
- commands, device commands or Safety Authority.

No network path is introduced. The browser fetches repository-local static projections only. No last-known-good, alternate model, observation substitution or provider refresh is allowed.

## Portal behavior

The Observation Planner retains the accepted F3-C astronomical projection as an independent read-only panel and adds a separate F4-D forecast panel. Separation is intentional: astronomical evidence and forecast evidence keep independent lineage and fail-closed behavior.

The F4-D panel shows model, run, validity, evidence run identity, `71/72` completeness, zero imputations, the excluded instant, `visibility=UNAVAILABLE`, attribution and authority boundary. It labels the data as evaluation context and explicitly states that it is not a planning decision.

## Validation and acceptance evidence

F4-D passed its deterministic verifier against the exact reconciled F4-C source evidence and the governance workflow re-ran the F4-C gate/reconciliation before F4-D verification. The accepted implementation head `f6aa9c5dffbc172d554872f9072029f56d1195ec` completed the applicable exact-head repository workflows successfully before expected-head merge.

PR #271 merged the exact reviewed head into `main` as `8f948ba9593dc2bfde291d2658fe92eafd4cce28`. All seven applicable push workflows completed successfully on the merge commit, including F4-D governance, F4-C reconciliation, F3-C regression protection, Developer Foundation, documentation validation, Word generation and GitHub Pages deployment. No provider call was introduced by implementation, review, merge or post-merge verification.

F4-D is therefore **Accepted / Post-Merge Verified** as a repository-local, metadata-only, read-only forecast projection and portal consumer. This acceptance does not authorize production runtime activation, protected-site acquisition, forecast value publication, ranking, readiness, scheduling, command execution or Safety Authority.

## Rollback

Rollback removes the F4-D schema, projection, verifier, workflow and forecast portal panel. F4-C immutable evidence and the accepted F3-C astronomical projection remain unchanged. No provider request is performed by rollback and S10 remains `UNAVAILABLE`.

## Successor boundary

With F4-D accepted and the F4 evidence chain reconciled, **F5 — Explainable Ranking Method and Read-Only Consumer** becomes the next dependency-ready BKL-031 slice. F5 remains a separately governed package and requires explicit method/factor definitions, validation evidence and review before any ranking output is implemented or accepted.

F5 grants no readiness, scheduling, automatic target selection, command path or Safety Authority. BKL-032 remains the separate owner of session readiness / go-no-go decision support, and S10 production runtime remains `UNAVAILABLE`.
