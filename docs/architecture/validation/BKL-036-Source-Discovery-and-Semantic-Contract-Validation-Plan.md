# BKL-036 — Source Discovery and Semantic Contract Validation Plan

**Identifier:** `BKL-036-VAL-001`  
**Status:** Proposed  
**Version:** 0.1  
**Runtime traffic:** None authorized

## Objective

Verify the BKL-036 source inventory and semantic contract before any score or runtime consumer is considered.

## Validation matrix

| Gate | Validation | Acceptance evidence |
|---|---|---|
| V1 | Source authority and ownership | Every candidate source has owner, system, field semantics and status |
| V2 | Evidence envelope | Timestamp, freshness, quality, coverage, provenance and correlation are explicit |
| V3 | Missingness | Missing, stale, partial, unavailable and conflicting inputs remain distinguishable |
| V4 | Semantic separation | Evidence, descriptive status, score, recommendation and Safety Authority are distinct |
| V5 | Compatibility | No cross-domain aggregation occurs without declared comparability |
| V6 | Privacy | Protected coordinates, credentials and raw sensitive payloads are excluded |
| V7 | Authority | No readiness, scheduling, remediation, command or interlock bypass is introduced |
| V8 | Repository quality | Links, navigation, identifiers, roadmap and backlog are consistent |

## Required negative cases

- absent source owner;
- missing observation timestamp;
- stale or future-dated evidence;
- conflicting domain observations;
- default zero replacing unknown;
- EAGLE host status presented as Safety Authority;
- descriptive health status presented as BKL-032 readiness;
- score/threshold/weight appearing in a source-discovery fixture;
- command or remediation field in a public projection;
- live provider or apparatus traffic during validation.

## Exit criteria

The package may advance to a future contract implementation only when all V1–V8 checks pass, open issues are dispositioned, and ARB plus Release Quality review the exact commit. This plan does not authorize a health score, runtime transport or device integration.
