# BKL-049 — Private registry validation and acceptance gates

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-REGISTRY-VALIDATION-001 |
| Version / date | 1.1 / 2026-10-01 |
| Status | Bounded candidate-validation implementation; production acceptance CLOSED TO ACTIVATION |
| Scope | Owner-approved manual route, selected external catalog context |
| Authority | Existing AP-013/AP-014; validator authority NONE |

## Current result

The [approved registration route](BKL-049-External-Origin-Registration-Plan.md) now has immutable draft retention and configuration structural checks. The catalog-context increment extends candidate checking to selected project, campaign, target, observation, session and session catalog-item metadata. It is read-only and returns a private source-bound report. It neither creates these scientific entities nor accepts them. BKL-049 remains OPEN; BKL-043 remains current and untouched.

The contract sources are [AP14-W01](../scientific-catalog/AP14-W01-Observation-Catalog-Conceptual-Model.md), [AP14-W02](../scientific-catalog/AP14-W02-Logical-Data-Model-and-Identifier-Standard.md) and [DSDM-002](../scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model.md). Existing observatory analytics generators remain unchanged. No external candidate is inserted into their inputs, and no generated catalog is hand-edited.

## Implemented validation matrix

| Source | Checks | Explicit limit |
|---|---|---|
| AP14-W02 2.3 | Schema/record version fields, creation/update UTC syntax/order, source system/version/digest presence | Source-digest meaning and authenticity are not established by syntax; private profile supports SHA-256 |
| AP14-W02 3, 4.1–4.4 | Project/campaign/target/observation ID patterns, mandatory fields, lengths, priority 1..5, known enums, optional date/numeric checks | No new identifiers, priority or astronomical classification generated |
| AP14-W02 4.5 | Session context, local date, optional UTC interval, quality/status vocabulary, configuration and site references | No inferred local-observing-date convention or timezone conversion |
| AP14-W02 4.12, 5 | Session-only catalog items, identity/version uniqueness, selected foreign keys, conflict-indexed rejection and self-supersession rejection | No indexing, global registry collision check, ledger transition or override policy |
| DSDM-002 2.2, 5.1/5.2/5.3/5.5 | Reuse the configuration checker; compare supplied session UTC instants with supplied configuration interval | Syntactic consistency never establishes historical use or scientific validity |

Input is an internal candidate selection with 1..8 records per collection, bounded by the existing 256 KiB / 32-level / 32,768-value JSON parser. Duplicate keys, nonfinite numbers and wrong expected byte digests reject. Unsupported fields and complex unimplemented subcontracts produce fixed findings. Optional unknowns may remain null only for fields declared optional. Diagnostic fields are fixed names and bounded numeric positions; private input values and unknown keys are not reflected. Reports retain the private selected digest and must not be published as raw evidence.

Duplicate selected identities do not enter lookup maps, so later references cannot silently resolve to the last duplicate. All selected rows are checked, including unselected-by-reference rows. Missing references never fall back to names. Selected canonical target names are case-insensitively unique. Broader alias resolution, global namespaces, cross-submission collisions and historical revision eligibility remain outside this offline selection check. The caller must supply governed identities; a syntactically plausible ID is not an allocated identity.

## Vocabulary gaps discovered in the current contracts

AP14-W02 requires project type, campaign status, observation status and completion state but does not enumerate their allowed values. A repository search found references to these named vocabularies without a defining enumeration. AP14-W01 enumerates project states, catalog states and the session/quality/observation-mode/reconciliation vocabularies, which this checker uses in their own catalog context. DSDM-002's different session/project lifecycle model is not silently substituted. A supplied catalog transfer state also remains unresolved until its mapping is governed.

The validator reports these unresolved fields separately as `VOCABULARY_UNRESOLVED`; missing values still produce REQUIRED. This does not approve arbitrary values. Defining the missing vocabularies and their scientific interpretation requires a concrete governed contract proposal and the applicable Owner decision. This increment neither changes those contracts nor uses neutral-looking defaults to make the real candidate pass.

## Mandatory acceptance conditions and unresolved implementation

The following conditions are cumulative, not interchangeable. This matrix operationalizes the already approved route's boundaries; it does not define new scientific quality thresholds.

| Gate | Required evidence | Current implementation disposition |
|---|---|---|
| Candidate integrity | Exact selected bytes/revision with independently retained current anchor | Draft journal and bounded parsers available; hashes are not operator authentication |
| Required scientific metadata | Complete applicable contract fields, governed vocabularies, references and per-field source evidence | Configuration, catalog-context and selected asset/storage/integrity subset checks available; complete provenance validation and unresolved vocabularies remain open |
| External context | Governed observatory/timezone, equipment/configuration, target and project/campaign/observation/session identities | Must be resolved by the existing responsible authority; no fictitious observatory session |
| Historical configuration | Truthful DSDM-002 validFromUtc and evidence tying the configuration to the acquisition | Mandatory, still not supplied by checking syntax or models; receipt/import times cannot substitute |
| Asset registration decision | Explicit accountable AP-013 registration event tied to exact candidate revision and byte identities | Decision operation not enabled; implementation approval is not this event |
| Catalog acceptance decision | Separate accountable AP-014 decision after unresolved scientific findings are settled | No default ACCEPTED; software review and Owner factual declarations do not replace this decision |
| Retention and currentness | Verified private location/access, independent current anchor, operational restore, collision/concurrency/revision/withdrawal/quarantine controls | Draft recovery is not production backup acceptance; accepted-record retention/export remains unimplemented |
| F4 handoff | Fresh independently anchored eligible snapshot and separately measured/declared exact original/preview/workflow association | Unchanged [F4 guard](BKL-049-F4-Exact-Binding-Guard.md) remains mandatory; no snapshot exported here |
| Publication | Exact permitted public aliases/fields/preview, rights/privacy, publisher policy and real gallery OAT | Separate later approval; no upload or access operation in this increment |

Every report retains DRAFT_NOT_ACCEPTED, PRIVATE_NOT_APPROVED, scientificAuthority NONE, catalogWritePerformed false and acceptanceEligible false. `NO_STRUCTURAL_FINDINGS` covers only the stated structural subset; vocabulary gaps and other unverified gates still block activation. Embedded ACCEPTED claims cannot change the report envelope. Observed, declared, suggested, partial and unavailable provenance semantics remain unchanged.

## Verification, delivery and rollback

Eighteen synthetic catalog-context tests exercise every mandatory field, reference chains, duplicates, malformed values, wrong types, source integrity/resource boundaries, private diagnostics, invalid dates/intervals, explicit vocabulary gaps and forged acceptance. CI runs them on Windows and Linux with the existing archive/configuration/draft suites. A private real-candidate dry run may select already retained facts and report missing records, but cannot allocate or accept entities or read image pixels.

Separate AI-assisted ARB then Release Quality, exact-head CI, expected-head merge under DSG-AEM-001/W-DSG-AEM-RULESET-001 and merge-SHA/Pages verification are recorded in the delivery PR. These reviews are not human scientific acceptance. The code is additive: rollback reverts the checker, tests, CI step and supporting documentation while preserving every private source/draft/receipt. No database migration, new dependency, cloud resource, device access or catalog write is introduced.

## Selected asset/storage/integrity and composed validation increment

`asset_metadata.check_asset_metadata` adds a read-only subset of DSDM-002 sections 2.2 and 7.1–7.5: asset metadata, storage volumes/locators, integrity records and asset relations. The caller selects the original and preview by explicit IDs, never by filename. Five collections are bounded to 1..8 rows each. Required fields, controlled enums where actually defined, numeric/hash constraints, duplicate identities, selected references, storage collisions, integrity predecessor coherence/cycles and the pair's declared derivative direction are checked. Existing AP-013/AP-014 and BKL-034 public schemas are not changed.

| Check | Failure behavior / boundary |
|---|---|
| Asset identity and size | Wrong type, negative/out-of-range size, duplicate ID or unresolved selection is a finding; matching hashes do not merge scientific identities |
| Storage locator | Relative-path syntax and exact selected volume/asset references checked without reading a path; duplicate active locations detected with separator normalization only; actual availability, filesystem aliases and ACLs remain unverified |
| Integrity receipt | Wrong locator ownership, inconsistent positive hash, cyclic/cross-asset predecessor or reversed receipt time is a finding; historical negative/partial results remain explicit eligibility findings |
| Original/preview relation | Candidate relation must explicitly point from selected preview to selected original using DERIVED_FROM/PUBLICATION_VARIANT_OF; this private comparison convention supplies no scientific lineage evidence |
| Independent full-file measurement input | Separate byte anchor required; original/preview IDs, full-file scope, size and SHA-256 compared exactly; header-only/missing/duplicate measurements cannot supply the comparison |
| Non-eligible selected state | Quarantine, withdrawal, unreadable/mismatched integrity or immutability violation remain eligibility findings, even when measured bytes match |
| Composed context | The registration checker retains both reports and checks explicit selected session/catalog/observation/target consistency; no workflow association or authoritative snapshot is constructed |

The measurement record's FULL_FILE_BYTES field is a claim from the selected evidence source, not proof that this validator measured a file. Its caller must independently establish authenticity, actual scope and currentness. This increment performs no hashing of images, pixel read, antivirus scan or new original-file access. SHA-256 is only the selected comparison profile; no hashing-policy authority is introduced. Hashes of FITS headers alone remain insufficient. Nested report digests derive from the anchored parent candidate and do not masquerade as independent anchors.

DSDM-002 names but does not enumerate shared lifecycle status, locator availability and relation confidence in these field tables. Those remain `VOCABULARY_UNRESOLVED`. Optional processing-run references are explicitly unsupported rather than accepted without resolution. UTC syntax is checked only on selected values; original retained evidence is never rewritten or silently converted. Global namespace/collision policy, per-field provenance, relationship authority, current lifecycle decisions and operational retention remain separate gates. All reports continue to prohibit scientific acceptance and catalog writes.

Twenty-five added synthetic tests cover mandatory fields, duplicates including unrelated selected rows, reference failures, relative-path rejection, storage collisions, hash mismatch, full-file versus header scope, predecessor cycles, negative eligibility and composed-context ambiguity. CI runs them on Windows/Linux alongside earlier suites. An authorized private dry run can carry retained original/preview byte facts into an incomplete candidate without allocating identities or fabricating receipts/relations; absent governed records and independent measurements remain findings. Private results stay outside Git. Rollback removes only the additive validators, tests, CI step and documentation; originals, retained drafts, measurements and other evidence are preserved.
