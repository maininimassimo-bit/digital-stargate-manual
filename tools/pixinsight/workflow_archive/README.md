# BKL-049 bounded local workflow import — F2

Repository implementation, not a PixInsight plugin or released gallery integration. Uses Python standard library only. Never executes JavaScript or PixelMath, opens embedded paths, modifies scientific images, registers catalog assets or publishes packets. No native/vendor code is included.

## Explicit invocation

Run from the repository root, using a selected UTF-8 history export and a **private existing directory** outside Git and the published site:

```text
python -m tools.pixinsight.workflow_archive.archive SOURCE_EXPORT PRIVATE_PACKET --receipt-id BKL049-UNIQUE_ID --imported-at YYYY-MM-DDTHH:MM:SSZ
```

Supply a real UTC import timestamp. It is not execution time. Reuse the same receipt ID/time and original bytes for deterministic retry. All output packets contain the original source (base64 is NOT encryption), private lexical values and hashes; never commit/upload them. Secure the destination using existing OS access controls before use. Real source/storage use remains governed separately from synthetic implementation testing.

Exit 0: supported subset retained, still UNLINKED and NOT_ESTABLISHED execution evidence. Exit 2: original retained with UNSUPPORTED extraction, normalized archive absent. Exit 1: file/context/integrity/commit error; do not assume an existing destination belongs to this attempt. A successful commit with staging cleanup failure returns CREATED_CLEANUP_PENDING (or DUPLICATE_NOOP_CLEANUP_PENDING), with the ordinary 0/2 extraction exit status. The complete target packet is valid; an exact retry is safe and returns DUPLICATE_NOOP. Never remove the target to resolve temporary residue. Console emits counts and fixed codes only, no source values, local paths or digests.

## Private packet contract 1.0

`build_packet` is the deterministic constructor and `verify_packet` the bounded contract verifier. UTF-8 canonical JSON uses ASCII escapes, sorted keys and compact separators. Verification requires an expected SHA-256 from a separately retained trusted receipt and reconstructs every field from the retained exact original bytes. Unknown fields or modified extracted values fail verification. Recomputing/replacing a trust anchor does not prove authenticity. `write_packet` checks internal consistency only; it cannot authenticate the operator or make a scientific association.

Fields: schemaVersion/importerVersion `1.0`, kind `BKL049_PRIVATE_SOURCE_PACKET`, restricted receiptId, explicit importedAt, fixed processing_evidence/NONE authority, PRIVATE_NOT_APPROVED publication state, source encoding/byteSize/sha256/originalBase64, extractionState, diagnostic, archive, NOT_ESTABLISHED executionEvidence and UNLINKED bindingState. The source hash covers original bytes including BOM and line endings; parser sourceSha256 covers decoded text re-encoded as UTF-8. Source character spans index decoded Unicode text, not byte offsets. Both original and lexical representation are retained distinctly.

The archive preserves one root, unique instances, supported parameter values and source spans, container child order, ordered mask commands, statements and comment spans. Numbers are `{kind: number, literal: ...}` including explicit sign/precision/exponent; enums are `{kind: enum, owner: ..., member: ...}`. These are **internal encoding**, not native semantic equivalence or an approved PXP export format. Strings/arrays/booleans/null remain literal data. No float conversion, expression evaluation, historical reconstruction, DECLARED attestation or OBSERVED execution is invented. F3 supplies the separately tested semantic/PXP adapter.

## Bounds and persistence

Source: 2 MiB; 200,000 tokens; 512 instances; value/container depth 32; 2,048 parameters/instance; 4,096 characters/string (including concatenation); 4,096 items/array; 128 characters/identifier or numeric literal; 128 mask commands/container; encoded packet 32 MiB. Excess is rejected or retained as UNSUPPORTED, never silently truncated.

Only an explicitly selected regular file is read, with size checked before and during read and metadata/identity rechecked afterward. Symlink/reparse components are rejected. Do not use hostile/shared writable directories: path checks are defensive, not OS isolation against an attacker changing parent directories or files concurrently. Run in a trusted local private directory under existing account controls; a malicious OS/storage administrator is outside this boundary.

One packet contains both original bytes and extracted result. It is staged in the selected output directory, flushed/fsynced, and published via atomic create-if-absent hard link. No rename-overwrite or non-atomic fallback. Filesystems without this primitive fail closed. Exact retry is DUPLICATE_NOOP; changed content or incomplete existing file is RECEIPT_CONFLICT. Ordinary errors attempt to clean the staging file; cleanup failure leaves private residue and never masks the original commit error. A power loss/process kill can leave a private `.bkl049-*` staging file; it is not an accepted packet and is never auto-imported. Local fsync does not guarantee disaster durability; backups and storage durability remain operational responsibilities. Deletion/cleanup is manual and must not remove accepted evidence.

## Tests and rollout

`python -m unittest tools.pixinsight.workflow_archive.test_archive -v` plus retained F0 grammar/header tests. All fixtures are synthetic and temporary. CI runs Windows and Linux; local Windows may skip creating symlinks without OS permission, with a deterministic reparse-attribute test plus Linux real-symlink coverage. No tests access scientific folders or PixInsight.

Original F0 parser is retained in Git history; its old path is now a compatibility shim to the single hardened parser. Rollback reverts this module/shim change; preserve already-created private packets and verify their version before future reads. No watcher, installation, automatic invocation, catalog/PXP delivery or gallery publication is wired by F2.


## F3 private PXP library

`provenance.build_sidecar` accepts verified packet bytes, an independently retained expected packet digest, an explicit source-bound declaration and a separate `exported_at` UTC timestamp. See `docs/architecture/assessments/BKL-049-F3-Declared-Evidence-Adapter.md` for the versioned lexical envelope, clock semantics and validation limits. The returned sidecar is private and unlinked; no publication or file writer is provided. Run `python -m unittest tools.pixinsight.workflow_archive.test_provenance -v` and `node .github/scripts/test-bkl049-provenance-bridge.mjs` for synthetic compatibility evidence.

## F4 private binding guard

`binding.build_binding` consumes independently anchored selected catalog/asset, measurement and Owner-association records before producing one exact original/preview binding. It does not read images, grant catalog authority, persist receipts or publish data. `compare_retained` only classifies immutable receipt retries. Full F4 retention/delivery and operational inputs remain open. See the F4 assessment for the private transfer profile and trust boundary.


F4 private delivery: `delivery.build_delivery`, `retain_delivery` and `load_delivery` retain/revalidate a single canonical source+binding artifact before AP14-W06 handoff. The caller supplies independently governed inputs, a trusted private local directory, an externally retained artifact digest and the fresh current snapshot anchor. No CLI, catalog writes, public upload or credential handling is added. Changed content for one binding ID conflicts; intentional revisions require a new ID. Destination privacy/backup and current authority are caller responsibilities. See the F4 assessment for limits.
