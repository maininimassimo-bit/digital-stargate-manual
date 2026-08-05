# ARB-006 — Independent Architecture Review of AP-004

| Campo | Valore |
|---|---|
| Identificativo | ARB-006 |
| Oggetto | AP-004 — Enterprise Telemetry and Observability Architecture |
| Tipo | Independent Architecture Review |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Data | 30/07/2026 |
| Baseline proposta | AP-004 e Enterprise Observability Reference Architecture presenti su `main` |
| Reviewer | Digital StarGate Architecture Review Board |
| Decisione | **APPROVED WITH CONDITIONS** |
| Punteggio complessivo | **90/100** |

## 1. Executive decision

L'Architecture Review Board approva AP-004 con condizioni.

Il package definisce una reference architecture coerente per metriche, log strutturati, correlation, health, audit, alerting ed evidence. La separazione tra observability, control e safety è esplicita: dashboard, alert, Warehouse, AI e notification channel non acquisiscono autorità safety né capacità implicita di comandare dispositivi. Il modello distingue inoltre stato fisico, stato applicativo, health, freshness e qualità del dato, evitando che assenza o stale telemetry producano falsi `SAFE`, `CLOSED` o `HEALTHY`.

L'approvazione riguarda il modello architetturale, i contratti candidati e il percorso di adozione. Non certifica stack, protocolli, deployment, volumi, cardinalità, retention, SLI/SLO, soglie, buffering, notification routing o operatività continua.

CAP-08 Live Telemetry resta `Planned`.

## 2. Scope della review

La review ha valutato:

- separazione metric/log/trace/health/audit/alert;
- boundary observability/control/safety;
- dependency direction e isolamento dagli SDK vendor;
- semantic envelope e contract boundaries;
- health, freshness e reconciliation;
- audit integrity, accesso e classificazione;
- alert lifecycle, escalation e runbook;
- degraded operation, buffering, backpressure e clock drift;
- migration, pilot, rollback ed evidence;
- coerenza con AP-002/ARB-004 e AP-003/ARB-005;
- tracciabilità verso CAP-08, CAP-16, CAP-17 e governance release.

## 3. Evidenze verificate

Sono stati verificati nel repository:

- AP-004 — Enterprise Telemetry and Observability Architecture;
- Enterprise Observability Reference Architecture;
- ARB-004 e condizioni su schema, lineage, retention, accesso ed evidence;
- ARB-005 e condizioni su health, audit, correlation, fault validation e safety boundary;
- Architecture Traceability Register;
- navigazione MkDocs.

## 4. Scorecard

| Categoria | Punteggio | Valutazione |
|---|---:|---|
| Completezza | 91 | Copre segnali, contratti, security, degraded modes, migration, rollback ed evidence; manca implementazione verificata. |
| Consistenza architetturale | 95 | Coerente con AP-002, AP-003 e relative review; nessuna authority safety assegnata alla telemetry. |
| Domain e layer integrity | 94 | Instrumentation e adapter isolano SDK e backend; i nomi delle porte restano candidati. |
| Semantic model | 93 | Separazione chiara dei signal e semantic envelope robusto; schema machine-readable non ancora pubblicato. |
| Safety boundary | 97 | Assenza/staleness non diventano safe; interlock locali restano indipendenti. |
| Security e audit | 89 | Least privilege, segregazione e anti-tampering richiesti; meccanismi concreti e access matrix assenti. |
| Operability e alerting | 88 | Lifecycle completo; mancano SLI/SLO, soglie, routing, fallback e prove operative. |
| Resilience e degraded modes | 90 | Copre collector/storage/network/clock/notification/power; budget e test non disponibili. |
| Migration e rollback | 93 | Inventory, contract, pilot, shadow observability e governance automation ben sequenziati. |
| Traceability ed enterprise readiness | 86 | Collegamenti presenti; owner, release mapping, pilot ed evidence CI restano aperti. |

**Punteggio complessivo: 90/100.**

## 5. Strengths

### 5.1 Separazione dei signal

Metriche, log diagnostici, correlation, health, audit e alert hanno significati e responsabilità distinti. Questa scelta riduce duplicazioni e impedisce che un log venga trattato come audit protetto o che un health check venga interpretato come safety state.

### 5.2 Osservabilità senza autorità

Il principio `Observability is evidence, not authority` è applicato in modo consistente. Nessun flusso da Operations o Governance verso la Local Safety Zone è implicito; ogni comando deve attraversare AP-003.

### 5.3 Health model prudente

Liveness, readiness, dependency e freshness non vengono appiattiti in un singolo booleano. `UNKNOWN` e `DEGRADED` sono mantenuti come stati espliciti e il restart richiede reconciliation dalle fonti autoritative.

### 5.4 Degraded operation completa

Il package considera perdita rete, collector e storage indisponibili, clock drift, volume anomalo, notification failure, restart e power loss. Drop, sampling e perdita di signal devono essere visibili e non silenziosi.

### 5.5 Migrazione misurata

La sequenza inventory → contracts → local pilot → shadow observability → operational adoption → governance automation evita una selezione prematura dello stack e richiede una baseline misurata prima di SLI/SLO e soglie.

## 6. Findings

### Blocker

Nessun Blocker architetturale rilevato.

### Major

#### ARB6-M01 — Inventory e capacità dei producer non verificate

Producer, signal, protocolli, frequenze, volumi, cardinalità e dipendenze non sono ancora registrati con owner ed evidence locator.

**Impatto:** impossibile dimensionare collection, storage, retention, rate control e disponibilità.

**Remediation:** completare la Fase 0 con catalogo verificato di producer e signal, classificazione, owner, volume osservato, cardinalità, frequenza e dependency.

#### ARB6-M02 — Nessun pilot end-to-end o resilience test

Non risultano prove di schema validation, correlation, buffering, recovery, backpressure, clock drift, restart, storage pressure o notification failure.

**Impatto:** la resilienza proposta non è dimostrata.

**Remediation:** eseguire un pilot non safety-critical con validation matrix, risultati, evidence locator e rollback.

#### ARB6-M03 — Audit contract e protezione dell'integrità non implementati

Il modello audit è corretto ma schema versionato, anti-tampering, retention, accesso, disposal e immutabilità non sono verificati.

**Impatto:** gli eventi non possono ancora essere usati come evidence certificabile.

**Remediation:** pubblicare schema machine-readable e policy operative allineate ad AP-002/ARB-004, con test di accesso e integrità.

#### ARB6-M04 — Alerting operativo non deliberato

Severity candidate, SLI/SLO, soglie, acknowledgement target, routing, fallback, escalation e closure criteria non sono ancora approvati.

**Impatto:** alerting non certificabile e rischio di alert storm, fatigue o mancata consegna.

**Remediation:** misurare la baseline, assegnare owner, collegare runbook e testare l'intero lifecycle dell'alert.

#### ARB6-M05 — Ownership, RACI e release mapping assenti

L'Observability Owner è proposto; non risultano accountability formalizzate per producer, collector, audit, alert, operations e data lifecycle.

**Impatto:** incidenti, waiver, retention e condizioni di release possono restare senza decision authority.

**Remediation:** pubblicare RACI e collegare AP-004 a milestone, quality gate, rollback e release decision.

### Minor

#### ARB6-m01 — Semantic contracts non machine-readable

I record sono descritti testualmente ma non risultano JSON Schema, DTO o contratti eseguibili versionati.

**Remediation:** formalizzare metric, structured event, health e audit schema con compatibility tests.

#### ARB6-m02 — Cardinality e cost governance da esplicitare

Il package richiede approvazione per label ad alta cardinalità ma non definisce budget, processo di eccezione o review.

**Remediation:** introdurre cardinality budget, owner, waiver con scadenza e gate di rilascio.

#### ARB6-m03 — Policy di priorità in storage pressure incompleta

Audit e fault critici sono protetti, ma non esiste una gerarchia deliberata di signal, drop e sampling.

**Remediation:** definire priorità, perdita ammessa, drain/export e recovery per ciascuna classe.

#### ARB6-m04 — Continuous operations e backup non coperti da evidence

La reference architecture riconosce il gap, ma non definisce ancora disponibilità target, backup, restore e disaster recovery.

**Remediation:** integrare AP-004 con decisioni infrastrutturali dopo inventory e pilot.

### Observation

#### ARB6-O01 — La neutralità vendor è appropriata

La selezione dello stack dopo inventory e pilot riduce lock-in e decisioni premature.

#### ARB6-O02 — CAP-08 resta correttamente Planned

La documentazione architetturale non viene confusa con implementazione o operatività continua.

## 7. Conditions of approval

L'approvazione è subordinata alle seguenti condizioni:

1. completare inventory verificato di producer, signal, protocolli, volumi, frequenze, cardinalità e dipendenze;
2. formalizzare owner e RACI per instrumentation, collection, storage, audit, alerting, operations e data lifecycle;
3. pubblicare contratti machine-readable versionati e compatibility tests;
4. definire access matrix, integrità, retention e disposal degli audit secondo AP-002/ARB-004;
5. eseguire un pilot end-to-end non safety-critical;
6. testare loss, buffering, backpressure, clock drift, restart, storage pressure e notification failure;
7. misurare baseline prima di approvare SLI, SLO, soglie e alert timing;
8. deliberare alert routing, fallback, acknowledgement, escalation, runbook e closure criteria;
9. definire cardinality budget, rate control e policy di priorità/drop/sampling;
10. collegare AP-004 a milestone, quality gate, rollback e release decision;
11. eseguire `mkdocs build --strict`, link check, lint e contract validation;
12. non promuovere CAP-08 senza implementation, test e operations evidence.

## 8. Re-review criteria

Una re-review mirata può chiudere le condizioni quando il repository contiene:

- inventory ed evidence annex AP-004;
- RACI approvata;
- semantic contracts versionati;
- audit integrity e access evidence;
- pilot validation matrix con risultati;
- baseline di volume/cardinalità e SLI candidate;
- alert lifecycle testato;
- buffering/backpressure/recovery evidence;
- release mapping e CI/build evidence.

## 9. Validazioni

### Eseguite

- ispezione repository sul branch `main`;
- review documentale di AP-004 e Reference Architecture;
- confronto con AP-002/ARB-004 e AP-003/ARB-005;
- verifica di semantic separation, dependency direction, safety boundary, degraded modes, migration e rollback;
- verifica della tracciabilità documentale e della navigazione MkDocs.

### Non eseguite

- `mkdocs build --strict`, link checker o lint;
- test di instrumentation, collector, storage, audit o notification;
- test rete, buffering, backpressure, clock drift, restart o power loss;
- misurazione di volumi e cardinalità;
- test di accesso, integrità o retention;
- definizione o verifica di SLI/SLO;
- runtime, continuous operations o disaster recovery test.

## 10. Final decision

**AP-004 — APPROVED WITH CONDITIONS.**

AP-004 può essere usato come reference architecture e base per inventory, contratti, pilot ed evidence. Non autorizza ancora la promozione di CAP-08, la selezione definitiva dello stack o una dichiarazione di observability readiness operativa.