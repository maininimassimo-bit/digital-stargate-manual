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

## 2. Baseline certificata e capability pianificate

| Capability / Scope | Stato verificato | Fonte autorevole | Evidence / Implementation | Review / Certificate | Disposizione |
|---|---|---|---|---|---|
| CAP-01 Analytics pipeline | Implemented, con limiti dichiarati | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Fondazione esistente; non ricostruire greenfield |
| CAP-02 Historical Analytics Dashboard | Implemented, operatività continua non certificata | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Evoluzione controllata e futura integrazione DSAP |
| CAP-03 Data Warehouse | Implemented, consumer layer incompleto | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 / ARB-004 / ARB-006 | AP-002 governa data product; AP-004 abilita evidence, condizioni operative aperte |
| CAP-04 Warehouse metadata and validation | Implemented, release certification assente | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 / ARB-004 / ARB-006 | Quality e observability definite; evidence runtime da completare |
| CAP-08 Live telemetry | Planned | PAA-002 v1.1 | AP-004 e Enterprise Observability Reference Architecture; nessun runtime verificato | ARB-002 / ABC-001 / ARB-006 | Nessuna promozione senza pilot e operations evidence |
| CAP-15 AllSky integration | Planned | PAA-002 v1.1 | `future.allsky: false` | ARB-002 / ABC-001 | Richiede contratti e health |
| CAP-16 Observatory Automation | Partial | PAA-002 v1.1 | Procedura di chiusura, ADR-005, Capability 002 e AP-003 | ARB-002 / ABC-001 / ARB-005…ARB-008 | Nessun runtime automatico autorizzato |
| CAP-17 Local safety interlocks | Partial | PAA-002 v1.1 | Evidenza documentale; hardware e fault test non inclusi | ARB-002 / ABC-001 / ARB-005…ARB-008 | Autorità locale preservata |
| CAP-18 AI boundary contracts | Prepared | PAA-002 v1.1 | `src/DigitalStarGate.Contracts/Ai/AiContracts.cs` | ARB-002 / ABC-001 / ARB-004 / ARB-006 / ARB-007 | AI usa dati governati; nessun privilegio implicito |
| CAP-19 AI Assistant | Planned | PAA-002 v1.1 | `future.ai_assistant: false` | ARB-002 / ABC-001 | Read-only first |
| CAP-31 Architecture Governance | Partial | PAA-002 v1.1 | AP-001, metamodel e registro | ARB-003…ARB-008 | Condizioni e automazione aperte |
| CAP-32 Documentation Governance | Partial | PAA-002 v1.1 | MkDocs, package e standard | ARB-003…ARB-008 | Standardizzare e automatizzare |
| CAP-33 Release Quality Governance | Partial | PAA-002 v1.1 | Processi e release note distribuiti | ARB-003…ARB-008 | Release mapping incompleto |
| CAP-34 Enterprise Analytics Platform | Planned | AMP-002 / DSGP-VIS-001 | Nessuna implementazione certificata | Nessuna review AP-011 | Governare DSAP senza pipeline parallele |
| CAP-35 Enterprise Operations Center | Planned | AMP-002 / DSGP-VIS-001 | Nessuna implementazione certificata | Nessuna review AP-012 | DSOC read-only first |
| CAP-36 Digital StarGate Portal | Planned | AMP-002 / DSGP-VIS-001 | Vision documentale | Nessuna review AP-011/AP-012 | Presentation boundary; non safety authority |
| CAP-37 Scientific Image Repository | Planned | AMP-002 / SIR-VIS-001 | Nessuna implementazione certificata | Nessuna review AP-013 | RAW e derivati su storage esterno, catalogati tramite asset ID, URI e checksum |
| CAP-38 Scientific Observation Catalog and Search | Planned | AMP-002 / SIR-VIS-001 | Nessuna implementazione certificata | Nessuna review AP-014 | GitHub come catalogo di metadati, manifest, link e workflow |
| CAP-39 Scientific Processing Provenance | Planned | AMP-002 / SIR-VIS-001 | Vision e contratto minimo proposto | Nessuna review AP-013/AP-014 | Processing Run immutabili, workflow versionati e sincronizzazione PixInsight governata |

## 3. Architecture Package Register

| Package | Scope | Capability interessate | Artefatti | Review | Stato |
|---|---|---|---|---|---|
| AP-001 | Enterprise Metamodel and Repository Information Architecture | CAP-31, CAP-32, CAP-33 | package, metamodel e registro | ARB-003 | Approved with conditions |
| AP-002 | Enterprise Data Governance | CAP-03, CAP-04 e consumer | package e data governance standard | ARB-004 | Approved with conditions |
| AP-003 | Observatory Automation Architecture | CAP-16, CAP-17 | package, reference architecture, ADR-005 | ARB-005 | Approved with conditions |
| AP-004 | Enterprise Telemetry and Observability Architecture | CAP-08 e trasversali | package e observability reference architecture | ARB-006 | Approved with conditions |
| AP-005 | Identity, Access and Remote Operations Security Architecture | trasversale | package e identity/trust reference architecture | ARB-007 | Approved with conditions, 91/100 |
| AP-006 | Enterprise Configuration and Asset Management Architecture | trasversale | package e configuration/asset reference architecture | ARB-008 | Approved with conditions, 92/100 |
| AP-007 | Enterprise Operations and Service Management Architecture | operations, incident, problem, change, runbook e KPI | da produrre | Nessuna | Planned — next package |
| AP-008 | Enterprise Integration Architecture | API, eventi, adapter e contratti | da produrre | Nessuna | Planned |
| AP-009 | Enterprise Infrastructure Architecture | rete, compute, storage, backup e resilience | da produrre | Nessuna | Planned |
| AP-010 | Enterprise Safety Assurance Architecture | CAP-16, CAP-17 | da produrre | Nessuna | Planned |
| AP-011 | Enterprise Analytics Platform Architecture | CAP-02, CAP-03, CAP-04, CAP-34, CAP-36 | da produrre; DSGP-VIS-001 | Nessuna | Planned |
| AP-012 | Enterprise Operations Center Architecture | CAP-08, CAP-15, CAP-16, CAP-17, CAP-35, CAP-36 | da produrre; DSGP-VIS-001 | Nessuna | Planned |
| AP-013 | Scientific Image Repository Architecture | CAP-37, CAP-39 | da produrre; SIR-VIS-001 | Nessuna | Planned |
| AP-014 | Scientific Observation Catalog and Search Architecture | CAP-38, CAP-39; supporta CAP-34 e CAP-36 | da produrre; SIR-VIS-001 | Nessuna | Planned |

## 4. Data Product Candidate Register

| ID | Data product | Fonte contrattuale verificata | Owner | Stato |
|---|---|---|---|---|
| DP-001 | `sessions.parquet` | `architecture/warehouse/datasets-and-schema.md`; schema eseguibile da localizzare | proposto | Candidate baseline |
| DP-002 | `targets.parquet` | stessa fonte | proposto | Candidate baseline |
| DP-003 | `equipment.parquet` | stessa fonte | proposto | Candidate baseline |
| DP-004 | `quality.parquet` | stessa fonte | proposto | Candidate baseline |
| DP-005 | `weather.parquet` | stessa fonte | proposto | Candidate baseline |
| DP-006 | Scientific Asset Manifest | SIR-VIS-001; schema da produrre in AP-013 | proposto | Planned candidate |
| DP-007 | Processing Run Manifest | SIR-VIS-001; schema da produrre in AP-013/AP-014 | proposto | Planned candidate |
| DP-008 | Workflow Definition | SIR-VIS-001; schema da produrre in AP-014 | proposto | Planned candidate |

Gli ID DP-001…DP-008 non costituiscono certificazione finché owner, grain, schema locator, consumer, quality, retention e lineage non sono verificati.

## 5. Assessment and governance chain

| Artefatto | Ruolo | Input | Output / Decision | Stato |
|---|---|---|---|---|
| PAA-002 v1.1 | Capability gap assessment | Baseline repository | Capability matrix, gap, dipendenze | Reviewed |
| ARB-002 | Independent review | PAA-002 v1.1 | Approved with conditions, 90/100 | Completed |
| ABC-001 | Baseline certificate | PAA-002, ARB-002, Evidence Annex | Conditionally certified | Completed |
| AMP-001 | Historical Architecture Master Plan | ABC-001 | Baseline iniziale; roadmap futura superata | Superseded in roadmap sections by AMP-002 |
| AMP-002 | Architecture Program Roadmap Realignment | AP-001…AP-006, ARB-003…ARB-008 | Roadmap AP-007…AP-014 e CAP-34…CAP-39 | Approved for planning |
| DSGP-VIS-001 | Digital Platforms vision | AMP-002, AP-002…AP-006 | Vision DSGP, DSAP e DSOC | Planned architecture vision |
| SIR-VIS-001 | Scientific image and processing provenance vision | AMP-002, riferimenti PixInsight e storage scientifico | Vision asset lifecycle, catalogo e PixInsight sync | Approved for architecture planning |
| AP-001 / ARB-003 | Metamodel and repository IA | baseline governance | Approved with conditions, 86/100 | Completed |
| AP-002 / ARB-004 | Enterprise Data Governance | AP-001 e Warehouse baseline | Approved with conditions, 88/100 | Completed |
| AP-003 / ARB-005 | Observatory Automation | safety e operations docs | Approved with conditions, 89/100 | Completed |
| AP-004 / ARB-006 | Telemetry and Observability | AP-002/AP-003 | Approved with conditions, 90/100 | Completed |
| AP-005 / ARB-007 | Identity and Remote Security | AP-002…AP-004 | Approved with conditions, 91/100 | Completed |
| AP-006 / ARB-008 | Configuration and Asset Management | AP-001…AP-005 | Approved with conditions, 92/100 | Completed |

## 6. Open traceability gaps

| ID | Gap | Impatto | Trattamento |
|---|---|---|---|
| TR-G01 | AMP-001 non coerente con i package realizzati | numerazione futura ambigua | AMP-002 creato; review indipendente |
| TR-G02 | Release-package mapping non sistematico | scope release difficile da certificare | aggiornamento release note |
| TR-G03 | Metadati storici non uniformi | automazione e query limitate | normalizzazione incrementale |
| TR-G04 | Alcuni ADR non sono nella directory canonica | IA non uniforme | migrazione non distruttiva |
| TR-G05 | Build strict e link check non eseguiti | pubblicabilità non certificata | CI o workspace |
| TR-G06 | Owner AP-001…AP-006 non formalmente assegnati | governance non operativa | RACI |
| TR-G07 | Schema DP-001…DP-005 non collegati | data product non certificabili | locator immutabili |
| TR-G08 | Retention non deliberate | lifecycle incompleto | decisione per data product e signal |
| TR-G09 | Lineage Analytics → Warehouse → consumer incompleto | riproducibilità limitata | Evidence Annex AP-002 |
| TR-G10 | Inventario sensori/controller/interlock non certificato | AP-003 non commissionabile | inventory e owner |
| TR-G11 | Timeout, retry, heartbeat e soglie safety non validati | comportamento non deterministico | commissioning |
| TR-G12 | Fault injection e isolamento non provati | CAP-16/17 non promuovibili | validation matrix |
| TR-G13 | Condizioni ARB-004 aperte | data product non certificabili | remediation AP-002 |
| TR-G14 | Matrice accessi dati e Data Issue lifecycle assenti | security e quality incompleti | AP-002 |
| TR-G15 | ADR-005 e Capability 002 restano Proposed | safety policy non deliberata | AP-010 |
| TR-G16 | Command authorization e audit contract assenti | comandi non governabili | AP-005/AP-012 |
| TR-G17 | Shadow mode, rollback e commissioning non collaudati | runtime non autorizzabile | evidence |
| TR-G18 | Inventory producer/signal/stack/volumi assente | AP-004 non ripetibile | pilot |
| TR-G19 | SLI, SLO, routing ed escalation non deliberati | operations non certificabili | AP-007/AP-012 |
| TR-G20 | Buffering e failure handling non testati | perdita signal non quantificata | pilot end-to-end |
| TR-G21 | Semantic contracts AP-004 non machine-readable | gate non automatizzabili | schema e test |
| TR-G22 | Audit integrity e disposal non verificati | evidence non certificabile | policy e test |
| TR-G23 | Cardinality budget assente | costi e saturazione | budget |
| TR-G24 | Continuous operations evidence assente | CAP-08 non promuovibile | OPS evidence |
| TR-G25 | Inventory identità e secret assente | privilegi non verificabili | AP-005 |
| TR-G26 | VPN, MFA e device trust non verificati | accesso remoto non certificabile | pilot |
| TR-G27 | Revocation non testata | privilegi eccessivi | policy e test |
| TR-G28 | Break-glass non collaudato | recovery non governato | exercise |
| TR-G29 | Session termination non deliberata | sessioni privilegiate non governabili | contract |
| TR-G30 | Inventario asset e CI incompleto | impact analysis incompleta | AP-006 |
| TR-G31 | Warranty/licenze/support status non verificati | lifecycle non governabile | reconciliation |
| TR-G32 | Versioni software e profili non baselined | rollback non ripetibile | baseline |
| TR-G33 | Relazioni asset/servizi/safety non verificate | failure impact incompleto | relationship register |
| TR-G34 | Drift detection non implementato | modifiche non rilevabili | pilot |
| TR-G35 | Restore e rollback non dimostrati | readiness non certificabile | exercise |
| TR-G36 | Policy IAM non machine-readable | gate non automatizzabili | schema e test |
| TR-G37 | Security failure exercise assenti | privileged access non certificabile | evidence |
| TR-G38 | Ownership KPI DSAP non definita | dashboard ambigua | AP-011 |
| TR-G39 | Protocollo live e freshness UI non deliberati | DSOC può mostrare stato ingannevole | AP-008/AP-012 |
| TR-G40 | BFF e command path non definiti | rischio UI-to-device | AP-008/AP-012 |
| TR-G41 | Degraded-mode UX non validata | portale non operabile in emergenza | AP-012 |
| TR-G42 | Storage scientifico, URI scheme e asset identity non deliberati | link fragili e asset non riconciliabili | AP-009/AP-013 |
| TR-G43 | Schema Processing Run e Workflow Definition assenti | storico PixInsight non confrontabile | AP-013/AP-014 |
| TR-G44 | Capacità reale di esportare process history PixInsight non provata | automazione potrebbe essere incompleta | PoC PixInsight con fallback manuale |
| TR-G45 | Checksum, idempotenza e reconciliation della sync non testati | catalogo e storage possono divergere | AP-008/AP-014 validation matrix |
| TR-G46 | Gestione credenziali per script/adapter non definita | rischio esposizione token GitHub | AP-005/AP-008 least privilege |
| TR-G47 | Versioni PixInsight, moduli e script non baselined | processing non riproducibile | AP-006/AP-013 |
| TR-G48 | Provenance degli step manuali non standardizzata | storia incompleta o fuorviante | schema con manual step e `unknown` esplicito |

## 7. Validazione del registro

Il registro copre la governance AP-001…AP-006, le review ARB-003…ARB-008, il riallineamento AMP-002 e le capability pianificate CAP-34…CAP-39. Non certifica implementazione, storage esterno, sincronizzazione PixInsight, export process history o operatività del catalogo.