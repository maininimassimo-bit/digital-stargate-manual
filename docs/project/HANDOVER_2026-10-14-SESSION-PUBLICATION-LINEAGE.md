# Handover — session publication lineage correction, 14 October 2026

## Problem and scope

The detail for `2026-09-19_2026-09-20` displayed fixed Processing/Publication placeholders despite a public M27 version associated with this session. Its metrics link escaped the Pages repository base and returned HTTP404.

The detail now joins the validated anonymous gallery collection by exact session ID and `OWNER_DECLARED` association. It renders every associated image/version and workflow, preserving partial capture and `NOT_ESTABLISHED` execution evidence. Target names never establish an association. Historical images without imported sessions remain unassociated.

## Refresh and failure semantics

Anonymous, bounded, no-store gallery GET on initialization, visibility return and every 60 seconds while visible; manual refresh is also available. Concurrent reads are suppressed. Previous publication links and graph nodes are cleared before refresh, so withdrawal or failure cannot retain a positive publication claim. Failure is unavailable/unknown, distinct from a successful empty collection. Detached page roots cannot receive a late response; their periodic refresh and visibility listener are removed.

Links bind session and exact image-version fragment in the gallery. Metrics point to the versioned repository evidence, with a constrained path. No authentication, provider upload, image publication, scientific processing, raw inventory inference or authority change is introduced. Existing acquisition/transfer projections remain unchanged. This is a public read model correction, not completion of scientific provenance.

## Validation and limits

- Seven regression tests cover M27/version/workflow, exact associations, multiple versions, withdrawal, unknown/error, gallery URLs and canonical metrics paths; seven existing routing tests also pass.
- CI exposed pre-existing quality-trend unit/browser tests fixed at ten scores, one QUATTRO score and twenty table rows, invalidated by the latest session import. Tests now compare all exact published session/score pairs, plotted session links, setup membership and available rows; production scoring is unchanged.
- MkDocs Pages strict build and inline-JavaScript gate passed before the final small presentation updates; final exact-head CI remains required.
- Local browser verification used a separately saved public gallery snapshot: M27/80 steps, withdrawal, failure and recovery passed. Live gallery requests from localhost are rejected by the existing cross-origin policy; this does not establish the final Pages-origin integration.
- Final CI, applicable reviews, merge, deployment and live-origin verification must be recorded on the PR. No released/accepted claim is made by this handover.

Rollback: revert this bounded UI/CI change and redeploy Pages; gallery records, scientific files and private services are untouched. BKL-046 reopening, M27 research STOP, BKL-051 OPEN/NOT_VALIDATED, P6 acceptance limits, BKL-043 lifecycle, BKL-050 and Safety remain unchanged.

## Esito finale registrato — 14 ottobre 2026

Il gate di rilascio inizialmente pending sopra è concluso per questo package: [PR587 / ricevuta post-merge](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/587#issuecomment-6165144093), head revisionato `552c0b9ef456d5dd652b942d7e903ab3d801d437`, merge `67a391d549c266f510c0d1a0a886cf9a3535d5f4`. ARB e poi RQ IA separate APPROVED sullo stesso head; CI PR10/10 e workflow sul merge9/9 SUCCESS, [Pages38540952820](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/38540952820) SUCCESS e verifica live registrata. Expected-head e zero-behind documentati sotto W-DSG-AEM-RULESET-001.

Le sezioni di implementazione restano lo snapshot del rispettivo incremento. Per lo stato consolidato dopo PR589 leggere il [riferimento tecnico](../developer/session-lineage-and-mission-control.md) e le [ricevute complete](../releases/2026-10-14-session-lineage-and-brand.md): gli incrementi successivi ampliano il rinnovo al catalogo/Mission Control e non stabiliscono nuova accettazione scientifica.
