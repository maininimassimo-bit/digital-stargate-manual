# BKL-031 F3-A3 — F3-OD05 Exact SPK Approval

| Field | Value |
| --- | --- |
| Identifier | BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16 |
| Status | **OWNER APPROVED — ARTIFACT IDENTITY ONLY / NO EXECUTION AUTHORITY** |
| Date | 2026-09-16 |
| Source baseline | `main@4312e4e71103bd6a36b697c875c3dc7ae2e2a68c` |
| Decision target | ADR-010 / F3-OD05 |
| Runtime impact | None |

## Decision

The Repository Owner approves the following immutable F3-OD05 identity:

| Property | Approved value |
| --- | --- |
| Artifact | `de442s.bsp` |
| Official source | `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de442s.bsp` |
| Size | `32701440` bytes |
| Format | SPICE `DAF/SPK` |
| SHA-256 | `54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c` |
| NAIF MD5 | `cc49327e06088124c0e39d8dde9f0b58` |
| Kernel coverage | `1849-12-26T00:00:00 ET` through `2150-01-22T00:00:00 ET` |
| Required chains | Solar System Barycenter `(0)`, Earth Barycenter `(3)`, Sun `(10)`, Moon `(301)`, Earth `(399)` |
| Future private data bucket | `digital-stargate-telemetry-183451329061-f3-data` |
| Future content-addressed URI | `gs://digital-stargate-telemetry-183451329061-f3-data/bkl-031/f3-a3/artifacts/spk/de442s/sha256/54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c/de442s.bsp` |

Every requested interval, bounded to seven days, must be fully contained within the kernel coverage. Any instant outside coverage must fail closed as `OUT_OF_COVERAGE`; extrapolation and silent kernel substitution are prohibited.

## Provenance evidence

A one-time owner-authorized acquisition was performed from the official NAIF HTTPS endpoint into a private temporary Cloud Shell directory solely for identity verification.

| Evidence | Value |
| --- | --- |
| Verified UTC | `2026-09-16T10:41:32Z` |
| SPICE header | `DAF/SPK` |
| Official MD5 result | `de442s.bsp: OK` |
| `aa_checksums.txt` SHA-256 | `3c618bed7d51a48ee059269097eeeab1f69f3b2641ec2aeb96132757418c845b` |
| `aa_summaries.txt` SHA-256 | `2b34f045b63731a6a315a83b1e2f240dd208a4b5a19ee3419be0573485c15f87` |
| `de442_tech-comments.txt` SHA-256 | `1722f24a198fe54f8c25ae089ccfd06efd4bf22092e71da5d9d410040af5f666` |
| NAIF rules snapshot SHA-256 | `ae85f851646e7c4f0a762db852907bc090a2ab50c815eb2a6cd8639e96b7e047` |
| NAIF credit snapshot SHA-256 | `e2b501b7a7ede59328784ab1f34c7e3158d1717e4d0594a75ce2a9e2dfed6645` |

The binary kernel, HTTP headers and temporary evidence files are not repository content.

## License, notice and retention outcome

NAIF permits kernels published on its server to be downloaded and used. Redistribution is permitted only while the kernel remains unmodified. NASA/JPL/NAIF attribution and the DE442 technical reference must be preserved.

Digital StarGate will:

- retain the exact unmodified kernel privately until the F3-A3 evidence lifecycle closes;
- perform no public redistribution under this decision;
- prohibit replacement, modification or deletion without a governed revision;
- retain source URLs, checksums, coverage and attribution in the campaign manifest.

## Authorization boundary

This approval closes F3-OD05 only at artifact identity, coverage, provenance and notice-policy level.

It does not authorize:

- creation of the future bucket or any other Google Cloud resource;
- upload of the kernel or evidence;
- further artifact acquisition;
- Terraform plan/apply or state migration;
- container build or publication;
- Cloud Run or scientific execution;
- Horizons traffic;
- protected-site processing;
- runtime, EAGLE, N.I.N.A., device, readiness, go/no-go or Safety Authority changes.

ADR-010 remains `PROPOSED`, S10 remains `UNAVAILABLE`, and ARB-213-MI01 and ARB-213-MI02 remain open pre-apply gates.
