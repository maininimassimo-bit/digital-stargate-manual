# BKL-037 F1 — Session Comparison Source Discovery and Semantic Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-037-F1 |
| Stato | Accepted |
| Accepted merge | `4050b232c079170e0270dbc7d733d821f70f8c52` |
| Data | 10/09/2026 |
| Package | BKL-037 — Session Comparison & Benchmarking |
| Baseline | `f3aa1a5b547281206b6d892670af9816c882e5e4` |
| Authority | Repository-governed analytical contract; read-only |

## 1. Scopo

Definire il primo incremento governato di BKL-037: quali evidenze di sessione possono essere confrontate, con quali condizioni di comparabilità, quali semantiche devono restare distinte e quali inferenze sono vietate.

BKL-037 non introduce un nuovo sistema di acquisizione dati. Riusa esclusivamente evidenze e read model già accettati da BKL-029, BKL-035, BKL-039, BKL-040 e BKL-045, preservandone provenance, completeness, unità e authority.

## 2. Driver approvati

La Functional Roadmap richiede confronto fra sessioni per:

- FWHM;
- guiding RMS;
- SQM;
- background;
- integrazione;
- frame validi/scartati;
- temperatura e meteo;
- errori;
- workflow di post-produzione;
- qualità finale.

Queste dimensioni sono candidate di confronto, non metriche automaticamente comparabili. F1 introduce quindi una classificazione esplicita della comparabilità.

## 3. Principi architetturali

1. **Read-only:** nessun device command, remediation, processing automatico o Safety Authority.
2. **Evidence before comparison:** una differenza numerica non è significativa se le due evidenze non sono semanticamente comparabili.
3. **No unit invention:** unità mancanti o non dimostrate non vengono inferite.
4. **No completeness invention:** una provenance PixInsight `UNAVAILABLE` o `PARTIAL` resta tale e non viene ricostruita come `OBSERVED`.
5. **No quality authority:** F1 non introduce score scientifici, ranking o soglie di qualità. Tali decisioni appartengono a BKL-041 o a package successivi.
6. **Same-dimension only:** differenze e benchmark sono ammessi solo fra misure della stessa dimensione semantica e con unità compatibili.
7. **Provenance preserved:** ogni valore confrontato deve mantenere source locator, timestamp/finestra, quality/completeness e riferimento alla sessione.

## 4. Comparison candidate model

Ogni valore candidato al confronto deve poter essere rappresentato come:

```text
ComparisonCandidate
  sessionId
  dimension
  value
  unit
  source
  observedAt / interval
  quality
  completeness
  provenanceRef
  comparabilityClass
  exclusionReason
```

`value` può essere numerico, categorico o strutturato. L'assenza del valore deve essere rappresentata esplicitamente e non convertita in zero.

## 5. Comparability classes

| Classe | Significato | Confronto numerico |
|---|---|---|
| `COMPARABLE` | stessa dimensione, unità compatibili, provenance sufficiente | consentito |
| `CONTEXT_ONLY` | valore utile come contesto ma non normalizzato per confronto quantitativo | vietato |
| `PARTIAL` | evidenza presente ma incompleta | vietato salvo confronto descrittivo esplicito |
| `UNAVAILABLE` | evidenza non disponibile | vietato |
| `INCOMPATIBLE` | dimensione/unità/metodo non compatibili | vietato |
| `UNKNOWN` | impossibile determinare la comparabilità | vietato |

Il default fail-closed è `UNKNOWN`.

## 6. Dimensioni candidate e regole F1

### 6.1 FWHM

FWHM è confrontabile numericamente solo quando entrambe le evidenze dichiarano una unità verificabile e compatibile. Campi storici come `average_fwhm` senza conversione o unit provenance non devono essere reinterpretati come arcsec.

Se una misura è esplicitamente `fwhm_arcsec`, può essere candidata a `COMPARABLE`; altrimenti resta `CONTEXT_ONLY` o `UNKNOWN` finché la source non dimostra l'unità.

### 6.2 Guiding RMS

Confrontabile solo quando:

- la metrica rappresenta la stessa grandezza RMS;
- l'unità è esplicita e compatibile;
- il periodo osservativo è identificabile;
- non vengono mescolati valori per asse e total RMS senza semantic mapping esplicito.

### 6.3 SQM

Usare `mag/arcsec²` solo quando proviene dalla pipeline BKL-029 con source/quality/coverage preservati. Valori mancanti o stale non possono essere trattati come misura della sessione.

### 6.4 Background

Non è comparabile per default. Richiede metodo, unità e stage dell'immagine compatibili. F1 lo classifica `CONTEXT_ONLY` finché un contratto successivo non definisce una normalizzazione verificabile.

### 6.5 Integration time

Confrontabile quando il valore rappresenta integrazione effettivamente accettata nella sessione e l'unità temporale è esplicita. Planned exposure time e accepted integration time sono dimensioni distinte.

### 6.6 Frames valid/rejected

Confrontabili come conteggi solo quando la policy di validazione/rejection è identificabile. Percentuali derivate sono consentite solo da conteggi con medesimo denominatore semantico.

### 6.7 Temperature / weather

Sono contesto osservativo. Il confronto quantitativo richiede stessa metrica, stessa unità e source quality compatibile. Nessuna metrica meteo può essere trasformata in Safety decision.

### 6.8 Errors

Gli errori sono confrontabili descrittivamente per categoria/source/window. F1 non introduce severity ranking o failure score.

### 6.9 PixInsight processing provenance

Il confronto può mostrare:

- workflow identity/version;
- numero e tipo di step realmente `OBSERVED`;
- step `DECLARED` come dichiarati;
- completeness `COMPLETE/PARTIAL/UNAVAILABLE` quando presente nel contratto sorgente;
- limitation e lineage.

È vietato concludere che due sessioni abbiano lo stesso processing solo perché entrambe hanno `UNAVAILABLE` o zero step osservati.

### 6.10 Final quality

F1 non definisce una metrica autonoma di qualità finale. Eventuali indicatori esistenti possono essere mostrati come evidence descrittiva con la loro authority originale. Un quality score comparabile è fuori scope e dipende da BKL-041.

## 7. Benchmark semantics

In F1 `benchmark` significa esclusivamente **baseline descrittiva derivata da un insieme esplicito di sessioni comparabili**.

Non significa:

- obiettivo operativo;
- soglia di accettazione;
- SLA/SLO;
- qualità minima;
- ranking automatico;
- decisione Safety;
- recommendation AI.

Ogni benchmark futuro deve riportare cohort definition, sample size, dimension, unit, aggregation method e excluded-session reasons.

## 8. Comparison set

Una `ComparisonSet` deve dichiarare almeno:

```text
comparisonSetId
sessionIds[]
dimension
unit
inclusionRules[]
exclusionRules[]
sourceRefs[]
createdAt
consumerMode = READ_ONLY
acceptanceAuthority = false
```

Le sessioni escluse per incompletezza o incompatibilità restano visibili come exclusions e non vengono silenziosamente eliminate.

## 9. Authority boundary

BKL-037 consuma ma non sostituisce:

- BKL-029 per SQM history/provenance;
- BKL-035 per target/session knowledge context;
- BKL-039 per descriptive equipment performance evidence;
- BKL-040 per historical timeline/context;
- BKL-045 per PixInsight workflow provenance.

AP-013/AP-014 restano authority per asset/session identity e catalog/reconciliation secondo i relativi contratti.

## 10. Safety and operational impact

Nessun impatto runtime sugli apparati. Nessun comando a EAGLE, montatura, cupola, camera, power o rete. Nessuna modifica a Safety Authority o interlock locali.

## 11. Acceptance criteria F1

F1 è accettabile quando:

1. le dimensioni candidate della roadmap sono mappate a regole di comparabilità esplicite;
2. `COMPARABLE` è fail-closed e richiede unit/provenance compatibili;
3. FWHM senza unità dimostrata non viene promosso ad arcsec;
4. PixInsight `UNAVAILABLE/PARTIAL` resta non confrontabile come complete observed history;
5. benchmark è definito come descrittivo e non authoritative;
6. score/ranking/threshold restano fuori scope;
7. CI/documentation gates applicabili sono verdi sull'exact HEAD.

## 12. Incrementi successivi proposti

- **F2 — Canonical comparison read model:** schema e deterministic builder per `ComparisonCandidate` / `ComparisonSet`.
- **F3 — Multi-session comparison projection:** differenze, aggregazioni descrittive ed exclusions.
- **F4 — Portal consumer:** vista read-only con provenance/completeness visibili.
- **F5 — Acceptance/closure:** real repository evidence, ARB, Release Quality, protected merge e post-merge verification.

La sequenza può essere raffinata solo tramite repository evidence e governance, senza anticipare BKL-041.
