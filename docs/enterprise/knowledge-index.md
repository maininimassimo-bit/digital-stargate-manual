# DSG-KNW-INDEX-001 - Knowledge, Document and Traceability Index

| Campo | Valore |
|---|---|
| Documento | Knowledge, Document and Traceability Index |
| Identificativo | `DSG-KNW-INDEX-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.0 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |

## 1. Scopo

Questo documento integra document index, document registry, traceability matrix, glossary, acronyms e references index. E il punto di accesso alla conoscenza enterprise senza duplicare i contenuti di [Enterprise Registry](registries/index.md) o [Appendici](appendices.md).

## 2. Gerarchia documentale approvata

```text
DSG-MR-001
  -> DSG-EAM-001
  -> DSRA-000
  -> DSRA-001
  -> ADR
  -> Assessments
  -> SOP
  -> Engineering Handbook
  -> Release Notes
  -> Project History
  -> Technical Manuals
```

## 3. Document Index

| Livello | Documento | ID | Stato |
|---|---|---|---|
| Roadmap | [Master Roadmap](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | `DSG-MR-001` | Approvata |
| Meta-modello | [Enterprise Architecture Meta Model](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md) | `DSG-EAM-001` | Baseline |
| Target architecture | [Vision Target Architecture](../enterprise-architecture/DSRA-000-vision-target-architecture.md) | `DSRA-000` | Baseline |
| Reference architecture | [Reference Architecture](../enterprise-architecture/DSRA-001-reference-architecture.md) | `DSRA-001` | Baseline |
| ADR | [ADR Index](adr/index.md) | `DSG-ADR-INDEX-001` | Baseline |
| Assessments | [Enterprise Assessment](assessment.md) | `DSG-ASMT-001` | Baseline |
| SOP | [Standard Operating Procedures](sop.md) | `DSG-SOP-001` | Baseline |
| Engineering Handbook | [Enterprise Handbook](handbook.md) | `DSG-HBK-001` | Baseline |
| Release Notes | [Release documentation](release-documentation.md) | `DSG-REL-001` | Baseline |
| Project History | [Project History](project-history.md) | `DSG-HIST-001` | Baseline |
| Technical Manuals | Capitoli tecnici MkDocs | `DSG-MAN-*` | AS-IS |

## 4. Document Registry

| ID | Documento | Percorso | Owner | Dipendenze |
|---|---|---|---|---|
| `DSG-PRG-001` | Enterprise Program Portfolio | `docs/enterprise/program-portfolio.md` | Massimo Mainini | `DSG-MR-001` |
| `DSG-REG-001` | Enterprise Registry | `docs/enterprise/registries/index.md` | Massimo Mainini | Portfolio, Governance |
| `DSG-GOV-001` | Enterprise Governance Framework | `docs/enterprise/governance.md` | Massimo Mainini | Roadmap, Registry |
| `DSG-PLAN-001` | Enterprise Planning Framework | `docs/enterprise/planning.md` | Massimo Mainini | Roadmap, Registry |
| `DSG-HIST-001` | Project History | `docs/enterprise/project-history.md` | Massimo Mainini | Release, Registry |
| `DSG-KNW-INDEX-001` | Knowledge Index | `docs/enterprise/knowledge-index.md` | Massimo Mainini | Appendici, Registry |

## 5. Traceability Matrix

| Roadmap area | Documento primario | Documento secondario | Controllo |
|---|---|---|---|
| Enterprise Foundation | `DSG-MR-001` | `DSG-GOV-001` | Roadmap Freeze Policy |
| Enterprise Architecture | `DSG-EAM-001`, `DSRA-000`, `DSRA-001` | ADR Index | `QG-ARCH` |
| Program Portfolio | `DSG-PRG-001` | Program Registry | Program review |
| Enterprise Registry | `DSG-REG-001` | Knowledge Index | Registry maintenance |
| Planning | `DSG-PLAN-001` | Release documentation | `QG-REL` |
| Governance | `DSG-GOV-001` | SOP, Handbook | Quality gates |
| Long-Term Vision | `DSG-MR-001`, `DSG-VISION-001` | Project History | Roadmap review |
| Technical Manuals | Capitoli MkDocs | Assessment, SOP | Document governance |

## 6. Glossary

| Termine | Definizione |
|---|---|
| AS-IS | Stato corrente documentato |
| Transition | Stato in consolidamento o migrazione |
| TO-BE | Stato target non necessariamente implementato |
| Capability | Capacita governabile collegata a roadmap o programma |
| Evidence | Prova verificabile: log, checklist, commit, build, report o review |
| Knowledge Graph | Modello semantico della conoscenza, `TBD` |
| Roadmap Freeze Policy | Regola che impedisce estensioni non approvate del perimetro `DSG-MR-001` |

## 7. Acronyms

| Acronimo | Significato |
|---|---|
| ADR | Architecture Decision Record |
| AI | Artificial Intelligence |
| DSRA | Digital StarGate Reference/Risk Architecture, secondo contesto documentale |
| EAM | Enterprise Architecture Meta Model |
| KPI | Key Performance Indicator |
| PR | Pull Request |
| RACI | Responsible, Accountable, Consulted, Informed |
| RPN | Risk Priority Number |
| SOP | Standard Operating Procedure |

## 8. References Index

| Area | Riferimento |
|---|---|
| Roadmap | [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) |
| Architecture | [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md), [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md), [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md) |
| Governance | [DSG-GOV-001](governance.md) |
| Portfolio | [Program Portfolio](program-portfolio.md) |
| Registry | [Enterprise Registry](registries/index.md) |
| Operations | [SOP](sop.md), capitoli tecnici Operations |
| Release | [Release documentation](release-documentation.md) |
| Technical Manuals | Capitoli `chapters/01` - `chapters/44` in MkDocs |

## 9. Elementi TBD

| ID | Elemento | Stato |
|---|---|
| `DSG-KNW-TBD-001` | Knowledge Graph schema | TBD |
| `DSG-KNW-TBD-002` | Mappatura automatica documenti -> registry | TBD |
| `DSG-KNW-TBD-003` | Copertura completa acronimi da capitoli tecnici | Da validare |

## 10. Riferimenti

- [Enterprise Registry](registries/index.md)
- [Appendici](appendices.md)
- [Project History](project-history.md)
- [Planning](planning.md)
