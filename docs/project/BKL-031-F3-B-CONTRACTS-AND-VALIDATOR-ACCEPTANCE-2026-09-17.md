# BKL-031 F3-B — Contracts and Validator Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTANCE CANDIDATE — POST-MERGE VERIFICATION PENDING** |
| Date | 2026-09-17 |
| Capability | BKL-031 F3-B |
| Contract digest | `b06932edb860cc4062b45d75b62e7874c3a327a4b4dbfd0b8cb70bdf115cd1f1` |
| Executable tests | 34/34 passing locally |
| Runtime effect | None; S10 remains `UNAVAILABLE` |

## Candidate decision

The F3-B increment is ready for exact-head ARB and Release Quality review. It materializes the three contracts authorized by the F3-A3 acceptance, verifies a bounded synthetic fixture and rejects semantic, lineage, privacy and authority drift fail closed.

The fixture is explicitly `TEST` with `authority=NONE`. The public projection contains a non-correlatable synthetic site reference and normalized facts; it excludes site coordinates, protected record identity, internal input/output/data digests, credentials and raw locators.

## Acceptance matrix

| Gate | Candidate disposition |
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

## Promotion condition

F3-B becomes Accepted / Post-Merge Verified only after all required checks pass on the exact reviewed head, the merge uses expected-head control, and all applicable push workflows including Pages succeed. Until then F3-C is not promoted.

After that condition is met, the next gate is F3-C bounded adapter and sanitized projection. F4 forecast, F5 ranking/consumer, BKL-032 readiness, commands and Safety Authority remain later independent scopes.
