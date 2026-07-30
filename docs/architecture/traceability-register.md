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
- L'assenza di review, test o release è indicata esplicitamente.
- `Approved with conditions` chiude il gate architetturale documentale ma non certifica runtime o chiusura delle condizioni.
- Una definizione architetturale non prova il comportamento runtime.
- Nessuna inferenza AI costituisce fonte autorevole senza provenance e citation.

## 2. Baseline e capability

| Capability / Scope | Stato verificato | Fonte autorevole | Evidence / Implementation | Review / Certificate | Disposizione |
|---|---|---|---|---|---|
| CAP-01 Analytics pipeline | Implemented, con limiti | PAA-002 v1.1 / AP-011 | ABC-001 Evidence Annex; ANA-PIPE-001 target | ARB-002 / ABC-001 / ARB-011 | Migrazione DSAP e nuove evidence; C03-C05 aperte |
| CAP-02 Historical Analytics Dashboard | Implemented, continuità non certificata | PAA-002 v1.1 / AP-011 | dashboard esistente; ANA-KPI-001 target | ARB-002 / ARB-011 | Migrazione al semantic layer; C02/C07 aperte |
| CAP-03 Data Warehouse | Implemented, consumer incompleto | PAA-002 v1.1 / AP-002 / AP-011 | warehouse baseline | ARB-004 / ARB-006 / ARB-011 | Recovery, lineage e serving evidence aperte |
| CAP-04 Warehouse metadata and validation | Implemented, release non certificata | PAA-002 v1.1 / AP-011 | ANA-PIPE-001 quality model | ARB-004 / ARB-006 / ARB-011 | Quality suite da provare |
| CAP-08 Live telemetry | Planned | AP-004 / AP-008 / AP-011 / AP-012 | reference architectures | ARB-006 / ARB-011; nessuna review AP-008/AP-012 | Protocollo, freshness e pilot richiesti |
| CAP-15 AllSky integration | Planned | AP-008 / AP-011 / AP-012 | adapter candidate e ingestion target | ARB-011; nessuna review AP-008/AP-012 | Contratti e health richiesti |
| CAP-16 Observatory Automation | Partial | AP-003 / AP-009 / AP-010 / AP-012 | target architecture e DSOC command boundary | ARB-005 / ARB-009 / ARB-010 | Runtime command enablement non autorizzato |
| CAP-17 Local safety interlocks | Partial | AP-003 / AP-010 / AP-012 | SAF-REF-001 / SAF-CAT-001 / OPSC-REF-001 | ARB-010 | Authority preservata; evidence aperta |
| CAP-18 AI boundary contracts | Prepared | AP-008 / AP-010 / AP-011 / AP-012 | integration, safety, analytics e command boundary | ARB-010 / ARB-011; nessuna review AP-008/AP-012 | AI advisory only |
| CAP-19 AI Assistant | Planned | AP-010 / AP-011 / AP-012 | ANA-GOV-001 / OPSC-CMD-001 | ARB-010 / ARB-011 | Nessun ruolo autorizzativo o command path |
| CAP-31 Architecture Governance | Partial | AP-001 | metamodel e registro | ARB-003…ARB-011 | Condizioni aperte |
| CAP-32 Documentation Governance | Partial | AP-001 | MkDocs e standard | ARB-003…ARB-011 | Automazione progressiva |
| CAP-33 Release Quality Governance | Partial | AP-001 | release note | ARB-003…ARB-011 | Mapping incompleto |
| CAP-34 Enterprise Analytics Platform | Approved with conditions | AP-011 / ANA-REF-001 / ANA-PIPE-001 / ANA-KPI-001 / ANA-GOV-001 | package e reference artifacts | ARB-011, 97/100 | Gate documentale chiuso; C01…C07 aperte |
| CAP-35 Enterprise Operations Center | In development — Sprint AP-012.2 document baseline complete | AP-012 / OPSC-REF-001 / OPSC-CMD-001 / OPSC-ALM-001 / OPSC-RUN-001 / OPSC-RACI-001 | package, reference architecture, authorization, alarm/incident, runbook e responsibility governance | Nessuna review AP-012 | validation evidence e ARB-012 richiesti; runtime non autorizzato |
| CAP-36 Digital StarGate Portal | Planned | DSGP-VIS-001 / AP-011 / AP-012 | semantic serving e operator-console boundary | ARB-011; nessuna review AP-012 | Non Safety Authority |
| CAP-37 Scientific Image Repository | Planned | SIR-VIS-001 / AP-009 | storage boundary | ARB-009 | Storage technology aperta |
| CAP-38 Scientific Observation Catalog and Search | Planned | SIR-VIS-001 / AP-008 / AP-011 | catalog e semantic boundary | ARB-011; nessuna review AP-014 | Manifest richiesti |
| CAP-39 Scientific Processing Provenance | Planned | SIR-VIS-001 / AP-011 | lineage e reproducibility rules | ARB-011; nessuna review AP-013/AP-014 | Run immutabili |
| CAP-40 Scientific Knowledge Layer | Planned | SKL-VIS-001 / AP-010 / AP-011 | AI governance boundary | ARB-010 / ARB-011 | Claim e citation governati |

## 3. Architecture Package Register

| Package | Scope | Artefatti | Review | Stato |
|---|---|---|---|---|
| AP-001 | Metamodel e repository IA | package, metamodel, registro | ARB-003 | Approved with conditions |
| AP-002 | Data Governance | package e standard | ARB-004 | Approved with conditions |
| AP-003 | Observatory Automation | package e reference architecture | ARB-005 | Approved with conditions |
| AP-004 | Telemetry and Observability | package e reference architecture | ARB-006 | Approved with conditions |
| AP-005 | Identity and Remote Security | package e reference architecture | ARB-007 | Approved with conditions, 91/100 |
| AP-006 | Configuration and Asset Management | package e reference architecture | ARB-008 | Approved with conditions, 92/100 |
| AP-007 | Operations and Service Management | AP-007, OPS-REF-001 | Nessuna registrata | Proposed for independent ARB review |
| AP-008 | Enterprise Integration | AP-008, INT-REF-001, INT-CAT-001 | Nessuna registrata | Proposed for independent ARB review |
| AP-009 | Enterprise Infrastructure | AP-009, INF-REF-001 | ARB-009 | Approved with conditions, 94/100 |
| AP-010 | Enterprise Safety Assurance | AP-010, SAF-REF-001, SAF-CAT-001 | ARB-010 | Approved with conditions, 97/100 |
| AP-011 | Analytics Platform | AP-011, ANA-REF-001, ANA-PIPE-001, ANA-KPI-001, ANA-GOV-001 | ARB-011 | Approved with conditions, 97/100 |
| AP-012 | Operations Center | AP-012, OPSC-REF-001, OPSC-CMD-001, OPSC-ALM-001, OPSC-RUN-001, OPSC-RACI-001 | Nessuna | In development — Sprint AP-012.2 document baseline complete; runtime not authorized |
| AP-013 | Scientific Image Repository | SIR-VIS-001 | Nessuna | Planned |
| AP-014 | Scientific Catalog and Search | SIR-VIS-001 | Nessuna | Planned |
| AP-015 | Scientific Knowledge Platform | SKL-VIS-001 | Nessuna | Planned |

## 4. Architecture Artifact Register

| ID | Artefatto | Package | Stato | Evidence |
|---|---|---|---|---|
| OPS-REF-001 | Operations and Service Management Reference Architecture | AP-007 | Proposed for review | documentale |
| INT-REF-001 | Enterprise Integration Reference Architecture | AP-008 | Proposed for review | documentale |
| INT-CAT-001 | Integration Contract Catalog | AP-008 | Initial candidate catalog | nessun runtime test |
| INF-REF-001 | Enterprise Infrastructure Reference Architecture | AP-009 | Approved with conditions via ARB-009 | evidence operativa aperta |
| SAF-REF-001 | Enterprise Safety Reference Architecture | AP-010 | Approved with conditions via ARB-010 | scenario validation aperta |
| SAF-CAT-001 | Safety Hazard and State Catalog | AP-010 | Initial governed catalog | owner, risk ed evidence da completare |
| ARB-009 | Independent Review of AP-009 | AP-009 | Completed | 94/100; C01…C05 open |
| ARB-010 | Independent Review of AP-010 | AP-010 | Completed | 97/100; C01…C05 open |
| ANA-REF-001 | Enterprise Analytics Reference Architecture | AP-011 | Approved with conditions via ARB-011 | runtime non certificato |
| ANA-PIPE-001 | Analytics Data Pipeline Reference | AP-011 | Approved with conditions via ARB-011 | quality/replay/recovery test non eseguiti |
| ANA-KPI-001 | Analytics KPI Catalog | AP-011 | Approved as initial governed catalog via ARB-011 | owner, formule e soglie da approvare |
| ANA-GOV-001 | Analytics Governance Standard | AP-011 | Approved with conditions via ARB-011 | role assignment ed evidence aperte |
| ARB-011 | Independent Review of AP-011 | AP-011 | Completed | 97/100; C01…C07 open |
| OPSC-REF-001 | Enterprise Operations Center Reference Architecture | AP-012 | Draft baseline — Sprint AP-012.1 | documentale; runtime validation non eseguita |
| OPSC-CMD-001 | Command Authorization Model | AP-012 | Draft baseline — Sprint AP-012.1 | policy, role, freshness, safety e idempotency test non eseguiti |
| OPSC-ALM-001 | Alarm & Incident Model | AP-012 | Draft baseline — Sprint AP-012.2 | taxonomy, lifecycle, correlation, escalation e audit definiti; runtime non validato |
| OPSC-RUN-001 | Operational Runbook Standard | AP-012 | Draft baseline — Sprint AP-012.2 | metamodel, safety checkpoint, rollback, recovery e versioning definiti; drill non eseguiti |
| OPSC-RACI-001 | Operations Responsibility Matrix | AP-012 | Draft baseline — Sprint AP-012.2 | ruoli, authority chain, RACI e segregation definiti; nomine aperte |

## 5. Data Product Candidate Register

| ID | Data product | Fonte | Stato |
|---|---|---|---|
| DP-001 | `sessions.parquet` | Warehouse schema / AP-011 | Candidate baseline; ARB-011-C01 open |
| DP-002 | `targets.parquet` | Warehouse schema / AP-011 | Candidate baseline; ARB-011-C01 open |
| DP-003 | `equipment.parquet` | Warehouse schema / AP-011 | Candidate baseline; ARB-011-C01 open |
| DP-004 | `quality.parquet` | Warehouse schema / AP-011 | Candidate baseline; ARB-011-C01 open |
| DP-005 | `weather.parquet` | Warehouse schema / AP-011 | Candidate baseline; ARB-011-C01 open |
| DP-006 | Scientific Asset Manifest | SIR-VIS-001 / AP-013 | Planned candidate |
| DP-007 | Processing Run Manifest | SIR-VIS-001 / AP-013/AP-014 | Planned candidate |
| DP-008 | Workflow Definition | SIR-VIS-001 / AP-014 | Planned candidate |
| DP-009 | Knowledge Entity and Relation Projection | SKL-VIS-001 / AP-015 | Planned candidate |
| DP-010 | Scientific Claim and Citation Projection | SKL-VIS-001 / AP-015 | Planned candidate |

## 6. Governance chain

| Artefatto | Ruolo | Stato |
|---|---|---|
| PAA-002 v1.1 | Capability gap assessment | Reviewed |
| ARB-002 | Independent review PAA-002 | Completed, 90/100 |
| ABC-001 | Baseline certificate | Conditionally certified |
| AMP-002 | Roadmap AP-007…AP-015 | Approved for planning |
| AP-001…AP-006 / ARB-003…ARB-008 | Foundation packages | Approved with conditions |
| AP-007 / OPS-REF-001 | Operations | Proposed for independent ARB review |
| AP-008 / INT-REF-001 / INT-CAT-001 | Integration | Proposed for independent ARB review |
| AP-009 / INF-REF-001 / ARB-009 | Infrastructure | Approved with conditions; C01…C05 open |
| AP-010 / SAF-REF-001 / SAF-CAT-001 / ARB-010 | Safety assurance | Approved with conditions; C01…C05 open |
| AP-011 / ANA-REF-001 / ANA-PIPE-001 / ANA-KPI-001 / ANA-GOV-001 / ARB-011 | Enterprise Analytics Platform | Approved with conditions; C01…C07 open |
| AP-012 / OPSC-REF-001 / OPSC-CMD-001 / OPSC-ALM-001 / OPSC-RUN-001 / OPSC-RACI-001 | Enterprise Operations Center | Sprint AP-012.1 e AP-012.2 completati a livello documentale; validation e ARB-012 aperti |

## 7. Open traceability gaps and conditions

| ID | Gap / Condizione | Impatto | Trattamento |
|---|---|---|---|
| TR-G05 | build strict e link check non eseguiti | pubblicabilità non certificata | CI/workspace |
| TR-G06 | owner non tutti formalizzati | accountability incompleta | OPSC-RACI-001 e nomine |
| TR-G10 | inventario safety non certificato | automation non commissionabile | ARB-010-C01/C05 |
| TR-G12 | fault injection non provata | capability non promuovibili | ARB-010-C04 |
| TR-G16 | command authorization non validata runtime | comandi non abilitabili | OPSC-CMD-001 test ed ARB-012 |
| TR-G19 | SLI/SLO/routing/escalation non deliberati | operations non certificabili | AP-007 pilot e AP-012 validation |
| TR-G38 / ARB-011-C02 | ownership KPI DSAP non definita | dashboard ambigua | ANA-KPI-001 owner assignment |
| TR-G79 / ARB-011-C01 | data product owner DP-001…DP-005 non nominati | qualità e lifecycle non attribuibili | enterprise data catalog |
| TR-G80 / ARB-011-C03 | quality gate suite non eseguita | dati errati pubblicabili | ANA-PIPE-001 validation |
| TR-G81 / ARB-011-C04 | lineage source-to-KPI non verificato | risultati non riproducibili | lineage test |
| TR-G82 / ARB-011-C03/C04 | freshness/stale/unknown non collaudati | dashboard ingannevoli | serving contract test |
| TR-G83 / ARB-011-C05 | analytics recovery e reprocessing non provati | storico non recuperabile | AP-009/AP-011 restore test |
| TR-G84 / ARB-011-C02/C07 | semantic definitions e KPI formule non approvate | metriche incoerenti | KPI e semantic governance |
| TR-G85 / ARB-011-C06 | volume, latency e capacity baseline assenti | saturation non prevedibile | AP-009/AP-011 measurement |
| TR-G86 | model governance owner non nominato | AI non governata | ANA-GOV-001 |
| TR-G87 | isolamento read-only/no-command non testato | rischio di bypass operativo | OPSC-REF-001 architecture and access test |
| TR-G88 | alarm, runbook e RACI specialistici AP-012 | baseline documentale completata, efficacia non provata | OPSC-ALM-001, OPSC-RUN-001, OPSC-RACI-001; validation e ARB-012 |
| TR-G89 | idempotency, expiry e safety denial non provati | esecuzione duplicata o non governata | OPSC-CMD-001 validation scenarios |
| TR-G90 | degraded, recovery ed emergency drill non eseguiti | comportamento in failure non certificato | OPSC-RUN-001 validation campaign |
| TR-G91 | alarm correlation, suppression ed escalation non collaudate | missed alarm o alarm noise | OPSC-ALM-001 scenario validation |
| TR-G92 | ruoli nominativi, deleghe e four-eyes non attivati | responsabilità non operative | OPSC-RACI-001 assignment e access review |
| ARB-009-C01…C05 | infrastructure evidence aperta | runtime resilience non certificata | remediation AP-009 |
| ARB-010-C01…C05 | safety evidence aperta | runtime safety non certificata | remediation AP-010 |
| ARB-011-C01…C07 | analytics evidence aperta | runtime analytics non certificato | remediation AP-011 |

## 8. Validazione del registro

Il registro verifica la presenza repository degli artefatti AP-012 Sprint 1 e Sprint 2. AP-012 resta `In development`: non sono certificati command authorization, alarm handling, safety enforcement, idempotency, role assignment, degraded mode, recovery o disponibilità runtime. La review indipendente ARB-012 e la successiva campagna di validazione restano necessarie prima di qualsiasi avanzamento del gate.
