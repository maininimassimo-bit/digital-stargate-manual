# BKL-031 F1 — Source and Semantic Validation Plan

| Field | Value |
|---|---|
| Identifier | BKL-031-F1-VAL-001 |
| Status | Proposed — validation plan only |
| Version | 0.1 |
| Date | 2026-09-13 |
| Contract under validation | `docs/architecture/scientific-assets/BKL-031-F1-Observation-Planner-Source-Discovery-and-Semantic-Boundary.md` |
| Runtime impact | None |

## 1. Objective

Define the evidence and negative tests required before BKL-031 may move beyond F1. This plan validates source classification and semantic separation; it does not validate an algorithm because no ranking implementation is authorized.

## 2. Review evidence matrix

| Gate | Evidence | Pass condition |
|---|---|---|
| V01 baseline | exact branch head and merge-base comparison | branch derives from the verified `main` baseline and contains only F1 documentation/navigation changes |
| V02 source inventory | BKL031-S01–S11 against exact repository locators | every source is resolvable or explicitly `UNAVAILABLE`; no family label is treated as an exact source |
| V03 authority | source classification and precedence table | every projection remains a projection and no downstream read model overrides its source class |
| V04 identity | BKL-035 target identity/conflict contracts | `target_key`, `target_id`, identity state, Citation, Provenance and conflicts are preserved |
| V05 time/freshness | policy review | UTC/validity semantics are explicit; stale or historical evidence cannot become current/forecast |
| V06 semantic separation | five-object contract review | candidate, context, dimension, factor and explanation have distinct responsibilities |
| V07 advisory boundary | BKL-031/BKL-032/Safety review | no readiness, go/no-go, command or Safety Authority claim is introduced |
| V08 resource/security | deployment and data-minimization review | no heavy EAGLE workload, secret, raw-log exposure or ungoverned external transfer is introduced |
| V09 documentation | strict build/link/navigation checks | new documents render and are reachable; no broken link or duplicate authority is introduced |

## 3. Mandatory negative cases for F2 and later validators

| Test | Injected condition | Expected fail-closed result |
|---|---|---|
| N01 | candidate omits source/Citation/Provenance | candidate rejected or affected evidence `UNKNOWN`; no explanation |
| N02 | BKL-035 identity is conflicted but consumer reports validated | validation failure; conflict preserved |
| N03 | unknown target name is fuzzy-matched to an existing target | validation failure; no inferred alias or merge |
| N04 | historical configuration is used as current without validity interval | setup `UNAVAILABLE_CURRENT`; no setup-specific claim |
| N05 | site ID, coordinates or timezone reference missing | celestial and lunar dimensions `UNAVAILABLE` |
| N06 | target coordinates lack epoch or conflict with governed evidence | celestial dimension `CONFLICTED` or `UNAVAILABLE` |
| N07 | ephemeris/lunar source or method/version missing | no altitude, transit, darkness, phase or separation output |
| N08 | forecast lacks provider run, issue time, valid interval or spatial applicability | forecast `UNAVAILABLE` or `STALE` |
| N09 | historical CloudWatcher data is substituted for forecast | validation failure |
| N10 | realtime `fresh_until_utc` precedes evaluation time | evidence `STALE`; value excluded as current |
| N11 | null, zero or empty value is interpreted as a valid measure without source semantics | validation failure or `UNKNOWN` |
| N12 | analytics/read-model value overrides higher-authority session evidence | validation failure; conflict retained |
| N13 | factor contains weight, numeric score, threshold, normalization curve or ordering | F1 contract validation failure |
| N14 | explanation omits excluded or stale dimensions | validation failure |
| N15 | output uses `safe`, `ready`, `go`, `no-go`, `approved` or equivalent operational conclusion | validation failure |
| N16 | planner path edits N.I.N.A. sequence or issues device/network/power command | validation failure and release blocker |
| N17 | workload requires computation or external calls on EAGLE | validation failure and architecture blocker |
| N18 | suggested result is re-ingested as observed evidence | validation failure; provenance kind preserved |
| N19 | provider credential or raw operational locator enters public projection | security validation failure |
| N20 | source conflict is resolved by recency, file order or UI text alone | validation failure; state `CONFLICTED` |

## 4. Positive semantic examples

These are contract examples, not calculated planner outputs:

- a reconciled BKL-035 target with historical registered sessions may be represented as a `TargetCandidate` with historical evidence available;
- a candidate may carry `UNAVAILABLE` celestial/lunar and forecast dimensions without being silently removed;
- a historical SQM median may be explained as historical `OBSERVED` evidence for its session, never as current sky quality or forecast;
- an explicitly attested setup may be `DECLARED` for its historical session while the active setup remains `UNAVAILABLE_CURRENT`;
- an explanation may state why no advisory evaluation is possible, provided it lists the missing sources and evidence references.

## 5. F1 publication checks

Required on the exact PR head:

1. Developer Foundation success when the changed paths match its governed trigger; otherwise record `NOT_TRIGGERED / NOT_APPLICABLE` for documentation-only F1;
2. documentation validation / `mkdocs build --strict` success;
3. Word/manual workflow success when triggered;
4. changed-file review confirms documentation/navigation scope only;
5. all internal paths referenced by the F1 documents resolve;
6. no generated projection is edited manually;
7. no runtime, schema, script, workflow or EAGLE file is changed.

## 6. Evidence not required at F1

- real ephemeris, Moon or forecast values;
- provider credentials or production endpoints;
- target ranking, numeric quality result or comparison;
- PC Principale/EAGLE operational acceptance;
- UI/API consumer, scheduler or N.I.N.A. integration.

Absence of this evidence is intentional because F1 is architecture-only; it must remain explicitly unavailable rather than simulated.

## 7. Review gate

After publication and exact-head CI, stop. Independent ARB and Release Quality review are separate actions. AI-assisted review mode or any exception to normal review/merge controls requires explicit owner authorization scoped to the then-current exact head.
