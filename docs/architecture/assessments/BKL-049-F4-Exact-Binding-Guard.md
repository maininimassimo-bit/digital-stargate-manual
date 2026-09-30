# BKL-049 F4 — Exact image/version binding guard

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-F4-GUARD-001 |
| Version / date | 1.0 / 2026-09-30 |
| Status | Guard increment ACCEPTED / POST-MERGE VERIFIED via PR #452; full F4 and real association OPEN |
| Entry | F3 accepted via PR #451, merge `f689bea2d0b0aba11774c589d47669486bf61978`; 19/19 post-merge runs SUCCESS, Pages verified |
| Authority | Processing evidence only; action NONE |

Delivery: [PR #452 post-merge evidence](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/452#issuecomment-5918948742), merge `171a42b09e7191563210a47b85a84f19a0f8f468`, 19/19 post-merge runs SUCCESS and Pages verified.

## Purpose and bounded profile

The private `tools/pixinsight/workflow_archive/binding.py` guard prevents a workflow from reaching the existing ID-based reconciliation on an ambiguous or unverified final-image association. It implements F1 section 7 for one selected original output and one existing preview. It does not claim general multi-output lineage, automatic catalog discovery, runtime capture, image publication or full F4 completion.

`build_binding` reconstructs the F3 sidecar from the verified F2 packet and its source-bound configuration declaration. It then consumes three **independently anchored** canonical private records: a selected governed snapshot, independently measured original/preview identities, and an explicit Owner association. Every record is bounded to 256 KiB and eight entries. The first profile supports a DECLARED association only; no native association is silently promoted to OBSERVED.

There is no filesystem/network/CLI operation in this guard. In particular, it does not hash images, write receipts, register a catalog item or obtain an attestation. A trusted caller must provide these inputs under the applicable authorization. Passing a digest computed from an untrusted candidate does not make it authoritative. This is an integrity and consistency guard, not an authentication service.

## Private input records

These internal versioned transfer records are selected projections of existing authority, not new public schemas or scientific records. No existing AP-013, AP-014, PXP or BKL-034 schema is changed. An operational snapshot producer must retain its governed source citations and selection evidence; the guard cannot grant the producer authority.

| Record kind | Required meaning |
|---|---|
| `BKL049_PRIVATE_BINDING_SNAPSHOT_V1` | AP-014/AP-013 revision with unique catalog entity/item IDs and unique image/object references. Catalog subset: entity ID, catalog item ID, quality state and target reference. Asset subset: image ID, immutable object reference, SHA-256, byte size, archive/metadata state, session/target references and derivative references. |
| `BKL049_PRIVATE_MEASUREMENTS_V1` | Separately measured original and preview byte size/digest, tied to those image/object identities and an explicit measurement time. Not copied from the expected catalog fields to manufacture a passing comparison. |
| `BKL049_PRIVATE_ASSOCIATION_V1` | Explicit actor/time, DECLARED class and `WORKFLOW_TO_ORIGINAL_AND_PREVIEW` scope, bound to packet/source/workflow, selected snapshot and both complete original/preview identities. A source-configuration declaration alone is insufficient. |

The first profile uses the existing `session:` and `target:` reference conventions, requiring the suffixes to equal the supplied PXP context. This is explicit structural mapping, not name similarity or creation of an observation session. Missing/unknown real context stays blocked. The demonstration material is Owner-declared external to Digital StarGate; an observatory session must not be invented to fit this profile. External catalog registration remains a governed prerequisite.

## Fail-closed checks and result

Duplicate image IDs, object references, catalog IDs or measurement identities are rejected before constructing lookup maps, including duplicates outside the selected pair. All selected identities must match both authoritative expected and independently measured records exactly. CATALOGED assets with COMPLETE asset metadata and an ACCEPTED catalog context are mandatory for this publication-oriented binding; PARTIAL **workflow content** does not waive asset eligibility.

The original must explicitly reference the preview object as a derivative, and both must share the governed context. The Owner declaration independently ties the same source/workflow to both immutable identities. Matching bytes or filenames alone cannot provide that association. Wrong digest/size/version, missing output, unrelated workflow, unknown context, quarantine, withdrawal, missing derivative relation or stale current snapshot anchor fails with fixed diagnostic codes, without reflecting private values.

The guard returns a new private sidecar with exactly one mandatory resolved original output, a private receipt and the selected reconciliation input. All exported process evidence stays DECLARED and PARTIAL/UNAVAILABLE; no step-level input/output/mask relation is guessed. Optional upstream data remain unresolved. The bridge test invokes existing AP14-W06 only after this guard and requires the one mandatory output and session to reconcile exactly. Its `matched` result does not prove complete processing history or authorize publication.

Receipt state is `VERIFIED_AGAINST_SELECTED_SNAPSHOT`, never universal/current validity. It retains source, sidecar, snapshot, measurement and association digests plus the immutable original/preview identities. The caller must refresh the current snapshot trust anchor before every regeneration. A changed/withdrawn record cannot reuse an old receipt as current eligibility. There is no live monitoring or automatic revocation service in this increment.

## Retry, retention and remaining F4 obligations

`compare_retained` classifies an exact immutable receipt retry as DUPLICATE_NOOP; changed bytes under the same binding identity are CONFLICT. Changed declaration, export time or context must become an explicit governed revision, never overwrite. This helper does not persist data and is not an atomic transaction or a replacement for retained evidence.

Before full F4 acceptance, implement and verify the private immutable retention/delivery coordinator with a concrete authorized destination, trusted receipt index, current-snapshot acquisition and a real eligible asset/context. Preserve packet, rich sidecar, association and binding together: the coarse manifest alone remains lossy. Storage ACL/backup, interruption recovery and trust-anchor administration are operational gates; neither synthetic tests nor this helper satisfy them.

F5 separately requires explicit per-field public selection, a permitted preview destination and the actual gallery image/version-to-workflow association. No real image, identity digest, scientific parameter payload, private path or personal source identity is included in this increment. The selected demonstration image is still unlinked and unpublished. F6 OAT and F7 release remain open; BKL-043 remains current.

## Verification and rollback

Sixteen synthetic Python tests cover exact identity, deterministic retry, changed receipt conflict, missing/incorrect trust anchors, duplicate IDs/versions, wrong measured size/digest, missing identity, unrelated source/workflow, unknown context, snapshot change, catalog withdrawal, quarantine, partial asset metadata, absent/wrong preview relation, Owner attestation and bounded input/fixed diagnostics. The synthetic Node bridge checks existing PXP/manifest validators and AP14-W06 exact mandatory output reconciliation while retaining DECLARED/PARTIAL/private status. Windows/Linux CI runs both.

Rollback removes the additive guard and tests via a reviewed revert, retaining all existing private evidence. No runtime, catalog or image migration exists. Delivery reviews, exact-head CI and merge-SHA/Pages verification are recorded in the PR; they do not close the remaining F4 operational gates.

ARB M01 remediation: malformed catalog/archive/metadata enum values now return fixed ArchiveError diagnostics, including list/dict/null/boolean/integer cases. No acceptance bypass existed; the fix prevents an undocumented caller exception.

RQ M02 remediation: the bound sidecar updates only the two F3 limitations superseded by the exact original/preview association. It now distinguishes that selected-snapshot result from unresolved upstream/step-level/mask relations and unapproved publication. Python and Node assertions prevent contradictory inherited text; the F3 source sidecar is unchanged.


## Private retention and replay increment

`delivery.py` now packages the verified source packet (including original export bytes), declaration, three binding input records and regenerated guard output into one canonical `BKL049_PRIVATE_DELIVERY_V1` bundle. This is a private internal artifact, not a scientific/public contract change. Total encoded size remains capped by the existing 32 MiB packet ceiling; oversized bundles fail closed.

`retain_delivery` reconstructs and validates the bundle, requires the caller's current independently governed snapshot digest, and commits to a deterministic filename derived from the binding ID within a caller-selected private directory. It reuses the F2 create-if-absent hard-link commit: source and binding cannot be partially committed as separate files. Same binding ID plus identical bytes returns DUPLICATE_NOOP; changed declaration, source, context, snapshot or export time conflicts. A deliberate new binding ID creates a separate revision and preserves the old artifact. Cleanup failure after a successful commit remains CREATED_CLEANUP_PENDING, not a false rejection.

`load_delivery` requires an externally retained trusted bundle digest and freshly supplied current snapshot digest. It reconstructs the F4 result from retained inputs and compares canonical bytes before returning the sidecar/receipt/reconciliation input to the private AP14-W06 caller. Corruption, forged stored output, changed authority revision, withdrawal/quarantine under the current authority or missing trust fails closed. The Node compatibility test now uses a real temporary-file retain/load roundtrip before existing PXP validation, mapping and reconciliation.

Trust limits remain explicit: hashes provide integrity, not actor authentication; the caller must establish the authority/measurement/declaration anchors before construction, retain the bundle digest independently and obtain the current snapshot before each use. A caller that deliberately supplies an obsolete snapshot cannot be detected by this offline library. Destination ACLs and backups are the caller's responsibility: use a pre-existing private local directory, never the public preview bucket or repository. Path/reparse checks do not defend against a hostile concurrent filesystem administrator. File content is flushed before atomic publication; directory-metadata power-loss durability is filesystem-dependent and no disaster-recovery claim is made.

Validation: 12 new synthetic retention tests cover roundtrip/source preservation, exact retry, conflicting revisions, stale authority, corruption, forged results, malformed canonical input, source changes/quarantine, atomic commit failure, cleanup residue, symlink rejection and input alias isolation. Combined F2/F3/F4 suite: 59 tests, 57 passed and 2 local Windows symlink-permission skips; Linux/Windows CI supplies platform evidence. No real scientific file is imported, catalog record created or image published by these tests.

This delivers a private persistence/handoff API, not a scheduled coordinator, catalog authority producer, cloud workflow store, public projection or whole F4 acceptance. Real external-origin context, measurements/source-bound attestations, private operational retention and gallery OAT remain open.
