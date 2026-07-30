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
- Gli identificatori esistenti non vengono rinumerati retroattivamente.
- Una workflow definition versionata non prova una Processing Run eseguita.
- Una knowledge projection o inferenza AI non è fonte autorevole senza provenance e citation.
- Un Architecture Package `Proposed for review` non è `Completed` finché non è sottoposto a review e le condizioni non sono governate.

## 2. Baseline certificata e capability pianificate

| Capability / Scope | Stato verificato | Fonte autorevole | Evidence / Implementation | Review / Certificate | Disposizione |
|---|---|---|---|---|---|
| CAP-01 Analytics pipeline | Implemented, con limiti | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Fondazione esistente |
| CAP-02 Historical Analytics Dashboard | Implemented, continuità non certificata | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-002 / ABC-001 | Evoluzione DSAP |
| CAP-03 Data Warehouse | Implemented, consumer incompleto | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-004 / ARB-006 | Condizioni operative aperte |
| CAP-04 Warehouse metadata and validation | Implemented, release non certificata | PAA-002 v1.1 | ABC-001 Evidence Annex | ARB-004 / ARB-006 | Evidence runtime da completare |
| CAP-08 Live telemetry | Planned | PAA-002 / AP-004 | Reference architecture | ARB-006 | Pilot e OPS richiesti |
| CAP-15 AllSky integration | Planned | PAA-002 | feature futura | ARB-002 | Contratti e health richiesti |
| CAP-16 Observatory Automation | Partial | AP-003 | documentazione operativa | ARB-005…ARB-008 | Runtime non autorizzato |
| CAP-17 Local safety interlocks | Partial | AP-003 | evidenza documentale | ARB-005…ARB-008 | Autorità locale preservata |
| CAP-18 AI boundary contracts | Prepared | PAA-002 | contratti presenti | ARB-004/006/007 | Nessun privilegio implicito |
| CAP-19 AI Assistant | Planned | PAA-002 | feature futura | ARB-002 | Read-only first |
| CAP-31 Architecture Governance | Partial | AP-001 | metamodel e registro | ARB-003…ARB-008 | Condizioni aperte |
| CAP-32 Documentation Governance | Partial | AP-001 | MkDocs e standard | ARB-003…ARB-008 | Automazione progressiva |
| CAP-33 Release Quality Governance | Partial | AP-001 | release note | ARB-003…ARB-008 | Mapping incompleto |
| CAP-34 Enterprise Analytics Platform | Planned | AMP-002 / DSGP-VIS-001 | vision | Nessuna review AP-011 | DSAP governato |
| CAP-35 Enterprise Operations Center | Planned | AMP-002 / DSGP-VIS-001 | vision | Nessuna review AP-012 | DSOC read-only first |
| CAP-36 Digital StarGate Portal | Planned | AMP-002 / DSGP-VIS-001 | vision | Nessuna review AP-011/AP-012 | Non safety authority |
| CAP-37 Scientific Image Repository | Planned | AMP-002 / SIR-VIS-001 | vision | Nessuna review AP-013 | Storage esterno |
| CAP-38 Scientific Observation Catalog and Search | Planned | AMP-002 / SIR-VIS-001 | vision | Nessuna review AP-014 | Catalogo e manifest |
| CAP-39 Scientific Processing Provenance | Planned | AMP-002 / SIR-VIS-001 | contratto proposto | Nessuna review AP-013/AP-014 | Processing Run immutabili |
| CAP-40 Scientific Knowledge Layer | Planned | AMP-002 / SKL-VIS-001 | vision | Nessuna review AP-015 | Claim e citation governati |

## 3. Architecture Package Register

| Package | Scope | Artefatti | Review | Stato |
|---|---|---|---|---|
| AP-001 | Metamodel e repository IA | package, metamodel, registro | ARB-003 | Approved with conditions |
| AP-002 | Data Governance | package e standard | ARB-004 | Approved with conditions |
| AP-003 | Observatory Automation | package e reference architecture | ARB-005 | Approved with conditions |
| AP-004 | Telemetry and Observability | package e reference architecture | ARB-006 | Approved with conditions |
| AP-005 | Identity and Remote Security | package e reference architecture | ARB-007 | Approved with conditions, 91/100 |
| AP-006 | Configuration and Asset Management | package e reference architecture | ARB-008 | Approved with conditions, 92/100 |
| AP-007 | Operations and Service Management | package AP-007 e OPS-REF-001 | Nessuna | Proposed for independent ARB review |
| AP-008 | Enterprise Integration | da produrre | Nessuna | Planned |
| AP-009 | Enterprise Infrastructure | da produrre | Nessuna | Planned |
| AP-010 | Enterprise Safety Assurance | da produrre | Nessuna | Planned |
| AP-011 | Analytics Platform | DSGP-VIS-001 | Nessuna | Planned |
| AP-012 | Operations Center | DSGP-VIS-001 | Nessuna | Planned |
| AP-013 | Scientific Image Repository | SIR-VIS-001 | Nessuna | Planned |
| AP-014 | Scientific Catalog and Search | SIR-VIS-001 | Nessuna | Planned |
| AP-015 | Scientific Knowledge Platform | SKL-VIS-001 | Nessuna | Planned |

## 4. Data Product Candidate Register

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

## 5. Assessment and governance chain

| Artefatto | Ruolo | Stato |
|---|---|---|
| PAA-002 v1.1 | Capability gap assessment | Reviewed |
| ARB-002 | Independent review PAA-002 | Completed, 90/100 |
| ABC-001 | Baseline certificate | Conditionally certified |
| AMP-001 | Historical master plan | Superseded in roadmap sections |
| AMP-002 | Roadmap AP-007…AP-015 | Approved for planning |
| DSGP-VIS-001 | Digital Platforms vision | Planned vision |
| SIR-VIS-001 | Scientific image and provenance vision | Approved for planning |
| SKL-VIS-001 | Scientific Knowledge Layer vision | Approved for planning |
| AP-001 / ARB-003 | Metamodel | Approved with conditions |
| AP-002 / ARB-004 | Data Governance | Approved with conditions |
| AP-003 / ARB-005 | Automation | Approved with conditions |
| AP-004 / ARB-006 | Observability | Approved with conditions |
| AP-005 / ARB-007 | Identity and Security | Approved with conditions |
| AP-006 / ARB-008 | Configuration and Assets | Approved with conditions |
| AP-007 / OPS-REF-001 | Operations and Service Management | Proposed for independent ARB review |

## 6. Open traceability gaps

| ID | Gap | Impatto | Trattamento |
|---|---|---|---|
| TR-G01 | AMP-001 non coerente con package realizzati | numerazione ambigua | AMP-002 |
| TR-G02 | Release-package mapping incompleto | scope release non certificabile | release governance |
| TR-G05 | Build strict e link check non eseguiti | pubblicabilità non certificata | CI/workspace |
| TR-G06 | Owner fondazione non tutti formalizzati | accountability incompleta | RACI |
| TR-G07 | Schema DP-001…DP-005 non collegati | data product non certificabili | locator immutabili |
| TR-G08 | Retention non deliberate | lifecycle incompleto | policy data product |
| TR-G09 | Lineage analytics incompleto | riproducibilità limitata | AP-002 evidence |
| TR-G10 | Inventario safety non certificato | AP-003 non commissionabile | inventory e owner |
| TR-G12 | Fault injection non provata | CAP-16/17 non promuovibili | AP-010 validation |
| TR-G13 | Condizioni ARB-004 aperte | data product non certificabili | remediation AP-002 |
| TR-G15 | ADR-005/Capability 002 Proposed | safety policy non deliberata | AP-010 |
| TR-G16 | Command authorization incompleta | comandi non governabili | AP-005/AP-012 |
| TR-G19 | SLI, SLO, routing ed escalation non deliberati | operations non certificabili | AP-007 pilot |
| TR-G24 | Continuous operations evidence assente | CAP-08 non promuovibile | OPS evidence |
| TR-G38 | Ownership KPI DSAP non definita | dashboard ambigua | AP-011 |
| TR-G39 | Protocollo live/freshness non deliberato | stato DSOC ingannevole | AP-008/AP-012 |
| TR-G40 | BFF e command path non definiti | rischio UI-to-device | AP-008/AP-012 |
| TR-G41 | Degraded-mode UX non validata | portale fragile in emergenza | AP-012 |
| TR-G42 | Storage scientifico e URI non deliberati | link fragili | AP-009/AP-013 |
| TR-G43 | Processing Run schema assente | storico non confrontabile | AP-013/AP-014 |
| TR-G44 | Export PixInsight non provato | automazione incompleta | PoC |
| TR-G45 | Reconciliation sync non testata | divergenza catalogo/storage | AP-008/AP-014 |
| TR-G46 | Credenziali adapter non definite | esposizione token | AP-005/AP-008 |
| TR-G47 | Versioni PixInsight non baselined | processing non riproducibile | AP-006/AP-013 |
| TR-G48 | Step manuali non standardizzati | provenance incompleta | schema manual/unknown |
| TR-G49 | Vocabolario scientifico senza owner | semantica incoerente | AP-015 |
| TR-G50 | Conflitti tra fonti non governati | claim fuorvianti | AP-015 |
| TR-G51 | Citation/confidence model assente | risultati non verificabili | AP-015 |
| TR-G52 | Graph/vector non valutato | lock-in prematuro | PoC dopo AP-014 |
| TR-G53 | Inferenze AI non governate | inferenze trattate come fatti | AP-015 |
| TR-G54 | Knowledge reconciliation non testata | indice stale | AP-008/AP-015 |
| TR-G55 | Service catalog e service owner non formalizzati | supporto ed escalation non attribuibili | AP-007 inventory e nomine |
| TR-G56 | Severity, priority e major incident process non collaudati | risposta non uniforme | AP-007 pilot/exercise |
| TR-G57 | Runbook non testati end-to-end | procedure non dimostrate | AP-007 evidence annex |
| TR-G58 | Operational Readiness Review non eseguita | attivazioni non governate | pilot AP-007 |
| TR-G59 | Degraded mode per servizio non definita | continuità rischiosa | service records AP-007 |
| TR-G60 | SLO numerici senza baseline misurata | obiettivi arbitrari | baseline SLI prima degli SLO |

## 7. Validazione del registro

Il registro include AP-007 e OPS-REF-001 come artefatti proposti per review. Non certifica operatività continua, service ownership, SLO, runbook, escalation, degraded mode, readiness o risultato di una review ARB indipendente.