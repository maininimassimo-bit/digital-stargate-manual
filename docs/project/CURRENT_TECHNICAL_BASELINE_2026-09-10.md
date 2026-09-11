# Digital StarGate Current Technical Baseline — 10/09/2026

| Campo | Valore |
|---|---|
| Stato | Current technical continuity baseline |
| Data | 11/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Accepted main baseline | `4ca5135043c508288fa2ba41b744f29b3b9032ed` |
| Current governed package | BKL-041 — Scientific Data Quality Score |
| Current increment | F3 — Deterministic Scoring and Confidence Engine |
| Accepted predecessor | BKL-041 F2; BKL-041 F1; BKL-037 capability closure |

## 1. Accepted comparison foundation

BKL-037 F1-F5 e la projection dynamic full-catalog sono CLOSED / ACCEPTED / POST-MERGE VERIFIED tramite PR #153, merge `9375697fd979f826b331104fa7b86da58bb9b670`. Il comparison layer mantiene:

- unità e provenance compatibili;
- completeness e exclusions visibili;
- statistiche esclusivamente descrittive;
- `READ_ONLY`, `acceptanceAuthority=false`, `actionAuthority=NONE`;
- nessun quality score, ranking, threshold, recommendation o Safety Authority.

## 2. BKL-041 accepted F1

F1 source discovery e semantic contract è Accepted tramite PR #159, merge `6d48318c460bad040fd0754b0300fbcd76a2d312`. Ha definito dimensioni candidate, normalization/weighting governance, confidence, explainability, missing-data behavior, provenance, bias e authority senza implementare uno score.

## 3. Accepted BKL-041 F2 and current F3

F2 è Accepted tramite PR #160, merge `4ca5135043c508288fa2ba41b744f29b3b9032ed`. Ha reso eseguibili `QualityEvidence`, `AssessmentProfile` e `DimensionAssessment` mediante:

- JSON Schema versionato;
- identity deterministica e known-answer digest;
- fixture bounded positive;
- casi negativi per missing evidence, unità, FWHM calibration, PixInsight completeness, evidence class e authority;
- validator fail-closed;
- divieto eseguibile F2 di score, peso, normalizzazione, contribution e confidence numerica.

F3 è ora l'incremento governato per normalizzazioni, weight set, scoring engine, confidence e decomposition. Il profilo è esclusivamente un dimostratore sintetico versionato: non rappresenta una calibrazione scientifica produttiva e non autorizza threshold, ranking, consumer o acceptance.

## 4. Data and provenance constraints

- AP-013 resta authority per asset identity/checksum/lifecycle;
- AP-014 resta catalog/synchronization boundary;
- BKL-045 governa PixInsight provenance;
- missing evidence resta missing;
- `OBSERVED`, `DECLARED` e `SUGGESTED` non sono intercambiabili;
- FWHM source-native non calibrato non può essere promosso ad arcsec;
- schema e fixture F2/F3 non sono projection di produzione.

## 5. Dynamic update boundary

F3 non modifica il flusso di import. Il requisito vincolante per F4 resta: la futura projection e il consumer BKL-041 devono rigenerarsi automaticamente dopo ogni nuova sessione scientifica importata tramite la pipeline governata, senza manutenzione manuale dei dati derivati e con freshness verificabile.

## 6. Runtime e safety

Nessuna modifica a EAGLE, servizi, scheduler, collector o apparati. Gli interlock fisici e la Safety Authority locale restano indipendenti.

## 7. Next validation

F3 richiede test locali e CI exact-head, ARB senza blocker/major e Release Quality recommendation. Nessuna acceptance F3 implica autorizzazione automatica per F4 o per un profilo produttivo.
