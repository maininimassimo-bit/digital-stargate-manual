# BKL-031 F2 — Context Contract Validation Evidence

| Field | Value |
|---|---|
| Identifier | BKL-031-F2-VAL-001 |
| Status | **ARB REMEDIATION CANDIDATE — RE-REVIEW NOT AUTHORIZED** |
| Date | 2026-09-14 |
| Baseline | `f6c4b253a56406c930f009af0658b46a12bc088a` |
| Pre-remediation review-publication head | `86021de468b91f14c38db41bac47551e08b04e53` |
| Remediation exact head | Established by the PR after atomic publication |
| Contract | `schemas/observation-planner-context-f2.schema.json` |
| Fixture | `docs/data/observation-planner-context-f2-fixture.json` |
| Normative validator | `.github/scripts/verify-observation-planner-context-f2.mjs` |
| Negative suite | `.github/scripts/test-observation-planner-context-f2.mjs` |
| Runtime / EAGLE impact | None |

## 1. Local deterministic evidence

```text
BKL-031 F2 context contract OK: 11 sources / 1 candidate / 7 dimensions / no ranking
tests 36
pass 36
fail 0
```

The suite contains one positive bounded-fixture test, the twenty negative cases transferred unchanged from the accepted F1 validation plan, and fifteen regressions for ARB findings M-01–M-04. An additional exploratory matrix exercised 250 malformed JSON variants: every call returned a deterministic, non-empty error array and none threw.

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
| M-04 | S02/S04 coordinate-source restriction, complete RA/Dec/epoch triplet, ranges, governed-value reconciliation and conflict-state enforcement | PASS |

The review documents remain immutable evidence of the decision made on their reviewed head. This remediation does not change that decision and does not constitute a re-review.

## 4. Source reconciliation evidence

- Candidate `dsg-target:m-27` resolves exactly in `docs/data/target-knowledge-read-model.json`.
- Historical sessions `2026-08-14_2026-08-15` and `2026-08-15_2026-08-16` resolve in the scientific session catalog.
- SQM evidence resolves to session `2026-09-13_2026-09-14` in the historical analytics projection and remains explicitly historical.
- S07–S11 match the accepted unavailable/current-unknown states and expose no fixture fact values.
- Public fixture Citations remain limited to three normalized repository paths; S02/S04 coordinate reconciliation is validator-only and does not publish raw evidence detail.

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

The pre-remediation review-publication head `86021de468b91f14c38db41bac47551e08b04e53` also produced 7/7 successful workflows, but the ARB decision remained `REWORK REQUIRED`. The remediation exact head and its workflow results must be recorded in PR #188 after atomic publication. Re-review remains a separate authorization.

## 6. Governance stop

This evidence supports publication of an implementation PR candidate only. It does not constitute ARB approval, Release Quality approval, acceptance, merge authorization, branch-protection waiver or authorization for F3 providers/ranking/runtime work.
