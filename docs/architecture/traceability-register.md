# Digital StarGate Architecture Traceability Register

| Campo | Valore |
|---|---|
| Documento | Architecture Traceability Register |
| Package | AP-001 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Stato | Active baseline — conditions open |
| Data | 30/07/2026 |

## 1. Regole

- Il registro collega capability, package, decisioni, evidenze, review e release.
- Le righe descrivono esclusivamente artefatti verificati nel repository.
- L'assenza di una review o release è indicata esplicitamente.
- Uno stato capability non viene promosso da questo registro.
- I locator di evidenza devono diventare puntuali quando usati per certificazione.

## 2. Baseline certificata

| Capability / Scope | Stato verificato | Fonte autorevole | Evidence / Implementation | Review / Certificate | Disposizione |
|---|---|---|---|---|---|
| CAP-01 Analytics pipeline | Implemented, con limiti dichiarati | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Fondazione esistente; non ricostruire greenfield |
| CAP-02 Historical Analytics Dashboard | Implemented, operatività continua non certificata | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Evoluzione controllata |
| CAP-03 Data Warehouse | Implemented, consumer layer incompleto | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 / ARB-004 | AP-002 governa data product e contratti; condizioni operative aperte |
| CAP-04 Warehouse metadata and validation | Implemented, release certification assente | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 / ARB-004 | AP-002 definisce quality, lineage e compatibility; evidenze da completare |
| CAP-08 Live telemetry | Planned | PAA-002 v1.1 | `future.telemetry: false` registrato da PAA-002 | ARB-002 / ABC-001 | Richiede package dedicato |
| CAP-15 AllSky integration | Planned | PAA-002 v1.1 | `future.allsky: false` registrato da PAA-002 | ARB-002 / ABC-001 | Richiede contratti e health |
| CAP-16 Observatory Automation | Partial | PAA-002 v1.1 | Procedura di chiusura, ADR-005, Capability 002 e AP-003 | ARB-002 / ABC-001 / ARB-005 | AP-003 approvato con condizioni; nessuna promozione senza TST/INT/OPS |
| CAP-17 Local safety interlocks | Partial | PAA-002 v1.1 | Evidenza documentale; hardware e fault test non inclusi | ARB-002 / ABC-001 / ARB-005 | Autorità locale preservata; safety readiness non certificata |
| CAP-18 AI boundary contracts | Prepared | PAA-002 v1.1 | `src/DigitalStarGate.Contracts/Ai/AiContracts.cs` | ARB-002 / ABC-001 / ARB-004 | AI deve consumare dati governati; condizioni AP-002 aperte |
| CAP-19 AI Assistant | Planned | PAA-002 v1.1 | `future.ai_assistant: false` registrato da PAA-002 | ARB-002 / ABC-001 | Read-only first |
| CAP-31 Architecture Governance | Partial | PAA-002 v1.1 | AP-001, metamodel e registro | ARB-003 / ARB-004 / ARB-005 | Package review operativa; condizioni e automazione aperte |
| CAP-32 Documentation Governance | Partial | PAA-002 v1.1 | MkDocs, package e standard | ARB-003 / ARB-004 / ARB-005 | Standardizzare, assegnare owner e automatizzare |
| CAP-33 Release Quality Governance | Partial | PAA-002 v1.1 | Processi e release note distribuiti | ARB-003 / ARB-004 / ARB-005 | Collegare package, gate, evidence e approval |

## 3. Architecture Package Register

| Package | Scope | Capability interessate | Artefatti | Review | Stato |
|---|---|---|---|---|---|
| AP-001 | Enterprise Metamodel and Repository Information Architecture | CAP-31, CAP-32, CAP-33; trasversale | `packages/AP-001-Enterprise-Metamodel-and-Repository-Information-Architecture.md`, `enterprise-metamodel.md`, presente registro | ARB-003 | Approved with conditions |
| AP-002 | Enterprise Data Governance | CAP-03, CAP-04, CAP-31, CAP-32, CAP-33; abilita consumer, telemetry e AI | `packages/AP-002-Enterprise-Data-Governance.md`, `data-governance-standard.md` | ARB-004 | Approved with conditions |
| AP-003 | Observatory Automation Architecture | CAP-16, CAP-17; dipendenze su weather safety, operations e contracts | `packages/AP-003-Observatory-Automation-Architecture.md`, `observatory-automation-reference-architecture.md`, ADR-005, Capability 002 | ARB-005 | Approved with conditions; non autorizza automation runtime o safety certification |

## 4. Data Product Candidate Register

| ID | Data product | Fonte contrattuale verificata | Owner | Stato |
|---|---|---|---|---|
| DP-001 | `sessions.parquet` | `architecture/warehouse/datasets-and-schema.md`; schema eseguibile da localizzare | proposto | Candidate baseline |
| DP-002 | `targets.parquet` | `architecture/warehouse/datasets-and-schema.md`; schema eseguibile da localizzare | proposto | Candidate baseline |
| DP-003 | `equipment.parquet` | `architecture/warehouse/datasets-and-schema.md`; schema eseguibile da localizzare | proposto | Candidate baseline |
| DP-004 | `quality.parquet` | `architecture/warehouse/datasets-and-schema.md`; schema eseguibile da localizzare | proposto | Candidate baseline |
| DP-005 | `weather.parquet` | `architecture/warehouse/datasets-and-schema.md`; schema eseguibile da localizzare | proposto | Candidate baseline |

Gli ID DP-001…DP-005 sono proposti da AP-002 e non costituiscono certificazione finché owner, grain, schema locator, consumer, quality, retention e lineage non sono verificati.

## 5. Assessment and governance chain

| Artefatto | Ruolo | Input | Output / Decision | Stato |
|---|---|---|---|---|
| PAA-002 v1.1 | Capability gap assessment | Baseline repository | Capability matrix, gap, dipendenze | Reviewed |
| ARB-002 | Independent review | PAA-002 v1.1 | Approved with conditions, 90/100 | Completed |
| ABC-001 | Baseline certificate | PAA-002, ARB-002, Evidence Annex | Conditionally certified | Completed |
| AMP-001 | Architecture Master Plan | ABC-001 | Priorità AP-001; contenuto repository verificato incompleto | Remediation required |
| AP-001 | Enterprise architecture package | PAA-002, ARB-002, ABC-001 | Metamodel e information architecture | Reviewed |
| ARB-003 | Independent review | AP-001 baseline `a97f2291a2376e2a0123e1a9a07405b22f74e1bd` | Approved with conditions, 86/100 | Completed |
| AP-002 | Enterprise architecture package | Warehouse baseline, platform contracts, AP-001, ARB-003 | Enterprise Data Governance | Reviewed |
| ARB-004 | Independent review | AP-002 publication baseline `6d485f59126afc83a55d0f034d012ff0563186c2` | Approved with conditions, 88/100 | Completed |
| AP-003 | Infrastructure and automation architecture package | PAA-002, ADR-005, Capability 002, operations documentation, AP-001/AP-002 | Observatory Automation Architecture | Reviewed |
| ARB-005 | Independent review | AP-003 and Observatory Automation Reference Architecture on `main` | Approved with conditions, 89/100 | Completed |

## 6. Open traceability gaps

| ID | Gap | Impatto | Trattamento |
|---|---|---|---|
| TR-G01 | AMP-001 incompleto rispetto al riepilogo precedente | Handoff e roadmap non completamente ripetibili | Correzione separata e review |
| TR-G02 | Release-package mapping non sistematico | Scope release difficile da certificare | Aggiornamento progressivo release note |
| TR-G03 | Metadati non uniformi nei documenti storici | Automazione e query limitate | Normalizzazione quando i file vengono modificati |
| TR-G04 | Alcuni ADR non sono nella directory canonica | Information architecture non uniforme | Inventario e migrazione non distruttiva |
| TR-G05 | Build strict e link check non eseguiti | Pubblicabilità non certificata | Eseguire in CI o workspace con checkout |
| TR-G06 | Owner AP-001, AP-002 e AP-003 non formalmente assegnati | Governance non operativa | RACI e nomina esplicita |
| TR-G07 | Schema eseguibili dei cinque dataset non ancora collegati nel registro | Data product non certificabili | Inventario con locator immutabili |
| TR-G08 | Retention concrete non deliberate | Lifecycle incompleto | Decisione per data product |
| TR-G09 | Lineage Analytics → Warehouse → consumer non registrato end-to-end | Impatto e riproducibilità limitati | Evidence Annex AP-002 |
| TR-G10 | Inventario sensori, controller, interlock e protocolli non certificato | AP-003 non commissionabile | AP-003 Fase 0 con locator e owner |
| TR-G11 | Timeout, retry, heartbeat e soglie safety non validati | rischio di comportamento non deterministico | commissioning e ADR/decisioni dedicate |
| TR-G12 | Nessuna evidenza fault injection o isolamento rete/alimentazione | CAP-16 e CAP-17 non promuovibili | validation matrix ed Evidence Annex AP-003 |
| TR-G13 | Condizioni ARB-004 non chiuse | Contratti dati definitivi e data product non certificabili | remediation AP-002 e re-review mirata |
| TR-G14 | Matrice accessi per classificazione e lifecycle Data Issue assenti | Controlli security e gestione qualità incompleti | completare standard operativo AP-002 |
| TR-G15 | ADR-005 e Capability 002 restano Proposed | policy safety applicativa non deliberata | review coordinata prima dei comandi automatici |
| TR-G16 | Command authorization matrix e audit event contract assenti | accesso fisico e audit non completamente governati | definizione allineata ad AP-002 e ARB-005 |
| TR-G17 | Shadow mode, rollback e commissioning non collaudati | automation runtime non autorizzabile | eseguire validation matrix e re-review mirata |

## 7. Validazione del registro

Il registro copre gli elementi necessari ad AP-001, ARB-003, AP-002, ARB-004, AP-003 e ARB-005. Non rappresenta ancora un inventario esaustivo di ogni file, schema, dispositivo, requirement, test o work item del repository.
