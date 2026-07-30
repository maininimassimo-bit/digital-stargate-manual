# AMP-002 — Digital StarGate Architecture Program Roadmap Realignment

| Campo | Valore |
|---|---|
| Documento | Architecture Program Roadmap Realignment |
| Identificativo | AMP-002 |
| Programma | Digital StarGate |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Data | 30/07/2026 |
| Autorità | Project Owner / Architecture Sponsor — Massimo Mainini |
| Stato | Approved for planning; implementation subject to package review |
| Supersedes | Le sezioni di roadmap e numerazione futura di AMP-001 |

## 1. Scopo

AMP-002 riallinea la roadmap al programma architetturale effettivamente realizzato nel repository. Preserva AP-001…AP-006 e assegna gli identificatori successivi senza rinumerare gli artefatti esistenti.

La precedente numerazione futura contenuta in AMP-001 è dichiarata superata. AMP-001 resta una fonte storica per principi, quality gate e baseline iniziale, ma non è più la fonte autorevole per la sequenza dei package successivi ad AP-006.

## 2. Baseline verificata

| Package | Titolo | Review | Stato |
|---|---|---|---|
| AP-001 | Enterprise Metamodel and Repository Information Architecture | ARB-003 | Approved with conditions |
| AP-002 | Enterprise Data Governance | ARB-004 | Approved with conditions |
| AP-003 | Observatory Automation Architecture | ARB-005 | Approved with conditions |
| AP-004 | Enterprise Telemetry and Observability Architecture | ARB-006 | Approved with conditions |
| AP-005 | Identity, Access and Remote Operations Security Architecture | ARB-007 | Approved with conditions |
| AP-006 | Enterprise Configuration and Asset Management Architecture | ARB-008 | Approved with conditions |

## 3. Roadmap autorevole

### Wave 1 — Foundation

AP-001…AP-006 costituiscono la baseline architetturale iniziale. Le condizioni ARB restano aperte fino a evidenza verificabile.

### Wave 2 — Enterprise Operations

**AP-007 — Enterprise Operations and Service Management Architecture**

Definisce operating model, service ownership, incident, problem, change, release, maintenance, runbook, readiness, KPI e gestione delle modalità degradate.

### Wave 3 — Enterprise Integration

**AP-008 — Enterprise Integration Architecture**

Definisce API, eventi, adapter, contratti, versioning, compatibilità, affidabilità e integrazione con sistemi esterni.

### Wave 4 — Enterprise Infrastructure

**AP-009 — Enterprise Infrastructure Architecture**

Definisce topologia di deployment, rete, VPN, Starlink, Teltonika, EAGLE, Raspberry Pi, controller, storage, backup, resilienza, failover e disaster recovery.

### Wave 5 — Enterprise Safety

**AP-010 — Enterprise Safety Assurance Architecture**

Definisce hazard, safe state, interlock, manual override, emergency stop, fault containment, recovery e validation evidence. La safety locale resta indipendente dal portale e dal cloud.

### Wave 6 — Digital Platforms

**AP-011 — Enterprise Analytics Platform Architecture**

Governa la Digital StarGate Analytics Platform (DSAP): KPI, analisi storiche, reporting, trend, data quality, analisi scientifiche e operative, insight predittivi e viste executive.

**AP-012 — Enterprise Operations Center Architecture**

Governa il Digital StarGate Operations Center (DSOC): stato live, freshness, health, eventi, allarmi, incident console, timeline, runbook e command console autorizzata.

Il **Digital StarGate Portal (DSGP)** è il punto di accesso unificato a DSAP e DSOC e non costituisce una safety authority.

## 4. Capability introdotte

| Capability | Nome | Stato iniziale | Package principale |
|---|---|---|---|
| CAP-34 | Enterprise Analytics Platform | Planned | AP-011 |
| CAP-35 | Enterprise Operations Center | Planned | AP-012 |
| CAP-36 | Digital StarGate Portal | Planned | AP-011 / AP-012 |

Lo stato `Planned` non implica implementazione, deployment o readiness operativa.

## 5. Principi vincolanti

1. **User interfaces are not authoritative.** Portali e dashboard rappresentano stato e invocano use case autorizzati; non sostituiscono dominio, interlock, policy o safety authority.
2. **Operational data has two governed views.** Il dato operativo può essere fruito live da DSOC e storicamente da DSAP, usando sorgenti e contratti autorevoli senza pipeline parallele.
3. **Unknown is not safe.** Stato mancante, stale o degradato deve essere esplicito e non può essere interpretato come sicuro.
4. **Commands cross application boundaries.** La UI non accede direttamente a device, relay, driver o protocolli infrastrutturali.
5. **Read-only before control.** DSOC deve essere validato inizialmente in modalità osservativa; i comandi richiedono autorizzazione, audit, policy e safety review dedicate.

## 6. Dipendenze

```text
AP-001..AP-006 Foundation
        |
        v
AP-007 Operations and Service Management
        |
        +--> AP-008 Integration
        +--> AP-009 Infrastructure
        +--> AP-010 Safety Assurance
        |
        +--> AP-011 Analytics Platform ----+
        |                                  |
        +--> AP-012 Operations Center -----+--> DSGP
```

AP-011 dipende almeno da AP-002, AP-004, AP-006 e AP-007. AP-012 dipende almeno da AP-003, AP-004, AP-005, AP-006, AP-007, AP-008, AP-009 e AP-010.

## 7. Sequenza di esecuzione

1. Produrre AP-007 e relativa reference architecture.
2. Sottoporre AP-007 a review ARB indipendente.
3. Produrre AP-008, AP-009 e AP-010 in ordine dipendente dalle decisioni emerse.
4. Avviare AP-011 e AP-012 soltanto quando contratti, ownership, freshness, authorization e safety boundary sono stabili.
5. Implementare DSGP per incrementi, mantenendo DSAP e DSOC separati nei boundary applicativi.

## 8. Acceptance criteria del riallineamento

- AP-001…AP-006 non sono rinumerati.
- AMP-001 è conservato come fonte storica ma non governa più la numerazione futura.
- AP-007…AP-012 hanno scope univoci.
- CAP-34…CAP-36 sono registrate come `Planned`.
- traceability register e MkDocs includono AMP-002 e la Portal Vision.
- nessuna dashboard è dichiarata safety authority.
- build, link check e runtime validation sono registrati separatamente.

## 9. Validazioni

### Eseguite

- verifica del repository e del branch `main`;
- verifica di AMP-001, metamodel, traceability register e `mkdocs.yml`;
- verifica della presenza e delle review di AP-001…AP-006;
- verifica dell'assenza di AMP-002.

### Non eseguite

- `mkdocs build --strict`;
- link checker automatico;
- CI GitHub Actions;
- test runtime di dashboard, telemetry, command, safety o analytics.

## 10. Decisione

AMP-002 è approvato come nuova fonte autorevole della roadmap di programma successiva ad AP-006. Ogni Architecture Package resta soggetto a produzione specialistica, validazione e review ARB indipendente.