# ARB-BKL-038-F2-A — Independent Re-Review — 2026-09-08

| Field | Value |
|---|---|
| Review ID | `ARB-BKL-038-F2-A-R2` |
| Capability | BKL-038 — Anomaly & Trend Center |
| Scope | F2-A — Machine-readable analytical schema and bounded fixture |
| PR | #121 |
| Reviewed HEAD | `c934d70a2cfaec07eb9ae95c34f43ab48d8b44b2` |
| Decision | **Approved** |
| Overall score | **98/100** |

## 1. Executive decision

The Architecture Review Board independently re-reviewed BKL-038 F2-A after the prior **REWORK REQUIRED** decision.

**Decision: APPROVED — 98/100.**

The three rework findings are closed by verified repository evidence and exact-head CI. The remaining EAGLE-fixture observation is non-blocking for this bounded F2-A slice and remains a mandatory entry condition for any future BKL-030 signal-history onboarding.

## 2. Exact-head validation evidence

Reviewed branch: `architecture/bkl-038-f2-analytical-schema`  
Reviewed HEAD: `c934d70a2cfaec07eb9ae95c34f43ab48d8b44b2`

Exact-head workflows:

- Genera manuale Word #1133 — SUCCESS;
- Validate documentation #708 — SUCCESS;
- Developer Foundation #1089 — SUCCESS.

Developer Foundation #1089 explicitly executed and passed:

- `Verify BKL-038 F2 analytical fixture`;
- `Test BKL-038 F2 fail-closed rules`.

## 3. Prior finding closure

### ARB-BKL-038-F2-A-M01 — F2 validator not executed by Developer Foundation

**Closed.** Developer Foundation now contains and executes the F2 positive validator. Exact-head run #1089 step 39 completed SUCCESS.

### ARB-BKL-038-F2-A-M02 — Missing negative fail-closed regression suite

**Closed.** `.github/scripts/test-anomaly-trend-f2.mjs` now mutates the bounded fixture and verifies fail-closed rejection of:

- trend self-promotion to anomaly;
- rule match without governed rule identity;
- correlation promotion;
- causation-guard removal;
- unresolved source/Citation/Provenance;
- authority escalation;
- action-authority escalation.

Exact-head run #1089 step 40 completed SUCCESS.

### ARB-BKL-038-F2-A-m01 — Deterministic identity claim not proven

**Closed by scope correction.** F2-A now claims only bounded-fixture ID uniqueness. The normative deterministic identity tuple from F1 remains required, while canonical serialization/generation is explicitly deferred to F3. F2-A does not claim that human-authored fixture IDs prove deterministic generation.

### ARB-BKL-038-F2-A-O01 — Repository-resolvable BKL-030 EAGLE history fixture

**Open observation, non-blocking for F2-A.** The slice correctly refuses to fabricate EAGLE signal history and keeps CI independent from the live EAGLE filesystem. Any future F2-B onboarding of BKL-030 history must use a bounded, accepted, repository-resolvable evidence sample/projection preserving upstream identity, timestamps, quality, source and provenance.

## 4. Architecture assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Source authority / projection boundary | 100 | Fixture resolves only accepted BKL-040 repository evidence and remains projection-only. |
| Semantic contract | 100 | Observation, trend and correlation candidate semantics remain distinct; no fabricated anomaly is introduced. |
| Citation / Provenance | 100 | Source, Citation and Provenance references resolve and are fail-closed. |
| Temporal integrity | 100 | Exact delta is verified against accepted BKL-040 correlation evidence, preserving sub-millisecond precision. |
| Threshold / severity governance | 100 | No arbitrary threshold, severity band or anomaly score is introduced. |
| Correlation / causation boundary | 100 | Correlation remains `NOT_ASSESSED` and requires `CAUSATION_NOT_INFERRED`. |
| Fail-closed validation | 100 | Positive and negative validators are part of Developer Foundation and pass on exact head. |
| Identity semantics | 96 | F2-A correctly narrows claims; deterministic generation remains a required F3 deliverable. |
| Runtime isolation | 100 | No runtime collector, EAGLE filesystem dependency, service or scheduler is introduced. |
| Safety / remediation boundary | 100 | `authority=projection`, `action_authority=NONE`; no Safety or remediation authority. |
| Migration / rollback | 98 | Additive repository-only slice; rollback is repository revert. |
| F2-B readiness | 84 | BKL-040 bounded slice is ready; EAGLE-history onboarding remains blocked pending governed repository-resolvable evidence. |

## 5. Explicit re-review checks

### 5.1 Exact temporal evidence

Approved. The validator no longer derives the accepted `6163877.6 ms` value through JavaScript `Date` precision. It compares the F2 measurement directly with accepted BKL-040 correlation evidence and verifies `BKL040-F3-EXACT-DELTA-1` plus upstream `NOT_ASSESSED` classification.

### 5.2 No fabricated anomaly

Approved. The bounded fixture contains observation, descriptive trend and correlation candidate only. No anomaly candidate is manufactured from evidence that lacks a governed anomaly rule.

### 5.3 No invented thresholds

Approved. No z-score, percentage threshold, severity cutoff or predictive boundary is added.

### 5.4 Upstream compatibility

Approved. F2-A consumes accepted BKL-040 `replay_event_id` semantics and does not retrofit TD-012 or manufacture `source_event_id` values.

### 5.5 Runtime and Safety

Approved. No PC/EAGLE execution is required. Local physical interlocks remain independent and authoritative.

## 6. Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observation

`ARB-BKL-038-F2-A-O01` remains open and carried forward: do not onboard BKL-030 EAGLE signal history until an accepted, bounded, repository-resolvable evidence sample/projection exists.

## 7. Decision

**APPROVED — 98/100.**

BKL-038 F2-A is architecturally acceptable and may proceed to Release Quality review.

The approval is bounded to the current BKL-040-derived fixture/schema/validator slice. It does not authorize F2-B EAGLE-history materialization, anomaly thresholds, causal inference, predictive maintenance, command execution, automatic remediation or Safety Authority.

## 8. Re-review criteria

ARB re-review is required if the package introduces:

- new source families;
- BKL-030 EAGLE history materialization without governed repository evidence;
- deterministic ID generation not governed by a versioned algorithm;
- anomaly/severity thresholds;
- causal/root-cause inference;
- predictive maintenance claims;
- runtime collectors/services;
- command/remediation or Safety Authority;
- upstream semantic rewrites.
