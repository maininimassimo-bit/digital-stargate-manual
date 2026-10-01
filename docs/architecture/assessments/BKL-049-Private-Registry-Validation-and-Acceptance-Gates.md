# BKL-049 — Private registry validation and acceptance gates

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-REGISTRY-VALIDATION-001 |
| Version / date | 1.0 / 2026-10-01 |
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
| Required scientific metadata | Complete applicable contract fields, governed vocabularies, references and per-field source evidence | Configuration and catalog-context subset checks available; full asset/provenance validation and unresolved vocabularies remain open |
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
