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

### Wave 7 — Scientific Image and Processing Heritage

**AP-013 — Scientific Image Repository Architecture**

Governa il ciclo di vita degli asset scientifici: RAW, calibration, master, intermedi, progetti PixInsight, prodotti finali, preview, checksum, immutabilità, retention, backup, storage esterno e processing provenance.

**AP-014 — Scientific Observation Catalog and Search Architecture**

Governa il catalogo GitHub dei metadati, i link allo storage esterno, la ricerca, l'indicizzazione, i manifest di sessione e di elaborazione, il provenance graph e la sincronizzazione automatica con PixInsight tramite adapter e script governati.

GitHub conserva conoscenza, metadati, workflow, manifest e riferimenti; non è lo storage primario dei RAW o degli altri file binari ad alto volume.

### Wave 8 — Scientific Knowledge Platform

**AP-015 — Scientific Knowledge Platform Architecture**

Governa la Scientific Knowledge Layer (SKL): vocabolario scientifico, knowledge entity, relazioni tipizzate, scientific claim, citation locator, provenance end-to-end, knowledge search e projection per DSAP, DSGP e AI read-only.

La SKL collega catalogo scientifico, Warehouse, documentazione GitHub, configurazioni e report senza sostituire le fonti autorevoli e senza duplicare obbligatoriamente i RAW. La scelta tra knowledge graph, semantic index, vector index o modello ibrido sarà trattata come decisione successiva basata su contratti, volumi e casi d'uso verificati.

## 4. Capability introdotte

| Capability | Nome | Stato iniziale | Package principale |
|---|---|---|---|
| CAP-34 | Enterprise Analytics Platform | Planned | AP-011 |
| CAP-35 | Enterprise Operations Center | Planned | AP-012 |
| CAP-36 | Digital StarGate Portal | Planned | AP-011 / AP-012 |
| CAP-37 | Scientific Image Repository | Planned | AP-013 |
| CAP-38 | Scientific Observation Catalog and Search | Planned | AP-014 |
| CAP-39 | Scientific Processing Provenance | Planned | AP-013 / AP-014 |
| CAP-40 | Scientific Knowledge Layer | Planned | AP-015 |

Lo stato `Planned` non implica implementazione, deployment o readiness operativa.

## 5. Principi vincolanti

1. **User interfaces are not authoritative.** Portali e dashboard rappresentano stato e invocano use case autorizzati; non sostituiscono dominio, interlock, policy o safety authority.
2. **Operational data has two governed views.** Il dato operativo può essere fruito live da DSOC e storicamente da DSAP, usando sorgenti e contratti autorevoli senza pipeline parallele.
3. **Unknown is not safe.** Stato mancante, stale o degradato deve essere esplicito e non può essere interpretato come sicuro.
4. **Commands cross application boundaries.** La UI non accede direttamente a device, relay, driver o protocolli infrastrutturali.
5. **Read-only before control.** DSOC deve essere validato inizialmente in modalità osservativa; i comandi richiedono autorizzazione, audit, policy e safety review dedicate.
6. **Scientific images are immutable assets.** I RAW originali non vengono modificati; ogni derivato possiede provenance esplicita.
7. **GitHub stores knowledge, not bulk pixels.** GitHub conserva catalogo, manifest, workflow, checksum e link; lo storage esterno conserva i binari voluminosi.
8. **Workflow definition and execution history are separate.** Una ricetta PixInsight versionata non prova la sua esecuzione; ogni elaborazione genera una Processing Run immutabile.
9. **Automation preserves truth.** Gli step PixInsight non acquisibili automaticamente devono essere dichiarati manualmente o marcati `unknown`, mai inventati.
10. **Knowledge references authoritative sources.** La SKL collega, indicizza e interpreta fonti governate; non le sostituisce e non risolve silenziosamente i conflitti.
11. **Claims require provenance and citations.** Ogni scientific claim derivato deve conservare fonte, metodo, versione e livello di confidenza.
12. **AI consumes governed knowledge read-only first.** Inferenze AI non diventano fatti autorevoli senza evidenza e approvazione esplicite.

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
        |
        +--> AP-013 Scientific Image Repository
                |
                +--> AP-014 Scientific Catalog, Search and PixInsight Sync
                        |
                        +--> AP-015 Scientific Knowledge Platform
                                |
                                +--> DSAP scientific analytics
                                +--> DSGP knowledge search
                                +--> Read-only AI retrieval
```

AP-011 dipende almeno da AP-002, AP-004, AP-006 e AP-007. AP-012 dipende almeno da AP-003, AP-004, AP-005, AP-006, AP-007, AP-008, AP-009 e AP-010.

AP-013 dipende almeno da AP-002, AP-006, AP-008 e AP-009. AP-014 dipende da AP-013 e usa i contratti di AP-008. L'integrazione PixInsight deve mantenere il prodotto come sistema esterno attraverso un adapter infrastrutturale.

AP-015 dipende almeno da AP-002, AP-006, AP-008, AP-011, AP-013 e AP-014. Il modello semantico può essere preparato dopo AP-014, ma la selezione tecnologica richiede contratti, volumi, ownership e query target misurabili.

## 7. Sequenza di esecuzione

1. Produrre AP-007 e relativa reference architecture.
2. Sottoporre AP-007 a review ARB indipendente.
3. Produrre AP-008, AP-009 e AP-010 in ordine dipendente dalle decisioni emerse.
4. Avviare AP-011 e AP-012 soltanto quando contratti, ownership, freshness, authorization e safety boundary sono stabili.
5. Produrre AP-013 dopo le decisioni su storage, data governance, backup e asset identity.
6. Produrre AP-014 dopo AP-013, includendo catalogo GitHub, ricerca, manifest e proof of concept della sincronizzazione PixInsight.
7. Produrre AP-015 dopo la stabilizzazione del catalogo scientifico, definendo vocabolario, relazioni, citation model, conflitti e query prioritarie prima della tecnologia.
8. Implementare DSGP per incrementi, mantenendo DSAP, DSOC, Scientific Catalog e Scientific Knowledge Layer separati nei boundary applicativi.

## 8. Acceptance criteria del riallineamento

- AP-001…AP-006 non sono rinumerati.
- AMP-001 è conservato come fonte storica ma non governa più la numerazione futura.
- AP-007…AP-015 hanno scope univoci.
- CAP-34…CAP-40 sono registrate come `Planned`.
- traceability register e MkDocs includono AMP-002, Portal Vision, Scientific Image Lifecycle Vision e Scientific Knowledge Layer Vision.
- nessuna dashboard o knowledge projection è dichiarata safety authority.
- RAW e binari voluminosi non sono pianificati nel repository GitHub.
- Processing Run, workflow version, input/output checksum e step manuali sono previsti dal modello di provenance.
- gli script PixInsight non contengono credenziali GitHub privilegiate.
- la SKL conserva citation locator, provenance e conflitti espliciti.
- la scelta della tecnologia knowledge/vector è differita fino a evidenza di requisiti e volumi.
- build, link check e runtime validation sono registrati separatamente.

## 9. Validazioni

### Eseguite

- verifica del repository e del branch `main`;
- verifica di AMP-001, metamodel, traceability register e `mkdocs.yml`;
- verifica della presenza e delle review di AP-001…AP-006;
- verifica dei riferimenti PixInsight già presenti nel repository;
- verifica della separazione corrente tra catalogo documentale GitHub e storage scientifico futuro;
- verifica della non sovrapposizione tra Warehouse, Scientific Catalog e Scientific Knowledge Layer.

### Non eseguite

- `mkdocs build --strict`;
- link checker automatico;
- CI GitHub Actions;
- test runtime di dashboard, telemetry, command, safety o analytics;
- proof of concept PixInsight;
- export reale di process history o metadata XISF;
- sincronizzazione con storage esterno o catalogo GitHub;
- proof of concept knowledge graph, semantic index, vector search o RAG.

## 10. Decisione

AMP-002 è approvato come fonte autorevole della roadmap di programma successiva ad AP-006. AP-013 e AP-014 includono formalmente la gestione del repository scientifico separato e la processing provenance PixInsight automatizzabile. AP-015 introduce la Scientific Knowledge Layer come livello semantico trasversale per ricerca, analytics e AI read-only. Ogni Architecture Package resta soggetto a produzione specialistica, validazione e review ARB indipendente.