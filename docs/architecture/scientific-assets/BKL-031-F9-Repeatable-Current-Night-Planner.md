# BKL-031 F9 — Repeatable current-night planner

| Field | Value |
|---|---|
| Status | **ACCEPTED — CLOSED / POST-MERGE VERIFIED** |
| Date | 2026-09-18 |
| Governing decision | ADR-012 |
| Environment / authority | `EVALUATION` / `NONE` / `READ_ONLY` |

## Purpose

F9 converts the bounded F8 demonstration into a repeatable current-night pipeline:

`MeteoHub run discovery → ephemeral GRIB acquisition → protected-site point extraction → current-night astronomy → setup/target suitability → explainable ranking/windows → sanitised portal projection`.

## Operating model

The scheduled GitHub workflow is defined for 09:30 and 17:15 UTC (11:30 and 19:15 Europe/Rome during CEST) for the current validation cycle. A separately authorized `workflow_dispatch` diagnostic path is available only with explicit `ALLOW_ONE_TEST_ACQUISITION` confirmation and a purpose string. The workflow imposes no daily acquisition counter: scheduled and authorized manual runs can execute independently. No automatic retry is introduced. GitHub cron is UTC; the first local-time display shifts to 10:30 during CET unless the schedule is adjusted seasonally. The public repository uses standard GitHub-hosted runners; the job additionally requires explicit activation variable `F9_ZERO_EUR_GUARD=CONFIRMED`. Once activated, the job discovers one fresh ICON-2I run, downloads the seven variables required by the accepted scoring method, extracts the governed site point server-side and disposes the temporary directory automatically.

The durable projection retains provider, authority, model, run, retrieval time, byte count and SHA-256 per source file. It never retains raw GRIB bytes or coordinates. An 18-hour run-age ceiling and complete current-night coverage are mandatory.

The projection carries forward the F8 governed setup profiles, target profiles, suitability evidence and advisory weights. Astronomy is recomputed for the current night using explicit Swiss Ephemeris Moshier mode plus sidereal-target geometry. The explicit `MOSEPH` flag prevents an implicit switch to external ephemeris files. No prior forecast or ranking is used as fallback.

## Failure behavior

Discovery failure, HTTP/content-type mismatch, oversized GRIB input, missing messages, non-finite values, variable-time misalignment, missing night coverage, stale run, invalid setup/target binding, privacy leakage or authority drift aborts publication. Because the consumer independently recomputes freshness, an old projection becomes unavailable rather than historical evidence being shown as current.

## Weather eligibility for ranked windows

The portal's hourly weather signal and ranked forecast windows use the same
published F9 eligibility policy. A forecast hour is eligible only when cloud
cover is at most 20%, precipitation is zero, wind is at most 15 km/h, gusts at
most 20 km/h, relative humidity at most 90%, and temperature-to-dew-point
margin at least 10 °C. The 20% cloud limit is the owner's stricter planning
constraint for dome/session suitability; it does not replace or change the
BKL-032 readiness threshold of 50%.

Each hourly row is explicitly GO or NO-GO with its failing weather reasons.
Multi-hour forecast windows are omitted from ranking when any included hourly
sample violates a required bound; unavailable, stale, incomplete or malformed
weather inputs fail closed and do not produce an eligible window. Consequently,
the target ranking is advisory only and can be absent while an older projection
is awaiting the next routine refresh. This presentation is not operational
readiness, dome-opening authorization, scheduling, command or Safety Authority;
BKL-032 and local physical interlocks retain their respective authority.

## Cost and retention

The approved monetary budget is EUR 0. MeteoHub is a no-fee open-data path and standard GitHub-hosted runners are free for this public repository. The explicit activation guard remains enabled. The workflow uploads no artifacts and commits only the sanitised JSON projection. GRIB retention is `NONE_EPHEMERAL_ONLY`.

## Acceptance boundary

Closure evidence is recorded in `docs/project/BKL-031-CLOSURE-2026-09-18.md`. PR #301 merged at `4a509d574a004fe7fb72bc6c678c9e7f71fe821f`; the governed workflows, documentation validation, Word generation and GitHub Pages deployment passed, and the public Manciano planner was verified directly. The F9 weather-eligibility portal increment is recorded in PR #373, merged as `fd59ba711697efcd324af8a77ae78855fb174f40` on 2026-09-24; its post-merge F9 governance, strict documentation validation and Pages workflows succeeded. S10 remains `UNAVAILABLE`; the capability remains advisory, read-only and outside readiness, scheduling, command and Safety Authority.
