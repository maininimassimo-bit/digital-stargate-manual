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


## Owner-selected retained project located

The Owner confirmed the same project directory as the source of the supplied histories. Bounded directory enumeration located a project bundle containing an 857,498-byte XML index and a data directory with 528 extensionless files and one seal file. The data files and seal contents were not read or interpreted. Calibration/raw-data subdirectories were not traversed.

A bounded generic XML inspection of the index rejected DTD/entity declarations and null-byte encodings, parsed without execution, and retained an index digest only in a private local report. File size and modification metadata stayed stable across the read; this is not an atomic snapshot or a digest of the whole project. No paths, names, attribute values, parameter content or digest are published.

Structural counts include five `ImageWindow` and five `MainView` elements, five `initialProcessing` elements, three `processing` elements, 33 `instance` elements, 31 `time` elements, 562 `parameter` elements, 86 `table` elements and 14 `mask` elements. These are XML element counts, **not executed-step counts**, unique process occurrences or proven mask applications. Initial/current history, saved instances, image states and unsupported semantics must not be conflated.

This establishes that a retained project source exists for further supported export verification. It does not establish a documented XOSM semantic importer, complete project integrity, image-version identity or supported automatic capture. The inspected official SDK references recognize the extension as XML but did not supply a project-format semantic contract in the examined files. No inferred internal parser, decompressor or block traversal is introduced. The separate private structural report is not yet part of the six-record index; no claim that the earlier index includes it is made.


## Cross-artifact structural comparison

A subsequent nonexecuting comparison verified that the project-index digest still matches the privately retained structural-inspection digest. It read only the selected XML index, supplied export and bounded final-XISF header. This is content corroboration, not a supported XOSM semantic importer: no binary block, seal, image state or `historyIndex` semantics were interpreted.

| Comparison | Result | Interpretation limit |
|---|---|---|
| Project MAIN `processing` versus supplied container | All 19 direct instance class labels agree in source order | Does not compare every MAIN parameter, nested container or mask state; no execution proof |
| Separate MAIN `initialProcessing` | Contains ImageIntegration | The supplied 19-entry export omits this separate initial structure; do not silently prepend it as a proven executed event |
| Candidate STARS structure | Initial StarXTerminator followed by PixelMath, ColorSaturation and SCNR | Agrees with supplied class sequence; not exact input/output version proof |
| RangeSelection structures | Two distinct views each have an initial RangeSelection | One supplied mask snippet cannot establish both masks' identities or use relationships |
| Candidate FINAL versus final-XISF embedded history | Three ordered instances agree in class/version/enabled attributes and parameter/table/time representations | Structural normalization sorts attributes and trims surrounding element-text whitespace; not byte-for-byte XML equality or proof of pixel identity |

The final comparison includes recursive parameter/table row/cell/time attributes and text; it deliberately excludes image-state and other project-only children. All three comparisons matched. The labels MAIN/STARS/FINAL above are corroborated research roles, not newly accepted catalog IDs. No private view identifier or parameter value is published.

These observations show why a single exported container cannot certify the entire project: the project retains additional initial structures and multiple mask candidates. A future supported exporter must distinguish initial versus subsequent processing, current versus retained/undone state, shared occurrences and exact image versions. It must not concatenate everything found in XML or count duplicate branch occurrences as independent executions. The separate comparison report remains private and outside the earlier six-record index. F0 and whole-workflow coverage remain PARTIAL/OPEN.


## Direct parameter and mask-candidate comparison

A further private comparison rechecked the project-index fingerprint, aligned the 19 direct MAIN entries by the already-matching class/order, and compared exported assignments with direct XML `parameter` children sharing the same identifier. Duplicate direct parameter identifiers were rejected. Strings were compared exactly, booleans only against explicit `true`/`false`, and numeric literals by Decimal equality without tolerance. No enum translation, table mapping, nested-container flattening or project-state semantics were inferred.

Of 303 assignments on those direct entries, 129 comparable values matched, 73 had representations outside this comparator, and 101 had no same-ID direct XML parameter. There were no differing values among the 129 supported comparisons. This does **not** mean all 303 match or that the remaining 174 are absent from the project: table-backed fields, enums and version-dependent representations require separate supported mappings. The three nested PixelMath instances (78 additional assignments in the full supplied export) are outside this comparison; the earlier 381-assignment export count remains consistent.

RC Astro instances illustrate the limit: some supplied parameter identifiers have no same-ID direct XML parameter. This is an observed representation difference, not proof of missing execution or a verified cause. Earlier official RC Astro evidence documents schema evolution, but this comparison does not establish that migration caused these particular differences. Never populate missing historical parameters from current defaults or rename them speculatively.

Both RangeSelection candidates have the same seven parameter identifiers as the supplied mask analysis. Candidate MASK-A matches all seven values; MASK-B matches four and differs in three. The labels refer only to these private comparison records. MASK-A is therefore more strongly corroborated as the supplied configuration, but parameter equality is not pixel/version identity, causal source proof or evidence of which immutable mask version was applied at every use.

The aggregate private report is retained separately from the original six-record index. No source strings, view names, file paths, parameter values or image bytes are published. Whole-workflow coverage, native automatic capture and F0 acceptance remain unproven.
