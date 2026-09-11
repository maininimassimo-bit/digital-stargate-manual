# BKL-045 F3-A — Provenance Sidecar Contract and Validation

**Status:** Accepted — BKL-045 closure  
**Version:** 1.0  
**Release:** RC3  
**Baseline:** `03615533d2edbe2bd4f22ea7963b617f070ab1ea`

## 1. Purpose

Implement the first executable repository-side vertical slice of ADR-008 without claiming PixInsight runtime evidence that has not yet been observed.

## 2. Scope

F3-A introduces:

- `pixinsight-workflow-provenance.schema.json` sidecar contract;
- deterministic canonicalization and SHA-256 digest;
- fail-closed validation for `OBSERVED` and `DECLARED` steps;
- ordered-step integrity;
- explicit completeness/limitations;
- negative tests for invented provenance and action authority;
- a dedicated GitHub governance workflow.

F3-A does **not** implement or validate the PixInsight-side PJSR exporter and does not claim access to Project/history fields.

## 3. Architectural drivers

ADR-008 selected hybrid native evidence + governed exporter. F1 requires `OBSERVED` facts to have evidence and `DECLARED` facts to remain explicitly user-declared. AP14-W06 remains the downstream synchronization/reconciliation boundary.

## 4. Current state

The accepted PixInsight synchronization manifest 1.0 is intentionally coarse and remains unchanged. It carries processes, inputs, outputs and parameters for AP14-W06 synchronization. It is not replaced by F3-A.

## 5. Target state

The provenance sidecar is a richer local evidence artifact. A later F3-B exporter may produce it from validated PixInsight-native evidence plus explicit user declarations. The sidecar can then be mapped into the existing AP14-W06 path; it cannot directly mutate the scientific catalog.

## 6. Contract rules

- `authority` is fixed to `processing_evidence`.
- `actionAuthority` is fixed to `NONE`.
- executed step evidence classes are only `OBSERVED` and `DECLARED`; `SUGGESTED` is rejected.
- every `OBSERVED` step requires at least one source locator.
- every `DECLARED` step requires declaration identity and timestamp.
- step ordinals start at 1, are unique and contiguous.
- `PARTIAL` and `UNAVAILABLE` captures require explicit limitations.
- an `UNAVAILABLE` capture cannot contain `OBSERVED` steps.
- unresolved asset references remain unresolved.
- deterministic canonical JSON produces a deterministic SHA-256 digest.

## 7. Compatibility

`docs/contracts/pixinsight-manifest.schema.json` version 1.0 remains supported and unchanged. F3-B/F4 must define the explicit mapping from the richer sidecar into the existing synchronization envelope or a separately governed compatible revision.

## 8. Security, safety and operations

The sidecar is local-first metadata. It grants no device command authority, no Safety Authority, no autonomous processing authority and no AI apply authority. No image binary upload is required by this contract.

## 9. Validation

Repository CI validates JSON parseability and Node contract tests. Runtime evidence remains Not Executed until F3-B/OAT is run inside a real supported PixInsight environment.

## 10. F3-B proof obligations

F3-B must provide real evidence for:

1. actual PixInsight/PJSR version and environment;
2. one real ordered workflow history;
3. fields actually observable from Project/history;
4. script/third-party process behavior;
5. masks/references where actually exposed;
6. repeated deterministic sidecar export;
7. explicit `DECLARED` manual step capture;
8. fail-closed incomplete/unavailable history behavior;
9. confirmation that export does not modify image-processing state.

No F3-B item may be marked passed from synthetic repository fixtures alone.

## 11. Acceptance criteria

F3-A is acceptable when the schema, validator, negative tests and dedicated governance workflow pass on the exact feature HEAD, with the PixInsight runtime/OAT gate explicitly remaining open for F3-B.
