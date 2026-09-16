# BKL-031 F3-A3 — Owner Decision Record 2026-09-15

| Field | Value |
|---|---|
| Identifier | BKL-031-F3-A3-OD-2026-09-15 |
| Status | **COMPLETE OWNER DECISION — F3-OD05 APPROVED / NO EXECUTION AUTHORITY** |
| Date | 2026-09-15 |
| Baseline | `main@527b298094b07e5a00317e60cab3abefed7a5759` |
| Decision target | ADR-010 |
| Runtime impact | None |

## Decision statement

The Repository Owner approved the prudent baseline for F3-A3:

- Astropy 8.0.1 local primary candidate;
- Skyfield 1.55 local implementation cross-check;
- Horizons API v1.3 validation-only with geocentric or unmistakably synthetic/generalized location;
- the per-metric accuracy thresholds recorded in ADR-010;
- pinned IERS-A snapshot policy with no execution-time download;
- Google Cloud Run Job in `europe-west8`, 2 vCPU, 2 GiB, one task, one-way parallelism, 120-second timeout and zero retries;
- the request/capacity limits recorded in ADR-010;
- repository-only Terraform/WIF preparation.

## F3-OD05 completion

F3-OD05 is completed by the separate exact approval record
[BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16](BKL-031-F3-A3-F3-OD05-SPK-APPROVAL-2026-09-16.md).

The approved artifact is `de442s.bsp`, SHA-256
`54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c`,
with exact coverage, provenance, notices, retention and future private
content-addressed object identity recorded in that approval.

No placeholder, mutable URL or generic “latest JPL kernel” satisfies this gate.

## Authorization boundary

This record authorizes repository documentation, Terraform source and non-authenticated validation CI. The separately authorized one-time SPK identity acquisition is complete. This record does not authorize GCP resource creation, container publication, further artifact acquisition, any upload, Cloud Run execution, protected-site processing, Horizons traffic or runtime work.

## Accepted accuracy profile

| Metric | Pass condition |
|---|---|
| geometric airless altitude | ≤60 arcsec, altitude ≥5° |
| geometric azimuth | ≤60 arcsec for altitude 5°–85° |
| near-zenith direction | spherical separation ≤60 arcsec above 85° |
| target–Moon separation | ≤60 arcsec |
| transit/culmination | ≤5 seconds |
| lunar illumination | absolute fraction difference ≤0.001 |
| rise/set when included | geometric event time ≤60 seconds |
| repeatability | identical normalized output for the same pinned container, input and artifacts |

Each case and metric passes independently. No average, weighted score or majority vote is allowed.

## Accepted capacity profile

| Limit | Value |
|---|---:|
| targets | 50 |
| instants per target | 2,016 |
| target×instant pairs | 10,000 |
| date span | 7 days |
| minimum grid step | 1 minute |
| serialized request | 256 KiB |
| concurrent requests | 2 |
| service hard timeout | 15 seconds |
| service p95 after warm-up | 5 seconds |
| spike task timeout | 120 seconds |

## Continuity rule

F3-OD05 is approved, but ADR-010 remains Proposed and S10 remains `UNAVAILABLE` until the authorized scientific campaign and all remaining acceptance gates are complete.
