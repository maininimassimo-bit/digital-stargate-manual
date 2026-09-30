# BKL-049 F0 — Real file identity and local evidence index

Date: 2026-09-30. Status: PARTIAL / F0 OPEN. Sanitized public report; private file identity and source records remain local.

## New evidence

After the [synthetic identity experiment](BKL-049-F0-Identity-Packet-Experiment.md), the Owner identified a standalone final XISF on the computer hosting this chat. The assistant enumerated only the top level of each specifically supplied directory and calculated SHA-256 and byte size of its sole XISF, without modifying or decoding the image. File size and last-write metadata were stable before/after each read; this was not an atomic locked snapshot.

The first candidate was explicitly identified by the Owner as belonging to a different processing project. It is excluded from the collected history association. A second Owner-provided location selected the final file for the project being discussed. Its filename corroborates the output identifier in the supplied recombination text, but name agreement is not causal proof.

Public aliases FINAL-CANDIDATE-EXCLUDED and FINAL-IDENTITY refer to these two distinct local records. No private path, filename, target identity, image bytes or measured image digest is included here. The measured digest records file-byte identity at the time of reading; it does not certify pixel interpretation, historical execution or full workflow completeness.

## Private index assembled

A local research index now fingerprints five analysis records: final-file identity, main history, mask history, stars history and recombination. It also verifies the original supplied project-export attachment against its previously recorded digest. Index entries distinguish analysis records from original exports; inline chat excerpts are not falsely labelled as original-byte export files.

| Association | Evidence basis | Status |
|---|---|---|
| Main history → stars history | Owner origin confirmation plus matching serialized process occurrence fields | DECLARED association / PARTIAL |
| Mask history → main history | Owner confirmation plus explicit exported mask references | DECLARED association / PARTIAL |
| Main and stars histories → recombination | Two explicit view references in supplied PixelMath; immutable input versions unresolved | PARTIAL |
| Recombination → final-file identity | Owner final-file selection plus corroborating output name; file digest measured independently | DECLARED association / PARTIAL |
| Final file → gallery asset | No matching digest in the inspected checked-in archive fixture | UNRESOLVED |

Five local record digests and the original project-export digest were verified when assembling the index. An additional digest protects the index against accidental change relative to a retained reference; it is not a signature or independent trusted timestamp. The index is not a self-contained archive: it references retained local records and an attachment rather than embedding all original sources or image content. It is not an AP-013 catalog record, PXP sidecar or production ingestion request.

## Gallery inspection boundary

The inspected gallery and F2 archive JSON files contain three bounded example entries. The measured final-file digest does not match the archive fixture. This conclusion is limited to those checked-in files, not a live-site check or an exhaustive scan of every authoritative catalog. No example record, synthetic identifier, target name or session was repurposed to force a match. No gallery or AP-013/AP-014 mutation occurred.

A real association must use the governed asset/version route and an established relationship between original image and any displayed derivative. Publishing documentation does not automatically grant scientific catalog acceptance or authorize raw image upload.

## Updated feasibility conclusion

We now have a measured real final-file identity, not merely synthetic image IDs. The relation between that file and the supplied history is still Owner DECLARED. This advances the evidence boundary without upgrading history steps to OBSERVED or declaring complete capture.

Remaining gaps include exact input/mask versions, upstream and full-project continuity, script/version attribution, supported automatic export, source encoding/version semantics and real gallery binding. The unrelated candidate provides a concrete reason to require explicit association rather than infer by location or apparent relevance. F0 remains open and the universal native recorder remains unproven.

## Subsequent bounded header inspection

A local read checked the structural signature and header layout against the official [pinned XISFFileSignature documentation](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/include/pcl/XISF.h#L728). Only the signature and bounded XML header were decoded. Remaining bytes were read solely to compare the whole-file SHA-256 with the measured identity; it matched. Size and last-write metadata were stable. No pixel decoding, execution, write or atomic snapshot is claimed.

The header is 14,121 bytes. It contains one image element, seven properties and an inline uncompressed String property named `PixInsight:ProcessingHistory`. That property contains ProcessingHistory 1.0 XML with three enabled instances in order: PixelMath, DynamicCrop and CurvesTransformation. No FITS HISTORY keyword was present; that does not negate the separate history property.

The embedded PixelMath expression, requested output identifier and recorded start time match the supplied recombination record exactly. String parameter values were read from element text and scalar values from attributes. This corroborates the supplied association with the saved file, without independently proving historical execution or exact input versions. Serialized instance-version fields were not interpreted as module/product versions.

The two subsequent steps establish that the recombination-only export was not all history embedded in the saved final file. Full upstream branches and mask relationships remain outside this three-instance list. The raw header and parameter values remain private.

A sixth local inspection record was added to the index and all record fingerprints were rechecked. The index still is not a self-contained archive. The one-off inspection enforces a 2 MiB header bound, signature/file-size checks and rejection of DTD/entity declarations; it is not a general XISF importer or a production security boundary.

No vendor contact, native module, scientific processing, image mutation, production contract change, EAGLE access or BKL-043 intervention occurred. File hashing and header inspection are distinct from scientific processing or historical execution evidence.


## Repeatable header-only experiment

The isolated [reader](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/read_xisf_header.py) reproduces the bounded inspection without reading beyond the XML header. Four synthetic test methods cover image scoping, counts-only privacy, attached/compressed/encoded representations, malformed signatures, truncation, reserved fields, size/depth limits, duplicate histories, DTD and null-byte rejection. Unsupported representations remain unsupported; no external resource or image block is followed. This is an original research implementation using Python standard-library XML parsing, not a general hardened importer or SDK implementation.

The real-file repeat found the same 14,121-byte header and three instances, with parameter/table counts 26/1, 25/0 and 11/11 respectively, each containing a time element. It reports one image-scoped property: the earlier count of seven covered the entire header, including properties outside that image scope. No private identifiers, process parameter values, paths or file digests are emitted by the command.

The repeat does not redo whole-file hashing or compare expressions: the prior identity and exact-value checks remain separate evidence. Its structural counts corroborate that inspection, not historical execution or a complete workflow. The command intentionally omits arbitrary process class names from public output; ordered process identities above come from the prior private inspection. No parameter-to-PXP adapter is introduced. F0 remains OPEN.


## Published gallery verification and next integration boundary

On 2026-09-30, a read-only HTTP inspection of the [published gallery](https://maininimassimo-bit.github.io/digital-stargate-manual/scientific-image-gallery/) returned HTTP 200 and confirmed its `data-source` points to the bounded BKL-034 gallery fixture. The published [gallery JSON](https://maininimassimo-bit.github.io/digital-stargate-manual/data/bkl034-scientific-image-gallery-fixture.json) and [archive JSON](https://maininimassimo-bit.github.io/digital-stargate-manual/data/bkl034-f2-image-archive-fixture.json) also returned HTTP 200. Each contained three entries and parsed equal to its checked-in counterpart at research commit `9058402e`. This extends the earlier repository-only check to these specific published resources; it does not enumerate other catalogs or storage systems.

The checked-in gallery renderer displays metadata references and placeholder previews. The fetched page references that renderer; no browser-rendered visual inspection is claimed. The archive fixture contains example digest identities. Consequently, this evidence does not establish a real final-file binding in the published gallery. The search-highlighting query in the Owner's URL is not an asset identity. No fixture was replaced and no real image or digest was uploaded.

### Required association sequence (research recommendation, not a new contract)

| Boundary | Present evidence | Required next proof | Failure state |
|---|---|---|---|
| Saved final version | Local measured file identity and inline history | Governed AP-013 identity/version acceptance, with retained integrity evidence | UNRESOLVED catalog binding |
| Last saved operations | Recombination corroboration followed by crop and curves | Preserve all three occurrences and source ordering; retain upstream histories separately | PARTIAL workflow |
| MAIN and STARS inputs | Explicit references in recombination and Owner attribution | Exact versions consumed, not merely current names or final branch files | PARTIAL input lineage |
| MASK inputs | Creation snippet, named use and inversion evidence | Mask version at each use and source version used to create it | PARTIAL mask lineage |
| Script and third-party context | Owner attribution and serialized process parameters | Script/module/model version evidence with explicit unavailable fields | PARTIAL reproducibility |
| Archive to gallery | Existing projection/reference route and synthetic tests | Accepted image identity plus workflow reference; explicit original-to-preview relation when applicable | UNRESOLVED gallery binding |

The archive must retain the original evidence outside a lossy consumer projection: current PXP-to-manifest behavior does not carry all parameter, mask or branch detail. This requirement does not approve a new graph schema, storage service or catalog authority. A successful card display or reconciliation match must never upgrade PARTIAL coverage to complete workflow capture.

The next Owner-assisted evidence should target the exact saved project or retained versions behind MAIN, STARS and MASK, if available. Do not request reprocessing to manufacture historical lineage: newly generated files cannot establish which historical input bytes were consumed. Missing retained versions must remain explicit. Selecting an existing source for read-only inspection is separate from authorizing uploads or catalog writes. No additional question is required to document this boundary.
