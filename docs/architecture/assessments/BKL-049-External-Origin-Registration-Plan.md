# BKL-049 — External-origin registration plan

| Field | Value |
|---|---|
| Date | 2026-10-01 |
| Status | PROPOSED; private candidate retained, catalog acceptance NOT PERFORMED |
| Scope | First external image and its exact workflow association |
| Authority | Existing AP-013/AP-014 only; importer and gallery authority NONE |

## Current result

The Owner supplied an external acquisition context, instrument models, nominal focal length and an observing-site description. These remain private DECLARED evidence, not independently observed instrument configuration. A third private candidate revision preserves the earlier drafts and references the source declarations. The selected final-file header inspection found none of the specifically searched acquisition/instrument FITS keywords; it does not establish that all metadata or other sources are absent. No coordinates, exact acquisition times, effective focal length, instrument generation or historical validity interval were inferred.

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
