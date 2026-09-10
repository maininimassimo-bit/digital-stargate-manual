# BKL-037 F3 — Multi-Session Comparison Projection

| Campo | Valore |
|---|---|
| Identificativo | BKL-037-F3 |
| Stato | Proposed |
| Data | 10/09/2026 |
| Baseline | `973c2e7c8f3a9220a758bd6c8afa5ed0ac316fcc` |
| Dipendenza | BKL-037 F2 ACCEPTED |
| Authority | Derived read-only analytical projection |

## Obiettivo

Costruire una projection deterministica multi-sessione esclusivamente da `SESSION_COMPARISON_SET` F2 già classificati. F3 non rivaluta la provenance e non rende comparabili evidenze che F2 ha escluso.

## Contratto

`SESSION_COMPARISON_PROJECTION` espone:

- `projectionId` e `generatedAt`;
- `comparisonSetId`, dimensione e unità;
- sessioni incluse con valore e provenance;
- exclusions esplicite con reason;
- summary numerico descrittivo quando applicabile;
- lineage verso il comparison set e le source refs;
- limitations e authority fail-closed.

## Aggregazioni ammesse

Per cohort `COMPARABLE` con almeno due valori numerici finiti sono ammesse esclusivamente:

- sample size;
- minimum;
- maximum;
- mean;
- median;
- range.

Queste statistiche sono descrittive. Non costituiscono score, ranking, target, soglia di accettazione, SLA/SLO o recommendation.

Valori categorici possono restare visibili nella cohort, ma F3 non inventa una loro aggregazione numerica.

## Exclusions

Le exclusions prodotte da F2 restano visibili e non partecipano alle aggregazioni. `INSUFFICIENT_COMPARABLE_EVIDENCE` produce `descriptiveSummary = null`.

In particolare:

- FWHM senza calibrazione/unit provenance sufficiente non entra nel summary;
- PixInsight history `PARTIAL/UNAVAILABLE` non viene ricostruita;
- valori stale/unknown o provenance insufficiente restano esclusi;
- background e final quality non vengono convertiti in score.

## Authority e safety

La projection è `READ_ONLY`, `acceptanceAuthority=false`, `actionAuthority=NONE`.

Non scrive AP-013/AP-014, non modifica sessioni o asset, non esegue PixInsight, non comanda EAGLE/cupola/montatura/camera/power/rete e non modifica la Safety Authority locale.

## Acceptance criteria

F3 è accettabile quando:

1. consuma esclusivamente il comparison set F2;
2. non riclassifica candidati esclusi;
3. aggrega solo cohort comparabili e valori numerici finiti;
4. mantiene exclusions e lineage;
5. non introduce ranking, score o acceptance threshold;
6. rigetta authority escalation;
7. i test e i gate repository applicabili sono verdi sull'exact HEAD.

## Passo successivo

F4 potrà esporre questa projection nel portale come consumer read-only, mantenendo visibili provenance, exclusions e limitations. BKL-041 resta separato per qualunque futura semantica di Scientific Data Quality Score.
