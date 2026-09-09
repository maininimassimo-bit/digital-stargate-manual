# BKL-045 F3-B — OAT Evidence Report

- **Status:** PASS WITH LIMITATION
- **PR:** #137
- **Probe:** `tools/pixinsight/DigitalStarGateProvenanceProbe.js`
- **Authority:** evidence only
- **Action authority:** NONE

> This result is based on two real PixInsight executions supplied by the operator on 2026-09-09. Repository CI or synthetic fixtures alone do not satisfy this OAT.

## Execution identity

| Field | Evidence |
|---|---|
| Operator | Massimo Mainini |
| PixInsight version | `1.9.4 build 1695` |
| Host ID | `WIN-QOOF3903TQS` |
| Workspace/project | `PIXINSIGHT-OAT-20260909-231843` |
| DSG session/OAT ID | `OAT-BKL045-F3B-20260909-231843` |
| Target | `BKL-045-F3B-OAT` |
| Active PixInsight view | `M64` |
| Probe baseline commit | `266b7c36b1feeebc57426e508b03ce66c178c45c` |

## Real execution — run 1

- Execution UTC: `2026-09-09T21:28:58.612Z`
- Sidecar: `PXP-20260909T212858612Z-OAT`
- Evidence: `docs/architecture/scientific-assets/evidence/BKL-045-F3B-PXP-20260909T212858612Z-OAT.json`
- Completeness: `UNAVAILABLE`
- Observed processing steps: `0`
- Declared processing steps: `0`

## Real execution — run 2

- Execution UTC: `2026-09-09T21:33:16.284Z`
- Sidecar: `PXP-20260909T213316284Z-OAT`
- Evidence: `docs/architecture/scientific-assets/evidence/BKL-045-F3B-PXP-20260909T213316284Z-OAT.json`
- Completeness: `UNAVAILABLE`
- Observed processing steps: `0`
- Declared processing steps: `0`

## Repeatability

PASS.

With unchanged semantic configuration and the same active PixInsight view, the two real captures are semantically identical after excluding the expected capture-identity fields `exportedAt` and `sidecarId`.

Unexplained semantic differences: **none**.

Both runs independently report:

- PixInsight `1.9.4 build 1695`;
- host `WIN-QOOF3903TQS`;
- active view `M64`;
- `captureMethod=GOVERNED_PJSR_EXPORT`;
- `actionAuthority=NONE`;
- processing-history completeness `UNAVAILABLE`;
- `observedStepCount=0`;
- `declaredStepCount=0`;
- limitations `PJSR_PILOT_DOES_NOT_CLAIM_ACCESS_TO_COMPLETE_PIXINSIGHT_PROCESS_HISTORY`, `NO_OBSERVED_PROCESSING_STEP_IS_EMITTED_BY_THIS_PROBE`, and `ACTIVE_WINDOW_ID_ONLY_IS_AUTOMATICALLY_OBSERVED`.

## Repository validation

The operator workstation did not have `node` available, so the standalone CLI validator could not be executed there. This is an environment/tooling limitation, not a sidecar validation failure.

The exact-head repository CI remains the required machine validation gate for the schema/validator and must be green after this evidence commit before merge. Final acceptance must not claim local Node validation.

## Non-mutation / authority boundary

| Check | Result |
|---|---|
| Image mutation path in probe | NONE |
| PixInsight process execution path | NONE |
| AP-013/AP-014/catalog write path | NONE |
| Network path | NONE |
| Action authority | `NONE`, confirmed in both real sidecars |
| Safety Authority change | NONE |

## Outcome

**PASS WITH LIMITATION.**

The OAT proves the bounded governed PJSR exporter executes repeatably in a real PixInsight 1.9.4 runtime, observes runtime/version and active-view identity, preserves `actionAuthority=NONE`, and fails closed when complete processing history is unavailable.

The retained limitation is material: this F3-B pilot does **not** demonstrate automatic extraction of complete PixInsight processing history and therefore does not authorize any processing step to be promoted to `OBSERVED`. A richer native-history adapter, if required, remains a separate governed evolution under ADR-008.

Final PR acceptance still requires exact-head CI plus independent Architecture Review Board and Release Quality gates.
