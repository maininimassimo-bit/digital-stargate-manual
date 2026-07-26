# DSG-APP-001 - Appendici Enterprise

| Campo | Valore |
|---|---|
| Documento | Appendici Enterprise |
| Identificativo | `DSG-APP-001` |
| Roadmap | `DSG-MR-001` |
| Versione | 1.0 |
| Stato | Approvata per revisione |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## 1. Glossario

| Termine | Definizione |
|---|---|
| ADR | Architecture Decision Record, documento che registra una decisione architetturale |
| DSRA | Digital StarGate Risk Assessment |
| EAGLE | Computer operativo PrimaLuceLab installato presso l'osservatorio |
| Evidence | Evidenza verificabile usata per dimostrare un controllo |
| MkDocs | Generatore del portale documentale |
| Quality gate | Controllo obbligatorio prima di una pubblicazione o release |
| RPN | Risk Priority Number, prodotto di probabilità, impatto e rilevabilità |
| SOP | Standard Operating Procedure |
| Warehouse | Livello dati consolidato per analytics e storico |

## 2. Mapping documentale

| Roadmap | Documento | Registro |
|---|---|---|
| `DSG-MR-M1` | Master Roadmap e indice | Deliverable, change log |
| `DSG-MR-M2` | Enterprise Architecture, ADR-004 | Decisioni, requisiti |
| `DSG-MR-M3` | DSRA | Rischi, controlli |
| `DSG-MR-M4` | Handbook, SOP, Governance | Requisiti, controlli |
| `DSG-MR-M5` | Assessment, Release, Appendici | Deliverable, readiness |

## 3. Template requisito

```markdown
| Campo | Valore |
|---|---|
| ID | DSG-REQ-AREA-000 |
| Titolo |  |
| Categoria |  |
| Priorità |  |
| Stato | Proposto |
| Fonte | DSG-MR-001 |
| Verifica |  |
| Owner |  |
```

## 4. Template rischio

```markdown
| Campo | Valore |
|---|---|
| ID | DSG-RSK-AREA-000 |
| Rischio |  |
| Area |  |
| Probabilità | 1-5 |
| Impatto | 1-5 |
| Rilevabilità | 1-5 |
| Controlli |  |
| Stato | Proposto |
```

## 5. Template ADR

```markdown
# ADR-000 - Titolo

## Contesto

## Opzioni considerate

## Decisione

## Conseguenze

## Collegamenti
```

## 6. Template SOP

```markdown
# DSG-SOP-AREA-000 - Titolo

| Campo | Valore |
|---|---|
| Trigger |  |
| Ruoli |  |
| Output |  |
| Controlli |  |

## Passi

## Criteri di controllo
```

## 7. Riferimenti interni

- [Master Roadmap](DSG-MR-001-master-roadmap.md)
- [Enterprise Architecture](enterprise-architecture.md)
- [DSRA](DSRA-risk-assessment.md)
- [Registri](registries/index.md)
- [Governance](governance.md)
- [Release documentation](release-documentation.md)

## 8. Regole di aggiornamento appendici

Le appendici devono essere aggiornate quando:

- viene introdotto un nuovo prefisso ID;
- un template cambia forma;
- una milestone della roadmap aggiunge un tipo documentale;
- un termine tecnico diventa ricorrente nei documenti enterprise;
- un mapping non rappresenta più lo stato reale della baseline.
