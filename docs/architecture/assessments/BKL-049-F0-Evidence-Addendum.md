# BKL-049 F0 — Reproducible evidence and gallery linkage addendum

Date: 2026-09-30. Status: RESEARCH / F0 OPEN. No F1 design acceptance, native runtime proof or production change.

This supplements the [F0 dossier](BKL-049-F0-SDK-Licensing-Feasibility-Dossier.md). The Owner's objective remains the entire PixInsight workflow associated with each Scientific Image Gallery image. A support subset is not an implicit substitute. During the Owner's absence, questions are queued below; no runtime authorization is inferred.

## 1. Versioned primary evidence

The [source registry](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/source-registry.json) records official repository URLs, immutable revisions, file paths and SHA-256 of Git blob contents. Hashes describe the inspected source, not a compiled or installed artifact. No vendor source is redistributed. PCL inspection uses revision `5a3902196a7d7a701385a7113cbdce2976ae1a85` (1.9.5 build 1706 / PCL 2.11.0) and historical revision `afea714e681853dfc21e70b5d53811ae41849e97` (PCL 2.10.4). PJSR revision `76e4f38c461320f07a0010bcc973fe26133f303a` is explicitly labelled for PixInsight 1.9.4 build 1695 in its commit metadata.

| Finding | Primary evidence | Classification and consequence |
|---|---|---|
| New SDK requires API 0x0188; older inspected header defines 0x0187 | PCL `include/pcl/api/APIInterface.h:27`; `src/pcl/API.cpp:118` rejects older runtime API | DOCUMENTED SOURCE. Exact Owner runtime API remains unmeasured; do not build latest SDK and assume it loads on 1695 |
| Extended image notification begins with 1696 and supplies a process pointer only for the same module | PCL `ProcessInterface.h`, extended notifications section; historical header lacks it | DOCUMENTED. Neither this notification on 1695 nor universal cross-module process capture is supported by this evidence |
| Official 1695 script serializes an initial process container into an image property | [BPP-Processing.js lines 196–203](https://gitlab.com/pixinsight/PJSR/-/blob/76e4f38c461320f07a0010bcc973fe26133f303a/src/scripts/BatchPreprocessing/BPP-Processing.js#L196) reads `mainView.initialProcessing`, serializes entries as XPSM 1.0 and writes `PixInsight:ProcessingHistory` | DOCUMENTED EXAMPLE, not a complete-history reader. Meaning and coverage of initial/current histories, script/global operations and reopening remain UNPROVEN. The writer was not executed |
| PCL supports reading image properties | PCL `FileFormatInstance.h`, `ReadImageProperty` / `ReadImageProperties`; `ImageOptions.h` has `embedProcessingHistory` default false | DOCUMENTED candidate extraction surface. Property presence, format, save preferences and actual history coverage require synthetic runtime proof. Class default is not the Owner's save configuration |
| Signing mechanism is present in official scripts | [SigningKeysGUI.js](https://gitlab.com/pixinsight/PJSR/-/blob/76e4f38c461320f07a0010bcc973fe26133f303a/src/scripts/SigningKeys/SigningKeysGUI.js#L87); [MSVC generator](https://gitlab.com/pixinsight/PJSR/-/blob/76e4f38c461320f07a0010bcc973fe26133f303a/src/scripts/MakefileGenerator/MakGenMSVC1xProjects.js#L316) | DOCUMENTED mechanism: local signing identity tied to license; generator invokes module signing with XSSK. Public distribution identity, entitlement and secure build procedure remain OPEN. No keys accessed or signing performed |
| Windows sample uses VC17/v143, C++20, x64, AVX2/FMA and linked PCL libraries | PCL Sandbox `.vcxproj` in registry | DOCUMENTED sample configuration. x64 alone does not establish AVX2/FMA availability. Exact Windows SDK version, library build recipe and installed compiler are not verified; no tool installed |

The signing generator can include a password argument. A future approved build must prevent credential exposure through command lines, logs or CI configuration; this observation is not permission to collect credentials. Source availability is not an application-license grant or proof of automated build entitlement.

### Preliminary linked-library notice inventory

The sample links PCL-pxi, lz4-pxi, zstd-pxi, zlib-pxi, RFC6234-pxi and lcms-pxi. Inspected notices are recorded in the registry: lcms has MIT terms; zstd has three-clause BSD terms; zlib has its origin/altered-source/notice restrictions; RFC6234 carries IETF Trust source/binary notice and non-endorsement conditions. LZ4's top-level license explicitly separates BSD-licensed library files from other GPL-licensed material. The actual selected compilation units and linked binaries must be inventoried before packaging; this is not a final SBOM or a conclusion that the whole dependency tree has one license. PCL and PJSR retain the PCL License 2.0.1 restrictions discussed in the dossier. No dependency or SDK binary is redistributed by this PR.

## 2. Reproducible contract findings

The isolated [probe instructions](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/README.md), [script](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/contract-probes.mjs) and [result](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/contract-probes.result.json) use synthetic data and existing DSG JavaScript functions. All twelve assertions reproduced their stated behavior. They do not execute PixInsight or certify full JSON Schema conformance. Synthetic OBSERVED labels only exercise the contract and do not become scientific evidence.

| Probe | Confirmed boundary | Requirement before native integration |
|---|---|---|
| C01 | `NATIVE_PCL` rejected by PXP 1.0 | Review capture-method/version semantics; never silently relabel native evidence |
| C02 | Reversed array with contiguous ordinal set passes validator; mapper retains reversed array | Establish one checked ordering invariant; preserve repeated executions rather than deduplicating by process name |
| C03 | Manifest omits per-step parameters and masks | Retain immutable rich sidecar/evidence alongside the AP14-W06 summary |
| C04 | 513 steps pass JS sidecar validation but exceed manifest's 512-process bound; sidecar schema ceiling is 2048 | Explicit overflow rejection or reviewed versioned representation; no truncation or silent split of a run |
| C05 | Ledger duplicate and same-ID conflict behave distinctly | Preserve byte-level idempotency; durable cross-restart journal remains separate work |
| C06 | Unresolved item with supplied asset ID passes JS validation and direct mapper selects that ID | Verify upstream resolution invariants; do not infer a proven image relationship from mapper output |
| C07 | Extra nested field passes JS validator despite schema prohibition | Full schema validation or equivalent reviewed boundary needed; this probe checks one constraint only |
| C08 | Read model copies arbitrary parameter text | Apply a reviewed privacy projection before public presentation; do not publish raw source strings |
| C09 | Read model accepts projection with no sidecar binding if acceptanceAuthority is false | Require positive sidecar/run/image binding in future gallery integration; unrelated projections must be rejected |
| C10–C11 | SUGGESTED rejected; UNAVAILABLE preserved | Retain fail-closed semantics through every consumer |
| C12 | Fresh export identity/time changes payload digest | Separate artifact integrity from semantic run identity and repeat-export equivalence |

C06/C09 are direct-call counterexamples, not claims of an exploitable production route. No upstream bypass or production behavior was changed. `REPRODUCED` is a research observation, including gaps, not a passing product acceptance gate.

## 3. Gallery association: required evidence chain

The current gallery uses a bounded fixture and textual references. Existing gallery/F2 archive contracts expose different reference families (`prov:pixinsight:...`, `workflow:pixinsight:...`, sidecar and manifest IDs). No prefix substitution establishes identity. The `PXP` prefix is also used for derived processing projection IDs; entity type must accompany the identifier.

A future reviewed design must demonstrate this chain with synthetic evidence first:

1. Gallery image ID resolves to its AP-013-authorized asset and the exact archived image version or derivative relationship; a filename or target name is insufficient.
2. That output resolves to an identified workflow run and step output, with input/mask relationships. Multi-output runs and multiple runs per image remain representable without overwriting history.
3. The run resolves to an immutable sidecar and retained source evidence, with digest, format/version, provenance and explicit completeness. AP14-W06 manifest/ledger/reconciliation remain derived processing evidence; they acquire no catalog acceptance or action authority.
4. A read-only public view exposes approved parameters and evidence status while private archival locators stay private. Gallery image availability and workflow completeness are independent states.
5. Missing, conflicting, orphaned, stale or redacted evidence remains visible as such. No green COMPLETE status follows merely from a successful upload, known process name, matched session or matching filename.

The authoritative archive and public gallery projection may require different retention/access policies. F0 does not select storage, upload data or grant deletion authority. The gallery's fixture ceiling (12 items), archive fixture ceiling (8 assets), and bounded reference arrays must not be mistaken for a production archive capacity promise.

### Required proof scenarios, not executed

| Scenario | Independent ground truth | Expected decision evidence |
|---|---|---|
| Built-in same-view process, repeated with different values | Approved synthetic execution log and saved process instances | Both executions, exact exposed values, correct ordering and image linkage |
| Cross-module and third-party process | Approved module/version inventory and synthetic log | Distinguish observable exposed parameters from inaccessible internals; mark missing detail explicitly |
| Script/global process with multiple inputs/outputs | Script/version, authorized arguments and independent output manifest | No assumption that per-view notifications enumerate internal operations; establish coverage per script family |
| Mask assigned, inverted, disabled, replaced and removed | Synthetic mask graph before/after each action | Preserve causal mask relationship and status, not just final mask name |
| Undo/redo, discarded branch, failed/aborted run | Independent event log and project snapshots | Distinguish final reconstruction history from all attempted actions; do not describe one as the other |
| Project save/reopen, renaming, close/restart | Synthetic project versions and stable asset mapping | Demonstrate continuity without private absolute paths or volatile view IDs |
| Saved history present/absent and reopened artifact | Synthetic image/property inventory | Present history proven; absent data produces PARTIAL/UNAVAILABLE, never inferred steps |
| Archive/export retry, conflict, large workflow, two images sharing a run | Synthetic IDs/digests and expected graph | Idempotency, no detail loss, no wrong-image attachment, explicit bounds |
| Public projection and missing evidence | Synthetic privacy markers and broken references | No private marker leak; no promotion of incomplete or declared data to observed complete history |

These are specifications for a separately approved experiment, not authorization to execute scientific processes, install modules or alter PixInsight. A native build alone cannot satisfy them.

## 4. Questions held for Owner return

No question is being sent during the requested absence. Environment reconfirmation is complete: 1.9.4 build 1695, Windows 11 Pro 25H2 build 26200.9550, x64. No hostname is needed.

First decision to present on return: whether the Owner authorizes a vendor clarification request concerning PCL License 2.0.1 and supported extraction interfaces. No message has been sent. Proposed inquiry content is concrete:

- Identify the permitted workflow for developing/distributing a DSG capture module with coding assistance under the license's automated-code-generation restrictions; clarify any required written permission, application/CI entitlement and dependency notices.
- Identify a supported SDK/API baseline for core 1695 and whether it can enumerate persisted and current histories with parameters, execution order, masks, global/script operations and project continuity across module boundaries.
- Clarify what `initialProcessing` and `PixInsight:ProcessingHistory` cover, and the supported way to retrieve current/project history without altering state; request explicit unsupported cases.
- Identify signing/distribution requirements for a third-party native module and supported reproducible Windows compiler/SDK configuration. Do not send account details, license files, keys or private datasets.

After that decision, ask one necessary question at a time: scope of an isolated synthetic runtime proof; relevant installed third-party process families; whether 'entire workflow' includes discarded/failed/undone actions as well as the final dependency graph; archival retention/access expectations. Until answered, preserve the broader objective and mark the distinction unresolved. No reduced scope is accepted by silence or elapsed time.

## 5. Gate update

G1 has a preliminary dependency/signing inventory but licensing and entitlement questions remain. G2 now has an explicit API-version mismatch risk and documented sample toolchain; runtime/build reproducibility remains unproven. G3 has a concrete history-property alternative to investigate, not a universal observer. G4 has twelve reproduced synthetic contract observations; it is no longer solely a static assessment, but end-to-end native/gallery compatibility is unproven. G5 remains NOT ACCEPTED. F0 stays OPEN; BKL-043 remains the current/next execution package and its monitor, pilot and protected PRs are unaffected.

Validation on 2026-09-30: 12/12 research assertions reproduced and saved JSON matched a fresh run; 37/37 existing provenance/manifest/ledger/reconciliation/read-model regression tests passed; roadmap generator/consistency checks passed with BKL-043 current/next. MkDocs strict build passed in 26.76 seconds after correcting research links to repository URLs. Targeted privacy and diff-whitespace checks passed. CI is verified separately on the PR head; these results do not establish SDK/runtime feasibility.

The follow-up [vendor inquiry and bounded proof protocol](BKL-049-F0-Vendor-Inquiry-and-Probe-Protocol.md) provides the complete unsent inquiry and staged experiment prerequisites, stop conditions and result requirements. Neither contact nor runtime execution has occurred.

## 6. Owner module inventory and upgrade candidate — 2026-09-30

Owner DECLARED regular use of RC Astro BlurXTerminator, NoiseXTerminator and StarXTerminator. At initial inventory, module/model versions and distribution were unknown. Subsequently the Owner confirmed the single unified RC Astro repository, completed the upgrade to PixInsight 1.9.5 build 1706 and reported the RC Astro tools working. This supersedes 1695 as the current DECLARED baseline. Exact RC Astro module/model versions remain unknown. No scientific processing, capture validation or independent runtime observation is inferred from the report.

Official RC Astro sources checked on 2026-09-30:

- [Installation instructions](https://www.rc-astro.com/pixinsight-installation-instructions/) cover all three products through PixInsight 1.9.5 via the unified repository `https://www.rc-astro.com/PixInsight`.
- [FAQ, tools disappeared or will not update](https://www.rc-astro.com/frequently-asked-questions/) explicitly states legacy individual repositories do not work with PixInsight 1.9.5.
- [Unified Suite announcement, 2026-07-27](https://www.rc-astro.com/unified-pixinsight-rc-astro-suite/) documents migration from individual repositories and changes/removal of some process parameters. Existing saved icons may show skipped-parameter warnings; scripts relying on removed parameters need adjustment.

This establishes vendor-declared compatibility for the unified distribution with the 1.9.5 family, not a verified installation on the Owner's workstation or proof of complete workflow capture. Before advising the upgrade, determine which repository/distribution is installed. No repository configuration, module, license activation, model download or application version was changed.

Research implications: each RC Astro test must identify product, module version and selected ML model version where exposed; record actual parameters, image inputs/outputs and evidence source. Missing model identity stays an explicit gap. Preserve original historical process representations and their version context; do not silently reinterpret old parameters using a newer module. StarXTerminator cases must check every actually generated output and its relationship to the input. Internal proprietary model computation is not claimed observable, and model binaries/weights are not collected or redistributed. These are proof requirements, not new runtime acceptance claims.

### Post-upgrade evidence boundary

Owner confirmation of the unified repository and successful upgrade is DECLARED evidence. PCL 2.11.0 source labels align with core 1706, and the documented minimum version for extended image notifications is met. This removes the earlier version-threshold obstacle, not the cross-module identity limitation. Historical 1695 analyses above remain comparisons; current SDK/load/signing tests and project/history/RC Astro capture coverage remain unproven. No further installation or processing authorization is inferred. The unsent vendor inquiry has been updated to target 1706.
