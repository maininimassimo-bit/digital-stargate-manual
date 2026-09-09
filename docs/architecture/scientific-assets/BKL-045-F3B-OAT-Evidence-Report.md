# BKL-045 F3-B — OAT Evidence Report

- **Status:** PENDING REAL PIXINSIGHT EXECUTION
- **PR:** #137
- **Probe:** `tools/pixinsight/DigitalStarGateProvenanceProbe.js`
- **Authority:** evidence only
- **Action authority:** NONE

> This report must not be marked PASS from synthetic fixtures or repository CI. Populate it only from a real PixInsight execution.

## Execution identity

| Field | Evidence |
|---|---|
| Execution UTC | PENDING |
| Operator | PENDING |
| PixInsight version | PENDING |
| Host ID | PENDING |
| Workspace/project | PENDING |
| DSG session/OAT ID | PENDING |
| Target | PENDING |
| Probe commit SHA | PENDING |

## Captured sidecar

- Evidence file: `PENDING`
- Sidecar ID: `PENDING`
- Capture completeness: `PENDING`
- Observed processing-step count: `PENDING` — expected `0` for the bounded F3-B probe
- Declared processing-step count: `PENDING`
- Limitations: `PENDING`

## Repository validation

Run from a checkout containing the exact probe/validator under test:

```powershell
node .github/scripts/validate-pixinsight-workflow-provenance-file.mjs <captured-sidecar.json>
```

Record:

- validation result: `PENDING`
- canonical digest: `PENDING`

## Repeatability check

Execute the probe twice with unchanged semantic configuration. `exportedAt`, `sidecarId`, and declaration timestamps are capture-time identity and are expected to differ. Compare all remaining semantic fields.

- second evidence file: `PENDING`
- semantic comparison: `PENDING`
- unexplained differences: `PENDING`

## Non-mutation verification

| Check | Result |
|---|---|
| Image pixels changed by probe | PENDING; required NO |
| PixInsight process executed by probe | PENDING; required NO |
| AP-013/catalog state changed | PENDING; required NO |
| Network action performed | PENDING; required NO |
| Action authority | PENDING; required NONE |

## Outcome

`PENDING`

Allowed outcomes: `PASS`, `PASS WITH LIMITATION`, `FAIL`.

A `PASS WITH LIMITATION` may prove the bounded governed PJSR exporter while retaining the explicit limitation that complete processing history is not automatically observable. It does not authorize promotion of declared or inferred steps to `OBSERVED`.
