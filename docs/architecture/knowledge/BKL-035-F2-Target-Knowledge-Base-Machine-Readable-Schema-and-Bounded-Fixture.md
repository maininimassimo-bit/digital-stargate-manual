# BKL-035 F2 — Target Knowledge Base Machine-Readable Schema & Bounded Fixture

| Field | Value |
|---|---|
| Identifier | BKL-035-F2 |
| Status | In Progress |
| Version | 0.1 |
| Date | 2026-09-07 |
| Parent | BKL-035 — Target Knowledge Base |
| Baseline | `79be46cde68c446ceb412491e600c439735622d6` |
| Predecessor | BKL-035 F1 — CLOSED / ACCEPTED |
| Authority | Projection contract |
| Runtime impact | None |
| Safety impact | None |

## 1. Purpose

Materialize the accepted F1 target-identity and relation semantics as a versioned machine-readable contract, a bounded source-backed fixture and deterministic fail-closed validation. F2 does not create a second scientific authority and does not authorize broad ingestion.

## 2. Artifacts

- `schemas/target-knowledge-base.schema.json` — JSON Schema 2020-12 structural contract;
- `docs/data/target-knowledge-base.json` — bounded governed fixture;
- `.github/scripts/verify-target-knowledge-base.mjs` — semantic/source reconciliation validator;
- `.github/scripts/test-target-knowledge-base.mjs` — negative fail-closed regression suite;
- `.github/workflows/developer-foundation.yml` — CI gate integration.

## 3. Target key encoding

F2 resolves the F1 open decision for the bounded projection key. `target_key` uses `dsg-target:<slug>` where the slug is a lowercase deterministic projection token derived from the accepted canonical target label. It is repository-local and never replaces a governed astronomical/catalog identifier.

The current fixture uses `dsg-target:ldn-1320` and `dsg-target:m-27`. The key is only a projection identity. F3 remains responsible for deterministic reconciliation and collision/conflict validation across a wider accepted source set.

## 4. Bounded fixture

The F2 fixture contains exactly two validated identities and four `TARGET_HAS_SESSION` relations, below the accepted F1 maxima of five identities and ten relations.

The source evidence is the governed Scientific Session Catalog on the accepted baseline. LDN 1320 is represented by sessions `2026-07-14_2026-07-15` and `2026-07-15_2026-07-16`; M 27 is represented by sessions `2026-08-14_2026-08-15` and `2026-08-15_2026-08-16`.

The repository also contains governed scientific metadata with exact `target_id` values (`TGT-LDN-1320`, `TGT-MESSIER-M27`), but F2 deliberately does not promote that analytics metadata file into the F1 ordered source inventory. F3 may reconcile those identifiers only after explicitly governing the additional source relation. This preserves the F1 authority boundary.

No incomplete/conflicted/unknown identity is manufactured merely for test coverage. Negative tests inject invalid copies in memory; they do not create false repository facts.

## 5. Citation and Provenance

Every validated identity has at least one Citation. Fixture citations resolve exactly to `docs/data/scientific-session-catalog.json` using `sessions[].sessionId`. Derived target keys and relation links carry versioned Provenance records with bounded F2 method identifiers.

Confidence is absent because the source facts do not require a Confidence value for identity acceptance. F2 does not invent one.

## 6. Relation scope

Although the schema preserves the F1 relation vocabulary, the bounded fixture materializes only `TARGET_HAS_SESSION`. SQM, setup, asset and processing-provenance relations remain reserved until their source-specific reconciliation is explicitly validated. This avoids premature authority promotion.

## 7. Fail-closed validation

The semantic validator rejects at minimum:

1. authority escalation away from `projection`;
2. fixture expansion beyond 5 identities / 10 relations;
3. validated identity without Citation;
4. unresolved source session;
5. canonical-name mutation relative to primary governed session evidence;
6. relation target/session mismatch;
7. non-canonical Session Catalog locator;
8. ungoverned derivation method;
9. unresolved Citation or Provenance;
10. conflicting governed coordinate evidence within one projected identity;
11. premature materialization of non-session relation types in the F2 fixture.

## 8. Migration and rollback

F2 is additive. Existing scientific catalogs, analytics datasets and runtime projections remain unchanged. Rollback is a repository revert of the F2 files and CI entries; there is no data migration, EAGLE deployment or runtime state to restore.

## 9. Security, safety and operations

F2 is repository-only and read-only. It introduces no observatory command path, scheduler, remediation, hardware control, weather decision, Safety Authority coupling, external provider, graph/vector database, RAG or AI inference runtime. Runtime observability and EAGLE OAT are Not Applicable.

## 10. Acceptance criteria

F2 is acceptable when:

- schema and fixture remain bounded and versioned;
- all fixture facts resolve to accepted governed sources;
- target keys remain projection-only;
- Citation/Provenance semantics are explicit;
- no Confidence is invented;
- fail-closed tests cover authority, bounds, source drift, identity mismatch and premature relation promotion;
- Developer Foundation, documentation and Word gates are green on the exact reviewed head;
- independent ARB review approves the package before merge.

## 11. Next increment

After F2 acceptance, **F3 — Deterministic Source Reconciliation and conflict/alias validation** may add governed reconciliation for exact target identifiers, aliases and additional relation source classes. F3 must not broaden ingestion implicitly and must preserve the F1/F2 safety and authority boundaries.
