# BKL-031 F4-A — Forecast Source Contract Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Capability | BKL-031 F4-A |
| Source authority | ItaliaMeteo/ARPAE ICON-2I |
| Delivery interface | Open-Meteo Single Runs with explicit model and run |
| Reviewed head | `d2ecedb2c141eb0a17f5a1d659748488802d4200` |
| Pull request | [#263](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/263) |
| Merge commit | `02a829f21bf76a0dc5d9ef29998ca5690d71395c` |
| Exact-head checks | 16/16 successful |
| Post-merge workflows | 13/13 successful |
| Provider traffic | Zero |
| Runtime effect | None; S10 remains `UNAVAILABLE` |

## Accepted decision

F4-A passed exact-head ARB and Release Quality review, expected-head merge and post-merge verification. ADR-011 is Accepted for repository source authority. The accepted contract requires one explicit `italia_meteo_arpae_icon_2i` run, UTC half-open validity, a maximum 72-hour horizon, an 18-hour run-age ceiling, eleven closed forecast variables and fail-closed handling for lineage, temporal, spatial, unit, licensing and privacy failures.

## Verification

All exact-head checks succeeded, including Developer Foundation, F4-A Governance, documentation, scientific governance, projection gates, infrastructure validation and Word generation. After merge, these 13 workflows succeeded against `02a829f21bf76a0dc5d9ef29998ca5690d71395c`: Scientific Platform Governance `35197123714`, F4-A Governance `35197123619`, BKL-041 F4 Governance `35197123709`, BKL-046 F4 governance `35197123893`, F3-B Governance `35197123616`, Governed Projection Sync `35197123708`, F3-C Governance `35197123681`, BKL-046 F5 governance `35197123614`, Word `35197123696`, F3-A3 GCP IaC Validation `35197123764`, documentation validation `35197123620`, Pages `35197123599` and Developer Foundation `35197123669`.

The package generated no provider request and disclosed no protected-site coordinate. Acceptance authorizes F4-B machine-readable request, source-profile and evidence schemas, a synthetic/generalized TEST/NONE fixture, the deterministic validator and all 24 negative cases. Provider acquisition remains a separate F4-C network/privacy gate. Production runtime, ranking, readiness, commands and Safety Authority remain unavailable.
