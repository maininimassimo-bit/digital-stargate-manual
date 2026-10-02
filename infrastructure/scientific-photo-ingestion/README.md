# Scientific session photo ingestion — runtime candidate

This is the Owner-approved successor procedure to the contract-only BKL-034 F2
and bounded BKL-049 archive. It implements uploads and private review, not a
change to the old AP-014 admission library or to BKL-042/EAGLE runtimes.

## Implemented procedure

The portal links from an imported session to `/scientific-photo-upload/`.
The existing Google web client identifies the Owner; every private HTTP route
verifies the token audience and verified email through google-auth and requires
the exact configured portal origin. Tokens stay in browser memory. No cloud
credentials reach the browser. Public routes read only the current publication
head and its approved sanitized previews. Buckets remain private, including
backups. Public preview URLs never select an arbitrary storage object.

One image can originate from 1–32 imported sessions with the same literal target.
For each new upload, the service independently reads the current analytics
catalogue from the fixed public repository projection URL, rejects redirects and
bounds the response. Its measured digest must match the exact catalogue bytes
shown by the Scientific Data Engine in the upload form. It retains that snapshot;
exact resume requests keep the original snapshot despite later updates. There
is no stale bundled fallback if the current catalogue cannot be verified.
The relationship is `OWNER_DECLARED`, not AP-014 registry admission,
independent target identification or acquisition metadata certification. Dates
and absent historical configuration are not inferred. Processing date is separate.

Original XISF/FITS (1 GiB), JPEG/PNG preview (32 MiB), and exported workflow
(2 MiB) upload in immutable 4 MiB chunks. Repeating an identical request or
chunk is idempotent; changed content under the same identity rejects. The browser
hashes files incrementally; the service independently measures complete bytes.
Status reads chunk metadata instead of re-downloading files. Browser session
storage holds only the request nonce and opaque upload identifier; filenames, tokens and file contents are
not persisted there. The authenticated archive can recover the nonce after a
browser restart. Reselecting identical files resumes only missing chunks.

Files remain quarantined until all three antivirus checks pass. ClamAV must have
fresh databases (48-hour operational security freshness, not a scientific
threshold); freshclam attempts an update when needed. Missing/expired definitions,
scanner errors and scan resource limits block publication. Private retention is
still permitted with the explicit quarantine state. `Ripeti controlli` constructs
a new immutable review and invalidates the previous field approval. It cannot
mutate a published version. The service never executes exported code or opens
embedded paths. Unsupported exports retain their exact bytes and have no invented
steps; supported subsets use the already-reviewed BKL-049 DECLARED adapter.

A passing preview is decoded under a 40-megapixel resource limit and saved into
a new JPEG pixel buffer, with orientation applied and EXIF/XMP/comments/ICC
omitted. This changes only the publication derivative, never original files.
The Owner sees that exact sanitized preview, selected sessions, title, processing
date and workflow fields before committing. Default public steps contain process
names only; each parameter requires an explicit name and exact-value digest
selection. Values too large for bounded public display stay private.

Save private and publish are separate state transitions. Version identity is
immutable; a new version may reuse an existing image identity of the same target.
Publication remains until explicit withdrawal (`validUntil=null`). A withdrawal
removes both discovery and anonymous preview access on the next request; already
downloaded copies cannot be recalled. Every state transition and its audit entry
are committed in one generation-guarded control object. Storage conflicts retry;
binary/review objects are immutable, and interrupted unreferenced writes do not
publish records. The library assumes trusted service identity and administrators;
hashes are integrity anchors, not proof against an administrator rollback.

## Persistence and recovery

`GCSStore` is the production adapter. `MemoryStore` exists only in synthetic
tests and is never used as a runtime fallback. `BackedUpStore` writes an immutable
recovery copy into a second private bucket before each primary write; backup
failure prevents the primary write. A primary compare-and-swap failure may leave
an uncommitted backup candidate; restore must select a verified committed head,
never the most recent candidate by timestamp. Both buckets must enable object
versioning. There is no automatic deletion or retention lock in this increment.
Chunks and originals are deliberately retained. A future retention/compaction
procedure requires its own reviewed plan; no silent cleanup is performed.

The first increment admits at most 64 uploads/versions, 4096 audit events and a
2 MiB control state. Capacity exhaustion fails explicitly; it never deletes old
versions. Backups are separate-bucket recovery evidence, not an offsite/provider
disaster recovery claim. Production restore/read-back verification is a runtime
activation gate, not established by synthetic tests.

## Deployment gate

The Owner separately approved the exact paid resource/cost proposal on 02/10/2026.
The service and two private versioned buckets are deployed; the old one-JPEG
grant remains separate. See the runtime activation evidence in
`docs/project/SCIENTIFIC-PHOTO-RUNTIME-ACTIVATION-2026-10-02.md`.
The portal configuration stages the verified HTTPS endpoint in
`OWNER_LOGIN_OAT_PENDING` mode: Google login and readonly archive retrieval are
available, while upload, review, publication and withdrawal controls are disabled.
An actual Owner Google login is still required; the endpoint is not operational
acceptance. A reviewed configuration change enables the complete procedure only
after this gate. Tokens remain in browser memory and are not extracted for evidence.
The new service has min=0/max=1 instances, request-based billing and no hard
spending cap. Storage/egress/build/registry charges remain possible while idle.

After authorization and reviewed source merge:

1. Verify existing project/account and absence of the exact proposed resources.
2. Create only the proposed registry, dedicated runtime identity and two private,
   versioned buckets in europe-west1; enforce public-access prevention and UBLA.
3. Primary IAM: objectCreator + objectViewer; objectUser only with a condition
   matching `control/state.json`, since GCS overwrite requires create+delete.
   Backup IAM: objectCreator + objectViewer, with no overwrite/delete grant.
4. Build the reviewed source through its Dockerfile-specific context allowlist,
   retain build evidence, resolve the registry digest and deploy that digest with
   the exact limits and six required environment variables listed in `app.py`.
   Use the already configured Google client ID, Owner email and portal origin.
   Set `DSG_INGESTION_PUBLIC_BASE` to the resulting HTTPS service origin.
5. Expose only the service HTTP surface; no public bucket IAM. Test anonymous and
   non-Owner denial, actual Google login, scanner readiness, sanitized metadata,
   multi-chunk interrupted upload, private save, exact field review, published
   preview, new version, withdrawal, state contention and separate-bucket restore
   using clearly synthetic files. Do not migrate or upload existing science files.
6. Submit the verified service URL as a separately reviewed portal configuration
   change in the readonly Owner-login verification mode; verify exact merge
   workflows and actual Pages. Complete actual Owner login, then review normal
   activation. Leave upload/mutation controls disabled if a live gate fails.
   Owner real-file OAT follows, without fake acceptance.

Rollback: leave all retained originals and recovery copies intact, set portal
`serviceUrl=null`, and disable new service requests. Revert portal code only via a
normal reviewed commit. Do not delete buckets or restore an older publication
head, which could revive withdrawn images. Existing BKL-049 publication is unchanged.

## Validation

Python ingestion/service tests cover selection conflicts, incomplete/changing
uploads, idempotency, resumption, full-file digests, quarantine, exact approval,
multiple versions, state conflicts, private retention, sanitation and withdrawal.
The browser regression drives the production HTTP adapter with a loopback-only
synthetic auth/scanner/store. This proves the UI and HTTP integration, not Google
token verification, Cloud IAM, live antivirus or deployed durability. The test
also compares streaming SHA-256 against Node crypto at padding/chunk boundaries,
uses a hostile text title, checks mobile overflow and private/public minimization.

Sources: [Cloud Run filesystem and resource contract](https://docs.cloud.google.com/run/docs/container-contract),
[Pillow preview sanitation guidance](https://pillow.readthedocs.io/en/stable/handbook/security.html),
[GCS overwrite permissions](https://docs.cloud.google.com/storage/docs/access-control/iam-permissions),
[Cloud Run billing](https://cloud.google.com/run/pricing).
