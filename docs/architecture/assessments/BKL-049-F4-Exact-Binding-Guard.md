# BKL-049 F4 — Exact image/version binding guard

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-F4-GUARD-001 |
| Version / date | 1.0 / 2026-09-30 |
| Status | F4 guard increment in review; full F4 and real association OPEN |
| Entry | F3 accepted via PR #451, merge `f689bea2d0b0aba11774c589d47669486bf61978`; 19/19 post-merge runs SUCCESS, Pages verified |
| Authority | Processing evidence only; action NONE |

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
