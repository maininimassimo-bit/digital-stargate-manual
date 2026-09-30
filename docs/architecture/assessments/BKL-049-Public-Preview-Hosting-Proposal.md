# BKL-049 — Public preview hosting decision candidate

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-PREVIEW-HOSTING-001 |
| Version / date | 1.0 / 2026-09-30 |
| Status | PROPOSED — Owner provider decision required; no resources or image publication authorized |
| Purpose | Supply an approved public preview URL for the mandatory exact gallery image/version-to-workflow relationship |

## Confirmed need

The Owner confirmed that no dedicated online image space exists. The selected demonstration material is external to Digital StarGate; its final-to-preview relationship is Owner-declared. No real catalog registration, publication classification or complete acquisition context has been accepted. Unknown acquisition data stay unknown. Identifying an author does not independently prove publication rights or establish scientific context.

F3 is accepted and the F4 identity guard is delivered separately. They do not supply binary hosting or authorize public exposure. [AP-013](../packages/AP-013-Scientific-Image-Repository-Architecture.md) keeps scientific binaries out of the manual repository, and [BKL-034-F2](../packages/BKL-034-F2-Storage-Boundary-Preflight.md) requires its storage/privacy/integrity gate before publication. GitHub Pages remains the read-only consumer.

## Recommended candidate

Use **one new, dedicated Google Cloud Storage bucket for approved web previews only**, region `europe-west1` (Belgium), Standard storage. Google Cloud is already used in the repository's separately governed infrastructure; this proposal does not reuse its private buckets, identities, permissions or deployment authorization. The exact project/bucket identity and organization policy remain to be verified in a bounded infrastructure plan after the provider decision. No paid resource has been created or inspected live for this proposal.

| Boundary | Candidate configuration |
|---|---|
| Public bytes | Only individually approved web-preview JPEG/PNG objects; no XISF, projects, raw histories, scientific originals or private sidecars |
| Repository/Pages | Minimized approved metadata and workflow projection, referencing an exact public preview version |
| Private retention | Existing local originals remain private; this decision does not migrate the scientific archive |
| Names/metadata | Neutral public identifiers; no private source paths, host/account identities or original scientific checksums in object names/metadata |
| Access | Public read only after acceptance; a read-without-listing role is the candidate. Dedicated authorized writer only; no credentials in Pages or PixInsight |
| Integrity/versioning | Exact preview checksum and size verified privately before/after upload; create-if-absent generation condition, new object version for changed bytes, no overwrite |
| Exposure boundary | Do not weaken an existing private bucket or organization-wide public-access policy. If the dedicated policy cannot be satisfied, stop and revise the plan |
| Pilot extent | One approved preview and its exact workflow link; no bulk upload, background sync, new recurring monitor or CDN/load balancer |
| Recovery | Disable the gallery link and public read on the dedicated object/bucket without deleting originals; cached/downloaded copies cannot be recalled reliably |

Google documents that public-access prevention blocks public sharing. It also offers an object-reader role without the listing permission and warns that public objects expose their metadata. These conditions must be checked for the selected bucket, rather than changing broader policies to force publication. [Official public-access guidance](https://docs.cloud.google.com/storage/docs/access-control/making-data-public).

## Cost and service conditions

Cloud Storage bills storage, requests and outbound traffic. No free allowance is assumed. As an illustration, the current selected JPEG is about 8.8 MB: 1,000 full downloads are about 8.22 GiB. At the currently listed first-tier transfer rate of US$0.12/GiB to European destinations, transfer alone is about **US$0.99**; 10,000 such downloads are about **US$9.87**. Storage, operations, taxes and currency conversion are additional; destination and usage can change the rate. These are scenarios, not a quote, cost ceiling or traffic forecast. [Official pricing, consulted 2026-09-30](https://cloud.google.com/storage/pricing).

A smaller separately approved web derivative could reduce transfer and page weight. None has been generated: resizing/metadata removal would require the Owner's specific image-operation authorization, preserve the original, use deterministic processing and create a separately verified derivative relationship. AI image generation is not part of the scientific preview plan.

Candidate pilot budget: a **EUR 5/month monitoring threshold** scoped to the new preview resource where supported, subject to Owner selection and billing access. An alerts-only budget is not a spending cap; this proposal does not authorize automated billing shutdown that could affect other Digital StarGate workloads. [Official budget documentation](https://docs.cloud.google.com/billing/docs/how-to/budgets). Exact regional storage/request pricing, billing currency and monitoring capability must be verified before an apply authorization. Existing Google Cloud account/service terms apply; no purchase, PixInsight SDK redistribution or new software installation is performed by this proposal.

## Separate gates, in order

1. **Provider/design decision:** accept or reject the dedicated Google Cloud preview candidate. This alone is not permission to create resources, reuse credentials, upload or publish an image.
2. Prepare exact infrastructure/security/billing plan and reviewable preview/metadata selection. Keep protected scientific sources local. Present any required account action to the Owner; never request secrets in chat.
3. Resolve the governed external asset/context record without fabricating a Digital StarGate observation session. Complete source-bound Owner association, current expected/measured identities and immutable private retention/delivery. Missing context cannot be bypassed by a hosting decision.
4. Complete MIME/magic, malware/metadata/privacy and publication-rights checks required by BKL-034-F2. Existing header inspection is not this full gate; incomplete evidence stays quarantined.
5. Obtain exact resource/apply and selected-image publication authority, then execute only the reviewed bounded plan. Verify public bytes, exact gallery/workflow relationship, rollback and real OAT before milestone closure.

BKL-049 remains OPEN. BKL-043, its monitor/pilot, private infrastructure and Safety Authority remain unchanged. This proposal records an unresolved owner decision under DSG-AEM-001 section 5 (provider/paid service/structural dependency selection), not an approved architecture or operational release.
