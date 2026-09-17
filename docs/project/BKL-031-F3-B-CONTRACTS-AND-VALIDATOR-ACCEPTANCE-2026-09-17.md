# BKL-031 F3-B — Contracts and Validator Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Capability | BKL-031 F3-B |
| Contract digest | `b06932edb860cc4062b45d75b62e7874c3a327a4b4dbfd0b8cb70bdf115cd1f1` |
| Reviewed head | `858a7094d2ae01329617c2c733075f6b87d44113` |
| Pull request | [#259](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/259) |
| Merge commit | `8c3b7b8424a15b4288c79f773b9f0fc3f7cd5c5f` |
| Executable tests | 34/34 passing locally and in governed CI |
| Runtime effect | None; S10 remains `UNAVAILABLE` |

## Accepted decision

The F3-B increment passed exact-head ARB and Release Quality review on `858a7094d2ae01329617c2c733075f6b87d44113`. Pull request #259 completed all 15 required checks successfully and was merged with expected-head control as `8c3b7b8424a15b4288c79f773b9f0fc3f7cd5c5f`. It materializes the three contracts authorized by the F3-A3 acceptance, verifies a bounded synthetic fixture and rejects semantic, lineage, privacy and authority drift fail closed.

The fixture is explicitly `TEST` with `authority=NONE`. The public projection contains a non-correlatable synthetic site reference and normalized facts; it excludes site coordinates, protected record identity, internal input/output/data digests, credentials and raw locators.

## Acceptance matrix

| Gate | Accepted disposition |
|---|---|
| source-neutral method/request/evidence schemas | PASS |
| bounded synthetic fixture | PASS — 4 instants, 9 facts, 24-hour maximum span |
| canonical identity and exact source binding | PASS |
| UTC/frame/epoch/datum/refraction semantics | PASS |
| normalized fact vocabulary, units and ranges | PASS |
| half-open validity and coverage | PASS |
| availability/value/reason fail-closed behavior | PASS |
| public-boundary privacy and non-correlation | PASS |
| prohibited forecast/ranking/readiness/command/Safety fields | PASS |
| F2 and authority-store preservation | PASS — unchanged |
| F3-C/runtime/protected-site/external-reference boundary | PASS — not executed |

## Post-merge verification

All 11 applicable push workflows completed successfully against the exact merge commit. This includes F3-B Governance `35192376713`, Developer Foundation `35192376992`, documentation validation `35192376744`, Pages deployment `35192376685`, Word generation `35192376644`, Governed Projection Sync `35192376652`, Scientific Platform Governance `35192376732`, F3-A3 GCP IaC validation `35192376738`, BKL-041 F4 Governance `35192376683`, BKL-046 F4 governance `35192376629` and BKL-046 F5 governance `35192376670`.

The next gate is F3-C bounded adapter and sanitized projection. F4 forecast, F5 ranking/consumer, BKL-032 readiness, commands and Safety Authority remain later independent scopes. S10 remains `UNAVAILABLE` until the F3-C adapter and projection pass their independent acceptance gate.
