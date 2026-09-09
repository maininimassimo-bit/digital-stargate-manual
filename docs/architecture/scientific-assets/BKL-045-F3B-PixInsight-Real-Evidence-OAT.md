# BKL-045 F3-B — PixInsight Real-Evidence OAT

- **Status:** Proposed / OAT pending
- **Version:** 1.0
- **Target:** BKL-045 F3
- **Decision:** ADR-008
- **Baseline:** F3-A accepted on `main` at `90122fd6ee55213abbbd6de98a22297c26fbef85`

## Purpose

Execute the first real PixInsight-side provenance pilot without fabricating processing history and without introducing command, safety, image-processing, or catalog-write authority.

## Pilot component

`tools/pixinsight/DigitalStarGateProvenanceProbe.js`

The pilot is intentionally bounded. It emits a workflow-provenance sidecar to the PixInsight console between `DSG_PXP_BEGIN` and `DSG_PXP_END` markers.

It does not:

- mutate an image;
- execute a PixInsight process;
- write the DSG catalog or AP-013 registry;
- use network access;
- claim access to complete PixInsight processing history;
- emit any processing step as `OBSERVED`.

## Evidence classification

Automatically read environment evidence may be represented only by source locators that name the actual PJSR observation point, for example the PixInsight application version and active image-window identifier.

Processing steps entered in the probe configuration are `DECLARED`. They require `declaredBy` and the export timestamp. They are not promoted to `OBSERVED`.

If complete processing history cannot be read through the governed pilot, the sidecar remains `PARTIAL` or `UNAVAILABLE` and records an explicit limitation. No reconstruction, inference, or fuzzy matching is allowed.

## OAT procedure

1. Use a workstation on which PixInsight is installed. This does not need to be the observatory EAGLE unless that is where the processing workflow actually runs.
2. Use an existing non-critical processing workspace or a disposable test image. The probe does not need to process the image.
3. Obtain `tools/pixinsight/DigitalStarGateProvenanceProbe.js` from the exact accepted F3-B branch/commit under test.
4. Edit only the `CONFIG` block:
   - `sessionId`: real DSG scientific-session identifier when available; otherwise use an explicitly labelled OAT identifier and do not correlate it authoritatively;
   - `target`: actual target;
   - `hostId`: actual workstation identity;
   - `workspaceId`: actual PixInsight workspace/project label used for the test;
   - `workflowId` and `runId`: unique OAT identifiers;
   - `declaredBy`: operator identity;
   - `declaredSteps`: optional operations the operator explicitly declares. Remove the example comment and add only operations the operator can attest to.
5. In PixInsight, run the script through the normal script execution facility appropriate to the installed PixInsight version.
6. Copy the JSON printed between `DSG_PXP_BEGIN` and `DSG_PXP_END` exactly as emitted. Do not hand-edit evidence fields after capture.
7. Save the captured JSON outside the image dataset as an OAT evidence file.
8. Validate the captured JSON with the repository F3-A validator before it is used for any DSG projection.
9. Run the probe a second time without changing the configured semantic inputs. Compare the semantic payload after excluding capture-time identity fields (`exportedAt`, `sidecarId`, declaration timestamps). Record whether the semantic result is stable.
10. Confirm by inspection that the test image/workspace was not modified by the probe.

## Acceptance evidence to record

The OAT report must include:

| Evidence | Required result |
|---|---|
| PixInsight version read from runtime | Present or explicitly unsupported |
| active image/window identifier | Present when an active window exists, otherwise explicit null limitation |
| sidecar validates against F3-A semantics | PASS |
| processing steps automatically observed | Zero for this bounded probe unless a later governed source adapter is implemented |
| declared steps | Preserved as `DECLARED` only |
| history limitation | Explicit; no inferred history |
| repeated semantic export | Deterministic for unchanged semantic inputs |
| image mutation | None |
| catalog/AP-013 mutation | None |
| action authority | `NONE` |

## OAT outcome states

- **PASS:** real PixInsight execution produced valid evidence, classification is correct, repeatability is demonstrated, and no mutation occurred.
- **PASS WITH LIMITATION:** same as PASS, but process-history extraction remains unavailable; the limitation becomes an input to the next source-adapter decision.
- **FAIL:** invalid sidecar, evidence misclassification, nondeterministic semantic output, unexpected image/catalog mutation, or runtime error that prevents evidence capture.

## F3-B completion rule

Repository CI can validate the probe source and contract integration, but cannot satisfy this OAT. F3-B must not be declared accepted for real `OBSERVED` provenance until a real PixInsight execution has produced reviewable evidence.

A PASS WITH LIMITATION is sufficient to prove the governed PJSR pilot boundary, but is not sufficient to claim automatic process-history provenance. Any richer history adapter requires separate evidence and review under ADR-008.
