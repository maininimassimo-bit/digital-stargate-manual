# BKL-031 F4-D — Sanitized Forecast Projection and Portal

| Field | Value |
|---|---|
| Identifier | `BKL-031-F4-D-PROJECTION-001` |
| Status | **IMPLEMENTED CANDIDATE — PRE-MERGE VALIDATION REQUIRED** |
| Date | 2026-09-17 |
| Predecessor | F4-C reconciliation merged in PR #270; post-merge workflows verified |
| Source evidence | `BKL031-F4C-EVIDENCE-35214129960` |
| Environment / authority | `EVALUATION` / `NONE` |
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

## Validation

The F4-D verifier must pass against the exact reconciled source evidence and fail if protected or unauthorized semantic keys appear. The governance workflow re-runs the F4-C gate and reconciliation before F4-D verification and checks browser JavaScript syntax.

Repository-wide acceptance additionally requires the normal BKL-031 quality gates, strict MkDocs builds, roadmap/status consistency, exact-head review, expected-head merge and post-merge verification. Until those complete, this package remains an implemented candidate rather than Accepted/Post-Merge Verified.

## Rollback

Rollback removes the F4-D schema, projection, verifier, workflow and forecast portal panel. F4-C immutable evidence and the accepted F3-C astronomical projection remain unchanged. No provider request is performed by rollback and S10 remains `UNAVAILABLE`.

## Successor boundary

F5 remains blocked until F4-D is accepted and the complete F4 acceptance reconciliation is post-merge verified. F4-D grants no runtime activation, protected-site acquisition, ranking, readiness, scheduling, command path or Safety Authority.
