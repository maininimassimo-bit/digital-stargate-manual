# Digital StarGate Current Technical Baseline — 10/09/2026

| Campo | Valore |
|---|---|
| Stato | Current technical continuity baseline |
| Data | 10/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Transition baseline | `438863afdcfd3ee1fefc8b44b6b10808751b773a` |
| Current governed package | BKL-041 — Scientific Data Quality Score |
| Accepted predecessor | BKL-037 — Session Comparison & Benchmarking |

## 1. Accepted comparison foundation

BKL-037 F1-F5 e la projection dynamic full-catalog sono accettati. Il comparison layer mantiene:

- unità e provenance compatibili;
- completeness e exclusions visibili;
- statistiche esclusivamente descrittive;
- `READ_ONLY`, `acceptanceAuthority=false`, `actionAuthority=NONE`;
- nessun quality score, ranking, threshold, recommendation o Safety Authority.

## 2. Current BKL-041 entry condition

Le dipendenze BKL-029, BKL-037 e BKL-045 sono soddisfatte. BKL-041 può iniziare da F1, ma nessuna semantica di scoring è approvata prima del relativo contratto e delle review.

## 3. Data and provenance constraints

- AP-013 resta authority per asset identity/checksum/lifecycle;
- AP-014 resta catalog/synchronization boundary;
- BKL-045 governa PixInsight provenance;
- missing evidence resta missing;
- `OBSERVED`, `DECLARED` e `SUGGESTED` non sono intercambiabili;
- FWHM source-native non calibrato non può essere promosso ad arcsec.

## 4. Analytics boundary

Analytics Center e Session Comparison sono projection/read model. Weather analytics resta full-window evidence con `NO_SAFETY_AUTHORITY`.

## 5. Runtime e safety

Nessuna modifica a EAGLE, servizi, scheduler, collector o apparati. Gli interlock fisici e la Safety Authority locale restano indipendenti.

## 6. Next validation

BKL-041 F1 deve definire un contratto verificabile e fail-closed prima di qualsiasi algoritmo, peso, soglia, score o consumer.
