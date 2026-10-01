# BKL-049 — External-origin registration plan

| Field | Value |
|---|---|
| Date | 2026-10-01 |
| Status | Manual route APPROVED FOR IMPLEMENTATION by Owner on 2026-10-01; real catalog acceptance NOT PERFORMED |
| Scope | First external image and its exact workflow association |
| Authority | Existing AP-013/AP-014 only; importer and gallery authority NONE |

## Current result

The Owner supplied an external acquisition context, instrument models, nominal focal length and an observing-site description. These remain private DECLARED evidence, not independently observed instrument configuration. The current private candidate preserves earlier drafts and references the source declarations. A bounded primary-header inventory of five available source frames and subsequent Owner confirmation reconcile the acquisition day separately from the processing day. Only primary headers were read; header fingerprints are not whole-file fingerprints, and collection membership is Owner-declared rather than an independently reconstructed processing lineage. Literal timestamps are not promoted to UTC where their time basis is unresolved. Header-reported focal length and Owner-declared nominal focal length remain separate evidence; no optical accessory or equipment replacement is inferred. The selected final-file header inspection found none of the specifically searched acquisition/instrument FITS keywords; it does not establish that all metadata or other sources are absent. No coordinates, exact acquisition times, effective focal length, instrument generation or historical validity interval were inferred.

The explicitly authorized antivirus scan of the selected JPEG completed with exit 0 and an explicit no-threats result; independently checked pre/post bytes were identical. The signed installed scanner used current definitions at scan time and remediation was disabled. Existing provider sample-submission settings were not changed; actual transmission was not measured. This is a bounded scan result, not a guarantee of safety or publication permission. Private receipts retain tool/version, hashes and output. [Sanitized scan evidence](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/458#issuecomment-5926259882).

The private archive import is available, but real F4 binding, F5 publication and milestone closure remain OPEN. The preview bucket remains private; this document performs no cloud operation, catalog registration or image publication.

## Existing boundary and implementation gap

[DSDM-002](../scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model.md) permits MANUAL/IMPORTER provenance. [AP14-W01](../scientific-catalog/AP14-W01-Observation-Catalog-Conceptual-Model.md) and [AP14-W02](../scientific-catalog/AP14-W02-Logical-Data-Model-and-Identifier-Standard.md) still require governed observation/session/configuration identities. A private draft is neither a conformant accepted catalog record nor an authority snapshot.

The existing `generate-scientific-session-catalog.mjs` reads observatory analytics CSVs; `generate-scientific-catalog.mjs` derives its catalog projection and maps validated analytics to accepted quality. Those generators do not provide an implemented manual external-registration route. Adding fictitious observatory analytics, fabricated GREEN quality, or editing generated catalogs would misrepresent the source and is prohibited.

The [F4 guard](BKL-049-F4-Exact-Binding-Guard.md) continues to require independently anchored CATALOGED/COMPLETE assets and ACCEPTED catalog context. Acceptance of a PARTIAL workflow does not waive asset identity or mandatory scientific metadata. The [BKL-034 preflight](../packages/BKL-034-F2-Storage-Boundary-Preflight.md) is a dry run, not registration authority.

## Candidate mapping and unresolved semantics

| Input or record | Available evidence | Required treatment before acceptance |
|---|---|---|
| External origin and authorship | Owner declarations | Preserve external attribution and accountable declaration references; separately resolve publication rights |
| Subject | Owner-supplied label | Retain label; no independent astronomical identification or invented catalog alias |
| Acquisition date | Owner day-precision declaration and site context | Resolve canonical local-observing-date convention; never manufacture UTC start/end from midnight |
| Observatory | Owner site/region description | Govern external AP-006 reference and timezone; no coordinates required by this task |
| Telescope/camera | Owner model declarations | Versioned equipment/configuration references; distinguish nominal focal length from measured effective focal length |
| Configuration validity | No historical timestamp established | DSDM-002 requires validFromUtc; do not substitute import time or guessed midnight. Resolve field semantics through existing governance before an accepted record |
| Observation/campaign | No accepted records | Govern identities, mode, status and required priority; import code must not assign scientific priority or infer acquisition mode |
| Original and preview | Retained exact byte identities and Owner derivative declaration | Revalidate expected identities and registration state; equality does not itself establish catalog acceptance |
| Workflow | Retained supported export subset | Source-bound DECLARED association and explicit PARTIAL limitations; historical model/branch gaps remain visible |
| Security and public selection | JPEG inspection and completed bounded antivirus scan | Review remaining metadata/privacy/rights and exact public field selection; scan alone does not approve publication |

Missing optional fields remain null where their contracts allow it. Missing mandatory fields keep the draft incomplete. Do not create raw-frame/acquisition records, exposure counts or zero-valued scientific measurements merely to fill the model. Archive receipt identifiers are not historic acquisition identifiers.

## Proposed next increment

Prepare a bounded manual submission path within the existing scientific-data-management boundary, separate from the PixInsight importer and observatory analytics. This is a proposal for the missing route, not an implemented or newly authorized scientific authority. Its detailed design must identify the existing registration owner, authoritative retention location, validation rules and acceptance evidence before any production write.

1. Keep a private immutable submission containing exact original/preview identities, declarations and unresolved fields. New revisions preserve earlier evidence. No accepted lifecycle is assigned by the draft builder.
2. Resolve the mandatory context and semantic gaps above under existing AP-013/AP-014 governance. If a contract or scientific interpretation must change, present the concrete decision to the Owner; do not implement a silent extension or exception.
3. Validate the complete submission and record the governed acceptance decision separately. An Owner declaration supplies evidence, not an automatic ACCEPTED quality transition. No session is introduced into observatory telemetry or analytics.
4. Produce an independently anchored, versioned authoritative snapshot through the approved boundary. Prove collisions, revision changes, withdrawal and incomplete input fail closed before handing it to the unchanged F4 guard.
5. Build and verify the private exact binding and delivery bundle. Only then select a minimized public projection and present the exact preview/fields/access operation for publication authorization.

Required implementation evidence includes duplicate/conflicting external identity rejection, provenance retention, mandatory-field failure, no fabricated telemetry, repeat-submission idempotency, revision/withdrawal invalidation, unchanged scientific schemas and existing pipeline regression checks. Synthetic route tests cannot substitute for the real registration decision.

## Alternatives and decision boundary

Recommended: retain the truthful private draft and design the missing governed manual route. This supports external material without weakening the existing exact-binding gate.

Keeping the image private and unlinked remains a valid fallback while required context is unavailable. Publishing an unverified association, relaxing acceptance to accommodate the draft, or masquerading as an observatory session are not selected. A different external-record model would be a separate contract proposal requiring an explicit decision.

Technical preparation and F5 projection hardening can proceed independently. Real registration cannot proceed until the route and mandatory semantics are resolved. No new Owner question about optional exposure details or coordinates is required by this increment. The next necessary decision must present a concrete design, rather than ask the Owner to invent technical catalog fields.

Rollback is to stop before registration/publication and retain the private evidence. Any documentation change can be reverted through a reviewed PR. No original bytes, cloud access, analytics, Safety Authority, BKL-043 work or EAGLE operation changes.

## Gate review and concrete registration proposal — 2026-10-01

The [gallery reader release](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/461#issuecomment-5928290802) is accepted: reviewed head `e68728c8da01a88e5d0d2466712f4952f5da181a`, merge `e78c5058b1f18ed847f3d2f239c06fd768fe367a`, 18 successful PR checks and 17 successful applicable post-merge runs. Live Pages verification found the deliberately empty collection, no real workflow cards and no JavaScript console errors. This closes the reader increment, not the real-data gate.

| Gate | Evidence / disposition |
|---|---|
| Acquisition versus processing day | Reconciled in private immutable declarations and candidate revision; no public case dates or timestamps |
| Source membership | Owner-declared source collection to selected final; no claim of independently reconstructed lineage |
| Instrument and historical validity | OPEN: literal header values retained separately; historical configuration validity not established |
| External registration authority | OPEN: MANUAL is a permitted source category, not an operational registration service |
| Real binding / private delivery | OPEN: no accepted authoritative context snapshot exists |
| Public gallery reader | ACCEPTED, synthetic tests and empty live collection only |
| Real preview, selected fields, publisher and OAT | OPEN; no cloud/publication authorization is inferred from this proposal |

### Proposed manual route (decision candidate, not activation)

Use the existing AP-013 asset-management and AP-014 catalog responsibilities with a **private, manually approved registration journal**. The PixInsight importer remains an evidence producer with no registration or acceptance authority. The journal is a proposed implementation of those responsibilities, not a new scientific authority or an accepted record created by this document.

The proposed accountable operator is the Project Owner acting explicitly in the registration role. Architecture review must confirm the role mapping before activation. A declaration of instrument/date/source, approval of this design, approval of a software release, and approval of an individual catalog record are four different events; none substitutes for another.

Proposed retention is a dedicated private local directory, outside Git and outside the preview bucket, using immutable revisions and a separately retained current-revision reference. The actual location, access controls, independent trust anchor and tested backup/restore destination must be recorded privately before real acceptance. Existing task-output drafts are evidence inputs, not a durable catalog. No new service, cloud resource or credential is selected by this design.

The bounded first implementation must provide these separate operations:

1. **Prepare:** consume explicitly selected retained evidence and create a draft with per-field provenance, original values, unresolved mandatory fields and stable proposed identifiers. Never infer astronomical identification, historical UTC validity, scientific priority, acquisition mode or quality. Repeating the same request is idempotent; conflicting identities stop.
2. **Validate:** check existing AP-013/AP-014 required fields, enumerations, references, byte identities and revisions. Missing mandatory context blocks acceptance. Optional unknowns remain null only where the governing contract permits it. Validation produces findings, not an ACCEPTED transition.
3. **Decide:** present the exact candidate digest, unresolved findings and source references to the authorized registration operator. Record a distinct asset-registration decision and catalog-acceptance decision under their existing responsibilities. A generic “proceed” or date correction is not a scientific quality decision. No default ACCEPTED, COMPLETE or CATALOGED state is allowed.
4. **Retain:** append the decision and accepted revision atomically, with optimistic concurrency and an independently retained integrity anchor. Preserve superseded evidence. Failure leaves the previous current reference intact. Retention has no image-deletion or processing operation.
5. **Export:** derive the minimal current snapshot needed by the unchanged F4 guard only from a presently eligible revision. Rejected, incomplete, withdrawn, quarantined or stale records fail closed. Reuse the existing private delivery and PXP/AP14-W06 path; never inject external records into observatory analytics or hand-edit generated catalogs.

Historical `validFromUtc` remains a prerequisite under the current model. It must not become the registration date or an assumed midnight. If it cannot be established truthfully, this route stays blocked for that record; a separate contract proposal would be required. Likewise, the proposal does not invent a neutral scientific priority or an observation mode to satisfy a schema. The complete acceptance rubric and vocabulary mapping must be reviewed against the current governing sources before the decision operation is enabled.

### Release and operational acceptance evidence

Before enabling real registration, require separate ARB and Release Quality review, exact-head CI, and synthetic checks for missing mandatory fields, unapproved decision, wrong digest, concurrent update, duplicate identities, idempotent retry, revision supersession, withdrawal, quarantine, stale export, interrupted writes, restore and unchanged existing catalog/analytics behavior. A restore test must recover both the record and its independently anchored current revision; a checksum alone does not authenticate an operator.

Then use a private dry run against the retained real candidate. Real acceptance requires the resolved mandatory context, a recorded authorized operator decision, verified private retention/restore and a fresh snapshot that passes the unchanged F4 guard. Publication is a later distinct gate: exact preview bytes, rights/privacy, public aliases and selected fields, publisher freshness/withdrawal policy, specific cloud access operation and real gallery OAT. No blind renewal of the reader's 24-hour validity window is permitted.

### Decision requested and alternatives

Recommended decision: approve implementation of this manual route within AP-013/AP-014, including the proposed private journal and explicit Owner registration role, while retaining all current eligibility requirements. Approval permits design implementation and synthetic/private dry runs; it does **not** accept the pilot record, change a scientific contract, upload an image or make the bucket public.

Alternative: retain the current private unlinked archive until an existing governed external registration service becomes available. This avoids implementing a journal but leaves the required real gallery association unfinished. A less restrictive external-archive eligibility profile is not silently adopted: it would change the current binding/contract semantics and needs its own concrete proposal and decision.

The decision boundary follows [DSG-AEM-001 section 5](../../project/DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md): “cambia esperienza utente, priorità di prodotto, authority, boundary, contratto pubblico o semantica scientifica”. The proposed operational authority/retention mapping must therefore be explicitly settled before activation; acceptance of partial workflow content alone does not settle it. BKL-049 remains OPEN and BKL-043 remains current.

### Owner decision — 2026-10-01

The Owner explicitly approved the private registry proposed in PR #462, including implementation, private tests and the Owner's responsibility for explicit registration and acceptance decisions. The decision applies to the proposal reviewed at `1788eb41961896ea30edf9841e6dbd7121a71396`; its earlier proposal wording is retained above for audit. No second authorization for that same implementation scope is required.

The route is approved for implementation, **not yet operationally accepted**; the first draft-only implementation increment is described below. Real-record eligibility, the acceptance rubric, retention/restore evidence, exact binding, field selection and public image/access authorization remain outstanding. No scientific contract or automatic record acceptance is approved. The next step is a separately reviewed bounded implementation and synthetic/private dry run under these constraints.

## Private draft retention increment

The first bounded implementation provides immutable draft retention under `tools/scientific_registry`, separately from scientific acceptance. It reuses the existing private archive's canonical/hash/filesystem utilities only; it neither parses PixInsight exports nor treats importer output as catalog authority. Original selected JSON bytes are retained with a fixed DRAFT_NOT_ACCEPTED / PRIVATE_NOT_APPROVED envelope and scientificAuthority NONE, even if embedded source content claims acceptance. No validation/acceptance, catalog export or publication API exists in this increment.

Each submission has a bounded digest-linked revision chain. A caller-supplied, independently retained current digest is required for reads/appends. Exact retries are idempotent; conflicting or stale revisions, altered/missing history, reparse paths and invalid input reject. Atomic create-if-absent preserves previous revisions when a write fails. Receipt timestamps are not historical acquisition/configuration timestamps. Original bytes, not normalized replacements, remain available privately.

Limits are 256 KiB per source, 512 KiB per revision, 128 revisions, 1,024 scanned directory entries, 32 JSON levels and 32,768 values. The caller owns access controls and fresh external anchors. Hashes do not authenticate the operator; obsolete anchors plus a rolled-back directory, hostile concurrent filesystem administration and directory-metadata power-loss durability are outside this offline assurance. Unsupported atomic-link filesystems fail closed. No scheduled backup or production retention claim is made.

Local validation: 49 combined draft/archive/delivery tests completed, 46 passed and 3 Windows symlink-privilege skips. The added suite includes actual simultaneous conflicting writers, exact-byte preservation, malformed/deep/oversized JSON, duplicate keys, forged acceptance envelope, rollback/corruption, failed commit and restore with the independent anchor. Linux/Windows CI runs the new suite. One initial deep-input test identified the need for an explicit nesting bound; the corrected implementation passes it.

An authorized private dry run retained the existing incomplete pilot candidate, restored its draft to a separate private scratch directory and verified exact equality against the separately retained journal anchor. The source remained unchanged; no scientific pixels were read and no catalog acceptance occurred. Private receipts hold the source and journal identities; no case values, paths or hashes are published. This is draft recovery evidence, not a production backup acceptance test.

The remaining route work is unchanged: governed metadata validation and acceptance rubric, explicit record decisions, complete mandatory context, operational retention/restore, eligible current snapshot export and F4 handoff. Real binding, public fields/preview, publisher and gallery OAT remain OPEN. Code/test rollback leaves private drafts and receipts intact. Full implementation guidance and API limits are in the module README.

## Configuration structural preflight increment

The next bounded implementation adds `configuration_preflight.check_configuration` within the approved private registry. It checks explicitly selected observatory, telescope, camera and configuration records against a structural subset of DSDM-002 sections 2.2 and 5.1/5.2/5.3/5.5. Mandatory presence/types, explicit UTC calendar syntax, interval ordering, positive versions/numeric quantities and exact selected equipment/site references produce fixed findings. It reuses the bounded draft JSON parser without retaining an envelope, reading images or assigning receipt/historical times.

The internal input and private source-bound report do not change scientific contracts. Known instrument models do not manufacture a configuration record. A valid timestamp does not establish the instrument's historical use; identity governance, provenance, timezone semantics and historical validity remain explicitly unverified. No optical accessories, local-to-UTC conversion, priority or quality are inferred. Unsupported fields are findings. An empty finding list is named NO_STRUCTURAL_FINDINGS, never VALIDATED/ACCEPTED, and acceptance eligibility remains false in every result.

This is a partial validator increment, not the full required-metadata validator or acceptance rubric. Existing private declarations remain authoritative only as declarations; historical configuration evidence remains unresolved. The distinct registration/catalog decisions, operational retention, snapshot export, real F4 binding and publication gates remain OPEN. BKL-043 and generated catalogs are unchanged. Eleven synthetic cases and the existing draft suite cover its failure and non-acceptance boundaries; exact-head review/CI and post-merge evidence belong in the delivery PR. Rollback reverts this additive checker/parser extraction and preserves private evidence.
