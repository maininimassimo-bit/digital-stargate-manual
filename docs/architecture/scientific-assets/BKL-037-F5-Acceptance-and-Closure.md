# BKL-037 F5 — Acceptance & Closure

| Campo | Valore |
|---|---|
| Identificativo | BKL-037-F5 |
| Stato | Proposed |
| Data | 10/09/2026 |
| Baseline | `2e58d440b78e2c5c6d2f2c5978ccdf738c8674c3` |
| Dipendenza | BKL-037 F4 ACCEPTED |

## Obiettivo

Chiudere BKL-037 con una projection persistita basata su evidenza reale, prova repository-side end-to-end del consumer e gate finali di architettura/release.

## Acceptance package

- F1 — source discovery e semantic contract: ACCEPTED;
- F2 — canonical comparison read model: ACCEPTED;
- F3 — deterministic multi-session projection: ACCEPTED;
- F4 — fail-closed read-only portal consumer: ACCEPTED;
- F5 — real-session persisted projection + acceptance evidence: candidate for final acceptance.

## Evidenza reale

La projection `docs/data/session-comparison-projection.json` confronta la mediana SQM di due sessioni scientifiche reali e governate:

- `2026-09-05_2026-09-06`;
- `2026-09-07_2026-09-08`.

Entrambe usano `AAG CloudWatcher SOLO HTTP / lightmpsas`, unità `mag/arcsec2`, quality `AVAILABLE` e locator repository verificabile.

## Closure invariants

La chiusura è consentita solo se restano vere tutte le seguenti condizioni:

1. nessuna unità o provenance viene inventata;
2. exclusions e unavailable evidence restano visibili;
3. PixInsight history incompleta non viene ricostruita;
4. FWHM senza unit provenance verificata non viene promosso ad arcsec;
5. nessun ranking, score, quality threshold o acceptance threshold viene introdotto;
6. BKL-041 resta authority futura separata per Scientific Data Quality Score;
7. portal e projection sono READ_ONLY;
8. `acceptanceAuthority=false` e `actionAuthority=NONE`;
9. nessun impatto su runtime, device, AP-013/AP-014 write authority o Safety Authority;
10. exact-head CI e post-merge CI devono risultare verdi prima di dichiarare BKL-037 CLOSED / ACCEPTED.

## Residual limitations

- il primo acceptance slice persistito copre SQM median; le altre dimensioni restano abilitate dal contratto ma richiedono evidence compatibile prima di essere pubblicate;
- nessuna prova manuale browser viene inventata: l'evidence attuale è repository-side e la build Pages verifica l'integrazione statica;
- nessuna semantica BKL-041 viene anticipata.

## Closure decision

Lo stato rimane **Proposed** finché ARB, Release Quality, exact-head CI, merge e post-merge verification non sono completati.
