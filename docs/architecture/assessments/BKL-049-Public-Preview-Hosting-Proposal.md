# BKL-049 — Public preview hosting decision candidate

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-PREVIEW-HOSTING-001 |
| Version / date | 1.1 / 2026-09-30 |
| Status | OWNER-SELECTED architecture — implementation and delivery gates remain |
| Purpose | Supply an approved public preview URL for the mandatory exact gallery image/version-to-workflow relationship |

Owner disposition (2026-09-30): **"Approvo la soluzione Google Cloud proposta"**, in response to the exact preview-only proposal and EUR 5/month monitoring threshold (not a guaranteed spending cap). This accepts the provider/design candidate, not service activation, new/extracted credentials or reuse of workload identities, paid activation, image changes or publication.

## Confirmed need

The Owner confirmed that no dedicated online image space exists. The selected demonstration material is external to Digital StarGate; its final-to-preview relationship is Owner-declared. No real catalog registration, publication classification or complete acquisition context has been accepted. Unknown acquisition data stay unknown. Identifying an author does not independently prove publication rights or establish scientific context.

F3 is accepted and the F4 identity guard is delivered separately. They do not supply binary hosting or authorize public exposure. [AP-013](../packages/AP-013-Scientific-Image-Repository-Architecture.md) keeps scientific binaries out of the manual repository, and [BKL-034-F2](../packages/BKL-034-F2-Storage-Boundary-Preflight.md) requires its storage/privacy/integrity gate before publication. GitHub Pages remains the read-only consumer.

## Recommended candidate

Use **one new, dedicated Google Cloud Storage bucket for approved web previews only**, region `europe-west1` (Belgium), Standard storage. Google Cloud is already used in the repository's separately governed infrastructure; this proposal does not reuse its private buckets, identities, permissions or deployment authorization. The existing project and a neutral candidate bucket identity were resolved privately during the bounded metadata preflight. The four selected effective organization constraints were subsequently read after the separately authorized API activation, as recorded below. No preview bucket or paid workload has been created.

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

Candidate pilot budget: a **EUR 5/month monitoring threshold** scoped to the new preview resource where supported, selected by the Owner as a monitoring objective, subject to verified billing currency/access and resource-filter support. An alerts-only budget is not a spending cap; this proposal does not authorize automated billing shutdown that could affect other Digital StarGate workloads. [Official budget documentation](https://docs.cloud.google.com/billing/docs/how-to/budgets). Exact regional storage/request pricing, billing currency and monitoring capability must be verified before an apply authorization. Existing Google Cloud account/service terms apply; no purchase, PixInsight SDK redistribution or new software installation is performed by this proposal.

## Separate gates, in order

1. **Provider/design decision — accepted:** the Owner selected the dedicated Google Cloud preview candidate. This alone is not permission to create resources, extract credentials, reuse workload identities, upload or publish an image.
2. Prepare exact infrastructure/security/billing plan and reviewable preview/metadata selection. Keep protected scientific sources local. Present any required account action to the Owner; never request secrets in chat.
3. Resolve the governed external asset/context record without fabricating a Digital StarGate observation session. Complete source-bound Owner association, current expected/measured identities and immutable private retention/delivery. Missing context cannot be bypassed by a hosting decision.
4. Complete MIME/magic, malware/metadata/privacy and publication-rights checks required by BKL-034-F2. Existing header inspection is not this full gate; incomplete evidence stays quarantined.
5. Obtain exact resource/apply and selected-image publication authority, then execute only the reviewed bounded plan. Verify public bytes, exact gallery/workflow relationship, rollback and real OAT before milestone closure.

BKL-049 remains OPEN. BKL-043, its monitor/pilot, private infrastructure and Safety Authority remain unchanged. The provider/design choice is Owner-approved; this document does not grant an operational release. DSG-AEM-001 section 5 remains binding for new/extracted credentials or workload-identity reuse, paid activation and publication.

## Prepared next step: bounded read-only cloud preflight

**PREPARED / read-only execution under standing authorization.** The Owner authorized autonomous noninvasive technical verification and selected Google Cloud. Normal metadata reads through the existing interactive user CLI session fall within that scope; they do not require an additional approval. This is not permission to extract/reuse tokens or keys, impersonate a service account or activate infrastructure. The scope is limited to the project already pinned by this repository's `GCP_PROJECT_ID` / authenticated-platform workflow. The existing BKL-031 deployment identities, WIF workflows, state/data/evidence buckets and BKL-043 resources are not reused or changed.

Before contacting Google Cloud, resolve the repository project value without displaying private configuration, verify it agrees with the pinned repository project, record a neutral candidate preview-bucket name privately, and check that an existing interactive CLI identity is available. No login, service-account impersonation, token printing/export, key file, secret lookup, SDK installation/update or persistent configuration change is allowed. A missing/ambiguous identity stops the preflight.

The allowlist is at most **nine high-level read commands**, once each, using an explicit project and JSON output retained only outside public Git. CLI internal transport retries are not represented as nine guaranteed HTTP requests. No broad bucket/object inventory or scientific bytes are read.

| Read command | Purpose and limit |
|---|---|
| `gcloud projects describe PROJECT` | Existing project's lifecycle/identity only |
| `gcloud services list --enabled --project=PROJECT --filter=config.name:storage.googleapis.com` | Confirm existing Storage API availability; never enable it |
| `gcloud org-policies describe storage.publicAccessPrevention --project=PROJECT --effective` | Detect an inherited public-access prohibition |
| `gcloud org-policies describe iam.allowedPolicyMemberDomains --project=PROJECT --effective` | Legacy domain restriction, if readable |
| `gcloud org-policies describe iam.managed.allowedPolicyMembers --project=PROJECT --effective` | Managed principal restriction, if readable |
| `gcloud org-policies describe gcp.resourceLocations --project=PROJECT --effective` | Check the selected European-region policy |
| `gcloud billing projects describe PROJECT` | Linked billing status/reference only; no enable/link/change |
| `gcloud billing accounts describe LINKED_ACCOUNT` | Only the already linked account's metadata, if authorized; no list of unrelated accounts, payment details or transactions |
| `gcloud storage buckets describe gs://CANDIDATE` | Only the new neutral preview name; permission denial is inconclusive, and absence does not reserve the name |

`PROJECT`, `LINKED_ACCOUNT` and `CANDIDATE` are private resolved inputs, not commands to run literally. All invocations use noninteractive mode and bounded execution time; no escalation or installation follows a denial. Unreadable policy/billing fields are UNAVAILABLE, never presumed permissive. The preflight is not an authorization to apply infrastructure or declare all permissions sufficient.

Official command references: [organization policy describe](https://docs.cloud.google.com/sdk/gcloud/reference/org-policies/describe), [project billing describe](https://docs.cloud.google.com/sdk/gcloud/reference/billing/projects/describe), [billing account describe](https://docs.cloud.google.com/sdk/gcloud/reference/billing/accounts/describe), [bucket describe](https://docs.cloud.google.com/sdk/gcloud/reference/storage/buckets/describe).

Expected result: a private evidence record and a sanitized availability/blocker summary sufficient to prepare the exact resource/apply plan. No new bucket, budget, IAM binding, upload, image conversion, public URL or chargeable runtime is activated. Any standard metadata-operation charges remain governed by the service's pricing; no zero-cost guarantee is made. An unavailable prerequisite requires an explicit Owner disposition, not a workaround through another identity or project.

## Initial read-only preflight evidence

The bounded preflight was completed with the already authenticated interactive user profile under the standing noninvasive-work authorization. No new login, token/key extraction, impersonation, service-account use or cloud mutation occurred. All nine high-level reads were attempted; private responses/identities stay outside Git.

- Project: ACTIVE; the selected Storage API is already enabled.
- Linked billing account: open, billing enabled, currency EUR. The selected EUR 5 monitoring objective therefore needs no invented currency conversion; filter support and actual budget creation remain unverified.
- Candidate preview name: NOT_FOUND at read time; this does not reserve it or prove create permission.
- All four policy reads: UNAVAILABLE with explicit `SERVICE_DISABLED` for `orgpolicy.googleapis.com`. This is not evidence that public access or the region is permitted, and it does not prove the underlying policy-read permissions.
- No storage object, budget, IAM binding or policy was created/changed. The selected image remains private and unlinked.

The minimum proposed unblock is **one service activation** in the same pinned project:

```text
gcloud services enable orgpolicy.googleapis.com --project=PROJECT
```

At the initial preflight this state change was **NOT AUTHORIZED / NOT EXECUTED**. That historical state is superseded only for this API by the subsequent explicit authorization and execution receipt below. It enables the administrative policy API only; it does not create a bucket, change a policy/IAM rule, enable public access, create a workload or upload an image. After authorization and the applicable review gate, rerun only the four policy descriptions above; permission failure stays blocked with no broader role grant or alternate identity. Verify the returned policy evidence before any storage apply plan.

The prior disabled state is recorded. Rollback, if specifically required, is disabling only this API after checking dependencies; never force-disable dependent services or change another workload. No recurring activity is introduced. [Official service-enable command](https://docs.cloud.google.com/sdk/gcloud/reference/services/enable).

## Authorized API activation and verified result

On 2026-09-30 the Owner explicitly authorized **only** Organization Policy API activation and the four policy reads. The API activation completed successfully, followed by four successful effective-policy responses in the same pinned project and existing interactive session. No credentials were extracted or identities impersonated. Private raw evidence and the authorization receipt remain outside Git.

| Effective constraint | Observed response |
|---|---|
| `storage.publicAccessPrevention` | `enforce=false` |
| `iam.allowedPolicyMemberDomains` | `allowAll=true` |
| `iam.managed.allowedPolicyMembers` | `enforce=false` |
| `gcp.resourceLocations` | `allowAll=true` |

Each response contained one unconditional rule. These four constraints do not themselves prohibit the proposed region/public reader at the time of reading. They do not prove bucket creation, IAM mutation or budget permissions; other controls and later changes may still block an operation. No organization policy was changed. No bucket, budget, IAM grant, upload or public image was created.

Architecture PR #453 is integrated at `731cc8ce1dd3322d088ca15811cd1476ed1a332a`: 17/17 post-merge runs succeeded, including Pages run 36773773573. The published proposal returned HTTP 200 with expected content. [Recorded post-merge and activation evidence](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/453#issuecomment-5919374995).

## Reviewable next operation: empty private preview bucket

**PREPARED / NOT EXECUTED / specific resource authorization required.** This step creates exactly one empty preview bucket in the already resolved project. It deliberately keeps public-access prevention enforced while the image and catalog gates are completed. The private receipt pins the neutral candidate name; no alternate project/name is selected silently if it is unavailable.

| Setting | Exact proposed disposition |
|---|---|
| Resource count | One new empty bucket; no objects |
| Location / class | `europe-west1` / `STANDARD` |
| Access model | Uniform bucket-level access; public-access prevention enforced |
| Principal changes | None; existing inherited project access is inspected after creation, not silently rewritten |
| Encryption | Google-managed default; no new key or key service |
| Recovery | Explicit seven-day soft deletion; no locked retention policy |
| Other features | No Autoclass, lifecycle deletion, object-versioning activation, website, CDN, CORS or background sync |
| Identity | Same existing interactive session; explicit project/account arguments; no service-account reuse |
| Output | Private creation/configuration/IAM receipts and sanitized public result |

Reviewed command shape (placeholders are resolved from the private preflight receipt, never literal public identifiers):

```text
gcloud storage buckets create gs://CANDIDATE --project=PROJECT --account=EXISTING_INTERACTIVE_ACCOUNT --location=europe-west1 --default-storage-class=STANDARD --uniform-bucket-level-access --public-access-prevention --soft-delete-duration=7d --quiet --format=json
```

Before the write, recheck the pinned project/session, candidate absence and relevant effective constraints. A conflict, permission failure or changed restrictive policy stops the operation; no role grant, alternate identity, replacement bucket or retry that changes scope follows. After an unknown write outcome, describe this exact candidate and establish ownership/configuration before considering any retry. After success, describe the bucket and read its IAM policy privately; verify region, class, uniform access, prevention and soft-delete interval. Unexpected inherited access is a blocker for uploading data, not permission to alter project IAM.

This creates a billable-service resource, with no stored bytes or public-download traffic in this step. No zero-cost guarantee is made: metadata operations and future usage follow service pricing. The selected EUR 5 monitoring objective is **not yet activated**, and no cost ceiling is claimed. Exact regional storage/request pricing and an approved budget/notification configuration remain prerequisites to uploading the pilot image. [Bucket creation flags](https://docs.cloud.google.com/sdk/gcloud/reference/storage/buckets/create).

Rollback for this step is to leave the empty bucket private and stop. Deletion requires a separate deliberate decision after proving it is still empty and exclusively this resource; no automatic deletion or project-wide rollback. Source originals remain local throughout.

## Subsequent publication and monitoring gates

These are **not included** in the empty-bucket authorization:

- Budget: EUR 5 monthly alerts-only objective. The CLI supports a resource-label filter and project filter, but a label must be applied and actual billing attribution verified before calling this a preview-only monitor. Budget API availability and creation permission remain unverified. Default budget notification recipients include billing administrators/users, so no default-recipient budget is created silently. Select and authorize the recipient configuration before enabling alerts; no billing shutdown. [Budget command and notification options](https://docs.cloud.google.com/sdk/gcloud/reference/billing/budgets/create).
- Preview: choose the exact approved bytes, complete integrity/MIME/malware/privacy/rights checks and the authoritative external-origin catalog association. No resize, upload or public classification follows from bucket creation.
- Publication: separately authorize lifting prevention **only on this dedicated bucket** and the public read-without-listing binding. Recheck effective policies first. Public-read bucket access exposes every object in that bucket: it must contain only individually approved previews, never private staging material. A public URL and its metadata are public even without listing. [Public access guidance](https://docs.cloud.google.com/storage/docs/access-control/making-data-public).
- Delivery: verify public bytes and exact image/version-to-workflow binding, minimized field selection, private retention/delivery and real gallery OAT. Revoking public access cannot recall cached/downloaded copies.

Full F4 and BKL-049 remain OPEN. BKL-043, its monitor, EAGLE and existing private storage/IAM remain untouched. This document is an operational plan, not evidence that the resource or monitoring exists.
