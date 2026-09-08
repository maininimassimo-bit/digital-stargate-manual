# BKL-038 F3-B — Deterministic Read-Only Trend Engine

| Field | Value |
|---|---|
| Identifier | `BKL-038-F3-B` |
| Capability | BKL-038 — Anomaly & Trend Center |
| Status | In Progress |
| Version | 0.1 |
| Base | BKL-038 F1, F2-A and accepted F3-A identity contract |
| Runtime impact | None — repository/CI only |
| Safety impact | None — local physical Safety Authority unchanged |

## 1. Objective

F3-B is the first executable analytical-engine slice. It projects bounded, deterministic and descriptive analytical records from the already accepted BKL-040 F3 replay evidence. It does not introduce anomaly thresholds, severity policy, prediction, causal inference, command authority or remediation.

## 2. Inputs and authority

The only executable input in this slice is `docs/data/night-timeline-replay-f3.json`. Its accepted `events` and `correlations` remain upstream evidence. F3-B never mutates them and does not promote browser/UI state to source authority.

BKL-030 EAGLE history remains outside this executable slice until a bounded immutable repository-resolvable fixture or governed evidence projection exists. F3-B must not read a live EAGLE filesystem and must not fabricate EAGLE records.

## 3. Component

`.github/scripts/anomaly-trend-engine.mjs` exposes `projectAnomalyTrend(replay)`.

The component:

1. requires input authority `projection`;
2. accepts only `PLACED` replay events for this bounded projection;
3. preserves replay source references, Citation and Provenance references;
4. emits one `OBSERVATION` per accepted event;
5. emits one descriptive `TREND_MEASUREMENT` per accepted BKL-040 `SEQUENTIAL` correlation using the already accepted `delta_ms` value;
6. requires upstream method `BKL040-F3-EXACT-DELTA-1` and classification `NOT_ASSESSED`;
7. generates derived identities through accepted F3-A method `BKL038-F3-DERIVED-ID-SHA256-1`;
8. emits `authority=projection` and `action_authority=NONE` on projection and records;
9. rejects duplicate derived identities.

The engine deliberately consumes accepted `delta_ms` instead of recomputing timestamps through JavaScript `Date`, preserving the accepted sub-millisecond BKL-040 evidence.

## 4. F3-B methods

### `BKL038-F3B-SOURCE-OBSERVATION-1` version `1.0`

Creates a source-preserving observation for a `PLACED` replay event. It does not reinterpret event meaning or assign severity.

### `BKL038-F3B-EXACT-DELTA-PROJECTION-1` version `1.0`

Creates a descriptive trend measurement from an accepted BKL-040 exact-delta correlation. Measurement unit is `ms`, `descriptive_only=true`, `candidate_state=null` and `rule_id=null`.

A temporal delta is not an anomaly and not evidence of causation.

## 5. Quality semantics

Accepted replay quality `CURRENT` maps to analytical `CURRENT_AT_OBSERVATION`. Any other source quality is preserved conservatively as `UNKNOWN` in this bounded slice; it is never converted to healthy/normal.

No current-time freshness is inferred from historical evidence.

## 6. Fail-closed rules

F3-B rejects:

- non-projection input authority;
- `UNPLACED` events rather than inventing placement;
- duplicate replay identities;
- unresolved correlation source references;
- non-`SEQUENTIAL` correlations;
- correlation methods other than accepted `BKL040-F3-EXACT-DELTA-1`;
- correlation classifications other than `NOT_ASSESSED`;
- negative, non-numeric or non-finite `delta_ms`;
- duplicate derived identities.

F3-B contains no threshold configuration, anomaly severity mapping, root-cause classifier, prediction or remediation path.

## 7. Deterministic bounded fixture expectations

For the accepted BKL-040 F3 fixture, the engine produces exactly five records: three observations and two descriptive trend measurements. The accepted trend values remain exactly `6163877.6 ms` and `5300122.4 ms`.

Known-answer derived IDs are asserted in the repository test suite so serialization or identity drift fails CI.

## 8. Validation

`.github/scripts/test-anomaly-trend-f3b-engine.mjs` validates deterministic repeatability, known-answer identities, exact accepted deltas, Citation/Provenance presence, authority immutability and negative fail-closed cases.

Developer Foundation must execute this suite before F3-B can enter independent ARB review.

## 9. Operational and Safety boundary

F3-B is repository/CI-only. It creates no EAGLE process, service, Scheduled Task, listener, device command, restart, USB reset, network change, filesystem cleanup or Safety integration.

Local physical interlocks remain the sole physical Safety Authority. Historical analysis cannot infer or override present-time safe/unsafe state.

## 10. Deferred work

- BKL-030 EAGLE historical analytical onboarding remains blocked on repository-resolvable governed evidence.
- Anomaly candidates require an explicit governed rule/pattern; none is introduced here.
- Statistical/predictive methods require separate governance and validation.
- Consumer/portal read model remains a later F4 slice.
