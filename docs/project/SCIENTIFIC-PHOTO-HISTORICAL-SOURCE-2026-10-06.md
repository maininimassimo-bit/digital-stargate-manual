# Historical source in photo ingestion — 6 October 2026

Owner-requested additive upload path for images acquired before their sessions
were imported into the portal. This extends the guided photo upload; it does not
close BKL-049-EXT-PIAI/P6, admit an AP-014 registry record or replace the separate
ADR-019 external registration/admission contracts.

The imported-session path keeps its measured catalogue snapshot and 1–32 real
sessions of the same target. The historical path instead requires an explicit
target, private provenance description and Owner attestation. It fixes
`sessionIds=[]`, `catalogSha256=null`, source `HISTORICAL_OWNER_DECLARATION` and
session/registry association `NOT_ESTABLISHED`. Mixed declarations reject before
any file writes. Historical creation and resume require no catalogue access.

Requests remain immutable under their upload identity. A resumed upload restores
and locks the exact source, target, provenance, title, date and version; changed
files or declarations require a new upload. Original, preview and exported
workflow retain the existing size, integrity, malware scanning, sanitation,
explicit rights, field selection, withdrawal and private-backup gates.

The public record exposes the declared historical origin and zero session links.
Its full provenance text remains private, even after publication. Original and
workflow source also remain private; process names are selected initially and
parameters require explicit field approval. Execution and full upstream History
are not established by an exported incremental workflow. Existing imported-session
records and legacy M27 remain unchanged.

Only the upload feature is authorized by this request: no real scientific file
is uploaded or published by the implementation or its synthetic tests. Publishing
M31 remains a separate Owner review of the exact sanitized preview and fields.

Release gates: exact-head CI, sequential separate AI-assisted ARB and RQ, merge,
API/Pages deployment and post-merge verification. Existing resource, IAM and
credential scope remains unchanged. Deploy the compatible portal reader before
any real historical publication. Rollback retains all immutable receipts and
current state; once a historical upload/publication exists, keep compatible
readers and disable new historical entry rather than reverting to a reader that
cannot handle zero-session records. Do not withdraw or rewrite current scientific
publications merely to test rollback.
`DSG_PHOTO_HISTORICAL_UPLOAD=0` suspends new historical uploads while preserving
exact retries, retained private reviews and public readers. `/health` advertises
this capability; the new form disables historical creation against an older or
suspended service. No credential, IAM or resource change is required.

Validation includes imported-session regressions and synthetic historical upload,
interrupted multi-chunk resume with unavailable catalogue, immutable declarations,
private provenance minimization, public gallery with no invented session links,
rights/scanner/actor gates and explicit withdrawal. Synthetic publication is not
real scientific-file acceptance or Owner operational acceptance.
