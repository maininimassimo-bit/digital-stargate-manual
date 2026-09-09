# BKL-045 F2 — PixInsight Extension Mechanism Assessment

**Status:** Proposed  
**Date:** 09/09/2026  
**Baseline:** `99fd9822334890baa7a82f4193a01ed9bbe2be2c`  

## Purpose

Assess the implementation mechanism for BKL-045 processing provenance capture using repository evidence and current PixInsight technical evidence. The assessment is limited to provenance capture/export; it does not authorize autonomous image processing.

## Repository baseline

The accepted F1 contract retains AP14-W06, `pixinsight-manifest.schema.json`, the manifest validator/digest, synchronization ledger, read-only reconciliation and processing projection as the integration baseline. AP-013 remains authoritative for scientific asset identity/checksum/lifecycle.

## External technical evidence

1. PixInsight exposes a maintained native module framework through PCL. Current PCL documentation continues to describe module/process/interface APIs and compatibility/deprecation rules.
2. PixInsight staff documentation/forum guidance confirms that **Projects** preserve images, processing histories and masking relationships and recreate them on reload.
3. Saved image processing history can be preserved as reference, while full undo/intermediate image states are a Project concern.
4. PJSR scripts integrate well with processes and can participate in processing histories through Script instances, but historical forum evidence documents limitations in script access/representation of processing history and workspace/history behavior. Therefore a script-only solution cannot be assumed to observe every arbitrary GUI/process action reliably.
5. Current PixInsight behavior also shows that command/script actions can create history entries when the implementation explicitly does so; this supports a controlled exporter/annotation layer but not universal interception by default.

## Options

### Option A — Native PCL module as primary capture mechanism

**Strengths**

- deepest integration with PixInsight process/module architecture;
- strongest theoretical access to native application structures;
- suitable if future evidence proves a stable supported API for complete event/history observation.

**Weaknesses**

- highest build, packaging and version-compatibility burden;
- greater coupling to PCL/API evolution;
- unnecessary complexity for the first provenance release when no requirement needs image-processing execution;
- repository evidence does not yet prove that a native module can globally intercept all third-party/native/script processing in a supported, stable way.

**Decision:** not selected for initial BKL-045 implementation.

### Option B — Governed PJSR script/package only

**Strengths**

- light deployment and local-first operation;
- easy integration with existing PixInsight scripting ecosystem;
- appropriate for sidecar export, user declarations, workflow metadata and reconciliation handoff;
- lower maintenance burden than a C++ module.

**Weaknesses**

- cannot be assumed to observe every process executed outside the script;
- historical evidence shows limitations around processing-history manipulation/introspection;
- a pure script-only model risks presenting incomplete capture as complete `OBSERVED` provenance.

**Decision:** retained as an important component, but not sufficient as the sole evidence source.

### Option C — Hybrid evidence capture + governed exporter

Use native PixInsight **Project / processing-history artifacts as the primary source of `OBSERVED` evidence where available**, complemented by a governed PixInsight script/package for:

- workflow/session correlation;
- explicit export to the Digital StarGate sidecar contract;
- capture of `DECLARED` manual operations/notes;
- environment metadata and source locators;
- validation and deterministic handoff into the existing AP14-W06 path.

A future PCL module remains an optional adapter if later evidence proves that it materially improves automatic observation coverage without breaking compatibility or operational simplicity.

**Strengths**

- aligns with PixInsight's own persistence model for complete project/history context;
- avoids falsely claiming that PJSR universally intercepts process execution;
- preserves a lightweight script/package for user-controlled export and declarations;
- local-first and does not require image upload;
- cleanly maps `OBSERVED` evidence to native artifacts and `DECLARED` evidence to explicit user input;
- keeps the AP14-W06 reconciliation path reusable.

**Weaknesses**

- Project/history formats and accessible metadata must be validated in F3 with real PixInsight evidence;
- some third-party/script processes may expose incomplete history details;
- portable sidecar generation may require bounded adapters per evidence source.

**Decision:** recommended.

## Weighted assessment

| Criterion | Weight | Native PCL | Script only | Hybrid |
|---|---:|---:|---:|---:|
| Evidence fidelity / fail-closed semantics | 25 | 20 | 13 | 23 |
| Version/upgrade resilience | 15 | 8 | 12 | 12 |
| Implementation/maintenance simplicity | 15 | 6 | 14 | 11 |
| Manual-workflow support | 10 | 6 | 9 | 10 |
| Local-first/privacy | 10 | 10 | 10 | 10 |
| Reuse of AP14-W06 | 10 | 6 | 10 | 10 |
| Testability without autonomous processing | 10 | 5 | 9 | 9 |
| Future extensibility | 5 | 5 | 3 | 5 |
| **Total / 100** | **100** | **66** | **80** | **90** |

The scores are architecture decision aids, not operational quality scores.

## Recommended F2 decision

Adopt **Option C — Hybrid evidence capture + governed exporter** for the first BKL-045 implementation:

1. native PixInsight Project/history evidence is treated as the preferred `OBSERVED` source when available and validated;
2. a governed PJSR package provides user-controlled export, session correlation and `DECLARED` annotations;
3. sidecars are versioned, deterministic and local-first;
4. ingestion continues through AP14-W06 validation/reconciliation rather than direct registry writes;
5. native PCL development is deferred unless F3 evidence identifies a specific observation gap that cannot be solved safely with the hybrid approach.

## F3 proof obligations

Before claiming implementation acceptance, F3 must demonstrate with real PixInsight evidence:

- what project/history information can be extracted without inventing fields;
- capture of ordered native process history for at least one real workflow;
- behavior for scripts and third-party modules;
- masks/reference relationships when available;
- deterministic export of the same evidence;
- explicit `DECLARED` manual step support;
- fail-closed handling when processing history is absent or incomplete;
- no image modification required for provenance export.

## Safety and authority

No observatory command authority, Safety Authority coupling, autonomous processing, remote script execution or external image upload is introduced by this decision.
