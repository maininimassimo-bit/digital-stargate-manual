# Session photo ingestion — implementation and activation gates (02/10/2026)

Owner-approved guided procedure, reserved initially to the Owner. The source
increment implements session selection, versioned private uploads, workflow
import, source-byte preservation, exact public field review, publication and
withdrawal. The three sample gallery cards are removed from the production page.
Existing BKL-049 real publication remains untouched.

Local verification: 16 Python boundary/security/persistence tests PASS; strict
MkDocs build PASS; browser regression PASS against the real HTTP adapter with
synthetic authentication, antivirus and storage. Streaming SHA-256 agrees with
Node crypto at padding and upload boundaries. Browser checks include private
save, default parameter omission, publication, mobile overflow, hostile text and
withdrawal. These tests do not establish cloud IAM, actual Google token OAT,
real ClamAV definitions, production storage/recovery or actual scientific-file
acceptance. CI and ARB/RQ exact-head review are pending at this source snapshot.

Production activation is NOT_EXECUTED. `docs/data/photo-ingestion-config.json`
has a null service URL and keeps upload unavailable. The exact proposed paid
resources/limits are in
`infrastructure/scientific-photo-ingestion/deployment-plan.json`; the full
implementation, recovery assumptions, resource envelope and rollout/rollback
steps are in its README. Owner approval of the functional procedure does not
broaden the earlier one-JPEG cloud/budget grant. An exact runtime decision under
DSG-AEM-001 section 5 is required after the implementation is concrete/reviewable.

Runtime acceptance requires actual Owner Google login, non-Owner/anonymous
rejection, private/backup bucket ACLs, complete uploaded-byte read-back, current
antivirus success and negatives, preview metadata inspection, resumable upload,
version preservation, publication/withdrawal and a verified separate-bucket
restore. No automated ingestion, migrated science files, AP-014 registry
promotion, device processing/control or BKL-043 runtime mutation is authorized.

Rollback disables the new service URL/requests while preserving all private
objects and recovery copies. It must not restore an old public head or revive
withdrawn records. The completed legacy contracts retain their original scopes.
