# BKL-031 F2 — Context Contract Validation Evidence

| Field | Value |
|---|---|
| Identifier | BKL-031-F2-VAL-001 |
| Status | **ACCEPTED / POST-MERGE VERIFIED** |
| Date | 2026-09-14 |
| Baseline | `f6c4b253a56406c930f009af0658b46a12bc088a` |
| Pre-remediation review-publication head | `86021de468b91f14c38db41bac47551e08b04e53` |
| First remediation exact head | `d21d57905b2669ccd572563449a523c1795bdcc2` |
| First remediation review-publication head | `9eb0af3b14c257163f2094ae334a5c1514b3a2de` |
| M-R1 remediation exact head | `8e46ae3eccdaca5763aee7103063e020f97e2946` |
| Final review-publication head | `09b6e2272f40688c7ead0eba964b8eb6f64a0920` |
| Merge commit | `7f861f7399079858c9744e69b6c773664b6b5b54` |
| Contract | `schemas/observation-planner-context-f2.schema.json` |
| Fixture | `docs/data/observation-planner-context-f2-fixture.json` |
| Normative validator | `.github/scripts/verify-observation-planner-context-f2.mjs` |
| Negative suite | `.github/scripts/test-observation-planner-context-f2.mjs` |
| Runtime / EAGLE impact | None |

## 1. Local deterministic evidence

```text
BKL-031 F2 context contract OK: 11 sources / 1 candidate / 7 dimensions / no ranking
tests 37
pass 37
fail 0
```

The suite contains one positive bounded-fixture test, the twenty negative cases transferred unchanged from the accepted F1 validation plan, and sixteen regressions for ARB findings M-01–M-04 and M-R1. An additional exploratory matrix exercised 250 malformed JSON variants: every call returned a deterministic, non-empty error array and none threw.

## 2. Mandatory negative-case traceability

| ID | Executable protection | Result |
|---|---|---|
| N01 | candidate source/Citation/Provenance required | PASS |
| N02 | BKL-035 conflict cannot become validated | PASS |
| N03 | exact target identity only; no fuzzy match | PASS |
| N04 | historical setup cannot become current | PASS |
| N05 | absent site keeps celestial/lunar unavailable | PASS |
| N06 | target coordinates require epoch | PASS |
| N07 | geometry/lunar output requires governed method/source | PASS |
| N08 | forecast requires run, issue, validity and spatial scope | PASS |
| N09 | historical weather cannot substitute forecast | PASS |
| N10 | expired realtime evidence becomes stale and value is excluded | PASS |
| N11 | null, zero, empty or semantically invalid measure rejected | PASS |
| N12 | analytics cannot override target authority | PASS |
| N13 | weight, score, threshold, normalization and ordering rejected | PASS |
| N14 | explanation must enumerate excluded/stale/conflicted evidence | PASS |
| N15 | operational conclusion vocabulary rejected | PASS |
| N16 | command, scheduler and sequence-edit fields rejected | PASS |
| N17 | EAGLE compute/external-call placement rejected | PASS |
| N18 | suggested output cannot be re-ingested as observed | PASS |
| N19 | raw locator or credential in public projection rejected | PASS |
| N20 | recency/file-order/UI-only conflict resolution rejected | PASS |

## 3. ARB remediation traceability

| Finding | Executable remediation | Result |
|---|---|---|
| M-01 | type-safe traversal, per-stage fail-closed guards, malformed root/container/missing/null regressions | PASS |
| M-02 | exact fact-to-source-field comparison and exact candidate/dimension/fact/explanation Provenance binding | PASS |
| M-03 | closed fact vocabulary per dimension plus prohibited readiness/safety/authorization/scoring semantics in keys and values | PASS |
| M-04 | S02 coordinate authority, complete RA/Dec/epoch triplet, ranges, governed-value reconciliation and conflict-state enforcement | PASS |
| M-R1 | S04 removed from coordinate fact sources; direct S04 locator rejected; current S04 non-attestation regression | PASS |

The review documents remain immutable evidence of their reviewed heads. The final owner-authorized AI-assisted re-review on `8e46ae3eccdaca5763aee7103063e020f97e2946` closed M-01–M-04 and M-R1 and returned `APPROVED — 99/100`; Release Quality returned `CONDITIONALLY READY`. These reviews are not equivalent to independent human approvals.

## 4. Source reconciliation evidence

- Candidate `dsg-target:m-27` resolves exactly in `docs/data/target-knowledge-read-model.json`.
- Historical sessions `2026-08-14_2026-08-15` and `2026-08-15_2026-08-16` resolve in the scientific session catalog.
- SQM evidence resolves to session `2026-09-13_2026-09-14` in the historical analytics projection and remains explicitly historical.
- S07–S11 match the accepted unavailable/current-unknown states and expose no fixture fact values.
- Public fixture Citations remain limited to three normalized repository paths. S02 is the only permitted F2 coordinate fact source; direct S04 coordinate Citations are rejected because current S04 metrics contain no RA/Dec/epoch fields and require S03 resolution.

## 5. Exact-head CI evidence

Developer Foundation executed both:

```text
node .github/scripts/verify-observation-planner-context-f2.mjs
node --test .github/scripts/test-observation-planner-context-f2.mjs
```

The pre-remediation implementation head `de5215ac7b63f442fc3e591467f8a6402942ce85` produced 7/7 successful workflows:

- Developer Foundation #1384 — SUCCESS, including both BKL-031 F2 steps;
- Validate documentation #1021 — SUCCESS;
- Genera manuale Word #1447 — SUCCESS;
- Scientific Platform Governance #84 — SUCCESS;
- BKL-041 F4 Governance #86 — SUCCESS;
- BKL-046 F4 governance #60 — SUCCESS;
- BKL-046 F5 governance #45 — SUCCESS.

The first remediation head `d21d57905b2669ccd572563449a523c1795bdcc2` and its review-publication head `9eb0af3b14c257163f2094ae334a5c1514b3a2de` each produced 7/7 successful workflows. The final M-R1 head `8e46ae3eccdaca5763aee7103063e020f97e2946` and review-publication head `09b6e2272f40688c7ead0eba964b8eb6f64a0920` also produced 7/7 successful workflows. Merge `7f861f7399079858c9744e69b6c773664b6b5b54` produced 9/9 successful post-merge workflows: Developer Foundation #1391, Validate documentation #1028, Genera manuale Word #1454, Scientific Platform Governance #91, Governed Projection Sync #33, Pages #794, BKL-041 F4 #93, BKL-046 F4 #67 and BKL-046 F5 #52.

## 6. Acceptance boundary

F2 is accepted only as a bounded repository contract and validation baseline. It provides no provider, ranking, readiness, scheduler, device-command, runtime or Safety Authority capability. `W-BKL031-F2-MERGE-001` is consumed/expired and creates no precedent. F3 and every successor increment require new owner authorization.
