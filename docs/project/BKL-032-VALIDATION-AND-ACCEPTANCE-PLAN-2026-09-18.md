# BKL-032 — Validation and Acceptance Plan

**Identifier:** `BKL-032-VAL-001`  
**Status:** Accepted with Conditions
**Release:** Release 2.x

## Scope

Validate the separate Session Readiness / Go-No-Go decision-support contract without runtime, provider traffic, EAGLE activity, device commands or Safety Authority changes.

## Test matrix

| Area | Required evidence |
|---|---|
| Contract | Valid session context and readiness record schemas |
| Positive path | Governed complete evidence produces the owner-approved positive state |
| Missing evidence | Fail-closed result with reason code |
| Stale evidence | Fail-closed result with freshness evidence |
| Conflict | Fail-closed result with conflict reason |
| Provenance | Source, run, timestamp, semantic type and correlation ID preserved |
| Live telemetry | Weather rain/wind/gust/cloudiness/humidity-dew point, dome, mount, camera, power, network and EAGLE health are present and current |
| Freshness | Forecast and readiness evidence no older than six hours |
| Weather blocking | Rain > 0; mean wind > 15 km/h; gust > 20 km/h; cloudiness > 50%; humidity > 90%; or dew-point margin < 10 °C produces `NO_GO` |
| Telemetry missingness | Any mandatory domain missing or stale produces `INDETERMINATE` and prevents `GO` |
| Privacy | Protected coordinates and exact site data absent from public projection |
| Boundary | No scheduler, command, automatic target selection or Safety Authority |
| Architecture | Domain/application/infrastructure dependency rules pass |
| Documentation | Links, navigation, roadmap and closure lineage consistent |

## Required owner decisions

The owner approved the state semantics and mandatory domains on 2026-09-18. `GO` requires forecast, current astronomy, setup compatibility and all mandatory live telemetry to be complete, fresh, consistent and passing. `NO_GO` applies to rain > 0 or wind/gust beyond documented local limits. `INDETERMINATE` applies to missing or stale mandatory domains. Forecast/readiness freshness is six hours.

The repository-level source inventory and owner-approved BKL-032 thresholds are recorded in `BKL-032-TELEMETRY-SOURCE-MAPPING-2026-09-18.md`. Remaining pre-implementation gate: acceptance of the read-only source/transport mapping for each domain. S10 remains `UNAVAILABLE`.

## Quality gates

Exact-head CI → process-separated ARB → Release Quality on the same SHA → expected-head merge → post-merge verification → acceptance reconciliation.

## Non-goals

No provider acquisition, live EAGLE inspection, dome/mount/camera/power/network command, scheduling, automated target selection or Safety Authority change is part of this plan.
