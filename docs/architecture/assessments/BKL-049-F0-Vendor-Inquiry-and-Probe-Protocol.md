# BKL-049 F0 — Vendor inquiry and bounded proof protocol

Date: 2026-09-30. Status: PREPARED / NOT SENT / NOT EXECUTED. F0 remains open.

This concretizes the questions and proof scenarios in the [evidence addendum](BKL-049-F0-Evidence-Addendum.md). It does not authorize vendor contact, installation, runtime processing or F1. The Owner's instruction to proceed continues the already authorized research scope.

## 1. Reviewable vendor inquiry

Proposed recipient: `info@pixinsight.com`, explicitly identified for written permission in the official PCL License 2.0.1. The Owner may send the text below or explicitly authorize a sending channel. No account or sending channel is assumed. The inquiry contains public project context and the already confirmed product/platform baseline, without private machine identities or scientific data.

Subject: PixInsight 1.9.5 build 1706 — supported workflow provenance capture and PCL development conditions

Hello PixInsight team,

We are assessing a proposed Digital StarGate integration that would archive a PixInsight workflow and associate its evidence with the exact resulting image in a scientific image gallery. This is a feasibility inquiry, not a claim that such capture is currently supported. The Owner has upgraded to PixInsight 1.9.5 build 1706 on Windows 11 Pro x64 and reports the unified RC Astro BlurXTerminator, NoiseXTerminator and StarXTerminator tools working. Complete workflow capture remains untested.

We have inspected the official PCL repository at revision 5a3902196a7d7a701385a7113cbdce2976ae1a85, the older PCL revision afea714e681853dfc21e70b5d53811ae41849e97, and the official PJSR revision 76e4f38c461320f07a0010bcc973fe26133f303a labelled for build 1695. No native module has been developed, installed or tested as part of this inquiry.

Could you clarify the following, or point us to authoritative documentation?

1. Development and distribution conditions. The PCL License 2.0.1 distinguishes restrictions on training, training datasets and API services for automated code generation. Does using a coding assistant to help develop an independent third-party module require written permission in the intended workflow? We are not proposing to train models on PCL, distribute PCL as a code-generation service, or redistribute PixInsight itself. Please identify any required permission, application-license/automated-build entitlement and requirements for distributing the resulting module and linked libraries. We do not assume that every use of a coding assistant is prohibited by the license.

2. Supported API baseline. Which PCL revision, API version, Visual Studio/toolset and Windows SDK should be used for a module targeting build 1706? We found API 0x0188 in current PCL and 0x0187 in the older header. Is there a supported reproducible build recipe for the appropriate libraries and module?

3. Execution and history coverage. Is there a supported interface to observe or enumerate process execution order, exposed parameter values, input/output relationships and mask relationships across built-in and third-party modules, scripts and global operations? The extended ImageUpdated callback appears to require build 1696 and to provide a process instance only for the same module. Please distinguish currently supported capabilities from unsupported or planned ones.

4. Persisted history and project continuity. The official BatchPreprocessing source serializes mainView.initialProcessing into the PixInsight:ProcessingHistory image property. What exactly does initialProcessing contain, and what supported read-only interface exposes current and persisted histories, including project reopen, mask relationships and multiple output images? Are script steps, undo/redo, discarded branches and failed/aborted executions represented? If no complete audit trail is available, please state the boundary explicitly.

5. Signing and distribution. Which signing identity and registration requirements apply to private testing and public distribution of a third-party module? Is the local license-linked signing mechanism sufficient for either use? Please indicate a supported way to keep signing secrets out of build logs and command-line history.

We can accept a clear statement that some capabilities are unavailable. We will represent incomplete evidence explicitly and will not infer unobserved operations or use undocumented hooks. No private images, account identifiers, license files or signing keys are included in this request.

Thank you.

## 2. Staged proof protocol for a later specific authorization

The minimum first runtime experiment is a **persisted-history capability check**, not a recorder installation. Selecting this experiment does not replace the full-workflow objective or accept reduced support. It tests one promising supported surface before committing to native development.

### Preconditions

- Resolve the applicable development/license questions before any SDK-derived implementation; obtain the supported build/API baseline before considering a native module.
- Obtain Owner authorization for this exact synthetic experiment on the confirmed workstation. Authorization must distinguish Owner-performed actions from assistant control; neither is assumed here.
- Close or set aside real projects without changing them, and use a new isolated scratch project containing only generated synthetic content. If isolation would require altering an existing scientific workspace, stop and let the Owner select a safe environment.
- Use existing licensed PixInsight facilities only. No SDK module, plugin, compiler or update is installed. No application save preferences are changed globally.
- Prepare an independent operation log with numbered actions and expected artifact relationships. Do not derive expected results from the candidate exporter itself.

### First stage: exact supported-interface inspection

Under the later authorization, use the documented product interface to identify the actual core/API baseline and available history export facilities. Consult the vendor response before choosing commands. Do not invoke a guessed history API, mutate historyIndex, use private hooks, sign a module or access license files. Record sanitized version evidence and whether supported read-only history/property access is available. If no supported access can be identified, stop with UNAVAILABLE and the reason; this is a useful result.

### Second stage: one synthetic image and persisted history

Only after the first stage identifies a supported route, present the exact built-in process sequence and artifact locations for the authorized execution method. The intended bounded sequence is: create a small synthetic image; apply two distinguishable built-in operations with recorded values; save a synthetic artifact with the documented history option, if available; reopen it in the isolated project; inspect history through the supported route. Repeat the save without embedded history only if a per-save option exists and the Owner's authorization covers that comparison. Do not assume the class default describes the user's settings.

Collect an allowlisted evidence record: core/module versions, synthetic image token, independent step ordinal, process identifier, exposed values, source-evidence locator, artifact digest, and presence/absence of persisted history. Replace volatile machine paths and view names with local research tokens before committing any result. Retain private local artifacts only under the Owner-approved scratch location; publish no pixel data by default.

A successful result requires agreement between independent ground truth and extracted entries, plus an explicit statement of whether the interface exposes initial, current or persisted history. A successful two-step example does not establish universal ordering, cross-module coverage, project continuity or script support. Missing entries or unreadable history produce PARTIAL/UNAVAILABLE with exact omissions. No synthesized OBSERVED step is allowed.

### Third stage: only after reviewing the first result

Propose separate bounded additions for masks, script/global operations, third-party modules, undo/redo and project reopen. Specify exact module versions, operations and independent expectations before running them. Do not extend authorization from two synthetic operations to arbitrary processing or the Owner's scientific projects. Failed/aborted attempts and discarded branches require separate audit semantics from the final reconstructable history.

### Stop, retention and rollback

Stop on unexpected access to a real project/image, requirement for an installation/update, unsupported API, missing entitlement, request for signing secrets, or mismatch between planned and actual operation. Preserve only sanitized diagnostic evidence; no upload to the gallery or AP-013/AP-014 write is performed. Close the isolated synthetic project after review; leave or remove its scratch artifacts according to the later explicit retention decision. No existing project, image, global preference or production catalog should require rollback because this protocol authorizes none of their modification.

## 3. Required result record

A later evidence record must state: authorization scope and date; exact product/API/source versions; methods actually executed; independent expected history; observed entries and missing entries; per-step input/output/mask bindings; source locators and artifact digests; privacy treatment; limitations; and next decision. Repository tests and CI must be reported separately from runtime findings. G1–G5 are not closed by preparation of this protocol.
