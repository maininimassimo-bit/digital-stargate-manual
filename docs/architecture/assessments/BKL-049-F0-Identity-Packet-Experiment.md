# BKL-049 F0 — Synthetic image-version identity experiment

Date: 2026-09-30. Status: RESEARCH / PARTIAL / F0 OPEN. No new production schema, storage service or AP-013 authority.

The [synthetic pipeline](BKL-049-F0-Synthetic-Pipeline-Experiment.md) used invented asset references. The [reconciliation probes](BKL-049-F0-Archive-Linkage-Experiment.md) showed that ID matching alone does not check expected bytes. This follow-up tests a small research identity envelope with generated files and deliberate mismatches. It does not claim a real gallery association.

## Experiment and limits

Run `python experiments/bkl049-f0/identity_packet_probes.py`. The [experiment source](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/identity_packet_probes.py) creates a temporary directory, writes synthetic non-image bytes, reads and hashes them, exercises ten scenarios, and removes only its own temporary directory on exit. It accepts no user file path and uses only Python standard libraries. The [saved result](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/identity-packet-probes.result.json) contains no paths or scientific data.

The original research verifier distinguishes entity kind, ID and version; compares payload size and SHA-256; checks a declared source-export/output association and a candidate gallery reference; and compares the packet against a separately supplied anchor digest. This is a deliberately controlled test object, not a fully validated public input format. Field/type validation, concurrency, time-of-check races, durable storage and trust-anchor management are outside this experiment. Tests characterize the proposed checks rather than certifying existing production behavior.

The filename is not an identity field. The same textual ID can exist in separate image/export namespaces. A declared association remains DECLARED even when all bytes match. Matching bytes establish neither process execution nor scientific equivalence or pixel-level identity across different file serializations.

## Results

| Probe | Outcome |
|---|---|
| I01 | Distinct typed image/export identities with the same textual ID resolve; result remains DECLARED/PARTIAL with no action or acceptance authority |
| I02 | Changing bytes under the same filename and ID fails the expected content digest |
| I03 | Missing source payload prevents packet verification |
| I04 | Duplicate typed ID/version is rejected instead of selecting a last record |
| I05 | Candidate gallery reference to a different image version is rejected |
| I06 | Output reference to an absent asset is rejected |
| I07 | An image cannot stand in for the source-export entity |
| I08 | Altering packet metadata fails the separately retained anchor |
| I09 | Renaming an unchanged file does not break explicitly supplied identity |
| I10 | Replacing data, metadata and the accepted anchor together still matches: hashes alone do not authenticate origin |

All ten scenarios reproduced the stated behavior. I10 is an intentionally demonstrated limit, not an accepted security property. A future trusted record must govern where an anchor comes from and who may replace it. This experiment neither signs evidence nor provides tamper-proof archival storage. No cryptographic authorship, execution proof or verified historical timestamp is claimed.

## Requirements exposed for the actual archive

1. Keep an explicit distinction between exported text, a process occurrence, an image asset and an image version. Prefix resemblance, common names and matching timestamps do not merge identities.
2. Obtain version identity and integrity through the existing AP-013 boundary. The experiment does not authorize an independent competing asset catalog.
3. Retain the actual source artifact and an integrity record under appropriate access controls. Public rendering must not require publishing private source text or file paths.
4. Record how each source-to-image association was established. A user's confirmation remains a declaration; a checksum does not turn it into automatic observation.
5. Bind the public gallery entry to the intended final version. A preview/thumbnail may be a derivative with different bytes and must have an explicit relationship rather than be compared as if it were the original.
6. Preserve PARTIAL/UNAVAILABLE independently of successful identity matching. Unknown earlier processing, scripts, mask origins and branches do not become complete when hashes match.

No gallery entry, scientific asset or production contract was edited. The actual Owner images were not accessed. Existing view-name links in the supplied exports are not upgraded to immutable version bindings by this experiment.

## Consolidated F0 position

Supported project/history artifacts now have supplied examples, a bounded nonexecuting reader, a synthetic DECLARED pipeline and tested identity-check requirements. This supports continued investigation of an artifact-based archive without contacting PixInsight. It does not establish the original universal native observer, complete workflow coverage, or a production-ready archive.

Remaining evidence cannot be replaced by more synthetic successes: supported automatic export on 1706; original/current module and model identities; full project input/output/mask continuity; exact real asset/version/gallery mapping; and complete scope evidence including unsupported cases. SDK-dependent licensing/build/signing questions remain open if a native implementation is retained. Contact with the vendor remains deferred, not required for all documentary research.

The next real-evidence step should collect a minimal, read-only identity record for a specifically selected final image/version and its corresponding exported history. That record needs the actual file digest and size, export digest, and the Owner's association declaration; it must not claim all processing was observed. Before any assistant access to scientific files, specify the exact scope and obtain the existing required authorization. No file discovery, upload or raw-data publication is implied. Metadata alone will not prove complete history.

Validation: all ten synthetic scenarios reproduced and saved output matched a fresh run; generated temporary paths were checked within the experiment scratch boundary before cleanup. MkDocs strict build passed (25.38 seconds), targeted privacy/whitespace checks passed, and roadmap consistency retained BKL-043 current/next. GitHub CI remains a separate exact-head gate.

Subsequent [real identity evidence index](BKL-049-F0-Real-Identity-Evidence-Index.md) records Owner-selected file hashing and a private local evidence index. This supersedes the absence of a measured final-file digest, while leaving causal association, input versions and gallery binding unresolved.
