# DSG-HIST-001 - Project History

| Campo | Valore |
|---|---|
| Documento | Project History |
| Identificativo | `DSG-HIST-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.0 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |

## Scopo

Questo documento ricostruisce la storia documentale e di governance del progetto Digital StarGate sulla base delle evidenze presenti nel branch. Non inventa date operative, risultati osservativi o dettagli tecnici non presenti.

## Ambito

La storia copre manuale tecnico, architettura, warehouse e analytics, baseline enterprise `DSG-MR-001`, portfolio, registri, governance, planning e knowledge baseline.

## Timeline documentale

| Data | Evento | Evidenza | Stato |
|---|---|---|---|
| Da validare | Creazione manuale tecnico osservatorio | Capitoli 1-44 | AS-IS |
| Da validare | Introduzione architettura warehouse e analytics | Sezioni Architecture e Analytics | AS-IS / Transition |
| 26/07/2026 | Pubblicazione Master Roadmap `DSG-MR-001` | [Master Roadmap](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | Approvata |
| 26/07/2026 | Pubblicazione Enterprise Architecture baseline | [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md), [DSRA-000](../enterprise-architecture/DSRA-000-vision-target-architecture.md), [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md) | Baseline |
| 26/07/2026 | Pubblicazione Program Portfolio | [Program Portfolio](program-portfolio.md) | Baseline |
| 26/07/2026 | Consolidamento Enterprise Registry | [Registri](registries/index.md) | Baseline |
| 26/07/2026 | Consolidamento Enterprise Governance Framework | [Governance](governance.md) | Baseline |
| 26/07/2026 | Completamento planning, history e knowledge baseline | [Planning](planning.md), [Knowledge Index](knowledge-index.md) | Baseline |

## Decisioni storiche note

| Decisione | Evidenza | Stato |
|---|---|---|
| Usare MkDocs come portale documentale | `mkdocs.yml`, manuale tecnico | Accepted |
| Mantenere ADR tecnici per session layer, quality gate e warehouse | [ADR Index](adr/index.md) | Accepted |
| Stabilire `DSG-MR-001` come roadmap enterprise | [Master Roadmap](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | Accepted |
| Consolidare registri enterprise in una fonte unica | [Enterprise Registry](registries/index.md) | Accepted |

## Dipendenze e rischi

| ID | Elemento | Stato |
|---|---|
| `DSG-HIST-DEP-001` | Completezza della cronologia Git precedente alla baseline | Da validare |
| `DSG-HIST-RSK-001` | Confondere storia documentale con storia operativa osservativa | Mitigato con marcatura `Da validare` |
| `DSG-HIST-RSK-002` | Inventare date non presenti | Mitigato: date sconosciute restano `Da validare` |

## Evidenze

- Navigazione MkDocs.
- Documenti enterprise.
- ADR esistenti.
- Registri e change log.
- Commit hash riportati nei riepiloghi di milestone.

## Elementi TBD

| ID | Elemento | Stato |
|---|---|
| `DSG-HIST-TBD-001` | Cronologia operativa osservatorio precedente alla baseline | Da validare |
| `DSG-HIST-TBD-002` | Date di prima introduzione di warehouse, analytics e dashboard | Da validare |
| `DSG-HIST-TBD-003` | Collegamento automatico tra release notes e commit storici | TBD |

## Riferimenti

- [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [Release documentation](release-documentation.md)
- [Enterprise Registry](registries/index.md)
- [ADR Index](adr/index.md)
