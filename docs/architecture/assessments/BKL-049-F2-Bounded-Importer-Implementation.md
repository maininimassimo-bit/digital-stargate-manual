# BKL-049 F2 — Bounded local importer

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-F2-IMPL-001 |
| Version / date | 1.0 / 2026-09-30 |
| Status | ACCEPTED / POST-MERGE VERIFIED, bounded repository scope; real import/OAT not performed |
| Entry gate | F1 accepted via PR #449, merge `32050f0a12ac1942c017f393c17b2e52466d6bd5` |
| Scope | Selected history export to private unlinked evidence packet |
| Action authority | NONE |

[F2 acceptance](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/450#issuecomment-5918149706): PR #450, merge `b57adb0e8ee8d43b5bf7d5e05a718341520128ab`, 19/19 post-merge workflows SUCCESS and Pages verified.

## Delivered code and boundaries

`tools/pixinsight/workflow_archive` implements the selected nonexecuting export parser, private source packet constructor/verifier and explicit local import CLI. The F0 reader path delegates to the single hardened parser; the original research revision remains in Git history. No vendor code, new dependency or PixInsight installation is introduced.

A packet retains exact original bytes separately from normalized lexical parameters, statement spans, exported container order and mask commands. It remains PRIVATE_NOT_APPROVED, UNLINKED and execution NOT_ESTABLISHED. Unsupported syntax/encoding retains original bytes with UNSUPPORTED extraction and no partially normalized result. File/context failures do not create an accepted packet. Successful commit followed by staging cleanup failure is reported as CREATED_CLEANUP_PENDING, not REJECTED; exact retry preserves the committed packet.

The parser rejects execution calls, unknown syntax, duplicate variables/properties, reused children, cycles, post-attachment mutation and resource excess. Explicit numeric signs, decimal precision and exponent representation survive as lexical data. Embedded file references and expressions are never followed or evaluated.

Input/output paths reject symlink/reparse components; only bounded regular files are read. Identity/size/time changes during a read are rejected. Packet publication uses flushed staging plus create-if-absent hard link: identical retry is a no-op, conflicting or incomplete existing output is never overwritten. Unsupported filesystems fail closed without a non-atomic fallback. This is a trusted local filesystem boundary, not isolation against a hostile OS administrator or concurrently replaced parent directory. Destination access controls, independent digest receipts and backups are operational responsibilities. The module does not scan or create source/output directories.

## Internal contract and retained limits

Private packet 1.0 is reconstructed from its original bytes by the verifier; unexpected fields, changed authority or inconsistent normalization are rejected. An expected packet digest must come from a separately retained trusted receipt. Internal consistency and hash equality do not authenticate a workflow or confer scientific acceptance. Console output excludes private values, paths and fingerprints.

Bounds: 2 MiB source, 200,000 tokens, 512 instances, depth 32, 2,048 parameters/instance, 4,096 characters/string and items/array, 128 characters/identifier and numeric literal, 128 mask commands/container, 32 MiB encoded packet. These engineering limits are explicit support limits, not completeness guarantees.

The internal tagged lexical values are not an approved PXP interchange encoding. PXP/manifest/catalog schemas are unchanged. F3 must implement and test truthful evidence mapping; F4/F5 must supply identity and public-projection guards. No automatic pipeline or gallery path invokes this importer.

## Validation

Local Windows after RQ M01 remediation: 22 packet/boundary tests executed, 21 passed and 1 real-symlink creation test skipped because the OS lacks creation permission. The deterministic Windows reparse-attribute rejection test passed. The 27 retained export grammar regressions and 4 supplementary XISF reader tests passed. The skipped case requires Linux CI evidence before acceptance; Windows/Linux CI also test actual local hard-link packet creation.

Cases cover byte retention/BOM/line endings, deterministic construction, lexical round-trip, integrity/trust-anchor failure, source mutation, excessive input/values, duplicate retry, changed-source conflict, concurrent conflicting writer, interrupted commit cleanup, incomplete output preservation, encoding/syntax quarantine, private console output and no embedded path follow. All fixtures are synthetic temporary files; no scientific folder, PixInsight runtime or real image was used for F2 tests.

The workflow `.github/workflows/bkl049-workflow-archive.yml` runs packet, export and supplementary header tests on Windows and Linux for relevant PRs and main pushes. Exact-head CI/review and merge-SHA evidence must be recorded in the delivery PR; the local result is not a CI claim.

RQ M01 on the initial F2 head identified a misleading rejection after successful commit followed by cleanup failure. This increment distinguishes committed-with-cleanup-pending from commit failure and tests both the retained packet/retry and failure-with-residue paths. Earlier CI results do not validate this revised head.

## Residual gates and rollback

F2 acceptance is limited to the supported repository importer and synthetic filesystem checks. F3 semantic/PXP adaptation, F4 authoritative source/image/version binding, F5 approved public projection/gallery access and F6 real authorized read-only OAT remain open. Source artifact licensing/selection and actual private destination access must be verified before operational use. A declaration connecting an original and preview is evidence, not publication permission or catalog registration.

Rollback reverts the module/workflow and compatibility shim through a reviewed change. Preserve existing private packets; their version must be validated by future tools. No device, image or catalog state is changed. A process kill may leave an unaccepted private staging file, never automatically imported; cleanup must not delete retained accepted evidence. BKL-043 remains current and untouched operationally.

## Revision history

- 1.0 — Bounded importer with original source retention and synthetic boundary tests; no real ingestion or public publication.


## Importer profile 1.1: retained long parameter literals

A selected real export was retained privately by profile 1.0 with UNSUPPORTED/STRING_LIMIT: one calibration reference-spectrum string has 9,620 characters, beyond the previous 4,096-character limit. Its original bytes remain retained and unchanged; unsupported did not mean discarded.

Profile 1.1 permits strings up to **16,384 decoded characters**, including literal concatenation, while keeping the 2 MiB source, token, instance, nesting, parameter and array limits unchanged. No execution, spectrum interpretation, scientific validation or publication is introduced. The scientific/PXP contract remains unchanged; only this private parser support profile advances.

Packets keep schemaVersion 1.0 and explicitly record importerVersion 1.0 or 1.1. Verification reconstructs with the recorded version, so a historical 1.0 unsupported packet remains byte-verifiable after the upgrade. New imports default to 1.1. Re-importing with improved support requires a new receipt ID and separate immutable packet; old records are never silently rewritten or reclassified. Unknown importer versions fail closed. The research parser's default remains profile 1.0 for reproducibility.

Synthetic tests cover the exact accepted bound, overflow through concatenation, a long synthetic reference value, unchanged verification of historical unsupported packets and rejection of unknown versions. A private read-only dry run of the selected source with 1.1 returned 23 instances (2 containers, 21 processes), 381 parameter assignments and 9 mask commands. These are export syntax observations only: no runtime order, complete lineage or scientific correctness is established. No raw parameter or source digest is published. Reviewed operational re-import and real binding remain separate.


## Real retained-source reimport — 2026-10-01

After PR #457 acceptance, the explicitly selected real history was reimported privately with profile 1.1 into a new immutable receipt. The original profile-1.0 UNSUPPORTED packet was preserved and verified under its stored version. The new packet was committed and independently reread against its separately retained digest: 23 instances (2 containers, 21 processes), 381 parameter assignments, 9 mask commands and 435 statements. No source parameter text or private digest is published here.

This is an actual private retained import, superseding the earlier in-memory dry run as operational importer evidence. It remains `PARSED_SUBSET`, `UNLINKED`, `PRIVATE_NOT_APPROVED`, with execution `NOT_ESTABLISHED` and workflow completeness `UNAVAILABLE`. It does not prove runtime execution, historical model identity, authoritative image/catalog binding or public gallery delivery. Original image bytes and PixInsight were not modified.
