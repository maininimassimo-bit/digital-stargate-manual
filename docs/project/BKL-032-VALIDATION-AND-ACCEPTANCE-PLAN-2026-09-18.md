# BKL-032 — Validation and Acceptance Plan

**Identifier:** `BKL-032-VAL-001`  
**Status:** Accepted with Conditions
**Release:** Release 2.x

## Scope

Validate the separate Session Readiness / Go-No-Go decision-support contract without runtime, provider traffic, EAGLE activity, device commands or Safety Authority changes.

## Test matrix

| Area | Required evidence |
|---|---|
| Contract | Valid session context and readiness record schemas |
| Positive path | Governed complete evidence produces the owner-approved positive state |
| Missing evidence | Fail-closed result with reason code |
| Stale evidence | Fail-closed result with freshness evidence |
| Conflict | Fail-closed result with conflict reason |
| Provenance | Source, run, timestamp, semantic type and correlation ID preserved |
| Privacy | Protected coordinates and exact site data absent from public projection |
| Boundary | No scheduler, command, automatic target selection or Safety Authority |
| Architecture | Domain/application/infrastructure dependency rules pass |
| Documentation | Links, navigation, roadmap and closure lineage consistent |

## Required owner decisions

The owner approved the state semantics on 2026-09-18: `GO` requires complete, fresh, consistent and passing mandatory evidence; `NO_GO` requires valid current evidence with at least one blocking failure; `INDETERMINATE` is the fail-closed result for missing, stale, conflicting or unavailable required evidence. Required checks and freshness thresholds remain to be defined and approved before implementation.

## Quality gates

Exact-head CI → process-separated ARB → Release Quality on the same SHA → expected-head merge → post-merge verification → acceptance reconciliation.

## Non-goals

No provider acquisition, live EAGLE inspection, dome/mount/camera/power/network command, scheduling, automated target selection or Safety Authority change is part of this plan.
