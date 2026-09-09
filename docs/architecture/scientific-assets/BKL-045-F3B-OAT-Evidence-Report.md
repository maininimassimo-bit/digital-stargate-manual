# BKL-045 F3-B — OAT Evidence Report

- **Status:** REAL PIXINSIGHT RUN 1 CAPTURED; repeatability and repository validation pending
- **PR:** #137
- **Probe:** `tools/pixinsight/DigitalStarGateProvenanceProbe.js`
- **Authority:** evidence only
- **Action authority:** NONE

> This report must not be marked PASS from synthetic fixtures or repository CI. Evidence below comes from a real PixInsight execution supplied by the operator on 2026-09-09.

## Execution identity — run 1

| Field | Evidence |
|---|---|
| Execution UTC | `2026-09-09T21:28:58.612Z` |
| Operator | Massimo Mainini |
| PixInsight version | `1.9.4 build 1695` |
| Host ID | `WIN-QOOF3903TQS` |
| Workspace/project | `PIXINSIGHT-OAT-20260909-231843` |
| DSG session/OAT ID | `OAT-BKL045-F3B-20260909-231843` |
| Target | `BKL-045-F3B-OAT` |
| Active PixInsight view | `M64` |
| Probe commit SHA | `266b7c36b1feeebc57426e508b03ce66c178c45c` |

## Captured sidecar — run 1

- Evidence file: `docs/architecture/scientific-assets/evidence/BKL-045-F3B-PXP-20260909T212858612Z-OAT.json`
- Sidecar ID: `PXP-20260909T212858612Z-OAT`
- Capture completeness: `UNAVAILABLE`
- Observed processing-step count: `0`
- Declared processing-step count: `0`
- Source evidence observed by the bounded probe: PixInsight runtime version and active view identifier.
- Limitations:
  - `PJSR_PILOT_DOES_NOT_CLAIM_ACCESS_TO_COMPLETE_PIXINSIGHT_PROCESS_HISTORY`
  - `NO_OBSERVED_PROCESSING_STEP_IS_EMITTED_BY_THIS_PROBE`
  - `ACTIVE_WINDOW_ID_ONLY_IS_AUTOMATICALLY_OBSERVED`

The `UNAVAILABLE` result is an expected fail-closed outcome for processing history. It proves that the bounded pilot does not fabricate processing steps when complete history is not available through its governed observation surface. It does **not** prove automatic process-history provenance.

## Repository validation

Run from a checkout containing the exact probe/validator under test:

```powershell
node .github/scripts/validate-pixinsight-workflow-provenance-file.mjs docs/architecture/scientific-assets/evidence/BKL-045-F3B-PXP-20260909T212858612Z-OAT.json
```

Record:

- validation result: `PENDING`
- canonical digest: `PENDING`

## Repeatability check

Execute the probe twice with unchanged semantic configuration. `exportedAt` and `sidecarId` are capture-time identity and are expected to differ. Declaration timestamps would also be expected to differ if declared steps were present. Compare all remaining semantic fields.

- run 1: `PXP-20260909T212858612Z-OAT`
- second evidence file: `PENDING`
- semantic comparison: `PENDING`
- unexplained differences: `PENDING`

## Non-mutation verification

| Check | Result |
|---|---|
| Image pixels changed by probe | No mutation path exists in the bounded probe; operator/runtime confirmation pending final OAT sign-off |
| PixInsight process executed by probe | No process-execution path exists in the bounded probe |
| AP-013/catalog state changed | No catalog-write path exists in the bounded probe |
| Network action performed | No network path exists in the bounded probe |
| Action authority | `NONE` — observed in real sidecar |

## Interim assessment

**RUN 1: PASS WITH EXPECTED LIMITATION; F3-B OAT NOT YET COMPLETE.**

Run 1 demonstrates real PixInsight execution, runtime/version observation, active-view observation, `actionAuthority=NONE`, and fail-closed behavior for unavailable processing history. Final F3-B OAT acceptance requires repository validation of the captured sidecar and a second real execution with unchanged semantic configuration for repeatability.

A final `PASS WITH LIMITATION` may prove the bounded governed PJSR exporter while retaining the explicit limitation that complete processing history is not automatically observable. It does not authorize promotion of declared or inferred steps to `OBSERVED`.
