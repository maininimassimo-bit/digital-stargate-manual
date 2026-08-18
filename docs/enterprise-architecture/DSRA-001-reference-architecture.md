# DSRA-001 - Reference Architecture

| Campo | Valore |
|---|---|
| Identificativo | `DSRA-001` |
| Titolo | Reference Architecture |
| Stato | Approvato per baseline |
| Versione | 1.0 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |
| Policy applicabile | `DSG-GOV-001` - Roadmap Freeze Policy |

## Scopo

Definire la reference architecture operativa di Digital StarGate, traducendo la visione `DSRA-000` in viste di dominio, responsabilità PC Principale / EAGLE, vincoli, decisioni e riferimenti.

## Ambito

La reference architecture descrive i domini richiesti e li mappa alla roadmap congelata:

- Observatory;
- Automation;
- Network;
- Data;
- Documentation;
- Analytics;
- AI;
- Knowledge Graph;
- Web Portal.

## Principi

| ID | Principio | Applicazione |
|---|---|---|
| `DSRA-001-PRN-001` | Operational separation | PC Principale ed EAGLE hanno ruoli diversi |
| `DSRA-001-PRN-002` | Safety boundary | Automation e AI non superano vincoli safety |
| `DSRA-001-PRN-003` | Data lineage | Dati e analytics devono avere fonte e qualità |
| `DSRA-001-PRN-004` | Documentation as control | MkDocs è controllo e conoscenza pubblicabile |
| `DSRA-001-PRN-005` | TBD discipline | Dettagli mancanti restano marcati |

## Vista dei domini

| Dominio | Responsabilità | Nodo primario | Stato |
|---|---|---|---|
| Observatory | Struttura, strumenti, sessione osservativa | EAGLE / campo | AS-IS |
| Automation | Sequenze, sincronizzazione, controlli operativi | EAGLE | Transition |
| Network | Accesso remoto e connettività | EAGLE / infrastruttura | AS-IS / Transition |
| Data | Log, report, dataset, repository scientifico | EAGLE + PC Principale | Transition |
| Documentation | Manuale, roadmap, SOP, registri | PC Principale | AS-IS / Transition |
| Analytics | KPI, dashboard, reporting | PC Principale | Transition |
| AI | Assistenza e analisi governata | PC Principale | TO-BE |
| Knowledge Graph | Modello semantico conoscenza | PC Principale | TO-BE / TBD |
| Web Portal | Pubblicazione MkDocs e dashboard | PC Principale / GitHub Pages | AS-IS / Transition |

## Vista PC Principale

Il PC Principale è il centro di engineering:

- sviluppo;
- Git;
- documentazione;
- MkDocs;
- dashboard;
- portale;
- analytics;
- release;
- attività di engineering e governance.

Architetturalmente il PC Principale produce, valida e pubblica conoscenza. Non è descritto come nodo di controllo diretto safety dell'osservatorio.

## Vista EAGLE

L'EAGLE è il nodo operativo:

- gestione dell'osservatorio;
- acquisizione;
- controllo degli strumenti;
- telemetria;
- automazione;
- sincronizzazione;
- operazioni sul campo.

Architetturalmente l'EAGLE produce dati e stato operativo. Dettagli di telemetria, scheduling e sincronizzazione sono `Da validare`.

## Vista di interazione

```text
PC Principale
  -> Git / MkDocs / Analytics / Release / Governance
  -> riceve o consolida dati approvati

EAGLE
  -> Observatory / Acquisition / Automation / Telemetry
  -> produce dati operativi e osservativi

GitHub / Web Portal
  -> pubblica documentazione, dashboard e release validate
```

## AS-IS

AS-IS include manuale tecnico, portale MkDocs, documentazione osservatorio, EAGLE, software astronomico, rete, procedure operative, warehouse e analytics già documentati.

## Transition

Transition include:

- consolidamento della nuova sezione enterprise architecture;
- mapping domini -> roadmap -> documenti;
- collegamento tra DSRA, ADR, assessment e manuale tecnico;
- definizione TBD per Knowledge Graph e AI;
- quality gate per documentazione e dati.

## TO-BE

TO-BE include:

- live operations validate;
- data lineage completo;
- repository scientifico governato;
- Knowledge Graph formalizzato;
- AI assistiva con audit;
- release e governance automatizzabili solo se verificate.

## Relazioni con altri documenti

| Documento | Relazione |
|---|---|
| [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | Fonte gerarchica |
| [DSG-EAM-001](DSG-EAM-001-enterprise-architecture-meta-model.md) | Meta-modello |
| [DSRA-000](DSRA-000-vision-target-architecture.md) | Target architecture |
| [DSG-GOV-001](../enterprise/governance.md) | Governance e freeze policy |
| [ADR-004](../enterprise/adr/ADR-004-enterprise-documentation-baseline.md) | Baseline documentale |
| [DSRA Risk Assessment](../enterprise/DSRA-risk-assessment.md) | Risk assessment |
| [Assessment](../enterprise/assessment.md) | Assessment enterprise |

## Vincoli

- Nessuna nuova piattaforma fuori `DSG-MR-001`.
- Nessun nuovo programma fuori portfolio roadmap.
- Nessuna configurazione sensibile pubblicata.
- Nessuna AI autonoma su safety.
- Nessuna duplicazione della roadmap: questo documento è reference architecture.

## Decisioni

| ID | Decisione | Stato |
|---|---|---|
| `DSRA-001-DEC-001` | PC Principale governa engineering, analytics, release e documentazione | Approvata |
| `DSRA-001-DEC-002` | EAGLE governa operazioni sul campo e acquisizione | Approvata |
| `DSRA-001-DEC-003` | Knowledge Graph e AI restano TO-BE fino a validazione | Approvata |
| `DSRA-001-DEC-004` | I domini richiesti sono mapping architetturali della roadmap congelata | Approvata |

## Elementi TBD

| ID | Elemento | Stato |
|---|---|---|
| `DSRA-001-TBD-001` | Schema Knowledge Graph | TBD |
| `DSRA-001-TBD-002` | Contratti telemetria | Da validare |
| `DSRA-001-TBD-003` | Policy sincronizzazione | Da validare |
| `DSRA-001-TBD-004` | Controlli AI specifici per use case | TBD |
| `DSRA-001-TBD-005` | Asset/configuration registry completo | Da validare |

## Riferimenti

- `docs/enterprise-roadmap/DSG-MR-001-master-roadmap.md`
- `docs/enterprise/governance.md`
- `docs/enterprise/enterprise-architecture.md`
- `docs/enterprise/DSRA-risk-assessment.md`
- `docs/architecture/ADR-001-Session-Layer.md`
- `docs/architecture/ADR-002-Analytics-Quality-Gates.md`
- `docs/architecture/ADR-003-Warehouse-Engine.md`
- `docs/architecture/assessments/EA-001-Environment-Repository-Assessment.md`
- `docs/architecture/assessments/EA-002-Integrated-Repository-and-Warehouse-Assessment.md`
- `docs/architecture/assessments/PAA-001-Project-Architecture-Assessment.md`
