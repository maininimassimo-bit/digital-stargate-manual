# ARB-BKL-038-F1 — Independent Architecture Review — 2026-09-08

| Field | Value |
|---|---|
| Review ID | `ARB-BKL-038-F1` |
| Capability | BKL-038 — Anomaly & Trend Center |
| Scope | F1 — Source Discovery & Semantic Contract |
| PR | #120 |
| Reviewed HEAD | `76aff69c7b874c17fbb5cec2940a1bd5c26711d5` |
| Decision | **Approved** |
| Overall score | **98/100** |

## 1. Executive decision

The Architecture Review Board independently reviewed BKL-038 F1 against repository truth, the accepted BKL-030 and BKL-040 foundations, BKL-044 semantic governance, TD-012, current roadmap/backlog state and exact-head CI.

**Decision: Approved.**

No Blocker, Major or Minor finding prevents F1 acceptance. The contract keeps anomaly/trend analysis downstream of accepted evidence, preserves source authority and historical temporal semantics, separates descriptive trend measurements from anomaly candidates, requires explicit governed rules for anomaly classification, prohibits invented thresholds and causal claims from correlation alone, and preserves the read-only/advisory and Safety boundaries.

## 2. Verified exact-head evidence

Reviewed branch: `architecture/bkl-038-anomaly-trend-center`  
Reviewed HEAD: `76aff69c7b874c17fbb5cec2940a1bd5c26711d5`

Exact-head workflows:

- Genera manuale Word #1125 — SUCCESS;
- Validate documentation #700 — SUCCESS;
- Developer Foundation #1081 — SUCCESS.

The PR contains one architecture-contract file only and introduces no runtime implementation.

## 3. Review scores

| Dimension | Score | Assessment |
|---|---:|---|
| Program / roadmap consistency | 100 | BKL-038 is current and dependency-ready over accepted BKL-030 + BKL-040 foundations. |
| Source authority separation | 99 | EAGLE history, BKL-040 replay and downstream read models are clearly distinguished by fact-class authority. |
| Semantic model integrity | 100 | Observation, trend measurement, anomaly candidate, correlation candidate and recommendation are explicitly distinct. |
| Temporal integrity | 100 | BKL-040 `event_time_utc`, `PLACED/UNPLACED` and immutable source timestamps are preserved. |
| Explainability / provenance | 100 | Derived records require method/version, source refs, Citation/Provenance, window and reason codes. |
| Data quality / fail-closed behavior | 99 | UNKNOWN/INCOMPLETE/CONFLICTED/UNSUPPORTED remain explicit and cannot become healthy/normal. |
| Threshold / inference governance | 100 | No statistical or operational threshold is invented; correlation is explicitly non-causal. |
| TD-012 compatibility | 100 | Accepted `source_event_id` / `replay_event_id` debt is acknowledged without silent retrofit. |
| Safety / command boundary | 100 | Action authority remains NONE; no remediation/device command/Safety Authority is introduced. |
| Runtime / operational isolation | 100 | F1 is repository-only; no PC/EAGLE collector, scheduler, service or API is introduced. |
| Migration / rollback | 98 | Additive documentation-only increment; rollback is repository revert. |
| F2 readiness | 95 | Semantic boundary is sufficient; repository-resolvable bounded fixtures must be materialized before executable analysis. |

## 4. Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observation — ARB-BKL-038-F1-O01 — Repository-resolvable fixture boundary for F2

BKL-030 G6 historical records originate from the accepted runtime persistence contract. F2 must not make CI or deterministic schema validation depend on access to the live EAGLE filesystem.

**Disposition:** non-blocking for F1. F2 must use a bounded, immutable repository fixture or governed evidence projection traceable to accepted BKL-030 history records. The fixture must preserve upstream identifiers, timestamps, quality, source and provenance and must not become a new source authority.

## 5. Explicit architecture checks

### 5.1 Source coverage honesty

Approved. The contract does not claim that all functional-roadmap channels are already available. It starts only from accepted BKL-030 history and channels/events actually present in accepted BKL-040 artifacts.

### 5.2 Descriptive trend vs anomaly classification

Approved. Numeric deltas, aggregates, counts and direction may be descriptive measurements; they do not become anomalies without an explicit governed rule.

### 5.3 Unknown / stale handling

Approved. Historical quality is interpreted at observation time. Missing evidence is never coerced to zero, normal or healthy.

### 5.4 Correlation vs causation

Approved. Temporal co-occurrence and directional relationships remain correlation candidates and cannot be promoted to root cause without separately governed inference semantics.

### 5.5 BKL-044 inheritance

Approved. Citation, Provenance, lifecycle and semantic-type preservation are mandatory for derived analytical records.

### 5.6 BKL-040 compatibility debt

Approved. TD-012 remains visible and BKL-038 consumes the accepted replay contract rather than rewriting it.

### 5.7 Safety and remediation boundary

Approved. No anomaly or trend can command dome, mount, camera, power, network, services or Safety state. Local physical interlocks remain independent.

## 6. F2 entry conditions

F2 may begin only after:

1. this ARB review is repository-integrated;
2. Release Quality confirms F1 merge readiness;
3. final exact-head CI is green;
4. PR #120 is merged with expected-head protection;
5. post-merge applicable workflows are green.

F2 must then provide:

- a versioned machine-readable analytical-record schema;
- bounded repository-resolvable fixtures derived from accepted evidence;
- deterministic identity rules;
- explicit quality enums and fail-closed validation;
- at least one descriptive trend example and one anomaly-candidate example driven only by an already-governed rule/data-quality exception;
- negative tests proving that invented thresholds and unsupported causal claims are rejected.

## 7. Re-review criteria

ARB re-review is required if F1/F2 scope changes to introduce:

- arbitrary statistical thresholds or severity policy;
- predictive-maintenance claims without a separately governed method;
- causal/root-cause promotion from correlation alone;
- automatic remediation or command execution;
- Safety Authority integration;
- new runtime collectors or permanent EAGLE workload;
- new source families not already accepted;
- silent changes to BKL-030/BKL-040 upstream semantics.

## 8. Final decision

**APPROVED — 98/100.**

BKL-038 F1 is architecturally coherent and may proceed to Release Quality review. F2 remains blocked until F1 is merged and post-merge validation is complete.