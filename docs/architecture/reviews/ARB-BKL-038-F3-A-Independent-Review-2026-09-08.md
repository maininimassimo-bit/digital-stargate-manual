# ARB-BKL-038-F3-A — Independent Architecture Review — 2026-09-08

| Field | Value |
|---|---|
| Review ID | `ARB-BKL-038-F3-A` |
| Capability | BKL-038 — Anomaly & Trend Center |
| Scope | F3-A — Deterministic Derived Identity Contract |
| PR | #122 |
| Reviewed HEAD | `0d643f018c725aa2ea0ec58a44e557d75cdd3532` |
| Base at review | `92cec8ab9b89602960b2cd3ca9369ce52a64e72f` |
| Decision | **Approved** |
| Overall score | **98/100** |

## 1. Executive decision

The Architecture Review Board independently reviewed BKL-038 F3-A after the feature branch was synchronized with the current `main` baseline that includes the EAGLE inventory update from PR #123.

**Decision: APPROVED — 98/100.**

No Blocker, Major or Minor findings prevent acceptance of F3-A. The slice is bounded to canonical deterministic identity generation and does not introduce anomaly thresholds, detector policy, runtime execution, causal inference, predictive maintenance, remediation authority or Safety Authority.

## 2. Exact-head evidence

Reviewed branch: `architecture/bkl-038-f3-deterministic-engine`  
Reviewed HEAD: `0d643f018c725aa2ea0ec58a44e557d75cdd3532`

Exact-head workflows:

- Genera manuale Word #1140 — SUCCESS;
- Validate documentation #715 — SUCCESS;
- Developer Foundation #1096 — SUCCESS.

Developer Foundation #1096 explicitly executed and passed:

- `Verify BKL-038 F2 analytical fixture`;
- `Test BKL-038 F2 fail-closed rules`;
- `Test BKL-038 F3 deterministic identity`;
- roadmap/backlog consistency;
- MkDocs strict build.

## 3. Architecture assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Upstream contract alignment | 100 | Identity tuple matches accepted F1 semantics and is applied downstream of accepted F2-A. |
| Deterministic identity method | 100 | Versioned method `BKL038-F3-DERIVED-ID-SHA256-1` is explicit and testable. |
| Canonical serialization | 99 | Fixed property order and compact JSON serialization are explicit; known-answer test prevents silent drift. |
| Idempotence | 100 | Same semantic tuple produces the same SHA-256 identifier. |
| Identity sensitivity | 100 | Semantic type, method version, ordered source refs and analysis window are tested as identity-significant. |
| Identity neutrality | 100 | Non-identity fields are tested not to perturb derived identity. |
| Fail-closed semantics | 98 | Missing core identity inputs fail closed; further schema-level restrictions remain inherited from F2. |
| Citation / Provenance boundary | 100 | Citation/Provenance do not drive logical identity but remain mandatory downstream semantics through F2/F1 contracts. |
| TD-012 compatibility | 100 | No upstream replay identity retrofit or `source_event_id` fabrication is introduced. |
| EAGLE evidence boundary | 100 | No BKL-030 signal-history onboarding occurs; prior ARB observation remains open. |
| Runtime / operational isolation | 100 | Repository-only Node.js validation logic; no EAGLE/PC workload, service, scheduler or API. |
| Safety / remediation boundary | 100 | No command, remediation or Safety Authority is introduced. |
| Migration / rollback | 99 | Additive repository-only change; rollback is repository revert. |
| F3-B readiness | 93 | Identity foundation is ready; dynamic derivation remains separately gated by accepted evidence and semantic constraints. |

## 4. Explicit review checks

### 4.1 Canonical identity tuple

Approved. The algorithm uses exactly:

1. `semantic_type`;
2. `method_id`;
3. `method_version`;
4. ordered `source_record_refs`;
5. `analysis_window.start_utc`;
6. `analysis_window.end_utc`.

No measurement, quality, presentation or explanation payload can silently change logical identity.

### 4.2 Known-answer and idempotence evidence

Approved. The fixed F2-A CloudWatcher-to-N.I.N.A. trend tuple has a repository known-answer SHA-256 identifier and the same tuple reproduces the same identifier on exact-head CI.

### 4.3 Source-order semantics

Approved. Source order is deliberately identity-significant and is regression-tested. No sorting or hidden normalization is performed.

### 4.4 Temporal integrity

Approved. Timestamp strings participate as declared evidence values. F3-A does not parse/rewrite timestamps and therefore does not degrade accepted BKL-040 sub-millisecond precision.

### 4.5 No anomaly fabrication

Approved. F3-A contains no anomaly rule, score, threshold or severity policy and cannot create a positive anomaly candidate by itself.

### 4.6 Correlation / causation boundary

Approved. F3-A does not alter F2 correlation semantics and introduces no causal/root-cause promotion.

### 4.7 EAGLE history onboarding

Not authorized. The prior observation remains open: BKL-030 EAGLE history may only be onboarded when a bounded, accepted, repository-resolvable evidence sample/projection exists preserving upstream identity, timestamps, quality, source and provenance.

### 4.8 Runtime and Safety

Approved. No PC/EAGLE command is required. Local physical interlocks remain independent and authoritative.

## 5. Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observations

1. The PR description still states the original F2-A baseline SHA even though the branch has since been synchronized with current `main`. GitHub base/head metadata and this review record are the current merge authority; the stale prose does not alter the package contract.
2. F3-A deliberately validates the identity algorithm only. F3-B must not interpret this approval as authorization for arbitrary anomaly detection, new source families, causal inference or runtime execution.
3. The open EAGLE repository-fixture observation remains carried forward unchanged.

## 6. Decision

**APPROVED — 98/100.**

BKL-038 F3-A is architecturally coherent and may proceed to Release Quality review after this ARB artifact is repository-integrated and exact-head CI is green again.

## 7. Re-review criteria

ARB re-review is required if subsequent changes introduce or alter:

- the canonical identity tuple;
- serialization order or hashing algorithm;
- source-order significance;
- timestamp normalization;
- anomaly thresholds or severity policy;
- causal/root-cause inference;
- BKL-030 EAGLE history onboarding;
- runtime collectors/services/schedulers;
- command/remediation authority;
- Safety Authority or interlock boundaries;
- upstream BKL-040 identity semantics.
