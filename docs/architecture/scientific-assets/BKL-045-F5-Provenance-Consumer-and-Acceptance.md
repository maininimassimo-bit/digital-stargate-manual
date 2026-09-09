# BKL-045 F5 — PixInsight Provenance Consumer and Acceptance

**Identifier:** BKL-045-F5  
**Status:** Proposed  
**Release:** RC3

## 1. Objective

Complete the BKL-045 delivery chain with a bounded read-only consumer model for PixInsight workflow provenance and acceptance evidence. F5 consumes the F3 provenance sidecar and, when available, the F4 AP14-W06 reconciliation projection. It does not create a new source of truth.

## 2. Consumer contract

The canonical builder is `.github/scripts/pixinsight-provenance-read-model.mjs`.

The consumer MUST:

- preserve `OBSERVED` and `DECLARED` evidence classes exactly;
- never expose `SUGGESTED` data as executed provenance;
- surface capture completeness as `AVAILABLE`, `PARTIAL` or `UNAVAILABLE` without inference;
- retain all source limitations;
- preserve AP-013 authority for scientific assets and provenance;
- treat AP-014 reconciliation as a derived catalog projection only;
- expose `acceptanceAuthority=false` and `actionAuthority=NONE`;
- fail closed on authority escalation or mismatched sidecar/projection correlation.

## 3. Real-evidence acceptance baseline

F5 uses the accepted real PixInsight OAT evidence captured during F3-B:

`docs/architecture/scientific-assets/evidence/BKL-045-F3B-PXP-20260909T212858612Z-OAT.json`

That evidence has `capture.completeness=UNAVAILABLE`, zero observed processing steps and zero declared processing steps. The F5 consumer therefore MUST render provenance state `UNAVAILABLE`; it MUST NOT invent a process history or interpret the active PixInsight view as evidence of executed processing steps.

This is an intentional acceptance condition, not a defect. It proves the consumer preserves the bounded evidence actually captured by PixInsight 1.9.4 build 1695 on the OAT workstation.

## 4. F4 reconciliation boundary

When an F4 processing projection is supplied, F5 may expose its projection identifier, reconciliation state and catalog item identifier. It may do so only when the projection references the same provenance sidecar and carries no acceptance authority.

F5 does not write AP-013 assets, AP-014 catalog state, PixInsight workspaces, images, devices or Safety Authority state.

## 5. Validation

`.github/scripts/test-pixinsight-provenance-read-model.mjs` verifies:

1. the real F3-B OAT sidecar remains `UNAVAILABLE` and read-only;
2. declared steps remain `DECLARED` and do not become observed;
3. action-authority escalation is rejected;
4. mismatched F4 projection linkage is rejected;
5. any projection carrying acceptance authority is rejected.

Repository CI remains machine validation. The F3-B real-runtime OAT remains the runtime evidence; CI does not replace it.

## 6. Acceptance gates

F5 may be accepted only after:

- exact-head CI is green;
- the real F3-B evidence is exercised by the F5 consumer regression test;
- independent Architecture Review Board approval;
- Release Quality readiness approval;
- protected merge;
- post-merge verification on the actual `main` merge SHA.

## 7. Retained limitation

BKL-045 still does not claim automatic extraction of complete ordered PixInsight process history. F5 exposes that limitation faithfully. A future richer native-history adapter may increase evidence completeness only after separate governed runtime evidence and review.

## 8. Safety and authority

F5 is presentation/read-model only. It introduces no process execution, image mutation, device control, remediation, network upload, AI apply path or Safety Authority coupling.
