# BKL-049 F0 — SDK, licensing and feasibility dossier

| Field | Value |
|---|---|
| Identifier | DSG-BKL-049-F0-001 |
| Version / date | 0.1 / 2026-09-30 |
| Status | IN PROGRESS — F0 NOT CLOSED; F1 NOT AUTHORIZED BY THIS DOSSIER |
| Scope | Official-source research, Owner-assisted artifact evidence, read-only identity/header checks and isolated nonproduction experiments |
| Repository baseline | `b848f9416693bdce0ab0b20a331e709d5028510e` — origin/main including PR #444 |
| Branch | `codex/bkl-049-f0` |
| Authority | Processing evidence only; `actionAuthority=NONE` |

## 1. Recommendation and current state

**Real identity follow-up:** the [local evidence index report](BKL-049-F0-Real-Identity-Evidence-Index.md) records a measured final-file digest and embedded-history corroboration of the Owner-declared association. The saved history contains the matching recombination and two further processes. The unrelated first candidate is excluded; the checked-in archive fixture has no matching digest. No gallery association or complete capture is claimed.

**Latest evidence:** the [Owner-assisted history report](BKL-049-F0-Owner-Assisted-History-Evidence.md) documents a rich project export, RC Astro instances, mask history and explicit recombination references. These make the artifact route concrete but do not establish complete coverage. Vendor contact is deferred at Owner request; sanitized public documentation is authorized. F0 remains OPEN.

**Owner-confirmed product objective (2026-09-30): archive the entire PixInsight workflow and associate it with the corresponding images in the [Scientific Image Gallery](https://maininimassimo-bit.github.io/digital-stargate-manual/scientific-image-gallery/).** The gallery image must be an entry point to its archived workflow: ordered steps, available execution parameters, inputs/outputs, masks, run/project continuity, evidence sources and explicit gaps. Association must use governed scientific asset identity and exact AP14-W06 reconciliation, not filenames or visual similarity. Multiple outputs or processing versions must retain their own run/asset relationships rather than silently overwrite lineage.

This is the acceptance objective, not a claim of current capability. A bounded support matrix is an evidence instrument, not permission to redefine “entire workflow” as only the convenient subset. Any material reduction requires an explicit Owner decision. Unsupported activity remains PARTIAL/UNAVAILABLE and prevents a complete-workflow claim; manual DECLARED entries do not silently satisfy automatic OBSERVED capture. A standalone event log or archive disconnected from gallery images does not meet the objective.

Repository inspection shows the current gallery uses a governed fixture with metadata/provenance references and non-materialized previews (`docs/scientific-image-gallery/index.md`, `docs/javascripts/bkl-034-image-gallery.js`). It does not demonstrate a real end-to-end image/workflow archive. The supplied live URL could not be retrieved by the research browser; no live-page verification is claimed. Gallery linkage remains an explicit F4/F5 end-to-end proof obligation, preserving AP-013 asset authority and the existing public-data boundary.

**Do not approve a universal passive native workflow recorder on the evidence available. Continue bounded F0 verification.** PCL provides useful instance, image and mask interfaces, but the inspected documentation does not establish a supported cross-module execution stream with process identity, execution-time parameters, complete lineage and project continuity. A reduced support matrix or a history-artifact adapter may be feasible; neither is selected or proven here. A platform upgrade alone does not resolve the cross-module limitation.

The Owner authorized F0 in parallel with BKL-043 on 2026-09-30. BKL-043 remains the current open package; its monitor, pilot, PRs #428/#438/#439 and runtime permissions are outside this work. A separate worktree was created from freshly fetched origin/main. The app worktree action was unavailable for this projectless chat (not a Git repository), so Git worktree creation was used against the existing repository without changing its checkout branch or files.

The [BKL-045 closure](../../project/BKL-045-CLOSURE-2026-09-10.md) and [F3-B report](../scientific-assets/BKL-045-F3B-OAT-Evidence-Report.md) remain accepted: repeatable export, zero automatically observed steps, `UNAVAILABLE` processing history. Historical claims about BKL-031 being current in the original BKL-049 plan are superseded by the current roadmap. Older AP14-W06 solution-document status does not override the later accepted BKL-045 F4 integration.

## 2. Evidence method and official sources

Access date: **2026-09-30**. Public official PCL repository retrieved using Git into an isolated research directory outside the DSG worktree. No SDK installation, compilation, module loading or PixInsight execution occurred. No vendor source is copied into this PR. File/member locators below are reproducible against immutable revisions; research facts are distinct from runtime `OBSERVED` workflow evidence.

Official current revision: **`5a3902196a7d7a701385a7113cbdce2976ae1a85`**, commit dated 2026-09-28, labelled **PixInsight 1.9.5 Lockhart build 1706 / PCL 2.11.0**. This is the retrieved SDK revision, not proof of the installed application version or a compatible binary.

| ID | Official source and locator | Evidence use |
|---|---|---|
| S1 | [PCL README](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/README.md), repository layout, Supported Compilers, Environment Variables | Availability and documented toolchain |
| S2 | [PCL LICENSE](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/LICENSE), version 2.0.1, 29 December 2025; same version in COPYING.md | Actual conditions override the README's BSD-like shorthand |
| S3 | [ProcessInterface.h](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/include/pcl/ProcessInterface.h), image notifications 1767–1861, mask notifications 2060–2150, process notifications 2341–2415 | Notification semantics and explicit version limitation |
| S4 | [ProcessInstance.h](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/include/pcl/ProcessInstance.h), Version, GetExecutionTimes, ToSource, ToHistorySource, ParameterValue, TableRowCount | Instance serialization is not an execution subscription |
| S5 | [ImageWindow.h](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/include/pcl/ImageWindow.h), Processing History, Mask, IsMaskEnabled, IsMaskInverted | Core history ownership and current mask state |
| S6 | [ProcessImplementation.h](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/include/pcl/ProcessImplementation.h), BeforeExecution/AfterExecution and global counterparts | Callbacks implemented by the process itself, not a universal observer |
| S7 | [PCL 2.10.4 ProcessInterface.h](https://gitlab.com/pixinsight/PCL/-/blob/afea714e681853dfc21e70b5d53811ae41849e97/include/pcl/ProcessInterface.h), image/process notifications | Historical comparison; exact 1695 SDK pairing still unproven |
| S8 | [Sandbox Windows project](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/src/modules/processes/Sandbox/windows/vc17/Sandbox.vcxproj) | Example v143, C++20 and DLL CRT settings; not a tested DSG build |
| S9 | [Version.h](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/include/pcl/Version.h) and [Process.h](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/include/pcl/Process.h) | Runtime version/build and installed-process metadata candidates |
| S10 | [XISF options documentation in source](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/src/modules/file-formats/XISF/XISFOptionsDialog.cpp), processing-history option | Optional embedded XML history candidate, not proven full-run capture |
| S11 | [Microsoft Visual Studio Community usage](https://visualstudio.microsoft.com/vs/community/) | Individual/organization eligibility differs; verify applicable 2022 terms before acquisition |

The PixInsight developer HTML and license website could not be retrieved through the research browser. The official Git repository supplied the primary license and API evidence; search snippets and third-party forks were not used as acceptance evidence. Current signing, developer credentials, application-license/CI entitlement and exact ABI pairing remain unresolved; no claim that an inaccessible page has been verified.

## 3. SDK access, use and distribution

Public read access to the official PCL repository succeeded without purchasing or installing anything. S2 permits source/binary use and redistribution, including modification, subject to retained notices, conditions, restrictions and disclaimer; binary distributions must reproduce them in accompanying materials. Product documentation/materials must include the required PixInsight acknowledgment. Names cannot imply vendor endorsement without written permission. Dependencies under third-party directories require their own notice/license inventory before packaging.

**Material restriction:** S2 prohibits training machine-learning/code-generation systems on this source, inclusion in their training corpora, and providing API services incorporating or deriving from the software for automated code generation; exceptions require written vendor permission. This dossier does not treat the SDK as unrestricted BSD, authorize AI-assisted PCL code generation, or decide that every form of inference is prohibited. The applicability to the proposed development workflow requires clarification before implementation; no native source or derivative module is generated in F0. The inspected historical 2.10.4 LICENSE also identifies version 2.0.1: pinning that revision is not evidence of avoiding this issue.

PCL access is distinct from entitlement to run or redistribute the proprietary PixInsight application. No application redistribution is proposed. Signing identity/issuance, package trust, compatible update-repository metadata, vendor fees (if any), and unattended build/test rights are **NOT VERIFIED**. No signing keys, license credentials or account data are requested or stored. These are F0 release-feasibility gates, not permission to install or purchase.

## 4. Target and build prerequisites

| Item | Established evidence | Remaining requirement |
|---|---|---|
| Owner runtime | Owner subsequently confirmed upgrade to **1.9.5 build 1706** on 2026-09-30 and reported all three RC Astro tools working; `DECLARED`, not independently observed. Earlier 1695 confirmation and BKL-045 OAT remain historical evidence | Owner supplied Windows 11 Pro 25H2, build 26200.9550, 64-bit OS, then Win32_Processor Architecture=9 confirming x64; research host is not assumed to be target |
| Current SDK | S1 revision labelled PCL 2.11.0 / core 1.9.5 build 1706 | Version label now aligns with Owner-declared 1706; compiled SDK/API/ABI compatibility remains untested |
| Historical candidate | S7 labelled PCL 2.10.4 / core 1.9.4 | Exact build 1695 support and vendor guidance not proven |
| Windows build | S1 specifies Visual C++ 2022, C++20; reference Windows 11; S8 uses v143 and release DLL CRT | Pin MSVC patch, Windows SDK, dependencies and reproducible commands; inspect actual library project availability (README layout alone is insufficient) |
| Environment | S1 documents PCLDIR, PCLINCDIR, PCLSRCDIR, PCLBINDIR/PCLBINDIR64, PCLLIBDIR/PCLLIBDIR64 | Configure only in an authorized isolated build environment; no machine environment changed |
| Other platforms | S1 lists Linux and macOS x64/ARM64 toolchains | Outside initial Windows matrix; portability claim is not binary/OAT evidence |
| Development tools | Community may be eligible under S11; no costs incurred | Owner confirms applicable usage/licensing before any installation; no assumption of free organizational eligibility |
| Runtime test environment | Existing PixInsight workstation only identified at bounded role level | Separate permission for no-op module loading, test data and rollback; no EAGLE use |

## 5. Preliminary support matrix

`DOCUMENTED` below describes a source statement, **not** a passed runtime test. All runtime proof is NOT EXECUTED. `PARTIAL`/`UNAVAILABLE` describe the maximum defensible present claim, not a released supported feature.

| Capability / process family | Documented interface or evidence | Limit / preliminary disposition | Required proof |
|---|---|---|---|
| Runtime version/build | PixInsightVersion in S9 | Metadata candidate; not workflow history | Read-only version probe on selected baseline |
| Process identity/version and parameters | ParentProcess, Version, ParameterValue/TableRowCount, ToSource/ToHistorySource (S4) for an available instance | `PARTIAL`: serialized configuration does not prove execution; instance version is not necessarily module binary version | Known scalar/table/string cases, unsupported/private fields, redaction and event-time snapshot |
| Process notifications | ProcessCreated/Updated/Deleted/Saved (S3/S7) | Instance lifecycle, not documented start/end/completion of every execution; ordered executed workflow `UNAVAILABLE` | Distinguish edit/icon-save from execute; repeated instance, abort and failure |
| Image notifications | ImageCreated/Updated/Renamed/Deleted (S3/S7) | `PARTIAL`: state change does not identify process, input set or success; notifications can be broadcast | Correlate without inferring causality, duplicates, previews, dynamic operations |
| Extended image update | S3 adds instance pointer from core 1.9.4 build 1696 / API 0x188 | **Unavailable on historical 1695; documented version threshold met by Owner-declared 1706, runtime untested**. Pointer is null for another module's process or core modification. Upgrade does not provide universal cross-module identity | Later same-module vs different-module test requires separate runtime authorization |
| Built-in/standard processes | Usually implemented in separate modules; S3/S6 | `PARTIAL` image/instance metadata; no automatic complete history demonstrated | Per-family in-place, global/multi-output, non-image and dynamic-process cases |
| Own process callbacks | Before/AfterExecution, global counterparts (S6) | Local process implementation lifecycle, not interception of arbitrary other modules; outside passive recorder proof | Vendor-supported observer mechanism or explicitly bounded cooperative design |
| Timing and order | GetExecutionTimes records latest execution of an available instance, zeros if missing (S4) | `PARTIAL`: no complete journal; repeated executions can supersede timing; timestamp sorting cannot prove global order | Repeated same-instance runs, concurrent/global work, cancellation, unknown times |
| Input/output relationships | Available view identifiers and exposed process parameters (S3/S4) | `PARTIAL`: parameter strings cannot automatically become scientific asset IDs; output creation alone is not causal lineage | Multi-input/output, rename/close/reuse, explicit asset correlation and unresolved references |
| Masks | MaskUpdated/Enabled/Disabled/Shown/Hidden and current Mask/IsMaskEnabled/IsMaskInverted (S3/S5) | `PARTIAL`: current mask state is not proof it was used by a particular executed step | Attach/remove/invert/disable, event ordering, step linkage and reopen |
| Scripts | Potential downstream image/instance changes | Script identity/version, internal operations and orchestration not established; opaque segments `UNAVAILABLE` | Script with process calls vs direct image changes and cancellation; no inference from downstream effects |
| Third-party modules | Public instance parameters may be exposed | Proprietary/internal operations and model/version state may remain opaque; `PARTIAL` or `UNAVAILABLE` per module | Explicit approved module/version inventory, exported/public interfaces and negative cases |
| History artifacts | S5 says history is core-owned; S4 serializes an already available instance; S10 exposes optional embedded XML history | Candidate bounded history export; no full history enumerator or cross-image run reconstruction demonstrated | Existing authorized sanitized artifact with known history, disabled/missing history, undo/redo branches |
| Project save/reopen and restart | Instance serialization/settings are not stable project/run identity APIs | `UNAVAILABLE` continuity; no verified project lifecycle subscription/replay | Supported project identifiers/events, save-as/reopen, crash/gap and duplicate recovery |
| Module inventory | S9 process enumeration is useful | Complete loaded-module binary inventory/version is not established by enumerating processes | Supported module inventory source including non-process modules |

Not finding a supported interface in this inspection is not proof that none can exist. It is a reason to keep the capability unproven and seek vendor documentation, not to use private hooks, binary interception, UI scraping or undocumented project parsing.

## 6. PXP / AP14-W06 compatibility assessment

Sources inspected: [PXP schema](../../contracts/pixinsight-workflow-provenance.schema.json), [F3-A contract](../scientific-assets/BKL-045-F3A-Provenance-Sidecar-Contract-and-Validation.md), [F4 adapter](../scientific-assets/BKL-045-F4-Provenance-Reconciliation-Adapter.md), [AP14-W06](../integration/AP14-W06-PixInsight-Synchronization-Adapter.md), and the existing validator, adapter, ledger, reconciliation and read-model tests under `.github/scripts`.

| Contract aspect | Fit / gap and required disposition |
|---|---|
| Evidence | Preserve `processing_evidence`, `actionAuthority=NONE`, OBSERVED source locators, DECLARED provenance; SUGGESTED excluded from executed steps |
| Ordering | Unique contiguous ordinals are supported; current validator checks the ordinal set, while mapper consumes array order. Future projector must canonicalize step order explicitly and test out-of-order arrays; no contract fix in F0 |
| Completeness | `PARTIAL`/`UNAVAILABLE` require limitations; `UNAVAILABLE` cannot include OBSERVED steps. Unknown activity cannot become a zero-processing assertion |
| Native capture method | Enum currently permits PROJECT_HISTORY_EXPORT, PROCESS_HISTORY_EXPORT, GOVERNED_PJSR_EXPORT, HYBRID only. No NATIVE_PCL value. Do not relabel a pure native source as PJSR/HYBRID to bypass validation. F1 must justify a truthful existing path or versioned migration; adding an enum is not automatically compatible with existing strict validators |
| Existing detail fields | Parameters, processVersion, inputRefs/outputRefs/maskRefs and workflow environment can carry bounded supported evidence. Limits include 2048 steps, 512 per-step input/output refs and 128 masks |
| New journal concepts | No dedicated journal-gap/recovery, API-build, durable event or project-transition contract. Keep research design separate; do not smuggle unsupported semantics into free-form parameters |
| Mapping loss | Existing mapper keeps observed process IDs, workflow-level inputs/outputs, counts, completeness, limitations and sidecar identity. It does not project all step parameters/versions/masks/locators into the coarse manifest. Preserve sidecar as richer evidence; do not promise full workflow UI from manifest alone |
| Validation boundaries | Mapper is not a full schema validator. Existing hand-written validator is not equivalent to all JSON Schema nested constraints/limits. F1/F4 must prove end-to-end enforcement; this dossier makes no hardening changes |
| Digest/retry | Existing digest hashes full canonical payload, including identity/time fields. Unchanged evidence with newly generated IDs/timestamps need not have the same digest. Define stable export identity vs semantic journal digest; identical retry must reuse identity/payload |
| Privacy | Required hostId/workspaceId and locators/parameters are leak surfaces. Use governed non-identifying values/opaque references where valid; public projection must minimize separately. Do not copy historical host identifiers into new evidence |
| Reconciliation | PXP-to-PXM mapping, validation, ledger and exact read-only AP-013/AP-014 lookup remain the only path. No fuzzy matching, catalog acceptance or scientific-authority changes |

Compatibility is **architecturally plausible, not demonstrated end-to-end for a native producer**. No schema, validator, mapper or scientific contract was altered.

The [reproducible evidence addendum](BKL-049-F0-Evidence-Addendum.md) adds a pinned source registry, twelve isolated synthetic contract probes, preliminary linked-library/signing inventory and full-workflow/gallery proof criteria. These establish contract boundaries, not native capture feasibility.

## 7. Alternatives and risks

| Option | Value | Constraint / recommendation |
|---|---|---|
| Passive universal PCL recorder | Intended transparent workflow archive | NO-GO on current evidence; cross-module identity, order and continuity missing |
| Bounded native state observer | Image/mask diagnostics and selected exposed metadata | Research candidate only; cannot claim complete executed workflow |
| Supported history-artifact adapter plus existing exporter | Reuses accepted ADR-008 boundary and may recover per-image persisted history | Recommended next feasibility inquiry; optional history and project/global gaps must remain explicit |
| Cooperative/wrapped process execution | Could know instances it invokes | Material UX/execution-authority change; outside current permission, requires Owner/ADR decision |
| Retain BKL-045 exporter | Proven fail-closed baseline and lowest operational impact | Default until richer evidence passes gates; automatic history remains UNAVAILABLE |
| Vendor-supported new observer API | Could address actual missing boundary | Ask for documentation/roadmap only after Owner authorizes contact; no promise of availability |

Principal risks: unverified compiled ABI on the new 1706 baseline; license/workflow uncertainty; false causality from callbacks; privacy leakage in source strings; lost undo/redo and project branches; journal gaps or resource overhead; coarse manifest losing detail. Treatments are version pinning, license clarification, explicit negative tests, allowlisted metadata/redaction, durable evidence design and preserving sidecar/source locators. CPU/I/O/latency budgets require later measurement; no numeric budget invented.

## 8. F0 exit and F1 entry evidence

| Gate | Current state | Evidence needed / owner |
|---|---|---|
| G0 parallel authorization and isolation | RECORDED | Owner request; dedicated branch; BKL-043 unchanged |
| G1 SDK and license inventory | PARTIAL | Official sources pinned; resolve workflow restriction, dependency notices, application/CI entitlement and signing path before development |
| G2 exact environment/ABI/toolchain | PARTIAL | Owner confirmed upgrade to core 1706 and RC Astro operation after previously supplying Windows 11 Pro 25H2 build 26200.9550, x64 (Win32_Processor Architecture=9); matching SDK/API and reproducible toolchain still needed |
| G3 support matrix | PARTIAL REAL-SOURCE + SYNTHETIC EVIDENCE | Supplied project histories support the artifact candidate; supported automatic extraction, full project coverage and exact source provenance remain unproven. No universal recorder claim; no implicit scope reduction |
| G4 contract feasibility | SYNTHETIC DECLARED PIPELINE VERIFIED; REAL END-TO-END UNPROVEN | Reader, existing-code pipeline and identity experiments recorded; real version/gallery association, accepted encoding, privacy and source trust remain open |
| G5 feasibility decision | NOT ACCEPTED | Review the evidence and alternative trade-offs; do not promote F1 automatically |

Before F1, resolve G1–G3 sufficiently to make an evidence-backed scope decision. If runtime proof is indispensable to resolve G3, propose a separate minimal experiment with exact binary/source baseline, license clearance, synthetic images, read-only observation behavior, installation/rollback and Owner authorization. It must not use scientific images, EAGLE, hidden hooks or production code. Compilation alone cannot prove observation completeness.

Later F2/F3/OAT must test built-in/script/third-party families, edits without execution, repeated executions, abort/failure, masks, multi-image global processes, undo/redo, project save/reopen, restart/crash, deterministic export/replay and privacy. Ground truth must be supplied independently of recorder output. Report omissions/duplicates, parameter equality, causal links and journal gaps. No runtime test in this list is claimed executed.

Owner input is requested one item at a time: (1) core/workstation reconfirmation received; (2) Windows 11 Pro 25H2 build 26200.9550 and x64 processor evidence received; (3) SDK-dependent development/licensing disposition remains open, with vendor contact explicitly deferred; (4) only if necessary, separately bounded experiment authorization. RC Astro product families and unified distribution are confirmed; exact module/model versions remain needed for supported cases. Private host/user identity, keys and raw science data are unnecessary.

The [identity experiment and consolidated F0 position](BKL-049-F0-Identity-Packet-Experiment.md) distinguish progress achievable synthetically from remaining real-source proof obligations.

## 9. Delivery, validation and rollback

This is a documentation/planning PR, kept draft while F0 gates remain open. No merge, rollout, F0 closure, F1 promotion or runtime acceptance is implied. Repository regression checks and documentation build results are reported in the dedicated PR; they validate this planning change and existing contracts, not PCL feasibility. No production tests were added to mirror prose.

Local validation on 2026-09-30: both governed generator checks PASS; roadmap consistency PASS with `currentPackage=BKL-043` and `nextMilestone=BKL-043`; 37/37 existing tests PASS across workflow provenance, provenance-to-manifest, manifest, ledger, reconciliation and provenance read model. `mkdocs build --strict` PASS (34.07 seconds); navigation/relative-link INFO messages were emitted for existing pages. Generated output stayed outside the repository. Diff whitespace/privacy inspection performed; no vendor source, private host/user/path, credential or scientific payload added. GitHub CI is a separate exact-head gate, recorded in the PR, not inferred from these local results. No .NET production change, native compile, install, signing, PixInsight OAT or EAGLE test was performed.

Rollback is a normal revert of this documentation/roadmap commit, followed by the governed projection generator; it has no PixInsight runtime effect. Generated roadmap/status files are produced only by the governed generators. BKL-043 remains `currentPackage` and `nextMilestone`.

| Revision | Change |
|---|---|
| 0.1 — 2026-09-30 | Parallel F0 start, current official SDK/license inspection, support/contract gaps, conditional recommendation and open proof gates; Owner Windows version evidence recorded |
