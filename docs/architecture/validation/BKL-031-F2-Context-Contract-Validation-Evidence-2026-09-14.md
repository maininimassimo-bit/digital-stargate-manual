# BKL-031 F2 — Context Contract Validation Evidence

| Field | Value |
|---|---|
| Identifier | BKL-031-F2-VAL-001 |
| Status | **IMPLEMENTATION HEAD VERIFIED — REVIEW NOT AUTHORIZED** |
| Date | 2026-09-14 |
| Baseline | `f6c4b253a56406c930f009af0658b46a12bc088a` |
| Verified implementation head | `de5215ac7b63f442fc3e591467f8a6402942ce85` |
| Contract | `schemas/observation-planner-context-f2.schema.json` |
| Fixture | `docs/data/observation-planner-context-f2-fixture.json` |
| Normative validator | `.github/scripts/verify-observation-planner-context-f2.mjs` |
| Negative suite | `.github/scripts/test-observation-planner-context-f2.mjs` |
| Runtime / EAGLE impact | None |

## 1. Local deterministic evidence

```text
BKL-031 F2 context contract OK: 11 sources / 1 candidate / 7 dimensions / no ranking
tests 21
pass 21
fail 0
```

The suite contains one positive bounded-fixture test and the twenty negative cases transferred unchanged from the accepted F1 validation plan.

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

## 3. Source reconciliation evidence

- Candidate `dsg-target:m-27` resolves exactly in `docs/data/target-knowledge-read-model.json`.
- Historical sessions `2026-08-14_2026-08-15` and `2026-08-15_2026-08-16` resolve in the scientific session catalog.
- SQM evidence resolves to session `2026-09-13_2026-09-14` in the historical analytics projection and remains explicitly historical.
- S07–S11 match the accepted unavailable/current-unknown states and expose no fixture fact values.
- Public Citations are limited to three normalized repository paths; no raw operational locator is published.

## 4. Exact-head CI evidence

Developer Foundation executed both:

```text
node .github/scripts/verify-observation-planner-context-f2.mjs
node --test .github/scripts/test-observation-planner-context-f2.mjs
```

The exact implementation head `de5215ac7b63f442fc3e591467f8a6402942ce85` produced 7/7 successful workflows:

- Developer Foundation #1384 — SUCCESS, including both BKL-031 F2 steps;
- Validate documentation #1021 — SUCCESS;
- Genera manuale Word #1447 — SUCCESS;
- Scientific Platform Governance #84 — SUCCESS;
- BKL-041 F4 Governance #86 — SUCCESS;
- BKL-046 F4 governance #60 — SUCCESS;
- BKL-046 F5 governance #45 — SUCCESS.

The governed projection commit is included in the verified head. This record documents evidence only; publishing it creates a later documentation-only head whose applicable workflows must also pass before any review request.

## 5. Governance stop

This evidence supports publication of an implementation PR candidate only. It does not constitute ARB approval, Release Quality approval, acceptance, merge authorization, branch-protection waiver or authorization for F3 providers/ranking/runtime work.
