# BKL-049 F0 — Real file identity and local evidence index

Date: 2026-09-30. Status: PARTIAL / F0 OPEN. Sanitized public report; private file identity and source records remain local.

## Current consolidated position

- The supplied MAIN export contains 381 assignments; 347 have corroborated representations in the retained project, including nested PixelMath and curve tables. This is not an execution/completeness score.
- Five RC Astro occurrences account for 58 export assignments: 24 same-ID values match and 34 are export-only. Their retained-project counterparts contain 44 assignments: the same 24 plus 20 project-only occurrences.
- Official documentation identifies schema changes for 11 of those 20 project-only occurrences; nine still lack a documented relationship in the inspected sources. A documented removal/replacement is not a verified value-preserving migration.
- Retained-project and final-XISF representations corroborate the three final processes. Initial history, multiple mask candidates and unknown state/version semantics prevent whole-workflow claims.
- Thirteen local analysis records are fingerprinted in a private successor index. No original image/project payload is archived by this PR. Real gallery binding and native automatic capture remain unproven.

The sections below preserve the investigation sequence; later consolidated totals supersede interim counts. F0 remains OPEN.

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


## Curves table and enumeration follow-up

The pinned official [CurvesTransformation parameter definitions](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/src/modules/processes/IntensityTransformations/CurvesTransformationParameters.h) identify eleven curve tables with x/y columns and the interpolation enumeration. The companion [implementation](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/src/modules/processes/IntensityTransformations/CurvesTransformationParameters.cpp) defines enumeration identifiers and numeric values. Both official file fingerprints were added to the source registry; no vendor implementation was copied, built or distributed.

Across the six direct CurvesTransformation instances, all 66 exported curve tables match the corresponding XML tables in row order and x/y numeric values, using Decimal equality without tolerance. Row counts, two-column shape and column identifiers were checked. All 66 interpolation assignments also agree under the explicit mapping defined by the pinned source; no default filling or guessed enum translation occurred. This source revision supports the representation comparison, not a claim about the originally installed module build or runtime behavior.

This resolves 132 of the earlier 174 unverified assignments. The cumulative direct-entry comparison is now **261 corroborated assignments out of 303, with 42 unresolved**. Tables count as assignments here, not as individual scalar cells. The 78 assignments in the three nested PixelMath instances remain outside this particular comparison. Original historical counts are retained above to show the scope progression, not competing final totals.

The private comparison report retains aggregate results. No parameter values or curve points are published. Remaining nonmatching representations, especially third-party fields, must not be equated speculatively. Better parameter coverage does not establish execution, historical image/mask versions, supported automatic project extraction or complete capture. F0 remains OPEN.


## Nested PixelMath and consolidated assignment coverage

The three direct children of the nested ProcessContainer were aligned in retained source order with the three exported PixelMath instances. All parameter identifier sets agree, with no duplicate direct XML identifiers. Each instance has 26 matching assignments: **78/78** in total. Strings, including expressions, were compared exactly without execution; booleans explicitly and numbers using Decimal equality without tolerance. The two SameAsTarget enum fields per instance were checked against the explicit definitions in the pinned official [header](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/src/modules/processes/PixelMath/PixelMathParameters.h) and [implementation](https://gitlab.com/pixinsight/PCL/-/blob/5a3902196a7d7a701385a7113cbdce2976ae1a85/src/modules/processes/PixelMath/PixelMathParameters.cpp). Both file fingerprints are now in the source registry. No default substitution, expression evaluation or vendor-code redistribution occurred.

Together with the direct-entry comparisons, **339 of the 381 exported MAIN assignments are corroborated; 42 remain unresolved**. This denominator covers supplied assignments, not every field in the project, every processing event or the entire workflow. It does not measure completeness as a percentage of the Owner's scientific workflow.

| Unresolved assignment group | Count | Required disposition |
|---|---|---|
| RC Astro parameters without same-ID direct XML counterparts | 34 | Preserve both original representations; seek version-specific documented correspondence without guessing migration or filling defaults |
| Other process enums | 7 | Explicit source-backed mapping for the relevant parameter/version, not numeric coincidence |
| Other process table | 1 | Verified column/row semantics and representation comparison |

The remaining non-RC fields belong to BackgroundNeutralization, SpectrophotometricColorCalibration, SCNR, LocalHistogramEqualization and MultiscaleMedianTransform. An unresolved field is not automatically a mismatch or loss. The private comparison record stays separate from the six-record index. Masks, state selection, omitted initial operations, exact image versions, automatic extraction and gallery binding remain independent open questions. F0 stays OPEN.


## Remaining non-RC representation checks

All seven remaining non-RC enum assignments use identical symbolic labels in the export and XML. Comparison verified the export enum owner equals the aligned process class, the parameter identifier agrees, and the member label equals the XML value. This resolves textual representation correspondence without inventing numeric enum semantics, relying on a default, or asserting historical module equivalence.

The MultiscaleMedianTransform table has five rows and seven columns. Its supplied export contains explicit column labels; these were matched to XML cell identifiers with duplicate/shape checks. All 35 cells agree, using explicit boolean text or Decimal numeric equality without tolerance. The labels are source-artifact evidence, not an independently certified general schema. This table counts as one assignment, not 35 assignments, in the cumulative totals.

**Current consolidated result: 347 of 381 supplied MAIN assignments corroborated; 34 RC Astro assignments remain unresolved.** This supersedes the interim 339/381 count above. All non-RC assignments in this particular supplied MAIN export have representation correspondence under the documented comparison rules. This does not establish all non-RC processes are supported, does not cover arbitrary exports, and does not certify entire-workflow completeness.

The outstanding 34 are distributed across two BlurXTerminator instances (five each), one StarXTerminator (six) and two NoiseXTerminator instances (nine each). They lack same-ID direct XML counterparts in this comparison. Do not relabel them as dropped, migrate them to similarly named fields or populate current defaults. The next useful evidence is a version-specific official representation/migration rule or supported export evidence retaining both schemas, rather than another generic equality test. No vendor contact, proprietary module inspection or execution is authorized by this result. A private aggregate comparison report was retained separately from the original evidence index.


Official RC Astro follow-up (retrieved 2026-09-30): the [unified-suite announcement](https://www.rc-astro.com/unified-pixinsight-rc-astro-suite/) explicitly documents that `ai_file` was replaced by numeric `ml_version`, and zero selects the latest available model. This resolves the current suite's selection-policy meaning, not the actual model used in a historical execution or a complete mapping of the 34 fields. Persisting only zero cannot pin reproducibility across changing available models. Preserve the original source values and distinguish model-selection policy from resolved model identity; no historical model number is inferred from today's installation. The same source documents removed parameters and a changed version-number scheme, reinforcing the need for version-specific comparison rather than silent migration.


## RC Astro two-sided schema difference and archival consequence

Comparison of parameter identifiers in the five aligned RC Astro instances yields differences in both directions:

| Process instances | Export-only assignments | Project-only assignments | Examples of project-only identifiers |
|---|---:|---:|---|
| BlurXTerminator, two | 10 | 12 | `ai_file`, `correct_first`, `lum_only`, `nonstellar_then_stellar`, `adjust_halos`, `nonstellar_psf_diameter` |
| StarXTerminator, one | 6 | 2 | `ai_file`, `stars` |
| NoiseXTerminator, two | 18 | 6 | `ai_file`, `denoise_lf`, `denoise_lf_color` |
| Total | 34 | 20 | Counts are occurrences across instances, not unique names |

Project-only fields are additional to the 381-assignment export denominator. Thus 347/381 is not a preservation/completeness score: it says nothing about fields omitted from that denominator. For example, similarly named halo, diameter or stars controls are not treated as equivalent without verified version-specific rules. Values, model paths and other private content remain unpublished.

The [official unified-suite announcement](https://www.rc-astro.com/unified-pixinsight-rc-astro-suite/), rechecked on 2026-09-30, documents changed/removed parameters and replacement of `ai_file` with `ml_version`. That supports schema-change risk, but neither certifies the migration of this project nor provides a complete field/value equivalence for the 34 assignments. No RC module binary was inspected, installed or executed and no vendor was contacted.

**Archival consequence:** preserve the original retained project and original export as distinct versioned evidence; do not replace one with the other or overwrite an original by re-saving solely to remove compatibility warnings. A future derived normalized representation must cite its source and transformation rules, retain unsupported fields privately and declare gaps. This is an F0 requirement/recommendation, not an implemented archival service or a change in scientific authority. Compatibility sufficient to open a project is not proof of historical provenance preservation or reproducibility.

A successor private evidence index now fingerprints all 13 local analysis records, including seven project/comparison records previously outside the original six-record index. All 13 fingerprints were verified. The earlier index remains byte-for-byte unchanged and is referenced by its digest. Both are research indexes, not self-contained original-source archives, signatures or trusted timestamps. No source files or pixel data were copied into the repository.


## RC compatibility matrix: documented change versus verified migration

The following classifies parameter-name evidence against the official unified-suite announcement, not against an assumed installed version:

| Group | Project-only occurrences | Official evidence | Archival disposition |
|---|---:|---|---|
| `ai_file`, across all five RC instances | 5 | Replaced by numeric `ml_version`; zero means latest available | Preserve original reference privately and preserve exported selector separately; exact model identity and value conversion unproven |
| `correct_first`, `lum_only`, `nonstellar_then_stellar`, across two BlurX instances | 6 | Listed among skipped/removed parameters | Retain original fields; do not erase their historical meaning or assert a successful replay |
| Remaining project-only identifiers | 9 | No explicit field-to-field equivalence established in inspected official material | Keep unresolved; similar naming does not authorize migration |
| Export-only assignments | 34 | New-suite behavior and selection policy are only partially documented | Retain as export-time representation; do not backdate them as historical execution values |
| Shared RC assignments | 24 | Values already compared equal in the selected instances | Content corroboration only; equal values do not prove equal module/model semantics |

The 11 documented-change occurrences remain within the 20 project-only occurrences; they do not reduce the 34 unresolved export assignments or increase the 347 corroborated total. This separates a schema-change explanation from a proven reversible conversion.

Exact current module versions are not available from the Owner's earlier statement that all tools work. Serialized instance-version fields and model selectors must not be substituted for module build identity. The Owner subsequently reported **BlurXTerminator 2.6.9** on 2026-09-30. Preserve that literal as DECLARED current product-version evidence; no binary/API verification or reinterpretation as a four-part unified module build is made. The Owner also reported **NoiseXTerminator 2.6.9** (DECLARED current version). The Owner finally reported **StarXTerminator 2.6.9** (DECLARED current version), completing the three-product declaration without any assistant execution, setting change or project resave. That information identifies today's representation only; it cannot establish the version used in the historical processing. The three current version declarations do not identify the binaries/models used in the historical run, nor independently establish suite build/ABI identity. No runtime or production work is unlocked by a version response.


## Owner-confirmed update date and retained model references

The Owner explicitly clarified that all three RC Astro tools were updated **on 2026-09-30**. Their reported 2.6.9 versions belong to the current post-update environment; they must not be backdated to the May processing. This chronology is DECLARED, not an independently observed installation event. It strengthens the need to distinguish historical retained content from current export representation, without proving a specific migration path.

A bounded presence-only inspection found one nonempty `ai_file` parameter in each of six retained RC Astro instance elements: two BlurXTerminator, two NoiseXTerminator and two StarXTerminator. This scope includes the additional STARS-branch occurrence; the five-instance MAIN comparison and its 34/20 counts are unchanged. Six XML occurrences do not establish six distinct executions.

No referenced path was followed, no model file was opened or fingerprinted, and no path/basename/value is published. A nonempty reference is useful retained evidence but not resolved model identity: the file may be absent, replaced or unrelated to actual historical execution. A future model-identity check would require an Owner-selected retained artifact and supported version/hash evidence, without automatic traversal of embedded paths or inspection of license credentials. Current latest-model selection cannot substitute for that evidence.

The new private baseline record is separate from the 13-record successor index. No earlier indexed record was rewritten. The useful autonomous result at this boundary is the preserved distinction between retained reference, selected model policy, current module version and historical execution evidence. Repeating equality counts cannot close the remaining native-interface, SDK-dependent licensing, historical-version and whole-workflow gates. F0 remains OPEN.
