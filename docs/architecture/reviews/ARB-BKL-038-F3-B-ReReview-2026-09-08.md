# ARB-BKL-038-F3-B — Independent Re-Review — 2026-09-08

| Field | Value |
|---|---|
| Review ID | `ARB-BKL-038-F3-B-R2` |
| Capability | BKL-038 — Anomaly & Trend Center |
| Scope | F3-B — Deterministic Read-Only Trend Engine |
| PR | #124 |
| Reviewed HEAD | `e83d90e2c64fbb4628dfbf4ade3680be5b4262f7` |
| Decision | **Approved** |
| Overall score | **98/100** |

## 1. Executive decision

The Architecture Review Board independently re-reviewed BKL-038 F3-B after the prior `REWORK REQUIRED — 90/100` decision.

**Decision: APPROVED — 98/100.**

The two Major findings are closed by repository evidence and exact-head CI. The scope remains bounded to deterministic, descriptive, read-only analytical projection over accepted BKL-040 replay evidence.

## 2. Exact-head validation evidence

Reviewed branch: `architecture/bkl-038-f3b-readonly-engine`  
Reviewed HEAD: `e83d90e2c64fbb4628dfbf4ade3680be5b4262f7`

Exact-head workflows:

- Genera manuale Word #1147 — SUCCESS;
- Validate documentation #722 — SUCCESS;
- Developer Foundation #1103 — SUCCESS.

Developer Foundation #1103 explicitly executed and passed `Test BKL-038 F3-B deterministic read-only engine`.

## 3. Prior finding closure

### M01 — observation-time quality semantics collapsed

**Closed.** The engine now uses an explicit governed mapping:

- `CURRENT` -> `CURRENT_AT_OBSERVATION`;
- `STALE` -> `STALE_AT_OBSERVATION`;
- `UNKNOWN` -> `UNKNOWN`.

Unsupported quality values fail closed instead of being silently converted. Two-event trend quality propagates stale conservatively, then unknown, and returns current only when both inputs are current. Regression tests cover stale propagation and unsupported-quality rejection.

### M02 — Citation/Provenance integrity not fail-closed

**Closed.** Citation and Provenance references must now be non-empty and each `id@version` must resolve against the accepted replay `citations` / `provenance_records` collections. Regression tests cover empty and unresolved references for both observation and correlation-derived records.

## 4. Architecture assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Source authority | 100 | Accepted BKL-040 replay remains upstream evidence; engine output remains projection only. |
| Determinism | 100 | F3-A SHA-256 identity contract is reused without modification. |
| Temporal integrity | 100 | Accepted `delta_ms` values are preserved directly; no timestamp precision loss. |
| Quality semantics | 100 | Current/stale/unknown are explicit and unsupported quality fails closed. |
| Citation/Provenance | 100 | Non-empty and resolvable evidence references are enforced. |
| Threshold/severity governance | 100 | No threshold, score or severity policy is introduced. |
| Correlation/causation boundary | 100 | Trend remains descriptive; no causal or root-cause promotion. |
| Fail-closed behavior | 99 | Source, quality, evidence and correlation contract violations are rejected. |
| Runtime isolation | 100 | Repository/CI-only implementation; no PC/EAGLE runtime dependency. |
| Safety/remediation boundary | 100 | No command, remediation or Safety Authority is introduced. |
| Migration/rollback | 99 | Additive repository-only change; rollback is repository revert. |
| Future-source readiness | 91 | EAGLE history remains correctly blocked pending governed repository-resolvable evidence. |

## 5. Explicit review checks

### 5.1 No anomaly fabrication

Approved. F3-B emits only source-preserving observations and descriptive trend measurements. `candidate_state` and `rule_id` remain null for trends.

### 5.2 Evidence lineage

Approved. Citation/Provenance references are preserved and validated against bounded upstream collections.

### 5.3 Historical quality

Approved. Historical stale is not rewritten as current or unknown and no present-time freshness is inferred.

### 5.4 Identity and TD-012

Approved. Derived IDs use the accepted F3-A contract and do not replace upstream replay identifiers or retrofit BKL-040 TD-012 semantics.

### 5.5 Runtime and Safety

Approved. No collector, service, scheduler, device command, restart, power/network action or Safety integration is introduced. Local physical interlocks remain independent and authoritative.

## 6. Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observation

BKL-030 EAGLE analytical onboarding remains blocked until bounded, accepted, repository-resolvable history evidence exists. This approval does not authorize fabrication or live-filesystem dependency.

## 7. Decision

**APPROVED — 98/100.**

BKL-038 F3-B may proceed to Release Quality review after this review artifact is repository-integrated and exact-head CI is green again.

## 8. Re-review criteria

ARB re-review is required if later changes introduce or alter:

- accepted source families;
- quality-state semantics;
- Citation/Provenance resolution rules;
- deterministic identity method;
- anomaly thresholds/severity;
- causal/root-cause inference;
- predictive maintenance;
- runtime collectors/services;
- command/remediation authority;
- Safety Authority or physical interlock boundaries.
