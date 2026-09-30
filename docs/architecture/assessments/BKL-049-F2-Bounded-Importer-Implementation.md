# BKL-049 F2 — Bounded local importer

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-F2-IMPL-001 |
| Version / date | 1.0 / 2026-09-30 |
| Status | Repository implementation for review; real import/OAT not performed |
| Entry gate | F1 accepted via PR #449, merge `32050f0a12ac1942c017f393c17b2e52466d6bd5` |
| Scope | Selected history export to private unlinked evidence packet |
| Action authority | NONE |

## Delivered code and boundaries

`tools/pixinsight/workflow_archive` implements the selected nonexecuting export parser, private source packet constructor/verifier and explicit local import CLI. The F0 reader path delegates to the single hardened parser; the original research revision remains in Git history. No vendor code, new dependency or PixInsight installation is introduced.

A packet retains exact original bytes separately from normalized lexical parameters, statement spans, exported container order and mask commands. It remains PRIVATE_NOT_APPROVED, UNLINKED and execution NOT_ESTABLISHED. Unsupported syntax/encoding retains original bytes with UNSUPPORTED extraction and no partially normalized result. File/context failures do not create an accepted packet.

The parser rejects execution calls, unknown syntax, duplicate variables/properties, reused children, cycles, post-attachment mutation and resource excess. Explicit numeric signs, decimal precision and exponent representation survive as lexical data. Embedded file references and expressions are never followed or evaluated.

Input/output paths reject symlink/reparse components; only bounded regular files are read. Identity/size/time changes during a read are rejected. Packet publication uses flushed staging plus create-if-absent hard link: identical retry is a no-op, conflicting or incomplete existing output is never overwritten. Unsupported filesystems fail closed without a non-atomic fallback. This is a trusted local filesystem boundary, not isolation against a hostile OS administrator or concurrently replaced parent directory. Destination access controls, independent digest receipts and backups are operational responsibilities. The module does not scan or create source/output directories.

## Internal contract and retained limits

Private packet 1.0 is reconstructed from its original bytes by the verifier; unexpected fields, changed authority or inconsistent normalization are rejected. An expected packet digest must come from a separately retained trusted receipt. Internal consistency and hash equality do not authenticate a workflow or confer scientific acceptance. Console output excludes private values, paths and fingerprints.

Bounds: 2 MiB source, 200,000 tokens, 512 instances, depth 32, 2,048 parameters/instance, 4,096 characters/string and items/array, 128 characters/identifier and numeric literal, 128 mask commands/container, 32 MiB encoded packet. These engineering limits are explicit support limits, not completeness guarantees.

The internal tagged lexical values are not an approved PXP interchange encoding. PXP/manifest/catalog schemas are unchanged. F3 must implement and test truthful evidence mapping; F4/F5 must supply identity and public-projection guards. No automatic pipeline or gallery path invokes this importer.

## Validation

Local Windows: 20 packet/boundary tests executed, 19 passed and 1 real-symlink creation test skipped because the OS lacks creation permission. The deterministic Windows reparse-attribute rejection test passed. The 27 retained export grammar regressions and 4 supplementary XISF reader tests passed. The skipped case requires Linux CI evidence before acceptance; Windows/Linux CI also test actual local hard-link packet creation.

Cases cover byte retention/BOM/line endings, deterministic construction, lexical round-trip, integrity/trust-anchor failure, source mutation, excessive input/values, duplicate retry, changed-source conflict, concurrent conflicting writer, interrupted commit cleanup, incomplete output preservation, encoding/syntax quarantine, private console output and no embedded path follow. All fixtures are synthetic temporary files; no scientific folder, PixInsight runtime or real image was used for F2 tests.

The workflow `.github/workflows/bkl049-workflow-archive.yml` runs packet, export and supplementary header tests on Windows and Linux for relevant PRs and main pushes. Exact-head CI/review and merge-SHA evidence must be recorded in the delivery PR; the local result is not a CI claim.

## Residual gates and rollback

F2 acceptance is limited to the supported repository importer and synthetic filesystem checks. F3 semantic/PXP adaptation, F4 authoritative source/image/version binding, F5 approved public projection/gallery access and F6 real authorized read-only OAT remain open. Source artifact licensing/selection and actual private destination access must be verified before operational use. A declaration connecting an original and preview is evidence, not publication permission or catalog registration.

Rollback reverts the module/workflow and compatibility shim through a reviewed change. Preserve existing private packets; their version must be validated by future tools. No device, image or catalog state is changed. A process kill may leave an unaccepted private staging file, never automatically imported; cleanup must not delete retained accepted evidence. BKL-043 remains current and untouched operationally.

## Revision history

- 1.0 — Bounded importer with original source retention and synthetic boundary tests; no real ingestion or public publication.
