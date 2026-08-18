# DSG-ADR-INDEX-001 - Architecture Decision Records Index

| Campo | Valore |
|---|---|
| Documento | Architecture Decision Records Index |
| Identificativo | `DSG-ADR-INDEX-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.0 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |

## Scopo

Questo indice governa gli Architecture Decision Records collegati alla baseline documentale Digital StarGate. Non introduce nuove decisioni architetturali: registra solo decisioni gia documentate o rese necessarie dalla struttura approvata.

## Ambito

L'indice copre:

- ADR tecnici gia presenti nella sezione Architettura;
- ADR enterprise pubblicati sotto `docs/enterprise/adr/`;
- stato, relazioni e riferimenti incrociati;
- criteri per creare ADR futuri senza violare la Roadmap Freeze Policy.

## Principi

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-ADR-PRN-001` | Decisioni reali | Non si inventano decisioni non documentate |
| `DSG-ADR-PRN-002` | Stato esplicito | Ogni ADR usa Proposed, Accepted, Superseded o Deprecated |
| `DSG-ADR-PRN-003` | Collegamento gerarchico | Ogni ADR rilevante richiama `DSG-MR-001` |
| `DSG-ADR-PRN-004` | Cross-reference | ADR correlati o sostituiti sono collegati |

## Registro ADR

| ID | Titolo | Stato | Percorso | Ambito | Correlazioni |
|---|---|---|---|---|---|
| `ADR-001` | Session Layer | Accepted | [ADR-001](../../architecture/ADR-001-Session-Layer.md) | Architettura sessioni | `ADR-002`, `ADR-003` |
| `ADR-002` | Analytics Quality Gates | Accepted | [ADR-002](../../architecture/ADR-002-Analytics-Quality-Gates.md) | Qualita analytics | `DSG-GOV-001`, `QG-DATA` |
| `ADR-003` | Warehouse Engine | Accepted | [ADR-003](../../architecture/ADR-003-Warehouse-Engine.md) | Warehouse | `ADR-002`, Data Governance |
| `DSG-ADR-004` | Enterprise documentation baseline | Accepted | [ADR-004](ADR-004-enterprise-documentation-baseline.md) | Baseline documentale `DSG-MR-001` | `DSG-GOV-001`, `DSG-REG-001` |

## ADR mancanti

Non sono stati creati ADR aggiuntivi per AI, Live Operations, Knowledge Graph o Disaster Recovery perche nel branch non risultano decisioni implementative approvate. Questi ambiti restano governati come `TBD` o `Da validare` nei documenti:

- [Enterprise Program Portfolio](../program-portfolio.md);
- [Enterprise Registry](../registries/index.md);
- [Enterprise Governance Framework](../governance.md);
- [DSRA-000](../../enterprise-architecture/DSRA-000-vision-target-architecture.md);
- [DSRA-001](../../enterprise-architecture/DSRA-001-reference-architecture.md).

## Template minimo ADR

```markdown
# ADR-000 - Titolo

| Campo | Valore |
|---|---|
| Stato | Proposed / Accepted / Superseded / Deprecated |
| Data | Da validare |
| Roadmap | DSG-MR-001 |
| Decisione correlata | TBD |

## Contesto

## Decisione

## Conseguenze

## ADR correlati o sostituiti

## Riferimenti
```

## Processo

1. Verificare se la decisione e reale e documentata.
2. Verificare che la decisione rientri in `DSG-MR-001`.
3. Collegare contesto, opzioni, decisione e conseguenze.
4. Collegare ADR correlati o sostituiti.
5. Aggiornare [Enterprise Registry](../registries/index.md) e [Release documentation](../release-documentation.md).

## Rischi

| ID | Rischio | Controllo |
|---|---|---|
| `DSG-ADR-RSK-001` | ADR creato per decisione non approvata | Roadmap Freeze Policy |
| `DSG-ADR-RSK-002` | Decisione architetturale non registrata | `QG-ARCH` |
| `DSG-ADR-RSK-003` | ADR tecnico scollegato dalla baseline enterprise | Registry e cross-reference |

## Elementi TBD

| ID | Elemento | Stato |
|---|---|
| `DSG-ADR-TBD-001` | ADR futuri per AI, Live Operations e Knowledge Graph | TBD, solo dopo decisione approvata |
| `DSG-ADR-TBD-002` | Eventuali relazioni di superseding tra ADR tecnici | Da validare |

## Riferimenti

- [DSG-MR-001](../../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [DSG-GOV-001](../governance.md)
- [Enterprise Registry](../registries/index.md)
- [Enterprise Assessment](../assessment.md)
