# Digital StarGate Architecture Traceability Register

| Campo | Valore |
|---|---|
| Documento | Architecture Traceability Register |
| Package | AP-001 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Stato | Initial baseline — proposed for ARB review |
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
| CAP-03 Data Warehouse | Implemented, consumer layer incompleto | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Consolidare access layer |
| CAP-04 Warehouse metadata and validation | Implemented, release certification assente | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Certificare compatibilità e release |
| CAP-08 Live telemetry | Planned | PAA-002 v1.1 | `future.telemetry: false` registrato da PAA-002 | ARB-002 / ABC-001 | Richiede package dedicato |
| CAP-15 AllSky integration | Planned | PAA-002 v1.1 | `future.allsky: false` registrato da PAA-002 | ARB-002 / ABC-001 | Richiede contratti e health |
| CAP-16 Observatory Automation | Partial | PAA-002 v1.1 | Documentazione operativa distribuita | ARB-002 / ABC-001 | Definire boundary safety/control/orchestration |
| CAP-17 Local safety interlocks | Partial | PAA-002 v1.1 | Evidenza documentale, test fault non inclusi | ARB-002 / ABC-001 | Interblocchi locali indipendenti |
| CAP-18 AI boundary contracts | Prepared | PAA-002 v1.1 | `src/DigitalStarGate.Contracts/Ai/AiContracts.cs` | ARB-002 / ABC-001 | Completare governance prima dell'AI runtime |
| CAP-19 AI Assistant | Planned | PAA-002 v1.1 | `future.ai_assistant: false` registrato da PAA-002 | ARB-002 / ABC-001 | Read-only first |
| CAP-31 Architecture Governance | Partial | PAA-002 v1.1 | ADR, assessment, roadmap e release distribuiti | ARB-002 / ABC-001 | AP-001 istituisce metamodel e registro |
| CAP-32 Documentation Governance | Partial | PAA-002 v1.1 | MkDocs e convenzioni esistenti | ARB-002 / ABC-001 | Standardizzare e automatizzare |
| CAP-33 Release Quality Governance | Partial | PAA-002 v1.1 | Processi e release note distribuiti | ARB-002 / ABC-001 | Collegare package, gate e approval |

## 3. Architecture Package Register

| Package | Scope | Capability interessate | Artefatti | Review | Stato |
|---|---|---|---|---|---|
| AP-001 | Enterprise Metamodel and Repository Information Architecture | CAP-31, CAP-32, CAP-33; trasversale alle altre capability | `packages/AP-001-Enterprise-Metamodel-and-Repository-Information-Architecture.md`, `enterprise-metamodel.md`, presente registro | Non ancora eseguita | Proposed for independent ARB review |

## 4. Assessment and governance chain

| Artefatto | Ruolo | Input | Output / Decision | Stato |
|---|---|---|---|---|
| PAA-002 v1.1 | Capability gap assessment | Baseline repository | Capability matrix, gap, dipendenze | Reviewed |
| ARB-002 | Independent review | PAA-002 v1.1 | Approved with conditions, 90/100 | Completed |
| ABC-001 | Baseline certificate | PAA-002, ARB-002, Evidence Annex | Conditionally certified | Completed |
| AMP-001 | Architecture Master Plan | ABC-001 | Priorità AP-001; contenuto repository verificato incompleto | Remediation required |
| AP-001 | Enterprise architecture package | PAA-002, ARB-002, ABC-001 | Metamodel e information architecture | Proposed for review |

## 5. Open traceability gaps

| ID | Gap | Impatto | Trattamento |
|---|---|---|---|
| TR-G01 | AMP-001 incompleto rispetto al riepilogo precedente | Handoff e roadmap non completamente ripetibili | Correzione separata e review |
| TR-G02 | Release-package mapping non sistematico | Scope release difficile da certificare | Aggiornamento progressivo release note |
| TR-G03 | Metadati non uniformi nei documenti storici | Automazione e query limitate | Normalizzazione quando i file vengono modificati |
| TR-G04 | Alcuni ADR non sono nella directory canonica | Information architecture non uniforme | Inventario e migrazione non distruttiva |
| TR-G05 | Build strict e link check non eseguiti | Pubblicabilità non certificata | Eseguire in CI o workspace con checkout |

## 6. Validazione del registro

Il registro è inizializzato per gli elementi necessari ad AP-001; non rappresenta ancora un inventario esaustivo di ogni file, requirement o work item del repository.