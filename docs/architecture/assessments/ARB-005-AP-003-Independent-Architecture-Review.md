# ARB-005 — Independent Architecture Review of AP-003

| Campo | Valore |
|---|---|
| Identificativo | ARB-005 |
| Oggetto | AP-003 — Observatory Automation Architecture |
| Tipo | Independent Architecture Review |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Data | 30/07/2026 |
| Baseline proposta | AP-003 e Observatory Automation Reference Architecture presenti su `main` |
| Reviewer | Digital StarGate Architecture Review Board |
| Decisione | **APPROVED WITH CONDITIONS** |
| Punteggio complessivo | **89/100** |

## 1. Executive decision

L'Architecture Review Board approva AP-003 con condizioni.

Il package è architetturalmente coerente con la baseline Digital StarGate e definisce correttamente la separazione tra safety authority locale, orchestrazione applicativa e controllo dei dispositivi. La proposta evita dipendenze vendor nel Domain, distingue Command da conferma fisica, tratta stati assenti o incoerenti come `UNKNOWN/FAULT`, preserva gli interblocchi locali e adotta una migrazione shadow-first con rollback manuale.

L'approvazione riguarda il modello architetturale e il percorso di adozione. Non certifica hardware, firmware, cablaggi, sensori, protocolli, soglie, timeout, comportamento in blackout, fault handling reale o readiness operativa dell'osservatorio.

CAP-16 Observatory Automation e CAP-17 Local Safety Interlocks restano `Partial`.

## 2. Scope della review

La review ha valutato:

- boundary Safety / Automation / Device Control;
- dependency direction Domain / Application / Infrastructure;
- porte applicative e adapter candidati;
- state model della copertura;
- orchestrazione di chiusura;
- failure mode e degraded modes;
- security e trust boundaries;
- observability e audit;
- migration, commissioning e rollback;
- coerenza con ADR-005, Capability 002, AP-002 e ARB-004;
- tracciabilità verso CAP-16 e CAP-17.

## 3. Evidenze verificate

Sono stati verificati nel repository:

- AP-003 — Observatory Automation Architecture;
- Observatory Automation Reference Architecture;
- ADR-005 — Weather Safety Interlock fail-safe, stato `Proposed`;
- Capability 002 — Weather Safety Interlock, stato `Proposed`;
- procedura di chiusura controllata dell'osservatorio;
- ARB-004 e condizioni applicabili ai contratti dati;
- Architecture Traceability Register;
- navigazione MkDocs.

## 4. Scorecard

| Categoria | Punteggio | Valutazione |
|---|---:|---|
| Completezza | 90 | Copre boundary, stati, failure mode, security, observability, migration e rollback; mancano evidenze implementative e commissioning. |
| Consistenza architetturale | 94 | Coerente con ADR-005, Capability 002, AP-001 e AP-002; non introduce authority safety applicativa. |
| Domain e layer integrity | 95 | SDK, process control, rete e persistenza restano fuori dal Domain. |
| Safety architecture | 96 | Interlock locali autoritativi, `UNKNOWN` fail-safe, nessun falso `CLOSED`, riapertura automatica esclusa. |
| Security e trust boundaries | 88 | Least privilege, segreti negli adapter, audit e divieto di comandi diretti da AI/dashboard; matrice autorizzativa concreta assente. |
| Operability e recovery | 87 | Degraded modes e principi di recovery solidi; timeout, escalation e procedure testate non disponibili. |
| Observability | 89 | Health per adapter, freshness, metriche, correlation e audit append-only definiti; schema ed evidence non implementati. |
| Migration e rollback | 93 | Inventario, simulatori, shadow mode, blocco apertura e chiusura controllata sono sequenziati correttamente. |
| Traceability | 86 | Collegamenti documentali presenti; ADR-005 e Capability 002 restano Proposed e la release mapping non è completa. |
| Enterprise readiness | 84 | Modello riusabile e governabile, ma ownership, inventory, test e commissioning impediscono readiness operativa. |

**Punteggio complessivo: 89/100.**

## 5. Strengths

### 5.1 Boundary corretti

La proposta separa chiaramente:

- autorità fisica degli interblocchi locali;
- decisione e orchestrazione applicativa;
- traduzione verso protocolli e SDK negli adapter infrastrutturali.

Questa separazione riduce il rischio che indisponibilità applicative, rete remota, dashboard o AI compromettano la safety.

### 5.2 Distinzione tra intenzione ed esito

Un Command esprime un'intenzione ma non prova l'esito. Gli stati `OPEN`, `CLOSED` e Park richiedono conferme locali o adapter verificati. Questo evita di dedurre lo stato fisico dall'ultimo comando inviato.

### 5.3 Failure handling prudente

La proposta considera perdita connettività, telemetria stale, power loss, controller failure, chiusura parziale, emergency stop, manual override, EAGLE bloccato e indisponibilità dei software astronomici.

### 5.4 Migrazione controllata

La sequenza inventario → simulatori → shadow mode → blocco apertura → chiusura automatica controllata limita il rischio e mantiene disponibile il ritorno alla procedura manuale.

### 5.5 Nessuna assunzione hardware trasformata in fatto

Controller, protocolli, soglie, timeout e comportamento elettrico sono esplicitamente lasciati da validare.

## 6. Findings

### Blocker

Nessun Blocker architetturale rilevato.

### Major

#### ARB5-M01 — Inventario fisico e contratti degli adapter non verificati

Sensori, finecorsa, controller, E-stop, alimentazioni, protocolli e capacità effettive non sono ancora associati a locator, versione e owner.

**Impatto:** AP-003 non è implementabile o commissionabile in modo ripetibile.

**Remediation:** completare la Fase 0 con inventario verificato, ownership, firmware/software version, interfacce, modalità di autenticazione e comportamento degradato.

#### ARB5-M02 — Nessuna evidenza di commissioning e fault validation

Non risultano test di isolamento rete, power loss, process termination, partial closure, contradictory sensors, controller failure, E-stop o manual override.

**Impatto:** il modello fail-safe non è dimostrato nel sistema reale.

**Remediation:** produrre una validation matrix con test ID, prerequisiti, expected result, actual result, evidence locator, owner e data.

#### ARB5-M03 — ADR-005 e Capability 002 restano Proposed

AP-003 dipende dalla policy Weather Safety Interlock, ma i due artefatti non risultano approvati.

**Impatto:** la decision authority e le invarianti safety non sono ancora una baseline deliberata.

**Remediation:** eseguire review e decisione formale su ADR-005 e Capability 002 oppure includerle in una re-review coordinata prima dell'abilitazione dei comandi automatici.

#### ARB5-M04 — Timeout, retry, heartbeat ed escalation non deliberati

La proposta richiede idempotenza e retry limitato, ma non definisce policy operative verificabili.

**Impatto:** rischio di comportamento non deterministico, comandi ripetuti o escalation tardiva.

**Remediation:** registrare decisioni separate e testate per timeout, retry budget, heartbeat, stale interval, escalation e reconciliation.

#### ARB5-M05 — Ownership operativa non formalizzata

L'owner di AP-003 è ancora proposto; non risultano assegnati owner per automation, local controller, safety validation, runbook e commissioning.

**Impatto:** condizioni, incidenti e waiver possono restare senza accountability.

**Remediation:** pubblicare RACI e autorità operative prima della Fase 1.

### Minor

#### ARB5-m01 — State model da rendere machine-readable

La state machine documentale è comprensibile, ma non esiste uno schema o modello eseguibile che impedisca transizioni illegali.

**Remediation:** introdurre una rappresentazione versionata e testabile degli stati e delle transizioni.

#### ARB5-m02 — Matrice autorizzativa dei comandi fisici assente

Sono dichiarati least privilege e audit, ma non sono definiti ruoli, comandi consentiti, contesto locale/remoto e requisiti di approvazione.

**Remediation:** creare una command authorization matrix con separazione read, operate, override e administration.

#### ARB5-m03 — Evidence contract di audit non definito

CorrelationId e audit append-only sono richiesti, ma schema, retention, accesso e protezione dell'integrità non sono ancora formalizzati.

**Remediation:** allineare gli audit event con AP-002 e condizioni ARB-004.

#### ARB5-m04 — Release mapping incompleto

AP-003 non è ancora associato a una release target e a relativi quality gate.

**Remediation:** collegare package, milestone, validation evidence, rollback e release decision.

### Observation

#### ARB5-O01 — La riapertura automatica resta correttamente fuori scope

La scelta è appropriata finché non esistono evidenze operative sufficienti.

#### ARB5-O02 — Il diagramma rappresenta boundary logici, non deployment verificato

Questa distinzione deve essere mantenuta nei package successivi.

## 7. Conditions of approval

L'approvazione è subordinata alle seguenti condizioni:

1. completare l'inventario verificato di dispositivi, controller, sensori, interlock, alimentazioni e protocolli;
2. formalizzare owner e RACI per automation, safety, commissioning, operations e incident response;
3. approvare o riesaminare formalmente ADR-005 e Capability 002;
4. definire timeout, retry, heartbeat, stale interval, reconciliation ed escalation con evidenza di test;
5. produrre simulatori e test architetturali prima di collegare hardware reale;
6. completare shadow mode e confrontare decisioni automatiche con procedure operatore;
7. eseguire fault test su rete, processi, alimentazione, sensori, controller, chiusura parziale, E-stop e override;
8. collaudare rollback manuale senza disabilitare interlock o protezioni locali;
9. definire command authorization matrix e audit event contract;
10. applicare le condizioni ARB-004 a schema, lineage, retention e accesso degli eventi operativi;
11. eseguire `mkdocs build --strict`, link check e lint;
12. non promuovere CAP-16 o CAP-17 senza evidenze TST/INT/OPS e decisione separata.

## 8. Re-review criteria

Una re-review mirata può chiudere le condizioni quando il repository contiene:

- inventory ed evidence annex AP-003;
- RACI approvata;
- ADR-005 e Capability 002 deliberate;
- validation matrix con risultati;
- state model e audit contract versionati;
- authorization matrix;
- runbook aggiornati;
- evidence di shadow mode, fault test e rollback;
- release mapping e CI/build evidence.

## 9. Validazioni

### Eseguite

- ispezione repository sul branch `main`;
- review documentale di AP-003 e Reference Architecture;
- confronto con ADR-005, Capability 002, AP-002 e ARB-004;
- verifica di dependency direction, safety boundary, failure modes, migration e rollback;
- verifica della tracciabilità documentale e della navigazione MkDocs.

### Non eseguite

- `mkdocs build --strict`;
- link checker o lint;
- test applicativi, architetturali o di integrazione;
- test N.I.N.A., CPWI, PHD2, ASCOM/Alpaca;
- test rete, VPN, failover o isolamento;
- test alimentazione e controller;
- fault injection;
- collaudo E-stop e manual override;
- commissioning fisico;
- certificazione safety.

## 10. Final decision

**AP-003 — APPROVED WITH CONDITIONS.**

AP-003 può essere usato come reference architecture e base per pianificazione, inventario, simulatori e shadow mode. Non autorizza ancora attivazione di comandi automatici sulla copertura, promozione delle capability o dichiarazione di safety readiness.
