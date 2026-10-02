# ADR-019 — External retrospective scientific records

**Status:** Owner-approved profile; private real record admitted; public activation pending

**Date:** 2026-10-01

**Scope:** BKL-049, additive AP-013/AP-014 external profile

**Decision owner:** Project Owner

## Context and explicit decision

The Owner explicitly approved the private completion proposal on 2026-10-01. Approval extends beyond partial processing history to a versioned external retrospective record with explicitly partial scientific metadata. It authorizes this contract and implementation direction, not registration, admission or publication of the real candidate. The proposal's current-state assessment does not claim the earlier structural validators form a complete registry.

The existing DSDM-002 instrument configuration requires `validFromUtc`; AP14-W02 requires planning hierarchy and governed metadata; the existing F4 guard requires COMPLETE metadata and ACCEPTED quality. A day-precision historical declaration cannot truthfully fill a UTC validity interval. Retrospective material must not fabricate a DSG observatory session, planning priority or scientific quality to pass those contracts.

## Versioned decision

`DSG_EXTERNAL_RETROSPECTIVE_V1` is a separate AP-013/AP-014 profile. V1 scientific catalog, asset, F4 and PXP/AP14-W06 consumers remain unchanged. No permissive fallback converts external records into their inputs. Authority remains AP-013 for asset registration/quarantine and AP-014 for external record admission/withdrawal. The same Owner may act in both roles, through two distinct exact-revision decisions.

An external acquisition has its own `EXT-` identity and no session alias. Planning project/campaign/observation hierarchy and retrospective priority are not required for this entity type. This does not loosen those requirements for observatory records. Administrative decision timestamps record the actual decision, never a historical acquisition/configuration time.

External admission means permission to retain and associate the explicitly limited record. It is **not scientific quality acceptance**: metadata remains PARTIAL and quality remains UNKNOWN throughout this first profile. Independent subject identification, chronology and complete workflow execution are not asserted. Additional profiles or changes to these semantics require their own review, not an enum fallback.

## Closed candidate contract

The executable closed-field validator is `tools/scientific_registry/external_registry.py`. Inputs use the bounded selected-source parser (256 KiB, duplicate/nonfinite rejection, 32 levels, 32,768 values). Unsupported keys, types and vocabulary values reject with fixed diagnostics. Exact original UTF-8 source text is retained inside the immutable event; canonicalization never replaces the source anchor.

| Candidate field | Required meaning |
|---|---|
| kind / profile | DSG_EXTERNAL_CANDIDATE_V1 / DSG_EXTERNAL_RETROSPECTIVE_V1 |
| acquisitionId / revision | EXT-prefixed governed private identity; integer starting at 1, sequential revisions |
| facts | Exactly the twelve fact envelopes below |
| evidence | 1..64 unique private evidenceId/SHA-256/scope entries; scope OWNER_DECLARATION, HEADER_ONLY or DOCUMENT |
| original / preview | Distinct exact imageId/objectRef/SHA-256/positive byteSize identities; objectRef denotes an immutable version |
| workflow | Exact packet SHA-256, source SHA-256 and archive workflowId |
| metadataState / qualityState | PARTIAL / UNKNOWN only |

Each fact envelope contains exactly `value`, `evidenceClass`, `evidenceRefs`, `reason`. The twelve facts are author, subject, acquisitionDate, site, telescope, camera, nominalFocalLengthMm, headerFocalLengthMm, timezoneId, validFromUtc, validToUtc and processingDate. The first six require a value and OBSERVED or DECLARED evidence. Acquisition/processing dates are calendar dates with DAY precision, never implicitly converted to UTC. Nominal and header focal lengths remain separate values. Timezone text never causes a conversion.

Optional unknown values use null, PARTIAL or UNAVAILABLE, and a nonempty reason. Non-null values require referenced evidence; SUGGESTED is allowed only for nonmandatory facts, and never for validity timestamps. Supplied validity instants require explicit UTC and a positive interval when both endpoints are present; missing start/end remain missing. Unknowns are explicitly permitted by this profile, not evidence of absence. All five classes OBSERVED/DECLARED/SUGGESTED/PARTIAL/UNAVAILABLE remain distinct.

The validator establishes structure and references, not source authenticity or scientific truth. The accountable operator verifies the evidence references against independently retained sources and preserves corrections. A matching source digest is neither a signature nor evidence that a field was observed.

## Distinct decisions and current authority

The closed `DSG_EXTERNAL_OWNER_DECISION_V1` record contains decisionId, operation, authority, scope, actor, decidedAtUtc, acquisitionId, candidateSha256, previousRecordSha256, measurementSha256 and rationale. Authenticity is established by the trusted manual operator from the actual Owner act, not by an API-provided actor string. No tool here obtains consent or signs on behalf of the Owner.

| Operation | Authority / exact scope | Transition |
|---|---|---|
| REGISTER | AP-013 / REGISTER_EXACT_EXTERNAL_ASSETS | New revision becomes REGISTERED; no admission inherited |
| ADMIT | AP-014 / ADMIT_EXTERNAL_RECORD_AND_EXACT_WORKFLOW_ASSOCIATION | Exact REGISTERED revision becomes ADMITTED; expressly includes declared original/preview/workflow relation |
| WITHDRAW | AP-014 / WITHDRAW_EXTERNAL_RECORD | REGISTERED or ADMITTED becomes WITHDRAWN |
| QUARANTINE | AP-013 / QUARANTINE_EXTERNAL_ASSETS | REGISTERED or ADMITTED becomes QUARANTINED |

Every act selects the exact candidate and prior per-record event digest. Registration additionally selects separately anchored `DSG_EXTERNAL_MEASUREMENTS_V1` evidence: measuredAtUtc, scope FULL_FILE_BYTES, and original/preview identities in that order. Header-only scope, duplicate/mismatched identities and future measurements reject. The validator does not read images or establish measurement freshness/authenticity by itself. Reuse of decision IDs, obsolete records, changed bytes under an allocated identity, cross-record identity collisions and timestamp reversal reject. Withdrawn/quarantined identities remain reserved and cannot be automatically readmitted in this profile. A future reinstatement policy would require a separate decision.

One bounded global journal serializes all allocations and state changes, up to 128 events. Each event carries sequence, previous journal digest, original source strings and decision digest. Deterministic numbered create-only files provide an atomic competing-writer conflict; replay checks the complete chain and a caller-supplied independently retained current head. Identical retries require the already retained new head. A crash between event commit and independent anchor update requires accountable reconciliation; the utility never adopts unanchored disk state. Capacity exhaustion fails closed; rotation/migration is not implemented.

This is a trusted private local-filesystem component, not an authenticated multiuser service. ACLs, restricted location, independently stored head, evidence access, actual full-file measurement provenance, backup media and an operational restore test are production prerequisites. An old head combined with a rolled-back directory cannot establish currentness. Restoring an old backup never authorizes old admission. Synthetic recovery tests do not certify the real operational location.

## External F4 and PXP V2 handoff

`export_snapshot` replays the journal and exports only an ADMITTED current revision. `BKL049_EXTERNAL_SNAPSHOT_V2` retains AP-013/AP-014 authority, current journal head, exact candidate, per-record admission event, PARTIAL/UNKNOWN and fixed limitations. Its digest alone does not make it authoritative.

`external_delivery.py` replays the full anchored journal rather than accepting a self-asserted eligible snapshot. It compares separately supplied full-file measurements and exact workflow packet/source/workflow identities. It reconstructs processing evidence through the existing F3 importer, preserving source, configuration order, DECLARED steps and missing historical versions. It never inserts a sessionId. The new `BKL049_EXTERNAL_PXP_V2` observationContext uses externalAcquisitionId, metadataState PARTIAL and qualityState UNKNOWN. It is wrapped in `BKL049_EXTERNAL_DELIVERY_V2` with journal, packet, measurements, declaration and reconstructed result.

This new private handoff is **not an input to the old AP14-W06 reconciliation path**. Its dedicated load/verify boundary reconstructs the complete result, rejects stale journal heads and rejects edited cached results. Legacy PXP validation rejects it. It conveys processing evidence and external admission, no scientific quality acceptance or action authority. Delivery is immutable, content-addressed and PRIVATE_NOT_APPROVED. Before every reuse the caller refreshes the authority head; any intervening journal change requires reconstruction/review, even if another record changed.

## Public projection and remaining real gates

The [external F5 extension](assessments/BKL-049-F5-External-Public-Projection-and-Publisher.md) supplies a V2 allowlisted projection, gallery reader and local collection publisher with explicit field/rights/preview approval, currentness, expiry and withdrawal. It preserves external origin, partial acquisition metadata, declared identification and partial/unavailable workflow. Real publication is not activated: the collection remains empty. Full workflows and originals remain private. No upload, cloud access change or operational equipment work is authorized by this ADR.

The private real registration/admission, retained event restore and exact external delivery were completed under explicit Owner approval on 2026-10-02, as recorded without private values in the external F5 assessment. Separately approved publication, cloud activation/served-byte verification and real gallery OAT remain required before milestone closure. No real registration/admission decision is manufactured in tests or preparation.

## Verification and rollback

Synthetic end-to-end tests cover day-only unknown configuration, field provenance, closed schemas, role separation, no admission by registration, immutable identities, revision re-admission, global collisions, revocation/quarantine, stale head, restore/tamper/conflict, exact workflow association and legacy rejection. Windows/Linux CI runs these with existing V1 regressions. Separate ARB then RQ, exact-head checks and post-merge checks remain mandatory.

Rollback removes the additive profile and delivery consumer without touching V1 or deleting private evidence. Existing external journal/delivery files must remain retained but unusable until a compatible verified reader is restored. No migration, new dependency, scientific image processing, public data, cloud write or Safety Authority change is included.
