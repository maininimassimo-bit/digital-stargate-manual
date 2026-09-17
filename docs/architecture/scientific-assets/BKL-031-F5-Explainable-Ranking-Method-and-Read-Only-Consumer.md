# BKL-031 F5 — Explainable Ranking Method and Read-Only Consumer

| Field | Value |
|---|---|
| Identifier | `BKL-031-F5-RANKING-001` |
| Status | **ACCEPTED — POST-MERGE VERIFIED** |
| Version | 1.0 |
| Date | 2026-09-17 |
| Parent | BKL-031 — Observation Planner intelligente |
| Implementation baseline | `main@28d2ddac6be1ebf758a0ac40ac0e080c62d51c38` |
| Reviewed exact head | `dfda963e7e9d088282516200a6bd8bb64dd0dd1d` |
| Pull request | #273 |
| Merge commit | `777924e2638430f15bf717fa33dd71057751625a` |
| Post-merge verification | 7/7 applicable push workflows successful |
| Predecessors | F3-C astronomical projection; F4-D sanitized forecast projection |
| Environment / authority | `EVALUATION` / `NONE` |
| Consumer mode | `READ_ONLY` |
| Runtime effect | None; S10 remains `UNAVAILABLE` |
| Safety effect | None |

## 1. Accepted decision and scope

F5 introduces a deterministic, explainable ranking demonstrator and a read-only repository projection. It validates the ranking method before any production planner exists. The two candidate identities are governed public target identities, while the factor values used by the F5 fixture are explicitly synthetic factor values for method validation only.

F5 does **not** claim that either target is currently observable, preferable for a real night, ready for acquisition, safe, schedulable or authorized. It creates no device path and performs no provider call.

## 2. Why the F5 fixture is synthetic

F4-D intentionally publishes metadata-only forecast evidence and no forecast value arrays. F3-C is a bounded TEST/NONE integration projection and is not a current production target evaluator. Creating target-specific current forecast or geometry values in F5 would therefore invent evidence.

The F5 fixture instead reuses only governed identities and semantic lineage while marking all ranking factor values as synthetic EVALUATION evidence. This preserves the fail-closed boundary and still permits known-answer, sensitivity and authority tests.

## 3. Factor method

| Factor | Weight | Range | Interpretation |
|---|---:|---:|---|
| `ASTRONOMICAL_ALTITUDE` | 0.45 | 0–90 deg | higher is better |
| `LUNAR_SEPARATION` | 0.25 | 0–180 deg | higher is better |
| `FORECAST_EVIDENCE_COMPLETENESS` | 0.20 | 0–1 | higher is better |
| `TARGET_IDENTITY_VALIDATION` | 0.10 | 0–1 | must equal 1 in F5 |

Weights are explicit, versioned and sum to 1 within IEEE-754 tolerance. No silent reweighting, clamping, imputation or fallback is allowed.

For every factor:

`normalized = (value - min) / (max - min)`

and:

`score = 100 * sum(weight * normalized)`

The engine exposes raw value, unit, normalized value, weight and contribution for every candidate. Sorting is score descending with `targetKey` as deterministic tie-breaker.

## 4. Known answer

The bounded fixture contains `LDN 1320` and `M 27`, both already present as validated identities in the target knowledge read model. The synthetic factor set deterministically yields:

- LDN 1320 — score `76.3889`, rank 1;
- M 27 — score `53.0556`, rank 2.

These numbers validate the method only. They are not scientific recommendations and must not be interpreted as real target suitability.

## 5. Forecast lineage and provider boundary

F5 binds the accepted F4-C/F4-D evidence digest `350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5` and the completeness `71/72` only. The provider request budget remains `2/2_EXHAUSTED`; no additional provider traffic is authorized or performed.

Because F4-D publishes no forecast value arrays, F5 does not reconstruct, infer or fetch temperature, cloud, wind, humidity, precipitation or visibility values.

## 6. Authority and safety boundary

The projection is fixed to:

- `environment = EVALUATION`;
- `authority = NONE`;
- `consumerMode = READ_ONLY`;
- `readinessAuthority = false`;
- `automaticTargetSelection = false`;
- `schedulingAuthority = false`;
- `actionAuthority = NONE`;
- `commandAuthority = NONE`;
- `safetyAuthority = LOCAL_PHYSICAL_INTERLOCKS`.

F5 has no readiness, go/no-go, scheduling, automatic target selection, command or Safety Authority. BKL-032 remains the separate owner of readiness/go-no-go decision support. Local physical interlocks remain independent and authoritative.

## 7. Failure model

The ranking engine fails closed on unknown properties, duplicate candidates, unvalidated identity, non-finite or out-of-range evidence, invalid factor weights, unsupported method/version or any authority escalation. Required factor values are never silently imputed and no last-known-good result is promoted.

## 8. Governed artifacts

- `.github/scripts/observation-planner-ranking-f5.mjs`
- `.github/scripts/verify-observation-planner-ranking-f5.mjs`
- `.github/scripts/test-observation-planner-ranking-f5.mjs`
- `schemas/observation-planner-ranking-f5.schema.json`
- `docs/data/observation-planner-ranking-f5-fixture.json`
- `docs/data/observation-planner-ranking-f5-projection.json`
- `.github/workflows/bkl-031-f5-governance.yml`
- `docs/javascripts/observation-planner-ranking-f5.js`
- `docs/observation-planner/index.md`

Portal consumption is read-only and displays the synthetic/evaluation warning together with factor decomposition. It exposes no button or route that schedules, commands, approves or marks a target ready.

## 9. Validation and acceptance evidence

The final exact reviewed head `dfda963e7e9d088282516200a6bd8bb64dd0dd1d` passed all six applicable pull-request workflows, including dedicated F5 governance, F3-C and F4-D regression checks, Developer Foundation, strict documentation validation and Word generation. Architecture Review Board issued **APPROVED WITH CONDITIONS** with no Blocker/Major finding; Release Quality issued **CONDITIONALLY READY FOR MERGE** with no waiver.

PR #273 was merged with expected-head control as `777924e2638430f15bf717fa33dd71057751625a`. All seven applicable push workflows completed successfully on the actual merge SHA: F3-C Governance, F4-D Forecast Projection Governance, F5 Explainable Ranking Governance, Developer Foundation, Validate documentation, Generate Word Manual and Deploy MkDocs artifact to GitHub Pages.

F5 is therefore **Accepted / Post-Merge Verified**. Acceptance authorizes only the bounded deterministic ranking method, synthetic validation fixture, read-only projection and portal consumer. It does not authorize real-night ranking evidence, readiness, go/no-go, scheduling, automatic target selection, protected-site provider acquisition, commands, production runtime or Safety Authority.

## 10. Rollback

Rollback removes the F5 engine, fixture, projection, schema, workflow and read-only portal panel. Accepted F3/F4 evidence remains unchanged. Rollback performs no provider request and has no runtime or hardware effect.

## 11. Successor boundary

With F5 Accepted/Post-Merge Verified, **F6 — real-evidence setup-aware E2E planner integration** becomes the next separately governed BKL-031 slice. F6 must bind the accepted F4-C real forecast evidence values, governed setup compatibility, accepted astronomical/lunar evidence and the F5 explainable ranking method into a deterministic read-only end-to-end planner proof and portal consumer. F6 performs no new provider request and must preserve the exhausted `2/2_EXHAUSTED` budget, no protected-site use, no readiness/go-no-go, no scheduling, no automatic target selection, no commands and no Safety Authority. BKL-031 capability closure is explicitly deferred until a later separately governed forecast-refresh/runtime gate proves how fresh forecast evidence is supplied without weakening ADR-011 lineage or the safety boundary.
