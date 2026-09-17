# BKL-031 F8 — Current Astronomy and Setup Suitability Acceptance

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F8-ACCEPTANCE-001 |
| Stato | **ACCEPTED — POST-MERGE VERIFIED** |
| Data | 17/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento | F8 — Current Astronomy + Explicit Setup Suitability |
| Implementation PR | #279 |
| Exact head reviewed | `3f05693482208df2b56b66dcb71162589880e72b` |
| Implementation merge | `20669f7164460297d7318fc3b5874e4bc7f4bcde` |
| Acceptance reconciliation PR | RECONCILIATION_PR_PENDING |
| Successore | **BKL-031 F9 repeatable current-night planner closure** |

## Evidence di acceptance

- exact-head PR workflow matrix: **9/9 SUCCESS** sul commit `3f05693482208df2b56b66dcb71162589880e72b`;
- ARB exact-head: **APPROVED WITH CONDITIONS**, 0 Blocker, 0 Major, 0 Minor, 2 Observations, nessun waiver;
- Release Quality exact-head: **CONDITIONALLY READY FOR MERGE**, nessun waiver;
- expected-head merge: `20669f7164460297d7318fc3b5874e4bc7f4bcde`;
- post-merge push workflow matrix: **10/10 SUCCESS**, incluso Developer Foundation;
- verifier F8 source-bound: meteo F7 verificato per istante, setup ottico verificato contro baseline approvata, FOV ricalcolato, coordinate target legate alla source scientifica registrata, suitability e advisory-window score ricalcolati;
- mutation tests fail-closed attivi su lineage F7, meteo, setup, suitability, projection, finestre advisory, privacy e authority boundaries.

## Risultato scientifico bounded

F8 accetta come evidence di integrazione la notte 17–18 settembre 2026. La projection combina forecast reale F7 site-specific, geometria astronomica night-specific e suitability esplicita OTA/camera/filter per i setup governati e i target bounded LDN 1320 / M 27. La projection pubblica non contiene coordinate protette.

Questa acceptance **non** equivale a runtime ricorrente o production readiness: F7 resta one-shot, F8 non effettua provider request e S10 resta `UNAVAILABLE`.

## Boundary preservati

- `authority = NONE`, consumer read-only/advisory;
- readinessAuthority=false;
- automaticTargetSelection=false;
- schedulingAuthority=false;
- actionAuthority=NONE;
- commandAuthority=NONE;
- Safety Authority = local physical interlocks;
- BKL-032 mantiene l'ownership di Session Readiness / Go-No-Go;
- nessun provider traffic ricorrente è autorizzato da questa acceptance.

## Transition

BKL-031 resta **In Progress**. F8 chiude il gap di astronomia corrente + suitability esplicita per una notte bounded, ma non dimostra ancora una supply ripetibile per la notte corrente. Il solo successore promosso è **BKL-031 F9 repeatable current-night planner closure**.

F9 deve dimostrare, in modo governato e ripetibile, il criterio finale: selezione setup → forecast della notte → target compatibili → classifica spiegabile → finestre migliori, mantenendo separati readiness/safety/action authority e ogni autorizzazione di traffico provider ricorrente.
