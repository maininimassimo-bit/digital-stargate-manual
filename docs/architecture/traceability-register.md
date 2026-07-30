# Digital StarGate Architecture Traceability Register

| Campo | Valore |
|---|---|
| Documento | Architecture Traceability Register |
| Package | AP-001 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Stato | Active baseline — conditions open |
| Data | 30/07/2026 |
| Roadmap autorevole | AMP-002 per i package successivi ad AP-006 |

## 1. Regole

- Il registro collega capability, package, decisioni, evidenze, review e release.
- Le righe descrivono esclusivamente artefatti verificati nel repository.
- L'assenza di una review o release è indicata esplicitamente.
- Uno stato capability non viene promosso da questo registro.
- I locator di evidenza devono diventare puntuali quando usati per certificazione.
- Gli identificatori esistenti non vengono rinumerati retroattivamente.
- Una workflow definition versionata non costituisce prova di una Processing Run eseguita.
- Una knowledge projection o inferenza AI non costituisce una fonte autorevole senza provenance e citation locator.

## 2. Baseline certificata e capability pianificate

| Capability / Scope | Stato verificato | Fonte autorevole | Evidence / Implementation | Review / Certificate | Disposizione |
|---|---|---|---|---|---|
| CAP-01 Analytics pipeline | Implemented, con limiti dichiarati | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Fondazione esistente; non ricostruire greenfield |
| CAP-02 Historical Analytics Dashboard | Implemented, operatività continua non certificata | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Evoluzione controllata e futura integrazione DSAP |
| CAP-03 Data Warehouse | Implemented, consumer layer incompleto | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 / ARB-004 / ARB-006 | AP-002 governa data product; condizioni operative aperte |
| CAP-04 Warehouse metadata and validation | Implemented, release certification assente | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 / ARB-004 / ARB-006 | Quality e observability definite; evidence runtime da completare |
| CAP-08 Live telemetry | Planned | PAA-002 v1.1 | AP-004 e reference architecture | ARB-002 / ABC-001 / ARB-006 | Nessuna promozione senza pilot e OPS |
| CAP-15 AllSky integration | Planned | PAA-002 v1.1 | `future.allsky: false` | ARB-002 / ABC-001 | Richiede contratti e health |
| CAP-16 Observatory Automation | Partial | PAA-002 v1.1 | AP-003 e documentazione operativa | ARB-005…ARB-008 | Nessun runtime automatico autorizzato |
| CAP-17 Local safety interlocks | Partial | PAA-002 v1.1 | Evidenza documentale | ARB-005…ARB-008 | Autorità locale preservata |
| CAP-18 AI boundary contracts | Prepared | PAA-002 v1.1 | contratti AI presenti | ARB-004 / ARB-006 / ARB-007 | Nessun privilegio implicito |
| CAP-19 AI Assistant | Planned | PAA-002 v1.1 | `future.ai_assistant: false` | ARB-002 / ABC-001 | Read-only first |
| CAP-31 Architecture Governance | Partial | PAA-002 v1.1 | AP-001, metamodel e registro | ARB-003…ARB-008 | Condizioni aperte |
| CAP-32 Documentation Governance | Partial | PAA-002 v1.1 | MkDocs, package e standard | ARB-003…ARB-008 | Standardizzare e automatizzare |
| CAP-33 Release Quality Governance | Partial | PAA-002 v1.1 | processi e release note | ARB-003…ARB-008 | Release mapping incompleto |
| CAP-34 Enterprise Analytics Platform | Planned | AMP-002 / DSGP-VIS-001 | Nessuna implementazione certificata | Nessuna review AP-011 | Governare DSAP senza pipeline parallele |
| CAP-35 Enterprise Operations Center | Planned | AMP-002 / DSGP-VIS-001 | Nessuna implementazione certificata | Nessuna review AP-012 | DSOC read-only first |
| CAP-36 Digital StarGate Portal | Planned | AMP-002 / DSGP-VIS-001 | Vision documentale | Nessuna review AP-011/AP-012 | Presentation boundary; non safety authority |
| CAP-37 Scientific Image Repository | Planned | AMP-002 / SIR-VIS-001 | Vision documentale | Nessuna review AP-013 | RAW e derivati su storage esterno |
| CAP-38 Scientific Observation Catalog and Search | Planned | AMP-002 / SIR-VIS-001 | Vision documentale | Nessuna review AP-014 | GitHub conserva catalogo, manifest e link |
| CAP-39 Scientific Processing Provenance | Planned | AMP-002 / SIR-VIS-001 | Contratto minimo proposto | Nessuna review AP-013/AP-014 | Processing Run immutabili e workflow versionati |
| CAP-40 Scientific Knowledge Layer | Planned | AMP-002 / SKL-VIS-001 | Vision documentale | Nessuna review AP-015 | Entità, relazioni, claim, citation e projection governate |

## 3. Architecture Package Register

| Package | Scope | Capability interessate | Artefatti | Review | Stato |
|---|---|---|---|---|---|
| AP-001 | Enterprise Metamodel and Repository Information Architecture | CAP-31, CAP-32, CAP-33 | package, metamodel e registro | ARB-003 | Approved with conditions |
| AP-002 | Enterprise Data Governance | CAP-03, CAP-04 e consumer | package e standard | ARB-004 | Approved with conditions |
| AP-003 | Observatory Automation Architecture | CAP-16, CAP-17 | package e reference architecture | ARB-005 | Approved with conditions |
| AP-004 | Enterprise Telemetry and Observability Architecture | CAP-08 e trasversali | package e reference architecture | ARB-006 | Approved with conditions |
| AP-005 | Identity, Access and Remote Operations Security Architecture | trasversale | package e reference architecture | ARB-007 | Approved with conditions, 91/100 |
| AP-006 | Enterprise Configuration and Asset Management Architecture | trasversale | package e reference architecture | ARB-008 | Approved with conditions, 92/100 |
| AP-007 | Enterprise Operations and Service Management Architecture | operations, incident, problem, change, runbook e KPI | da produrre | Nessuna | Planned — next package |
| AP-008 | Enterprise Integration Architecture | API, eventi, adapter e contratti | da produrre | Nessuna | Planned |
| AP-009 | Enterprise Infrastructure Architecture | rete, compute, storage, backup e resilience | da produrre | Nessuna | Planned |
| AP-010 | Enterprise Safety Assurance Architecture | CAP-16, CAP-17 | da produrre | Nessuna | Planned |
| AP-011 | Enterprise Analytics Platform Architecture | CAP-02, CAP-03, CAP-04, CAP-34, CAP-36 | DSGP-VIS-001 | Nessuna | Planned |
| AP-012 | Enterprise Operations Center Architecture | CAP-08, CAP-15, CAP-16, CAP-17, CAP-35, CAP-36 | DSGP-VIS-001 | Nessuna | Planned |
| AP-013 | Scientific Image Repository Architecture | CAP-37, CAP-39 | SIR-VIS-001 | Nessuna | Planned |
| AP-014 | Scientific Observation Catalog and Search Architecture | CAP-38, CAP-39; supporta CAP-34 e CAP-36 | SIR-VIS-001 | Nessuna | Planned |
| AP-015 | Scientific Knowledge Platform Architecture | CAP-40; supporta CAP-34, CAP-36 e CAP-19 | SKL-VIS-001 | Nessuna | Planned |

## 4. Data Product Candidate Register

| ID | Data product | Fonte contrattuale verificata | Owner | Stato |
|---|---|---|---|---|
| DP-001 | `sessions.parquet` | Warehouse schema; locator eseguibile da verificare | proposto | Candidate baseline |
| DP-002 | `targets.parquet` | stessa fonte | proposto | Candidate baseline |
| DP-003 | `equipment.parquet` | stessa fonte | proposto | Candidate baseline |
| DP-004 | `quality.parquet` | stessa fonte | proposto | Candidate baseline |
| DP-005 | `weather.parquet` | stessa fonte | proposto | Candidate baseline |
| DP-006 | Scientific Asset Manifest | SIR-VIS-001; schema da produrre in AP-013 | proposto | Planned candidate |
| DP-007 | Processing Run Manifest | SIR-VIS-001; schema da produrre in AP-013/AP-014 | proposto | Planned candidate |
| DP-008 | Workflow Definition | SIR-VIS-001; schema da produrre in AP-014 | proposto | Planned candidate |
| DP-009 | Knowledge Entity and Relation Projection | SKL-VIS-001; schema da produrre in AP-015 | proposto | Planned candidate |
| DP-010 | Scientific Claim and Citation Projection | SKL-VIS-001; schema da produrre in AP-015 | proposto | Planned candidate |

Gli ID DP-001…DP-010 non costituiscono certificazione finché owner, grain, schema locator, consumer, quality, retention e lineage non sono verificati.

## 5. Assessment and governance chain

| Artefatto | Ruolo | Input | Output / Decision | Stato |
|---|---|---|---|---|
| PAA-002 v1.1 | Capability gap assessment | baseline repository | capability matrix, gap e dipendenze | Reviewed |
| ARB-002 | Independent review | PAA-002 v1.1 | Approved with conditions, 90/100 | Completed |
| ABC-001 | Baseline certificate | PAA-002 e ARB-002 | Conditionally certified | Completed |
| AMP-001 | Historical Architecture Master Plan | ABC-001 | baseline iniziale; roadmap futura superata | Superseded in roadmap sections |
| AMP-002 | Architecture Program Roadmap Realignment | AP-001…AP-006 | Roadmap AP-007…AP-015 e CAP-34…CAP-40 | Approved for planning |
| DSGP-VIS-001 | Digital Platforms vision | AMP-002 | Vision DSGP, DSAP e DSOC | Planned architecture vision |
| SIR-VIS-001 | Scientific image and processing provenance vision | AMP-002 | Vision asset lifecycle, catalogo e PixInsight sync | Approved for architecture planning |
| SKL-VIS-001 | Scientific Knowledge Layer vision | AMP-002, SIR-VIS-001, metamodel | Vision semantic layer, claims e citations | Approved for architecture planning |
| AP-001 / ARB-003 | Metamodel and repository IA | governance baseline | Approved with conditions, 86/100 | Completed |
| AP-002 / ARB-004 | Enterprise Data Governance | Warehouse baseline | Approved with conditions, 88/100 | Completed |
| AP-003 / ARB-005 | Observatory Automation | safety e operations docs | Approved with conditions, 89/100 | Completed |
| AP-004 / ARB-006 | Telemetry and Observability | AP-002/AP-003 | Approved with conditions, 90/100 | Completed |
| AP-005 / ARB-007 | Identity and Remote Security | AP-002…AP-004 | Approved with conditions, 91/100 | Completed |
| AP-006 / ARB-008 | Configuration and Asset Management | AP-001…AP-005 | Approved with conditions, 92/100 | Completed |

## 6. Open traceability gaps

| ID | Gap | Impatto | Trattamento |
|---|---|---|---|
| TR-G01 | AMP-001 non coerente con i package realizzati | numerazione futura ambigua | AMP-002 e review indipendente |
| TR-G02 | Release-package mapping non sistematico | scope release difficile da certificare | aggiornamento release note |
| TR-G05 | Build strict e link check non eseguiti | pubblicabilità non certificata | CI o workspace |
| TR-G06 | Owner AP-001…AP-006 non formalmente assegnati | governance non operativa | RACI |
| TR-G07 | Schema DP-001…DP-005 non collegati | data product non certificabili | locator immutabili |
| TR-G08 | Retention non deliberate | lifecycle incompleto | decisione per data product e signal |
| TR-G09 | Lineage Analytics → Warehouse → consumer incompleto | riproducibilità limitata | Evidence Annex AP-002 |
| TR-G10 | Inventario sensori/controller/interlock non certificato | AP-003 non commissionabile | inventory e owner |
| TR-G12 | Fault injection e isolamento non provati | CAP-16/17 non promuovibili | validation matrix |
| TR-G13 | Condizioni ARB-004 aperte | data product non certificabili | remediation AP-002 |
| TR-G15 | ADR-005 e Capability 002 restano Proposed | safety policy non deliberata | AP-010 |
| TR-G16 | Command authorization e audit contract assenti | comandi non governabili | AP-005/AP-012 |
| TR-G19 | SLI, SLO, routing ed escalation non deliberati | operations non certificabili | AP-007/AP-012 |
| TR-G24 | Continuous operations evidence assente | CAP-08 non promuovibile | OPS evidence |
| TR-G38 | Ownership KPI DSAP non definita | dashboard ambigua | AP-011 |
| TR-G39 | Protocollo live e freshness UI non deliberati | DSOC può mostrare stato ingannevole | AP-008/AP-012 |
| TR-G40 | BFF e command path non definiti | rischio UI-to-device | AP-008/AP-012 |
| TR-G41 | Degraded-mode UX non validata | portale non operabile in emergenza | AP-012 |
| TR-G42 | Storage scientifico, URI scheme e asset identity non deliberati | link fragili | AP-009/AP-013 |
| TR-G43 | Schema Processing Run e Workflow Definition assenti | storico PixInsight non confrontabile | AP-013/AP-014 |
| TR-G44 | Export process history PixInsight non provato | automazione potenzialmente incompleta | PoC con fallback manuale |
| TR-G45 | Checksum, idempotenza e reconciliation sync non testati | catalogo e storage divergenti | AP-008/AP-014 |
| TR-G46 | Credenziali script/adapter non definite | esposizione token | AP-005/AP-008 |
| TR-G47 | Versioni PixInsight, moduli e script non baselined | processing non riproducibile | AP-006/AP-013 |
| TR-G48 | Provenance step manuali non standardizzata | storia incompleta | schema con `manual` e `unknown` |
| TR-G49 | Vocabolario scientifico e ownership non definiti | entità e relazioni incoerenti | AP-015 semantic governance |
| TR-G50 | Regole di conflitto tra fonti assenti | claim contraddittori o fuorvianti | AP-015 conflict model |
| TR-G51 | Citation locator e confidence model non definiti | risultati non verificabili | AP-015 contract e validation |
| TR-G52 | Tecnologia graph/vector non valutata su query e volumi reali | lock-in o complessità prematura | PoC comparativo dopo AP-014 |
| TR-G53 | Governance delle inferenze AI non definita | inferenze trattate come fatti | AP-015/AP-019 read-only policy |
| TR-G54 | Reconciliation della knowledge projection non testata | indice semantico stale | AP-008/AP-015 validation matrix |

## 7. Validazione del registro

Il registro copre la governance AP-001…AP-006, le review ARB-003…ARB-008, il riallineamento AMP-002 e le capability pianificate CAP-34…CAP-40. Non certifica implementazione, storage esterno, sincronizzazione PixInsight, knowledge graph, semantic index, vector search, RAG o operatività del catalogo e della SKL.