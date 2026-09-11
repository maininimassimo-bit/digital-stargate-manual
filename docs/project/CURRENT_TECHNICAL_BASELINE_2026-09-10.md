# Digital StarGate Current Technical Baseline — 10/09/2026

| Campo | Valore |
|---|---|
| Stato | Current technical continuity baseline |
| Data | 11/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Accepted main baseline | `249a90265b9cd2323df6e1dfb0ab09c5c64f5f1b` |
| Current governed package | BKL-046 — AI Post-Processing Assistant for PixInsight |
| Current increment | BKL-046 F1 — Source Discovery and Advisory Semantic Contract |
| Accepted predecessor | BKL-041 capability closure; BKL-045; BKL-044; BKL-015 |

## 1. Accepted comparison foundation

BKL-037 F1-F5 e la projection dynamic full-catalog sono CLOSED / ACCEPTED / POST-MERGE VERIFIED tramite PR #153, merge `9375697fd979f826b331104fa7b86da58bb9b670`. Il comparison layer mantiene:

- unità e provenance compatibili;
- completeness e exclusions visibili;
- statistiche esclusivamente descrittive;
- `READ_ONLY`, `acceptanceAuthority=false`, `actionAuthority=NONE`;
- nessun quality score, ranking, threshold, recommendation o Safety Authority.

## 2. BKL-041 accepted F1

F1 source discovery e semantic contract è Accepted tramite PR #159, merge `6d48318c460bad040fd0754b0300fbcd76a2d312`. Ha definito dimensioni candidate, normalization/weighting governance, confidence, explainability, missing-data behavior, provenance, bias e authority senza implementare uno score.

## 3. Accepted BKL-041 F2–F5 and capability closure

F2 è Accepted tramite PR #160, merge `4ca5135043c508288fa2ba41b744f29b3b9032ed`. Ha reso eseguibili `QualityEvidence`, `AssessmentProfile` e `DimensionAssessment` mediante:

- JSON Schema versionato;
- identity deterministica e known-answer digest;
- fixture bounded positive;
- casi negativi per missing evidence, unità, FWHM calibration, PixInsight completeness, evidence class e authority;
- validator fail-closed;
- divieto eseguibile F2 di score, peso, normalizzazione, contribution e confidence numerica.

F3 è Accepted tramite PR #161, merge `89d8979fa4e5b151d85ef889efe03ad468efcad1`, con ARB 98/100 e Release Quality `READY FOR MERGE`. Ha introdotto normalizzazioni, weight set, scoring engine, confidence e decomposition con un profilo esclusivamente sintetico.

F4 è Accepted tramite PR #162, merge `ed9ffcc92e1a5252b0d8c37634bc652397f3cde1`, con ARB 98/100, Release Quality `READY FOR MERGE` e Pages #761 verde. Ha introdotto projection full-catalog, integrazione nella pipeline automatica e consumer con freshness fail-closed.

F5 e la capability BKL-041 sono CLOSED / ACCEPTED / POST-MERGE VERIFIED tramite PR #163, merge `e4ccd216b0a0ca4033277ece513f051b052d2b83`, ARB R1 98/100, Release Quality `READY FOR MERGE` e Pages `34602219671` verde. La baseline contiene 15 sessioni, 2 target noti, 5 assessment available, 3 unavailable e 7 invalid: l'uso produttivo resta non autorizzato.

## 4. Data and provenance constraints

- AP-013 resta authority per asset identity/checksum/lifecycle;
- AP-014 resta catalog/synchronization boundary;
- BKL-045 governa PixInsight provenance;
- missing evidence resta missing;
- `OBSERVED`, `DECLARED` e `SUGGESTED` non sono intercambiabili;
- FWHM source-native non calibrato non può essere promosso ad arcsec;
- schema/fixture F2/F3 e projection F4 non sono evidence di calibrazione produttiva.

## 5. Dynamic update boundary

F4/F5 estendono `analyze-session-automatic.yml`: projection e validation BKL-041 vengono rigenerate automaticamente dopo ogni nuova sessione scientifica importata ed entrano nello stesso commit governato del catalogo. Il consumer ricalcola SHA-256 di catalogo, projection e validation e non rende dati stale come correnti.

## 6. Runtime e safety

Nessuna modifica a EAGLE, servizi, scheduler, collector o apparati. Gli interlock fisici e la Safety Authority locale restano indipendenti.

## 7. Current entry condition

BKL-046 F1 è corrente per source discovery e semantic contract. Deve separare recommendation, human decision ed execution evidence, preservare provenance/missingness e ruolo advisory; non può trattare BKL-041 come ground truth o autorizzazione produttiva. F1 non seleziona model/provider, non implementa un apply path e non introduce remediation, device command o Safety Authority.
