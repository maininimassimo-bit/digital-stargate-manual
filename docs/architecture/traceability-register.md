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
| CAP-01 Analytics pipeline | Implemented, con limiti | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Fondazione esistente |
| CAP-02 Historical Analytics Dashboard | Implemented, continuità non certificata | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Evoluzione DSAP |
| CAP-03 Data Warehouse | Implemented, consumer incompleto | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-004 / ARB-006 | Evidence runtime da completare |
| CAP-04 Warehouse metadata and validation | Implemented, release non certificata | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-004 / ARB-006 | Evidence runtime da completare |
| CAP-08 Live telemetry | Planned | PAA-002 / AP-004 / AP-008 | reference architectures | ARB-006; nessuna review AP-008 | protocollo e pilot richiesti |
| CAP-15 AllSky integration | Planned | PAA-002 / AP-008 | adapter candidate | nessuna review AP-008 | contratti e health richiesti |
| CAP-16 Observatory Automation | Partial | AP-003 / AP-009 / AP-010 | target architecture | ARB-005 / ARB-009 / ARB-010 | runtime non autorizzato |
| CAP-17 Local safety interlocks | Partial | AP-003 / AP-010 | SAF-REF-001 / SAF-CAT-001 | ARB-010 | authority preservata; evidence aperta |
| CAP-18 AI boundary contracts | Prepared | PAA-002 / AP-008 / AP-010 | integration e safety boundary | ARB-010; nessuna review AP-008 | AI advisory only |
| CAP-19 AI Assistant | Planned | PAA-002 / AP-010 | feature futura | ARB-010 | read-only first |
| CAP-31 Architecture Governance | Partial | AP-001 | metamodel e registro | ARB-003…ARB-010 | condizioni aperte |
| CAP-32 Documentation Governance | Partial | AP-001 | MkDocs e standard | ARB-003…ARB-010 | automazione progressiva |
| CAP-33 Release Quality Governance | Partial | AP-001 | release note | ARB-003…ARB-010 | mapping incompleto |
| CAP-34 Enterprise Analytics Platform | Planned | AMP-002 / DSGP-VIS-001 / AP-009 / AP-010 | vision e guard rail | ARB-009 / ARB-010 | pianificazione AP-011 autorizzata; condizioni ereditate |
| CAP-35 Enterprise Operations Center | Planned | AMP-002 / DSGP-VIS-001 / AP-010 | command e safety boundary | ARB-010 | read-only first |
| CAP-36 Digital StarGate Portal | Planned | AMP-002 / DSGP-VIS-001 / AP-010 | vision | ARB-010 | non Safety Authority |
| CAP-37 Scientific Image Repository | Planned | AMP-002 / SIR-VIS-001 / AP-009 | storage boundary | ARB-009 | storage technology aperta |
| CAP-38 Scientific Observation Catalog and Search | Planned | AMP-002 / SIR-VIS-001 / AP-008 | catalog e reconciliation pattern | nessuna review AP-014 | manifest richiesti |
| CAP-39 Scientific Processing Provenance | Planned | AMP-002 / SIR-VIS-001 | contratto proposto | nessuna review AP-013/AP-014 | run immutabili |
| CAP-40 Scientific Knowledge Layer | Planned | AMP-002 / SKL-VIS-001 / AP-010 | AI safety boundary | ARB-010 | claim e citation governati |

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
| AP-011 | Analytics Platform | DSGP-VIS-001 | Nessuna | Active planning; inherits ARB-009/010 conditions |
| AP-012 | Operations Center | DSGP-VIS-001 | Nessuna | Planned |
| AP-013 | Scientific Image Repository | SIR-VIS-001 | Nessuna | Planned |
| AP-014 | Scientific Catalog and Search | SIR-VIS-001 | Nessuna | Planned |
| AP-015 | Scientific Knowledge Platform | SKL-VIS-001 | Nessuna | Planned |

## 4. Architecture Artifact Register

| ID | Artefatto | Package | Stato | Evidence |
|---|---|---|---|---|
| OPS-REF-001 | Operations and Service Management Reference Architecture | AP-007 | Proposed for review | documentale |
| INT-REF-001 | Enterprise Integration Reference Architecture | AP-008 | Proposed for review | documentale |
| INT-CAT-001 | Integration Contract Catalog | AP-008 | Initial candidate catalog | nessun runtime test |
| INF-REF-001 | Enterprise Infrastructure Reference Architecture | AP-009 | Approved with conditions via ARB-009 | as-built/failover/restore evidence aperta |
| SAF-REF-001 | Enterprise Safety Reference Architecture | AP-010 | Approved with conditions via ARB-010 | scenario validation aperta |
| SAF-CAT-001 | Safety Hazard and State Catalog | AP-010 | Approved as initial governed catalog via ARB-010 | owner, risk ed evidence da completare |
| ARB-009 | Independent Review of AP-009 | AP-009 | Completed | 94/100; C01…C05 open |
| ARB-010 | Independent Review of AP-010 | AP-010 | Completed | 97/100; C01…C05 open |

## 5. Integration Adapter Candidates

| ID | Sistema | Stato | Evidence |
|---|---|---|---|
| ADP-NINA-001 | N.I.N.A. | Candidate | non implementato |
| ADP-PHD2-001 | PHD2 | Candidate | non implementato |
| ADP-CPWI-001 | CPWI | Candidate | non implementato |
| ADP-DOME-001 | Dome/PLC | Candidate | non implementato |
| ADP-WX-001 | Weather | Candidate | non implementato |
| ADP-ALLSKY-001 | AllSky | Candidate | non implementato |
| ADP-PIX-001 | PixInsight | Candidate | non implementato |
| ADP-STORAGE-001 | Storage | Candidate | non implementato |
| ADP-GH-001 | GitHub | Candidate | non implementato |

## 6. Data Product Candidate Register

| ID | Data product | Fonte | Stato |
|---|---|---|---|
| DP-001 | `sessions.parquet` | Warehouse schema | Candidate baseline |
| DP-002 | `targets.parquet` | Warehouse schema | Candidate baseline |
| DP-003 | `equipment.parquet` | Warehouse schema | Candidate baseline |
| DP-004 | `quality.parquet` | Warehouse schema | Candidate baseline |
| DP-005 | `weather.parquet` | Warehouse schema | Candidate baseline |
| DP-006 | Scientific Asset Manifest | SIR-VIS-001 / AP-013 | Planned candidate |
| DP-007 | Processing Run Manifest | SIR-VIS-001 / AP-013/AP-014 | Planned candidate |
| DP-008 | Workflow Definition | SIR-VIS-001 / AP-014 | Planned candidate |
| DP-009 | Knowledge Entity and Relation Projection | SKL-VIS-001 / AP-015 | Planned candidate |
| DP-010 | Scientific Claim and Citation Projection | SKL-VIS-001 / AP-015 | Planned candidate |

## 7. Governance chain

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

## 8. Open traceability gaps and ARB conditions

| ID | Gap / Condizione | Impatto | Trattamento |
|---|---|---|---|
| TR-G05 | build strict e link check non eseguiti | pubblicabilità non certificata | CI/workspace |
| TR-G06 | owner non tutti formalizzati | accountability incompleta | RACI e nomine |
| TR-G10 | inventario safety non certificato | automation non commissionabile | ARB-010-C01/C05 |
| TR-G12 | fault injection non provata | capability non promuovibili | ARB-010-C04 |
| TR-G15 | ADR-005/Capability 002 Proposed | safety policy non deliberata | remediation AP-010 |
| TR-G16 | command authorization incompleta | comandi non governabili | AP-005/AP-008/AP-010/AP-012 |
| TR-G19 | SLI/SLO/routing/escalation non deliberati | operations non certificabili | AP-007 pilot |
| TR-G24 | continuous operations evidence assente | live telemetry non promuovibile | operations evidence |
| TR-G38 | ownership KPI DSAP non definita | dashboard ambigua | AP-011 |
| TR-G39 | live/freshness non collaudati | stato remoto ingannevole | contract test |
| TR-G40 | BFF e command path non implementati | rischio UI-to-device | AP-008/AP-012 |
| TR-G42 | storage scientifico e URI non deliberati | link fragili | ARB-009-C05 / AP-013 |
| TR-G58 | Operational Readiness Review non eseguita | attivazioni non governate | AP-007/AP-009 |
| TR-G69 / ARB-009-C01 | inventario as-built non verificato | fault domain non dimostrati | infrastructure inventory |
| TR-G70 / ARB-009-C03 | failover/failback Starlink-LTE non testati | continuità WAN ignota | recovery validation |
| TR-G71 / ARB-009-C05 | RTO/RPO/retention non approvati | recovery non governato | BIA e capacity model |
| TR-G72 / ARB-009-C03 | backup restore non provato | recuperabilità non dimostrata | restore drill |
| TR-G73 / ARB-009-C05 | capacity baseline assente | saturation non prevedibile | measurement e threshold |
| ARB-009-C02 | network/power as-built assente | segmentazione e fault domain non verificati | diagrammi e configuration check |
| ARB-009-C04 | configuration baseline incompleta | drift e rollback non governati | collegamento AP-006 |
| TR-G74 / ARB-010-C01 | hazard owner e residual risk non assegnati | safety accountability incompleta | formal hazard register |
| TR-G75 / ARB-010-C02 | soglie meteo/collision envelope non validate | protezioni non dimostrate | safety validation plan |
| TR-G76 / ARB-010-C04 | scenari emergency/recovery non eseguiti | safe-state behavior ignoto | failure injection ed exercise |
| TR-G77 / ARB-010-C02/C04 | override manuale non collaudato | bypass persistente possibile | scenario validation |
| ARB-010-C03 | Safety Requirements Traceability Matrix assente | requirement orfani possibili | matrice hazard-control-test |
| ARB-010-C05 | Safety Evidence Annex assente | controlli non verificabili | annex governato |
| TR-G78 | Safety Readiness Review runtime non eseguita | safety non certificata | review per capability |

## 9. Validazione del registro

Il registro verifica la presenza repository di ARB-009 e ARB-010 e registra AP-009 e AP-010 come `Approved with conditions`. Non certifica topologia as-built, failover WAN, UPS, backup/restore, hazard controls, interlock, soglie o emergency transition. AP-011 può iniziare come pianificazione architetturale, ereditando integralmente i vincoli e le condizioni aperte di ARB-009 e ARB-010.