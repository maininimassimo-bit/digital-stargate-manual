# BKL-031 F4-B — Forecast Contracts Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Reviewed head | `ba8f63a9d923f1daf2aca7c7c2173aacf6c0e051` |
| Pull request | [#265](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/265) |
| Merge commit | `b3a136efc2bd8b7afd16a817a22cfaa9211f069e` |
| Exact-head checks | 18/18 successful |
| Post-merge workflows | 14/14 successful |
| Tests | 26/26, including 24/24 mandatory negative cases |
| Contract digest | `a96a8268c571c2fc7fbe715cce8183ecc3ee02d45cbea91aaaa1a46506533d48` |
| Provider traffic | Zero |
| Runtime effect | None; S10 remains `UNAVAILABLE` |

F4-B v1.0 passed exact-head architecture and release review, expected-head merge and all post-merge workflows. The accepted repository authority covered the three closed JSON Schemas, deterministic TEST/NONE fixture and fail-closed validator. The fixture contained four synthetic hourly instants and eleven governed variables; it was not a provider response.

The F4-C execution exposed a contract defect: v1.0 named the Previous Runs host while declaring the Single Runs interface, and included visibility although the official ICON-2I page marks it unavailable. The v1.1 correction candidate uses `single-runs-api.open-meteo.com`, ten supported variables, explicit unavailable visibility and contract digest `22d547c5c91a713ff5ca6398a8eb13a1abdc9b4f90759c900f07a8c6ec90c954`. This paragraph records remediation scope; it does not rewrite the evidence or status of PR #265.

Post-merge workflows: Projection Sync `35199409940`, F3-B `35199410115`, F4-B `35199410036`, F3-C `35199410006`, F4-A `35199409978`, BKL-046 F5 `35199410041`, BKL-041 F4 `35199410046`, BKL-046 F4 `35199410079`, Scientific Platform `35199410084`, Word `35199410020`, documentation `35199410123`, Pages `35199410012`, F3-A3 IaC `35199409970` and Developer Foundation `35199410080`.

Acceptance promotes preparation of the F4-C bounded synthetic/generalized acquisition gate. Provider traffic, protected-site egress, recurring acquisition, production runtime, public projection, ranking, readiness, commands and Safety Authority remain unauthorized until their separate gates pass.
