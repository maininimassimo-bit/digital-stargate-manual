# DSG-APP-001 - Appendici Enterprise

| Campo | Valore |
|---|---|
| Documento | Appendici Enterprise |
| Identificativo | `DSG-APP-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.1 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |

## 1. Scopo

Le appendici consolidano glossario, acronimi, riferimenti, template e mapping documentali della baseline enterprise. Il [Knowledge Index](knowledge-index.md) resta il punto di accesso alla traceability matrix.

## 2. Glossario

| Termine | Definizione |
|---|---|
| AS-IS | Stato corrente documentato |
| Transition | Stato in consolidamento |
| TO-BE | Stato target non necessariamente implementato |
| ADR | Documento che registra una decisione architetturale reale |
| Capability | Capacita governabile collegata a roadmap o programma |
| Configuration Registry | Registro delle configurazioni pubblicabili, sensibili o da validare |
| Data lineage | Tracciabilita da origine dati a KPI o pubblicazione |
| Evidence | Log, checklist, commit, build, report o review |
| Knowledge Graph | Modello semantico della conoscenza; schema `TBD` |
| Quality gate | Controllo obbligatorio prima di pubblicazione o release |
| Roadmap Freeze Policy | Policy `DSG-GOV-001` che impedisce estensioni non approvate |
| Warehouse | Livello dati consolidato per analytics e storico |

## 3. Acronimi

| Acronimo | Significato |
|---|---|
| ACM | Asset and Configuration Management |
| ADR | Architecture Decision Record |
| AI | Artificial Intelligence |
| DSRA | Digital StarGate Reference/Risk Architecture, secondo contesto |
| EAGLE | Computer operativo PrimaLuceLab presso l'osservatorio |
| EAM | Enterprise Architecture Meta Model |
| KPI | Key Performance Indicator |
| PR | Pull Request |
| RACI | Responsible, Accountable, Consulted, Informed |
| RPN | Risk Priority Number |
| SOP | Standard Operating Procedure |

## 4. Mapping documentale

| Gerarchia | Documento | Registro |
|---|---|---|
| `DSG-MR-001` | Master Roadmap | Deliverable, traceability |
| `DSG-EAM-001` | Enterprise Architecture Meta Model | Component/Platform Registry |
| `DSRA-000` | Vision Target Architecture | Planning/Vision |
| `DSRA-001` | Reference Architecture | Component Registry |
| ADR | ADR Index e ADR esistenti | Decision Registry |
| Assessments | Enterprise Assessment | Risk/Control Registry |
| SOP | Standard Operating Procedures | Control Registry |
| Engineering Handbook | Handbook | Quality gates |
| Release Notes | Release documentation | Change log |
| Project History | Project History | Change log |
| Technical Manuals | Capitoli MkDocs | Knowledge Registry |

## 5. References index

| Area | Riferimento |
|---|---|
| Roadmap | [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) |
| Architecture | [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md), [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md), [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md) |
| ADR | [ADR Index](adr/index.md), [ADR-004](adr/ADR-004-enterprise-documentation-baseline.md) |
| Portfolio | [Program Portfolio](program-portfolio.md) |
| Registry | [Enterprise Registry](registries/index.md) |
| Governance | [Governance](governance.md) |
| SOP | [SOP](sop.md) |
| Handbook | [Engineering Handbook](handbook.md) |
| Assessment | [Enterprise Assessment](assessment.md) |
| Release | [Release documentation](release-documentation.md) |
| Knowledge | [Knowledge Index](knowledge-index.md) |
| History | [Project History](project-history.md) |
| Vision | [Vision](vision.md) |

## 6. Template requisito

```markdown
| Campo | Valore |
|---|---|
| ID | DSG-REQ-AREA-000 |
| Titolo |  |
| Categoria |  |
| Priorita |  |
| Stato | Proposed |
| Fonte | DSG-MR-001 |
| Verifica |  |
| Owner | Da validare |
```

## 7. Template rischio

```markdown
| Campo | Valore |
|---|---|
| ID | DSG-RSK-AREA-000 |
| Rischio |  |
| Area |  |
| Probabilita | 1-5 |
| Impatto | 1-5 |
| Rilevabilita | 1-5 |
| Controlli |  |
| Stato | Proposed |
```

## 8. Template ADR

```markdown
# ADR-000 - Titolo

| Campo | Valore |
|---|---|
| Stato | Proposed |
| Data | Da validare |
| Roadmap | DSG-MR-001 |

## Contesto

## Decisione

## Conseguenze

## Riferimenti
```

## 9. Template SOP

```markdown
# DSG-SOP-AREA-000 - Titolo

| Campo | Valore |
|---|---|
| Prerequisiti |  |
| Responsabilita |  |
| Trigger |  |
| Input |  |
| Output |  |
| Controlli |  |

## Procedura

## Gestione errori

## Evidenze

## Rollback

## Elementi TBD
```

## 10. Elementi TBD

| ID | Elemento | Stato |
|---|---|
| `DSG-APP-TBD-001` | Glossario completo dei capitoli tecnici | Da validare |
| `DSG-APP-TBD-002` | Acronimi operativi specialistici | Da validare |
| `DSG-APP-TBD-003` | Template automatici per issue/PR | TBD |

## 11. Regole di aggiornamento

Le appendici vengono aggiornate quando viene introdotto un nuovo prefisso ID, un template cambia forma, una milestone aggiunge un tipo documentale, un termine tecnico diventa ricorrente o un mapping non rappresenta piu lo stato reale della baseline.
