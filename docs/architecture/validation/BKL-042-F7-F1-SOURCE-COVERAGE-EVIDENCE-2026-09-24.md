# BKL-042 F7 — F1 Source Coverage Increment Evidence

| Field | Value |
|---|---|
| Evidence ID | `BKL042-F7-SOURCE-COVERAGE-2026-09-24` |
| Status | Method v3 deployed on existing relay with max 1 instance; owner-witnessed OAT and formal acceptance pending |
| Authority | Bounded advisory / read-only |
| Owner / accountable | Massimo Mainini |
| Method | `bkl042-static-projection-retrieval-v3` |
| Base `main` | `50624ba6ac94b83a41647ae7f5f716ea00ec5ce7` |
| Merged `main` | `6e6cf43fdf7d29d67d4800541049a4acdf7f42ee` (PR #360; merged 2026-09-24) |
| Reviewed implementation head | `8b89c048828187a5ca67e06bc51fa94a6f6649fc` |
| Final PR head | `7d7bc9d2c134a710e67b779d5d33cbc0e1aeb53d` |

## Scope

Extend the existing bounded retrieval without closing BKL-042. Only published,
versioned projections with explicit provenance, freshness classification and
semantic limitations are passed as evidence. The increment does not deploy or
promote Cloud Run and does not alter provider, OAuth, command, broker, scheduler,
remediation or Safety Authority paths.

## Added eligible sources

| Source | Evidence and allowlist | Freshness / authority | Limitation |
|---|---|---|---|
| BKL-037 session comparison | `docs/data/session-comparison-projection.json`; dimension, unit, comparison state and bounded descriptive statistics | source digest and timezone-qualified `generatedAt`; historical projection / descriptive projection | no score, quality threshold, acceptance or recommendation |
| BKL-041 scientific data quality | `docs/data/scientific-data-quality-projection.json`; session, target, observation time and assessment state only | source digest and timezone-qualified `generatedAt`; `EXPERIMENTAL_NOT_ACCEPTED` / experimental context only | synthetic scores, confidence and decomposition are never forwarded; not production, ground truth, ranking or recommendation |

The existing observation index, target read-model and historical session catalog
remain enabled. Retrieval caps evidence at five records and at two per source so a
large experimental projection cannot crowd out other cited sources. The comparison
and quality portal routes are allowlisted; source digests remain attached to records.

## F1 classes not added as factual evidence

These classes remain in the F1 inventory; the present repository evidence does not
meet the eligibility gate for a production/current assertion:

| F1 class | Current evidence | Disposition |
|---|---|---|
| BKL-033 Digital Twin | bounded fixture only; no materialized runtime projection | excluded; do not treat fixture as observed asset status |
| BKL-034 image projection | target and session identity are already covered; image gallery dataset remains bounded fixture-backed | no new image/provenance facts added |
| BKL-034-F2 archive | contract fixture only; no real ingested archive projection | excluded; no image checksum/archive claims |
| BKL-045 PixInsight provenance | real OAT evidence does not establish complete, session-correlated production provenance | excluded; missing workflow facts are not reconstructed |
| BKL-031 planner | published current-night window ended `2026-09-24T07:00:00Z`; F5 ranking projection explicitly uses synthetic factors | excluded as current planner evidence |
| BKL-032 readiness | no eligible live readiness projection; S10 production runtime remains unavailable | excluded; no GO/NO-GO assertion |
| BKL-036-F5 EAGLE Health | inspected public snapshot is `UNAVAILABLE`, quality `UNKNOWN`, reason `NO_CURRENT_SNAPSHOT` | excluded as live health evidence; no stale/unknown value is presented as current |
| BKL-041 quality score | projection is explicitly `EXPERIMENTAL_NOT_ACCEPTED` | included only as clearly labeled status/context; synthetic numeric score fields excluded |

BKL-037 is included as a descriptive historical projection referenced by the
BKL-041 source contract; it does not change the F1 eligibility inventory.

## Verification

- `python -m unittest discover -v` in `infrastructure/bkl042-ai-relay`: 12 tests passed.
- Live, unauthenticated read-only replay against the published static projections:
  all five configured sources returned `AVAILABLE`; the M 27 session query returned
  session/target records without unrelated quality context; the SQM comparison query
  resolved to the BKL-037 comparison citation; an explicit scientific-quality query
  resolved to experimental records with numeric score fields withheld. Both new
  citation routes returned HTTP 200.
- Negative tests cover source-schema fail-closed behavior, query normalization,
  cross-source result caps, citation-route allowlisting, and exclusion of synthetic
  score/decomposition fields.
- Runtime output remains consultative; `command_authority=NONE`,
  `execution_authority=NONE`, `safety_authority=NONE`, and acceptance is
  `HUMAN_ONLY`.

## Merge and post-merge verification

PR [#360](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/360)
was merged to `main` as `6e6cf43fdf7d29d67d4800541049a4acdf7f42ee`. Every applicable
final-head workflow on `7d7bc9d2c134a710e67b779d5d33cbc0e1aeb53d` passed before
merge. All applicable post-merge workflows on the merge commit also passed:

| Workflow | Run | Result |
|---|---:|---|
| Developer Foundation | `35969957210` | SUCCESS |
| Validate documentation (no deploy) | `35969957340` | SUCCESS |
| Genera manuale Word | `35969957208` | SUCCESS |
| Deploy MkDocs artifact to GitHub Pages | `35969957266` | SUCCESS |
| Governed Projection Sync | `35969957197` | SUCCESS |
| Scientific Platform Governance | `35969957278` | SUCCESS |
| BKL-031 F3-B / F3-C | `35969957346` / `35969957352` | SUCCESS / SUCCESS |
| BKL-031 F4-A / F4-B / F4-C / F4-D | `35969957290` / `35969957338` / `35969957382` / `35969957388` | SUCCESS / SUCCESS / SUCCESS / SUCCESS |
| BKL-031 F5 / F6 | `35969957202` / `35969957125` | SUCCESS / SUCCESS |

The only failed run visible in the recent main history is
`35961982173` (“Analyze Observatory Session Automatically”) on superseded commit
`e404b282799f7379aa7b7af9b8b9c289ff646d81`; it is not a run on the merged F7 head.
The deployment and live configuration are recorded separately in
`docs/architecture/validation/BKL-042-F7-V3-DEPLOYMENT-EVIDENCE-2026-09-24.md`.
Method v3 is now deployed to the existing relay; the BKL-042 portal gateway is
unchanged. No authenticated OAT has yet been performed on v3. The deployment was
separately authorized by the owner to enable that OAT; no new service or package
closure is authorized by the source-coverage review.

## Remaining gates

This document records implementation evidence only. BKL-042 is **not closed**.
Required next gates are owner-witnessed authenticated OAT on method v3 and separate
formal owner acceptance. Source classes excluded above need eligible,
fresh, provenance-resolved upstream projections before later inclusion.
