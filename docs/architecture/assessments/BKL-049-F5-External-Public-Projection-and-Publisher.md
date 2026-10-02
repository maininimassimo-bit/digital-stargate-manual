# BKL-049 F5 — External public projection and local publisher

| Field | Value |
|---|---|
| Date | 2026-10-02 |
| Scope | ADR-019 external retrospective records, reviewed public selection, gallery V2 |
| Authority | Processing evidence only; no scientific quality or action authority |
| Activation | Real publication NOT AUTHORIZED; collection remains empty |

## Result and prerequisite

[ADR-019](../ADR-019-External-Retrospective-Scientific-Records.md) permits a distinct retrospective external record with PARTIAL metadata and UNKNOWN scientific quality. Its private delivery replays two separate Owner decisions and exact original/preview/workflow identities. Registration and admission are not public consent.

`external_public.py` now builds a minimal V2 public record from a verified private external delivery and an independently selected current public approval. It also prepares and atomically replaces a bounded, explicitly selected **local** public collection. It makes no network call, Git commit, preview upload or cloud access change. The gallery reader accepts the separate V2 record with explicit scientific limitations and an approved preview; V1 record validation remains closed and unchanged in meaning.

## Exact public approval

The closed `BKL049_EXTERNAL_PUBLIC_SELECTION_V2` record requires scope `EXACT_EXTERNAL_PREVIEW_AND_WORKFLOW`, exact delivery digest, approvedBy/approvedAt/validUntil, rightsConfirmed true, three public aliases (image/version/workflow), title, attribution, preview URL/alt/exact preview SHA-256, and selected workflow steps. Current journal head and current selection digest come from the accountable operator's independently maintained authority, never from an old rendered row. Actor strings and hashes are not authentication. An actual Owner field/rights/preview decision is required; fixture approvals are synthetic only.

Every step selects the exact stepId and processId. Parameters additionally select name and digest of the exact lexical value. A shared projection helper retains order and omission counts; it does not evaluate parameters or copy unselected data. The old V1 producer uses the same helper after its existing V1 authority guard. Empty step selection remains UNAVAILABLE; selected exported configurations remain DECLARED/PARTIAL and execution NOT_ESTABLISHED.

Approval is limited to at most 24 hours. The caller supplies trusted current UTC; future, expired, replaced or mismatched approvals reject. Release time/expiry must fit wholly inside the approval interval. Rebuilding or renewing requires current source/selection anchors; changing a delivery revision invalidates its old selection. No scheduler or automatic consent renewal is supplied.

## Public fields and gallery behavior

The closed schema is `schemas/bkl049-public-workflow-external.schema.json`. Its scientificContext is fixed to external origin, PARTIAL metadata, UNKNOWN quality and DECLARED_NOT_INDEPENDENTLY_VERIFIED subject identification. These labels cannot be omitted or promoted. Title, attribution and alt text are explicitly approved strings. Private actor identities, evidence sources, journal/candidate/source/file digests, paths and acquisition identifiers are not copied. An approved free-text field can itself contain sensitive information, so the Owner must review its exact content before approval.

Preview URLs are restricted to explicit HTTPS `storage.googleapis.com` bucket/object URLs for jpg/jpeg/png/webp, with a closed ASCII shape and no query, fragment, credentials, escapes or parent traversal. This supports the previously selected provider without publishing any actual bucket identity. Matching the selected preview digest to the private delivery verifies the intended file, **not the bytes currently served by a remote URL**. Authorized upload, immutable object naming and remote-byte verification remain real publication/OAT duties. Originals and full private workflows must never be uploaded as previews.

The panel displays the external/partial/unassessed/declared-identification labels alongside the preview and exact image/version/workflow link. Text uses textContent. Images use the validated URL, a supplied alt, lazy loading and no-referrer; load failure produces an unavailable message. Collection expiry, empty withdrawal and refreshed current selection remove cards. Browser/network caching and offline pages cannot provide instantaneous global revocation; the bounded release lifetime remains the maximum supported client display window. Existing no-JavaScript and unavailable behavior remains.

## Local publication transaction

`build_external_collection` accepts 0..8 fresh external selections. Duplicate image/version or workflow aliases reject. The nonempty collection has a current interval of at most 24 hours; the empty withdrawal collection has null publication/expiry. Maximum record/collection sizes remain 256 KiB / 2 MiB. The collection wrapper stays V1 and permits V1 or external V2 rows in its reader schema. This publisher constructs the **whole external collection**; it never merges cached V1 rows. The operator must review the whole replacement, including removal of any previous entries. A mixed legacy/external publisher is not provided.

`publish_external_collection` requires the explicitly selected existing local `bkl049-public-workflows.json` and its independent predecessor digest. It acquires an exclusive sibling lock, rechecks predecessor bytes, reconstructs all rows against current authority/approval, writes and flushes a same-directory temporary file, rechecks the predecessor and atomically replaces it. Failures before replace leave the original unchanged; byte-identical retry is a no-op. Lock conflicts and stale predecessor reject. Cleanup failure after commit is reported separately rather than misreporting the commit as failed. Trusted local parent, cooperating writers and fresh input authority are prerequisites; hostile filesystem administration and directory-entry power-loss durability are not claimed. A leftover lock requires accountable inspection, not automatic deletion.

The resulting local file is not a cloud deployment. Actual publication must still use the repository's reviewed PR/CI/ARB/RQ/expected-head merge/Pages workflow and an exact Owner-approved public selection. Rollback can publish the empty collection through the same review route; do not restore an expired historical projection. Emergency withdrawal does not require fabricating a new scientific admission.

## Private real progress, publication still closed

On 2026-10-02 the Owner explicitly approved both distinct acts for the previously reviewed private candidate and its disclosed local retention scope. The actual REGISTER and ADMIT events were retained separately, independently anchored, copied and replayed after restore. A real exact external F4/PXP V2 delivery was retained and restored; current full-file measurements matched the reviewed identities. Metadata stays PARTIAL, quality UNKNOWN and workflow evidence DECLARED/PARTIAL. Private identifiers, hashes, locations and the actual record remain outside Git. Same-volume local recovery is not disaster recovery.

This operational progress is not permission to publish. The exact public fields/rights/preview decision, authorized upload/access configuration, served-byte verification and real gallery OAT remain open. BKL-049 remains open; unrelated programs and scientific analytics are untouched.

## Verification and rollback

Synthetic tests cover role/consent separation, source/currentness mismatch, private-field exclusion, forbidden URLs, scientific-state promotion, approval/release expiry, empty withdrawal, duplicate IDs and bounded atomic replacement including failure/lock/stale predecessor/no-op. JS tests consume the actual Python-generated V2 fixture. Browser regression adds external labels, preview rendering, text-only injection safety, mobile layout, rejection of promoted quality and expiry; remote providers are intercepted, never contacted. Existing V1 suites remain required.

Rollback removes the additive V2 producer/reader support only after withdrawing public V2 rows. Preserve all private evidence and decisions. No dependency, cloud credentials, provider change or Safety Authority change is introduced. Separate ARB then RQ, exact-head CI and post-merge/Pages verification belong to the delivery PR.
