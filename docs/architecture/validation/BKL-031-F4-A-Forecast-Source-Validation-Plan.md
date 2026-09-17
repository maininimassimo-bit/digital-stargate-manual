# BKL-031 F4-A — Forecast Source Validation Plan

| Field | Value |
|---|---|
| Identifier | `BKL-031-F4-A-VAL-001` |
| Status | **ACCEPTED REPOSITORY VALIDATION PLAN — NOT EXECUTED AGAINST A PROVIDER** |
| Date | 2026-09-17 |
| Contract | `BKL-031-F4-A-CONTRACT-001` |
| Runtime impact | None |

## 1. Purpose

This plan converts the accepted F1 forecast negative cases and the F4-A source decision into executable requirements for F4-B and later gates. F4-A validation is repository-only: links, terms, source characteristics, contract completeness and authority boundaries are checked without a provider request.

## 2. F4-A publication gates

| Gate | Pass condition |
|---|---|
| V01 predecessor | F3-C is Accepted / Post-Merge Verified and the public route is verified |
| V02 source identity | provider, upstream authority and exact model selector are distinct and explicit |
| V03 run lineage | one `runInitialisationUtc` is mandatory; `best_match`, seamless and stitched modes are prohibited |
| V04 time | UTC, half-open validity and 72-hour model horizon are explicit |
| V05 space/privacy | protected site reference is distinct from outbound coordinates and public grid metadata |
| V06 variables | the bounded ten-variable ICON-2I vocabulary and exact units are specified; unsupported visibility is explicit |
| V07 freshness | source-specific 18-hour run-age ceiling and fail-closed missed-cycle behavior are explicit |
| V08 licensing | attribution, non-commercial evaluation boundary and production decision gate are recorded |
| V09 security | off-EAGLE server-side acquisition, allow-list, no redirect, timeout and size bounds are required |
| V10 semantics | forecast remains advisory context; ranking, readiness, command and Safety claims are prohibited |
| V11 continuity | backlog, roadmap, knowledge map, project index and navigation agree on F4-A state |
| V12 build | workflow YAML, roadmap generation, strict MkDocs build and diff hygiene pass |

## 3. Mandatory F4-B negative cases

| ID | Injected condition | Expected result |
|---|---|---|
| N01 | missing provider, upstream authority, model or run | reject before network; forecast `UNAVAILABLE` |
| N02 | model is `best_match`, seamless or an unapproved selector | reject before network |
| N03 | run hour is not 00 or 12 UTC | reject before network |
| N04 | run age exceeds 18 hours at retrieval | `STALE`; no last-known-good fallback |
| N05 | request crosses the 72-hour run horizon | reject before network |
| N06 | local time, missing offset or unordered interval | reject |
| N07 | multiple locations, models or runs | reject |
| N08 | unknown query parameter or model-unavailable `visibility` variable | reject |
| N09 | provider request contains elevation or an unapproved exact-site precision | privacy rejection before network |
| N10 | redirect, non-allow-listed host, timeout or oversized response | acquisition fails closed |
| N11 | HTTP error, non-JSON response or provider error envelope | forecast `UNAVAILABLE`; no retry-derived evidence unless profile permits a bounded retry |
| N12 | response model/run cannot be bound to the request | reject evidence |
| N13 | returned spatial cell is absent or outside the approved applicability rule | `UNAVAILABLE` or `CONFLICTED` |
| N14 | missing unit, changed unit or array-length mismatch | reject affected dimension |
| N15 | duplicate, non-monotonic or out-of-range instant | reject evidence |
| N16 | non-finite cloud, humidity, wind, temperature or precipitation value | reject affected fact |
| N17 | cloud or humidity outside 0–100%, negative precipitation or wind | reject affected fact |
| N18 | missing raw-response digest, Citation, Provenance or terms revision | reject evidence |
| N19 | historical CloudWatcher data fills a missing forecast value | reject semantic substitution |
| N20 | a second run fills a gap or silently extends validity | reject run mixing |
| N21 | public projection exposes protected coordinates, raw URL, API key or internal locator | security/privacy release blocker |
| N22 | output claims safe/ready/go/no-go, ranking, score, command or automatic schedule | release blocker |
| N23 | terms or attribution requirements differ from the approved source profile | fail closed pending contract review |
| N24 | free endpoint is configured for production or commercial use without a recorded decision | release blocker |

## 4. Positive F4-B fixture

The first machine-readable fixture must remain `TEST` / `NONE`, use a synthetic/generalized Italian-domain location, contain one explicit 00 or 12 UTC ICON-2I run, no more than 72 hourly instants inside a half-open 72-hour horizon and the exact ten-variable vocabulary. It must record `visibility` as unavailable, include a canonical request digest, raw-response digest placeholder clearly marked synthetic, returned grid metadata, explicit units, Citation/Provenance, CC BY attribution and all prohibited-capability flags set to false/none.

No real response may be fabricated. A synthetic fixture is labelled synthetic; a future captured provider response requires its own network gate and immutable raw evidence.

## 5. Future bounded source OAT

Before F4-C performs a provider request, its exact head must record:

- approved synthetic/generalized coordinates or a separately approved protected-site outbound policy;
- exact endpoint, model, run, query fields, variable order, timeout, response-size limit and request count;
- observed terms revision and attribution text;
- preconditions proving zero earlier calls in the gate;
- postconditions proving the raw digest, normalized evidence, one run, one location and no public protected data;
- a stop condition after the bounded acquisition; no production scheduler or recurring traffic.

## 6. Stop condition

F4-A is Accepted / Post-Merge Verified and promotes F4-B schema, fixture and validator work. Stop before provider acquisition: F4-A does not authorize provider traffic, protected-site use, runtime, ranking, readiness, commands or Safety Authority.
