# Handover — session publication lineage correction, 14 October 2026

## Problem and scope

The detail for `2026-09-19_2026-09-20` displayed fixed Processing/Publication placeholders despite a public M27 version associated with this session. Its metrics link escaped the Pages repository base and returned HTTP404.

The detail now joins the validated anonymous gallery collection by exact session ID and `OWNER_DECLARED` association. It renders every associated image/version and workflow, preserving partial capture and `NOT_ESTABLISHED` execution evidence. Target names never establish an association. Historical images without imported sessions remain unassociated.

## Refresh and failure semantics

Anonymous, bounded, no-store gallery GET on initialization, visibility return and every 60 seconds while visible; manual refresh is also available. Concurrent reads are suppressed. Previous publication links and graph nodes are cleared before refresh, so withdrawal or failure cannot retain a positive publication claim. Failure is unavailable/unknown, distinct from a successful empty collection. Detached page roots cannot receive a late response; their periodic refresh and visibility listener are removed.

Links bind session and exact image-version fragment in the gallery. Metrics point to the versioned repository evidence, with a constrained path. No authentication, provider upload, image publication, scientific processing, raw inventory inference or authority change is introduced. Existing acquisition/transfer projections remain unchanged. This is a public read model correction, not completion of scientific provenance.

## Validation and limits

- Seven regression tests cover M27/version/workflow, exact associations, multiple versions, withdrawal, unknown/error, gallery URLs and canonical metrics paths; seven existing routing tests also pass.
- MkDocs Pages strict build and inline-JavaScript gate passed before the final small presentation updates; final exact-head CI remains required.
- Local browser verification used a separately saved public gallery snapshot: M27/80 steps, withdrawal, failure and recovery passed. Live gallery requests from localhost are rejected by the existing cross-origin policy; this does not establish the final Pages-origin integration.
- Final CI, applicable reviews, merge, deployment and live-origin verification must be recorded on the PR. No released/accepted claim is made by this handover.

Rollback: revert this bounded UI/CI change and redeploy Pages; gallery records, scientific files and private services are untouched. BKL-046 reopening, M27 research STOP, BKL-051 OPEN/NOT_VALIDATED, P6 acceptance limits, BKL-043 lifecycle, BKL-050 and Safety remain unchanged.
