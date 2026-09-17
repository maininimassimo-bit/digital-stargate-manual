# ADR-011 — Forecast Source and Run Lineage

| Field | Value |
|---|---|
| Status | **PROPOSED — F4-A REVIEW CANDIDATE** |
| Date | 2026-09-17 |
| Capability | BKL-031 F4 |
| Decision scope | Forecast source evaluation and run-lineage contract |
| Runtime impact | None |

## Context

BKL031-S11 remains unavailable after F3-C. F1 requires provider/model run, issue time, valid interval and spatial applicability; historical weather cannot substitute for forecast. The public planner currently proves only bounded TEST/NONE ephemeris/lunar integration.

## Decision

Use ItaliaMeteo/ARPAE ICON-2I as the upstream deterministic forecast model candidate and Open-Meteo Single Runs as the bounded delivery interface. Every evidence envelope binds the exact model selector `italia_meteo_arpae_icon_2i` and one explicit UTC `run`. The generic `best_match`, seamless series, stitched output and automatic model fallback are prohibited.

ICON-2I is selected for evaluation because the official source documents Italy-domain coverage at about 2.2 km, hourly output, 00/12 UTC runs and a 72-hour horizon. ECMWF IFS 0.25° remains a separately gated reference candidate and cannot replace ICON-2I automatically.

The source contract, validation plan, privacy decision and license mode must pass separate gates before any network call. The free Open-Meteo endpoint is limited to bounded non-commercial evaluation. Production requires a commercial-service or self-hosting decision and a new review.

## Consequences

- forecast facts have stable provider/model/run/spatial lineage;
- missing or late runs fail closed instead of switching models;
- the 72-hour horizon limits the first implementation but matches short-range observation planning;
- exact-site disclosure remains blocked until an outbound privacy decision exists;
- attribution and terms revision become required evidence;
- no ranking, readiness or Safety meaning is introduced.

## Rejected alternatives

- `best_match` and seamless products: convenient but incompatible with stable single-run lineage;
- historical CloudWatcher data: observed, not forecast;
- direct GRIB ingestion in F4-A: higher operational and decoding complexity before the contract is validated;
- dual-provider automatic fallback: hides conflict and source switching;
- ECMWF IFS 0.25° as primary: longer horizon but materially coarser than ICON-2I for the selected Italy-domain evaluation.

## Promotion condition

ADR-011 becomes Accepted for repository source authority only after exact-head ARB and Release Quality review, required checks, expected-head merge and post-merge verification. Acceptance still does not authorize provider traffic or production runtime.
