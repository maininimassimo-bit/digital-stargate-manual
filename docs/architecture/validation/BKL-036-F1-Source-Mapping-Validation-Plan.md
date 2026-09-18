# BKL-036-F1 — Source Mapping Validation Plan

**Identifier:** `BKL-036-F1-VAL-001`  
**Status:** Accepted / Post-Merge Verified
**Version:** 0.1  
**Runtime traffic:** None authorized

## Objective

Validate the governed source mapping and evidence-compatibility boundary without implementing a score, consuming live telemetry or changing any observatory authority.

## Validation matrix

| Gate | Validation | Acceptance evidence |
|---|---|---|
| F1-V1 | Source authority and ownership | Every mapped dimension cites a governed repository source or an explicit gap |
| F1-V2 | Field semantics | Field, unit/scale and semantic type are explicit; unresolved values remain `UNKNOWN`/`PARTIAL` |
| F1-V3 | Time/freshness | Observation timestamp and freshness representation are preserved; no cadence is generalized silently |
| F1-V4 | Evidence status | `PRESENT`, `MISSING`, `STALE`, `UNAVAILABLE`, `PARTIAL` and `CONFLICTING` remain distinct |
| F1-V5 | Compatibility | `COMPARABLE`, `CONTEXT_ONLY`, `INCOMPATIBLE` and `UNKNOWN` are assigned only from evidence |
| F1-V6 | Plane separation | Repository evidence, live telemetry and runtime/consumer acceptance are not conflated |
| F1-V7 | Safety and authority | No score, threshold, readiness transfer, command, remediation or interlock change appears |
| F1-V8 | Privacy/security | No coordinate, credential, token, secret, raw live payload or personal data is introduced |
| F1-V9 | Traceability | ADR, package, source record, validation plan, graph, roadmap and navigation resolve |
| F1-V10 | Regression | BKL-031/BKL-032 contracts and evaluator remain unchanged in behavior |

## Required negative cases

- source present but runtime interface unverified;
- missing unit or observation timestamp;
- stale or future-dated evidence;
- partial CloudWatcher/weather or dome/power source;
- conflicting source observations;
- historical session evidence presented as live health;
- EAGLE host health presented as Safety Authority;
- `COMPARABLE` assigned across incompatible units or temporal bases;
- score, weight, threshold, ranking, remediation or command field added to F1;
- protected coordinate, credential, token or live traffic appearing in the package.

## Exit criteria

F1 is ready for review only when all F1-V1–F1-V10 checks are evidenced on the exact commit, with no unresolved Blocker/Major. ARB and Release Quality must review the same SHA before merge. This plan does not authorize runtime transport, score calculation or device integration.
