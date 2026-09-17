# BKL-031 F9 — Repeatable current-night planner

| Field | Value |
|---|---|
| Status | **IMPLEMENTATION CANDIDATE** |
| Date | 2026-09-17 |
| Governing decision | ADR-012 |
| Environment / authority | `EVALUATION` / `NONE` / `READ_ONLY` |

## Purpose

F9 converts the bounded F8 demonstration into a repeatable current-night pipeline:

`MeteoHub run discovery → ephemeral GRIB acquisition → protected-site point extraction → current-night astronomy → setup/target suitability → explainable ranking/windows → sanitised portal projection`.

## Operating model

The scheduled GitHub workflow runs at 04:15 and 17:15 UTC. These are the only acquisition triggers and therefore cap execution at two cycles per day. It discovers one fresh ICON-2I run, downloads the seven variables required by the accepted scoring method, extracts the governed site point server-side and disposes the temporary directory automatically.

The durable projection retains provider, authority, model, run, retrieval time, byte count and SHA-256 per source file. It never retains raw GRIB bytes or coordinates. An 18-hour run-age ceiling and complete current-night coverage are mandatory.

The projection carries forward the F8 governed setup profiles, target profiles, suitability evidence and advisory weights. Astronomy is recomputed for the current night using explicit Swiss Ephemeris Moshier mode plus sidereal-target geometry. The explicit `MOSEPH` flag prevents an implicit switch to external ephemeris files. No prior forecast or ranking is used as fallback.

## Failure behavior

Discovery failure, HTTP/content-type mismatch, oversized GRIB input, missing messages, non-finite values, variable-time misalignment, missing night coverage, stale run, invalid setup/target binding, privacy leakage or authority drift aborts publication. Because the consumer independently recomputes freshness, an old projection becomes unavailable rather than historical evidence being shown as current.

## Cost and retention

The approved monetary budget is EUR 0. The workflow uses standard GitHub-hosted runners for the public repository and the no-fee MeteoHub open-data path. It uploads no artifacts and commits only the sanitised JSON projection. GRIB retention is `NONE_EPHEMERAL_ONLY`.

## Acceptance boundary

Implementation presence alone does not close BKL-031. Acceptance requires exact-head CI, ARB, Release Quality, expected-head merge, one successful governed refresh, portal verification and post-merge workflow evidence. Until then S10 remains `UNAVAILABLE`.
