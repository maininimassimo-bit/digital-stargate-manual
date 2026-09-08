# BKL-038 F3-B — Deterministic Read-Only Trend Engine

| Field | Value |
|---|---|
| Identifier | `BKL-038-F3-B` |
| Capability | BKL-038 — Anomaly & Trend Center |
| Status | In Progress — ARB remediation |
| Version | 0.2 |
| Base | BKL-038 F1, F2-A and accepted F3-A identity contract |
| Runtime impact | None — repository/CI only |
| Safety impact | None — local physical Safety Authority unchanged |

## 1. Objective

F3-B is the first executable analytical-engine slice. It projects bounded, deterministic and descriptive analytical records from the already accepted BKL-040 F3 replay evidence. It does not introduce anomaly thresholds, severity policy, prediction, causal inference, command authority or remediation.

## 2. Inputs and authority

The only executable input in this slice is `docs/data/night-timeline-replay-f3.json`. Its accepted `events`, `correlations`, `citations` and `provenance_records` remain upstream evidence. F3-B never mutates them and does not promote browser/UI state to source authority.

BKL-030 EAGLE history remains outside this executable slice until a bounded immutable repository-resolvable fixture or governed evidence projection exists. F3-B must not read a live EAGLE filesystem and must not fabricate EAGLE records.

## 3. Component

`.github/scripts/anomaly-trend-engine.mjs` exposes `projectAnomalyTrend(replay)`.

The component:

1. requires input authority `projection`;
2. accepts only `PLACED` replay events for this bounded projection;
3. preserves replay source references, Citation and Provenance references;
4. resolves every emitted Citation/Provenance reference against the bounded replay evidence and fails closed on empty or unresolved references;
5. emits one `OBSERVATION` per accepted event;
6. emits one descriptive `TREND_MEASUREMENT` per accepted BKL-040 `SEQUENTIAL` correlation using the already accepted `delta_ms` value;
7. requires upstream method `BKL040-F3-EXACT-DELTA-1` and classification `NOT_ASSESSED`;
8. generates derived identities through accepted F3-A method `BKL038-F3-DERIVED-ID-SHA256-1`;
9. emits `authority=projection` and `action_authority=NONE` on projection and records;
10. rejects duplicate derived identities.

The engine deliberately consumes accepted `delta_ms` instead of recomputing timestamps through JavaScript `Date`, preserving the accepted sub-millisecond BKL-040 evidence.

## 4. F3-B methods

### `BKL038-F3B-SOURCE-OBSERVATION-1` version `1.0`

Creates a source-preserving observation for a `PLACED` replay event. It does not reinterpret event meaning or assign severity.

### `BKL038-F3B-EXACT-DELTA-PROJECTION-1` version `1.0`

Creates a descriptive trend measurement from an accepted BKL-040 exact-delta correlation. Measurement unit is `ms`, `descriptive_only=true`, `candidate_state=null` and `rule_id=null`.

A temporal delta is not an anomaly and not evidence of causation.

## 5. Quality semantics

F3-B uses an explicit observation-time mapping for accepted replay quality:

- `CURRENT` -> `CURRENT_AT_OBSERVATION`;
- `STALE` -> `STALE_AT_OBSERVATION`;
- `UNKNOWN` -> `UNKNOWN`.

Any other source quality fails closed; it is not silently collapsed into `UNKNOWN` or converted to healthy/normal.

For a two-event trend, any stale input produces `STALE_AT_OBSERVATION`; otherwise any unknown input produces `UNKNOWN`; only two current inputs produce `CURRENT_AT_OBSERVATION`.

No current-time freshness is inferred from historical evidence.

## 6. Fail-closed rules

F3-B rejects:

- non-projection input authority;
- `UNPLACED` events rather than inventing placement;
- unsupported source quality states;
- duplicate replay identities;
- unresolved correlation source references;
- empty or unresolved Citation references;
- empty or unresolved Provenance references;
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

`.github/scripts/test-anomaly-trend-f3b-engine.mjs` validates deterministic repeatability, known-answer identities, exact accepted deltas, Citation/Provenance resolution, authority immutability, explicit stale/unknown quality behavior and negative fail-closed cases.

Developer Foundation executes this suite before F3-B can re-enter independent ARB review.

## 9. ARB remediation traceability

Initial independent ARB on exact head `76e9d68f2e8e8034cdabee5ee56334d144d1e47e` issued `REWORK REQUIRED — 90/100`.

- **M01 — quality semantics collapsed:** remediated structurally by explicit `CURRENT`, `STALE`, `UNKNOWN` mapping, fail-closed unsupported values and regression tests.
- **M02 — Citation/Provenance integrity not fail-closed:** remediated structurally by mandatory non-empty references, bounded evidence resolution and mutation tests for empty/unresolved references.

These remediations do not expand the accepted source inventory or runtime/Safety authority. Final resolution remains subject to exact-head CI and independent ARB re-review.

## 10. Operational and Safety boundary

F3-B is repository/CI-only. It creates no EAGLE process, service, Scheduled Task, listener, device command, restart, USB reset, network change, filesystem cleanup or Safety integration.

Local physical interlocks remain the sole physical Safety Authority. Historical analysis cannot infer or override present-time safe/unsafe state.

## 11. Deferred work

- BKL-030 EAGLE historical analytical onboarding remains blocked on repository-resolvable governed evidence.
- Anomaly candidates require an explicit governed rule/pattern; none is introduced here.
- Statistical/predictive methods require separate governance and validation.
- Consumer/portal read model remains a later F4 slice.
