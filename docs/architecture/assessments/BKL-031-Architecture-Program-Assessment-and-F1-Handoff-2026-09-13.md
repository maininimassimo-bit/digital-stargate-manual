# BKL-031 — Architecture Program Assessment and F1 Handoff

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-APA-F1-001 |
| Stato | Ready for F1 architecture — implementation not authorized |
| Data | 13/09/2026 |
| Baseline | `main` @ `3d680dd3a05c70b2a4654c4187c293e36b0af4a7` |
| Capability | Observation Planner intelligente |
| Incremento | F1 — Source Discovery and Semantic Boundary |

## 1. Decisione di programma

Con BKL-046 chiuso e verificato, BKL-031 diventa il package governato corrente esclusivamente per F1. La sequenza resta `BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

La promozione non autorizza implementazione, ranking operativo, scheduling automatico, go/no-go, device command o Safety Authority.

## 2. Objective F1

Produrre un inventario verificato delle source e un semantic contract per un futuro ranking target per setup, considerando:

- Target Knowledge Base;
- setup, camera, OTA e filtri;
- altitudine, transito, finestra astronomica e contesto temporale;
- fase, altitudine e separazione lunare;
- forecast meteo e SQM;
- storico scientifico e disponibilità delle sessioni.

F1 deve definire i significati, non calcolare o pubblicare un ranking.

## 3. Dependency readiness

| Dipendenza | Stato | Uso consentito in F1 |
|---|---|---|
| BKL-015 Knowledge Graph foundation | Accepted | identity, relation e provenance contract |
| BKL-035 Target Knowledge Base | Accepted | target identity e source lineage |
| BKL-029 meteo/SQM | Accepted | telemetry semantics e historical evidence |
| AP-013/AP-014 session catalog | Accepted | session identity e historical context |
| Ephemeris/Lunar source | Da verificare | source authority, precision, timezone e freshness |
| Forecast source | Da verificare | origin, horizon, update cadence e missingness |
| Setup configuration source | Da verificare | stable identity, validity interval e conflicts |

Una dipendenza non verificata deve rimanere `UNAVAILABLE` o `UNKNOWN`; non può essere sostituita da assunzioni.

## 4. Deliverable F1 richiesto

Il package F1 deve includere:

1. source inventory con owner, authority, locator, update cadence, retention e sensitivity;
2. semantic contract per `TargetCandidate`, `PlanningContext`, `EvidenceDimension`, `RankingFactor` e `RankingExplanation`;
3. regole di identity/correlation per target, setup, sessione e tempo;
4. missingness, staleness, conflict e timezone policy fail-closed;
5. separazione fra fatti osservati, dati dichiarati e suggerimenti;
6. boundary fra ranking advisory, readiness e Safety Authority;
7. privacy/security/resource placement, escludendo workload pesante su EAGLE;
8. traceability e validation plan per la futura implementazione.

## 5. Scope escluso

- algoritmo, pesi, score, soglie o ordinamento reale;
- forecast provider o ephemeris provider scelto senza source discovery;
- scheduler, prenotazione o modifica sequenze N.I.N.A.;
- go/no-go o session readiness, che appartengono a BKL-032;
- remediation, device command, dome/mount control o interlock bypass;
- LLM/ML/RAG, confidence numerica o training;
- nuova produzione, credenziali o runtime su EAGLE.

## 6. Rischi iniziali

| ID | Rischio | Trattamento F1 |
|---|---|---|
| BKL031-R01 | ranking interpretato come via libera operativo | advisory-only e separazione esplicita da BKL-032/Safety |
| BKL031-R02 | ephemeris errate per tempo/coordinate/horizon | authority, timezone, site identity e precision contract |
| BKL031-R03 | forecast stale o assente | freshness e missingness fail-closed |
| BKL031-R04 | setup/target identity non stabile | correlation key e conflict policy |
| BKL031-R05 | storico introduce bias o self-supporting evidence | provenance, representativeness e explanation obbligatorie |
| BKL031-R06 | carico sul computer EAGLE | analytics pesanti fuori EAGLE; solo source bounded/read-only |
| BKL031-R07 | score implicito senza semantica | nessun peso o threshold in F1 |

## 7. Acceptance gate F1

F1 può passare a review soltanto quando tutte le source candidate sono classificate, le non verificate restano esplicite, il contratto non contiene score nascosti, authority e Safety boundary sono invariati, e il validation plan include negative test per staleness, missingness, conflict, timezone e identity mismatch.

Dopo la pubblicazione del package F1: fermarsi prima della review. ARB, Release Quality, eventuali modalità AI-assistite e ogni deroga richiedono autorizzazioni proprie.

