# DSG-EAM-001 - Enterprise Architecture Meta Model

| Campo | Valore |
|---|---|
| Identificativo | `DSG-EAM-001` |
| Titolo | Enterprise Architecture Meta Model |
| Stato | Approvato per baseline |
| Versione | 1.0 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |
| Policy applicabile | `DSG-GOV-001` - Roadmap Freeze Policy |

## Scopo

Definire il meta-modello architetturale enterprise di Digital StarGate, cioè il modo con cui roadmap, domini, capability, piattaforme, componenti, asset, configurazioni, documenti, decisioni e controlli vengono collegati senza introdurre ambiti non previsti dalla roadmap congelata `DSG-MR-001`.

## Ambito

Il meta-modello copre i domini architetturali richiesti:

- Observatory;
- Automation;
- Network;
- Data;
- Documentation;
- Analytics;
- AI;
- Knowledge Graph;
- Web Portal.

`Automation` e `Knowledge Graph` sono trattati come domini architetturali derivati da capability già previste in `DSG-MR-001`; non costituiscono nuovi programmi indipendenti.

## Principi

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-EAM-PRN-001` | Roadmap-first | `DSG-MR-001` governa programmi, capability e confini |
| `DSG-EAM-PRN-002` | Freeze compliance | Nessun nuovo programma, piattaforma o dominio fuori roadmap |
| `DSG-EAM-PRN-003` | AS-IS / Transition / TO-BE | Ogni elemento architetturale dichiara lo stato |
| `DSG-EAM-PRN-004` | Evidence-based | Le informazioni non confermate restano `TBD` o `Da validare` |
| `DSG-EAM-PRN-005` | Separation of concerns | PC Principale ed EAGLE hanno responsabilità distinte |

## Architettura del meta-modello

```text
DSG-MR-001
  -> Program Portfolio
  -> Platform Domain
  -> Capability
  -> Component
  -> Asset / Configuration
  -> Document / ADR / Assessment
  -> Risk / Control / Quality Gate
  -> Release Evidence
```

## Entità del meta-modello

| Entità | Descrizione | Stato |
|---|---|---|
| Roadmap | Fonte gerarchica e perimetro congelato | AS-IS |
| Domain | Vista logica della piattaforma | Transition |
| Capability | Capacità governabile collegata alla roadmap | Transition |
| Component | Elemento tecnico o documentale identificabile | AS-IS / Transition |
| Asset | Oggetto fisico, digitale o informativo | Da validare |
| Configuration | Parametro o configurazione pubblicabile o sensibile | Da validare |
| Evidence | Log, checklist, commit, report, build o review | Transition |
| Decision | ADR o decisione registrata | AS-IS / Transition |

## Domini architetturali

| Dominio | Programma roadmap collegato | Stato | Note |
|---|---|---|---|
| Observatory | Observatory | AS-IS | Sistema astronomico e struttura osservativa |
| Automation | Operations / Live Operations | Transition | Automazione operativa, non nuovo programma |
| Network | Infrastructure / Security | AS-IS / Transition | Accesso remoto e connettività |
| Data | Data / Image and Scientific Repository | Transition | Dataset, sessioni, repository scientifico |
| Documentation | Documentation | AS-IS / Transition | MkDocs, registri, handbook, SOP |
| Analytics | Analytics and Reporting | Transition | KPI, dashboard, report |
| AI | AI | TO-BE | Casi d'uso e strumenti `TBD` |
| Knowledge Graph | Knowledge | TO-BE | Modello semantico `TBD` |
| Web Portal | Documentation / Analytics | AS-IS / Transition | Portale MkDocs e viste pubblicate |

## Modello operativo approvato

### PC Principale

Il PC Principale è il nodo di engineering e governance.

Responsabilità approvate:

- sviluppo;
- Git;
- documentazione;
- MkDocs;
- dashboard;
- portale;
- analytics;
- release;
- attività di engineering e governance.

### EAGLE

L'EAGLE è il nodo operativo sul campo.

Responsabilità approvate:

- gestione dell'osservatorio;
- acquisizione;
- controllo degli strumenti;
- telemetria;
- automazione;
- sincronizzazione;
- operazioni sul campo.

## Relazioni con altri documenti

| Documento | Relazione |
|---|---|
| [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | Fonte gerarchica |
| [DSG-GOV-001](../enterprise/governance.md) | Governance e freeze policy |
| [DSG-ADR-004](../enterprise/adr/ADR-004-enterprise-documentation-baseline.md) | Decisione baseline documentale |
| [DSG-EA-001](../enterprise/enterprise-architecture.md) | Baseline enterprise precedente da non duplicare |
| [DSRA](../enterprise/DSRA-risk-assessment.md) | Rischi e controlli |
| [Assessment](../enterprise/assessment.md) | Valutazione maturità |

## Vincoli

- Non introdurre programmi non presenti in `DSG-MR-001`.
- Non trattare `Knowledge Graph` come piattaforma implementata.
- Non pubblicare configurazioni operative sensibili.
- Non duplicare documenti esistenti: questo documento definisce il meta-modello, non una nuova roadmap.
- Usare `TBD` o `Da validare` per dettagli non confermati.

## Decisioni

| ID | Decisione | Stato |
|---|---|---|
| `DSG-EAM-DEC-001` | `DSG-MR-001` è la fonte gerarchica primaria | Approvata |
| `DSG-EAM-DEC-002` | I domini richiesti sono viste architetturali, non nuovi programmi | Approvata |
| `DSG-EAM-DEC-003` | PC Principale ed EAGLE restano separati per responsabilità | Approvata |

## Elementi TBD

| ID | Elemento | Motivazione |
|---|---|---|
| `DSG-EAM-TBD-001` | Schema formale del Knowledge Graph | Non presente nella roadmap come implementazione approvata |
| `DSG-EAM-TBD-002` | Registro asset completo | Da consolidare con inventario e configurazioni |
| `DSG-EAM-TBD-003` | Contratti telemetria EAGLE | Da validare sul campo |

## Riferimenti

- `docs/enterprise-roadmap/DSG-MR-001-master-roadmap.md`
- `docs/enterprise/governance.md`
- `docs/enterprise/enterprise-architecture.md`
- `docs/enterprise/DSRA-risk-assessment.md`
- `docs/architecture/ADR-001-Session-Layer.md`
- `docs/architecture/ADR-002-Analytics-Quality-Gates.md`
- `docs/architecture/ADR-003-Warehouse-Engine.md`
- `docs/architecture/assessments/PAA-001-Project-Architecture-Assessment.md`
