# BKL-031 F4-A — Forecast Source Discovery and Integration Contract

| Field | Value |
|---|---|
| Identifier | `BKL-031-F4-A-CONTRACT-001` |
| Status | **REVIEW CANDIDATE — NO PROVIDER TRAFFIC AUTHORIZED** |
| Date | 2026-09-17 |
| Predecessor | F3-C Accepted / Post-Merge Verified |
| Source dimension | BKL031-S11 forecast |
| Runtime impact | None |
| Safety impact | None |

## 1. Decision

F4-A selects a bounded candidate path for forecast evidence and defines the normative integration contract before any provider request. The selected evaluation path is the Open-Meteo Single Runs API with the explicit model selector `italia_meteo_arpae_icon_2i`. The upstream model authority is ItaliaMeteo/ARPAE ICON-2I; Open-Meteo is the delivery and normalization service, not the meteorological model authority.

The adapter must request one explicit UTC model initialization through the `run` parameter. `best_match`, seamless products, stitched time series and silent fallback are prohibited because they do not preserve one stable run identity across the evidence envelope.

This package authorizes only repository documentation, validation rules and the next machine-readable contract gate. It performs zero provider calls, uses zero protected-site facts and does not activate runtime, ranking, readiness, commands or Safety Authority.

## 2. Verified source discovery

| Candidate | Verified characteristics | Disposition |
|---|---|---|
| ItaliaMeteo/ARPAE ICON-2I through Open-Meteo Single Runs | Italy and surrounding region; about 2.2 km grid; hourly output; 00/12 UTC cycles; forecast horizon 72 hours; explicit `run` and explicit model selector available | **SELECTED FOR BOUNDED EVALUATION** |
| Open-Meteo generic Forecast API `best_match` | chooses and stitches model output dynamically | **REJECTED** for governed evidence because model/run lineage can change inside the returned series |
| Open-Meteo `icon_seamless` or other seamless product | may combine regional and global products | **REJECTED** as primary evidence; no implicit model transition is permitted |
| ECMWF IFS 0.25° open data / `ecmwf_ifs025` single run | global 0.25° product; four daily cycles; longer horizon; CC BY 4.0 | **REFERENCE CANDIDATE ONLY** for a later, separately authorized comparison; never an automatic fallback |
| Historical CloudWatcher or repository weather | observed historical evidence | **REJECTED AS FORECAST**; it retains `OBSERVED` semantics and cannot satisfy BKL031-S11 |

Official evidence reviewed on 2026-09-17:

- [ARPAE model forecast description](https://www.arpae.it/it/temi-ambientali/meteo/previsioni-meteo/previsioni-meteo-modellistiche) states that ICON-2I is produced at 00 and 12 UTC, covers Italy at 2.2 km and runs to 72 hours;
- [Open-Meteo ItaliaMeteo/ARPAE documentation](https://open-meteo.com/en/docs/italia-meteo-arpae-api) exposes the exact model selector and variables at hourly resolution;
- [Open-Meteo Single Runs API](https://open-meteo.com/en/docs/single-runs-api) defines `run` as the model initialization time and preserves one forecast run;
- [Open-Meteo model-update metadata](https://open-meteo.com/en/docs/model-updates) exposes initialization, modification and availability times and documents eventual consistency;
- [Open-Meteo terms](https://open-meteo.com/en/terms) and [pricing](https://open-meteo.com/en/pricing) distinguish the non-commercial free endpoint from commercial service and require CC BY 4.0 attribution;
- [ECMWF Open Data](https://www.ecmwf.int/en/forecasts/datasets/open-data) confirms the reference product's 0.25° resolution, four daily cycles, rolling availability and CC BY 4.0 terms.

Provider documentation is time-varying evidence. A later implementation must pin an observed documentation revision or content digest in its source profile and fail closed when the contractual fields or terms change.

## 3. Required request contract

The future request envelope is closed and must carry:

- `requestId`, contract version and generation UTC;
- protected `siteAuthorityRef`, never raw site facts in repository or public output;
- an outbound-location policy and a server-side resolved WGS84 point only after a separate privacy authorization;
- exact `providerId=OPEN_METEO`, `upstreamAuthorityId=ITALIAMETEO_ARPAE`, `modelId=italia_meteo_arpae_icon_2i` and `runInitialisationUtc` at 00 or 12 UTC;
- `timezone=GMT`, ISO-8601 time format, `cell_selection=land` and `elevation=nan` so the provider does not receive site elevation and no undocumented elevation downscaling is introduced;
- a half-open requested interval `[startUtc,endUtc)` wholly inside `runInitialisationUtc` through `runInitialisationUtc + 72h`;
- exactly these hourly variables: `temperature_2m`, `relative_humidity_2m`, `dew_point_2m`, `precipitation`, `cloud_cover`, `cloud_cover_low`, `cloud_cover_mid`, `cloud_cover_high`, `visibility`, `wind_speed_10m`, `wind_gusts_10m`;
- maximum 72 hourly instants in the half-open 72-hour horizon, one location, one model and one run per request;
- network policy, timeout, response-size ceiling and attribution profile supplied by a separately reviewed source profile.

Unknown query parameters, default model selection, local-time output, interpolated sub-hourly values, multiple locations, multiple models or a range beyond 72 hours are rejected before network access.

## 4. Required evidence contract

One accepted response is normalized into a closed `ForecastEvidence` envelope containing:

1. request identity and canonical request digest;
2. provider, upstream authority, model and exact run initialization;
3. retrieval UTC, provider availability UTC when known and raw-response SHA-256;
4. requested coordinates kept protected plus returned grid latitude, longitude and elevation kept in restricted evidence;
5. grid resolution, native temporal resolution and selected cell policy;
6. half-open validity interval and ordered UTC forecast instants;
7. values paired with exact units and explicit availability for every requested variable and instant;
8. Citation, Provenance, provider terms revision and required attribution;
9. `availabilityState`, reason codes and all exclusions;
10. explicit boundaries: `rankingImplemented=false`, `readinessImplemented=false`, `commandAuthority=NONE`, `safetyAuthority=LOCAL_PHYSICAL_INTERLOCKS`.

The public projection may expose normalized forecast values, model name, run time, validity, coarse grid metadata, retrieval time, attribution and reason codes. It must not expose protected coordinates, provider credentials, subscription identifiers, raw request URLs or internal locators.

## 5. Freshness, validity and missingness

- The selected run must be named explicitly and must be available before the data request. Metadata indicating a new run does not authorize use until the documented replication buffer has elapsed.
- The evaluation profile must define a source-specific maximum run age. F4-A sets a conservative ceiling of 18 hours at retrieval for the twice-daily ICON-2I cadence; a missed cycle therefore fails closed instead of extending last-known-good evidence.
- Every forecast instant must be at or after the run initialization, within the provider's 72-hour horizon and inside the requested interval.
- The evidence becomes `STALE` when evaluated outside its validity interval or when its run exceeds the profile's maximum age. It is never silently refreshed or combined with another run.
- Missing variables, length mismatch, non-finite values, unit drift, non-monotonic instants, spatial mismatch, unresolved Citation/Provenance or changed license terms make the affected evidence `UNAVAILABLE`, `STALE` or `CONFLICTED` as applicable.
- Historical observations and a newer forecast run cannot fill holes in an accepted run.

## 6. Security, privacy and licensing

No browser calls the provider. Acquisition and normalization must run in a separately authorized off-EAGLE server-side job with allow-listed HTTPS hosts, no redirects, bounded response size, fixed timeout, no credential logging and an immutable evidence output.

The exact site point remains protected. F4-B uses a synthetic/generalized test location. Any later protected-site request requires an explicit outbound privacy decision recording the minimum coordinate precision, permitted recipient and retention behavior.

The free Open-Meteo endpoint is eligible only for bounded non-commercial evaluation under its then-current fair-use terms. Production use requires a recorded commercial subscription decision or a separately reviewed self-hosted deployment. Every displayed value requires Open-Meteo and upstream-model attribution under CC BY 4.0. Terms drift fails closed.

## 7. Prohibited interpretations

Forecast evidence is advisory context. Cloud cover, humidity, precipitation, visibility or wind values are not observatory safety evidence. The contract cannot emit `safe`, `unsafe`, `ready`, `go`, `no-go`, target order, numeric suitability score, automatic schedule or device command. BKL-032 and physical local interlocks remain separate authorities.

## 8. Successor gates

1. **F4-B — machine-readable contract, synthetic fixture and validator:** no provider traffic; execute the negative cases in the validation plan.
2. **F4-C — bounded synthetic/generalized-source acquisition and normalized evidence:** exact-head review and explicit network/privacy authorization required before one provider call.
3. **F4-D — sanitized projection and portal integration:** read-only forecast context only; no ranking or readiness.
4. **F4 acceptance reconciliation:** exact-head review, expected-head merge, post-merge verification and deployed-route verification.

F5 remains blocked until F4 is accepted. Production runtime S10 remains `UNAVAILABLE`.
