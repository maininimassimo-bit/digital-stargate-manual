# ARB-BKL-040-CLOSURE — Independent Architecture Review

**Decision:** Approved  
**Date:** 2026-09-08  
**Scope:** BKL-040 — Night Timeline / Observatory Replay final closure, PR #118  
**Reviewed branch:** `docs/bkl-040-final-closure`  
**Reviewed head:** `c3ea176edb8865b05bf8b60051741fe2af1489cf`  
**Base:** `80d22a255540ac582733c60dfe9bbf7807bcdf9b`  
**Overall score:** **100/100**

## 1. Independence statement

This review is an independent assessment of the package as found at the reviewed exact head. No package remediation was performed during the assessment. The review record itself is written only after the architecture decision was reached.

## 2. Repository truth and evidence reviewed

The review verified the live repository, PR #118, the BKL-040 F1-F4 chain, final closure, backlog, canonical roadmap source, generated roadmap projection, Technical Debt Register including TD-012, current continuity documentation, and exact-head CI.

Exact-head validation evidence for `c3ea176edb8865b05bf8b60051741fe2af1489cf`:

- Developer Foundation #1075 — SUCCESS;
- Validate documentation #694 — SUCCESS;
- Genera manuale Word #1119 — SUCCESS.

The reviewed branch is a linear descendant of `main` base `80d22a255540ac582733c60dfe9bbf7807bcdf9b`.

## 3. Review dimensions

| Dimension | Score | Evidence / assessment |
|---|---:|---|
| F1-F4 acceptance integrity | 100/100 | Closure records all four merged increments with exact merge SHAs and preserves their accepted boundaries. |
| Temporal contract integrity | 100/100 | Canonical UTC, `PLACED/UNPLACED`, no invented timestamp and deterministic ordering remain explicit. |
| F1/F2 compatibility debt disposition | 100/100 | TD-012 explicitly records the bounded envelope/tie-break incompatibility and prohibits silent retrofit. |
| Source-order / tie-break traceability | 100/100 | F1 `source_event_id` versus accepted downstream `replay_event_id` divergence is surfaced as debt rather than hidden. |
| Channel coverage honesty | 100/100 | Executable foundation is bounded; no false claim that Power/Network/Safety are historical BKL-040 channels. |
| Authority / projection boundary | 100/100 | Replay, roadmap data and consumer models remain projections and do not promote source authority. |
| Replay operational boundary | 100/100 | Consumer remains `READ_ONLY` / `VISUAL_ONLY`; historical command execution and remediation are explicitly prohibited. |
| Safety boundary | 100/100 | Local physical interlocks / Safety Authority remain independent; no Safety delegation, bypass or present-time inference is introduced. |
| Dependency and roadmap consistency | 100/100 | BKL-037 remains Planned pending BKL-045; BKL-038 is the first dependency-ready successor based on accepted BKL-030 + BKL-040. |
| Continuity documentation | 100/100 | 08/09 bootstrap, baseline, Context, Knowledge Map, backlog, roadmap, debt and workflow hierarchy are aligned. |
| Migration / rollback | 100/100 | Changes are additive repository projections; rollback is repository revert with no runtime/hardware migration requirement. |
| CI / repository quality evidence | 100/100 | Exact-head Developer Foundation, documentation and Word workflows are all green. |

## 4. Explicit ARB checks requested for closure

### 4.1 BKL-040 F1-F4 acceptance

Verified. F1 through F4 are merged and the closure correctly distinguishes increment acceptance from final package integration.

### 4.2 Bounded channel coverage

Verified. F3/F4 executable materialization is not represented as complete implementation of every channel listed by the functional roadmap. N.I.N.A., PHD2 and CloudWatcher are the principal synchronized executable sources, with session projection where defined. SQM/EAGLE remain separate foundations/candidates; Power/Network/Safety are not falsely materialized.

### 4.3 TD-012 / F1-F2 compatibility debt

Verified and accepted as P2 technical debt. The closure does not invalidate prior acceptance and does not silently retrofit the F2 baseline.

### 4.4 `source_event_id` versus `replay_event_id`

Verified as a known bounded compatibility divergence. It must be handled only by a future versioned compatibility/migration increment with fail-closed tests and ARB review.

### 4.5 Authority/projection boundaries

Verified. Replay and portal consumers remain projection-only and preserve source authority, Citation and Provenance.

### 4.6 Replay `READ_ONLY` / `VISUAL_ONLY`

Verified. No execution path, remediation authority, device command or operational playback is authorized.

### 4.7 Safety Authority independence

Verified. Historical evidence cannot become present-time Safety Authority and local physical interlocks remain authoritative.

### 4.8 Backlog / roadmap / closure consistency

Verified on the reviewed head. BKL-040 is completed, BKL-038 is current/active and the generated roadmap is semantically aligned with the canonical source.

### 4.9 BKL-037 blocked by BKL-045

Verified. BKL-037 is not dependency-ready while BKL-045 remains Planned.

### 4.10 BKL-038 dependency readiness

Verified. Its declared dependencies BKL-030 and BKL-040 are accepted.

### 4.11 Continuity documentation 08/09

Verified. The root bootstrap points to the 08/09 handover/current baseline and the mandatory Context/Knowledge Map/governance sequence is represented consistently.

### 4.12 No false Power/Network/Safety coverage

Verified. Closure and Technical Debt review explicitly preserve bounded source coverage and prohibit fabricated channels.

## 5. Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observations

1. Historical F1/F2 architecture documents retain proposal-era status headers. They are treated as historical increment artifacts; current acceptance authority is the merged PR/evidence/closure chain. They should not be rewritten merely to restate current status.
2. The public GitHub Pages Roadmap remains pre-closure until PR #118 is merged to `main` and the authoritative Pages workflow deploys. This is an expected pre-merge state, not evidence of architecture inconsistency on the reviewed branch.
3. GitHub PR metadata has intermittently reported `mergeable=false` despite `main` remaining at the PR base and the branch being a linear descendant. Release Quality must independently verify actual merge readiness immediately before merge; this ARB decision does not override repository merge protection.

## 6. Decision

**APPROVED — 100/100.**

The BKL-040 final closure is architecturally coherent, bounded, traceable and safe to advance to Release Quality review. The accepted TD-012 debt is explicit and does not invalidate F1-F4 acceptance. No Power/Network/Safety historical coverage is implied, replay remains read-only/visual-only, and local Safety Authority remains independent.

## 7. Re-review criteria

ARB re-review is required if, before merge, any change alters:

- BKL-040 source/channel coverage;
- F1/F2/F3/F4 temporal or ordering contracts;
- authority, Citation/Provenance or lifecycle semantics;
- replay command/remediation behavior;
- Safety Authority or physical-interlock boundaries;
- dependency ordering for BKL-037/BKL-038;
- TD-012 disposition.

A commit that only records this review or Release Quality evidence does not by itself change the architecture decision, but exact-head CI must still be re-verified before merge.