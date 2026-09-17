# BKL-031 F7 — Fresh Forecast Supply Validation Evidence

| Field | Value |
|---|---|
| Status | **PROTECTED-SITE EVIDENCE ACQUIRED — REVIEW CANDIDATE** |
| Date | 2026-09-17 |
| Workflow run | `35255829165` |
| Workflow head | `2c46ca8be59c9ea8245fa03de71e936249c52a1b` |
| Run attempt | `1` |
| Artifact | `10512359912` / `bkl-031-f7-protected-site-evidence-35255829165` |
| Artifact digest | `sha256:9c2c58f4f4d63bced1110b94de4463f17eb0a2bc14362c22bb3435cbce9455ef` |
| Protected-site request budget | **`1/1_EXHAUSTED`** |
| Site classification | `PROTECTED_EXACT_SITE` — coordinates not published |

## Result

The owner-authorized protected-site F7 request completed successfully against Open-Meteo Single Runs for upstream ItaliaMeteo/ARPAE ICON-2I run `2026-09-17T12:00Z`.

The server-side adapter resolved the request location only from the approved governed site record. Preflight verified the site authority and explicit outbound privacy decision before network execution. Coordinates were used only to construct the provider request; they were not written to the request plan, normalized supply, logs, durable repository evidence or public projection.

Retrieval completed at `2026-09-17T17:57:24.089Z`; observed run age was `5.956691` hours, within the ADR-011 18-hour ceiling, so freshness is `FRESH`.

The provider response contains 72 hourly positions. Normalization accepts 71 complete positions, excludes the initialization instant `2026-09-17T12:00Z` because `precipitation` is null/non-finite, leaves 66 accepted instants in the future at retrieval time, and performs zero imputations. Availability is therefore `DEGRADED`, not silently upgraded to `AVAILABLE`.

Raw response SHA-256: `1d66a83464c946b203ef60730a993acb913a9ee12bbf5ec0ab0839bff54b3046`.

Normalized supply SHA-256: `1df1894917962b29f83c4f24cbeb6572f71371e3b0877cdd4cf04833395577c8`.

The repository retains only the raw digest plus a gzip/base64 sanitized normalized supply. The raw provider body is not committed.

## Public projection verification

`docs/data/observation-planner-forecast-f7-site-projection.json` contains all 71 accepted real hourly forecast rows and an explicit night window for the Observation Planner. The public projection contains a generalized site label only and excludes protected coordinates, elevation, provider grid location and raw request URL.

The browser consumer verifies lineage, completeness, authority boundaries and prohibited privacy keys. It recomputes current run age and fails closed after the 18-hour freshness ceiling rather than presenting historical data as a current forecast.

## Boundary verification

- protected-site provider use: `true`;
- coordinate persistence: `false`;
- coordinate publication: `false`;
- recurring traffic: `false`;
- production runtime activated: `false`;
- readiness authority: `false`;
- scheduling authority: `false`;
- automatic target selection: `false`;
- command authority: `NONE`;
- Safety Authority: `LOCAL_PHYSICAL_INTERLOCKS`.

## Superseded generalized validation evidence

Earlier run `35243920092` remains immutable evidence that the fresh-supply mechanics worked at a synthetic/generalized point. It is retained for traceability only and is not the Observation Planner's current site forecast source.

## Replay protection

The protected-site authorization is exhausted after one request. The executable one-shot protected-site acquisition path must be removed before exact-head review; any later provider traffic requires a separately governed runtime/refresh authorization.
