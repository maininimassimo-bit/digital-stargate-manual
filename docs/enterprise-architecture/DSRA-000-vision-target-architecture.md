# DSRA-000 - Vision Target Architecture

| Campo | Valore |
|---|---|
| Identificativo | `DSRA-000` |
| Titolo | Vision Target Architecture |
| Stato | Approvato per baseline |
| Versione | 1.0 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |
| Policy applicabile | `DSG-GOV-001` - Roadmap Freeze Policy |

## Scopo

Descrivere la target architecture di Digital StarGate in coerenza con `DSG-MR-001`, distinguendo chiaramente AS-IS, Transition e TO-BE e preservando il modello operativo PC Principale / EAGLE.

## Ambito

Il documento copre la visione architetturale dei domini Observatory, Automation, Network, Data, Documentation, Analytics, AI, Knowledge Graph e Web Portal.

Sono esclusi dettagli tecnici non documentati, configurazioni operative sensibili e qualsiasi programma non previsto dalla roadmap congelata.

## Principi

- La target architecture deriva dalla roadmap, non la estende.
- Le capacità AI e Knowledge Graph restano TO-BE finché non sono approvate e validate.
- Le funzioni safety non sono delegate a AI o automazioni non approvate.
- Il PC Principale governa engineering e pubblicazione.
- L'EAGLE governa operatività sul campo e acquisizione.

## Architettura AS-IS

| Dominio | Stato AS-IS | Evidenza |
|---|---|---|
| Observatory | Documentato nel manuale tecnico | Capitoli osservatorio e sistema astronomico |
| Automation | Procedure e software documentati | Capitoli automazione e acquisizione |
| Network | Infrastruttura e accesso remoto documentati | Capitoli rete e sicurezza |
| Data | Gestione dati e warehouse documentati | Sezioni dati e Warehouse |
| Documentation | MkDocs e manuale operativi | `mkdocs.yml` e capitoli release |
| Analytics | Dashboard e report presenti | Sezione Analytics |
| AI | Non baseline | `TBD` |
| Knowledge Graph | Non implementato come capability approvata | `TBD` |
| Web Portal | Portale MkDocs operativo | Home, Analytics, Release Notes |

## Architettura Transition

La fase Transition consolida i domini AS-IS in una piattaforma governata:

- roadmap e registri diventano fonte di tracciabilità;
- warehouse e analytics vengono collegati a quality gate;
- documentazione e release seguono governance esplicita;
- Automation e Live Operations vengono trattate con controlli safety;
- AI e Knowledge Graph ricevono governance prima di qualsiasi implementazione.

## Architettura TO-BE

La visione TO-BE è una piattaforma data-driven con:

- Observatory governato da procedure e registri;
- Automation verificabile e soggetta a safety;
- Network resiliente e documentato;
- Data layer con schema, qualità e lineage;
- Documentation layer come fonte di conoscenza;
- Analytics layer con KPI affidabili;
- AI assistiva, auditabile e non autonoma su safety;
- Knowledge Graph come modello semantico della conoscenza, `TBD`;
- Web Portal come punto di accesso a manuale, dashboard e stato.

## Modello operativo approvato

| Nodo | Responsabilità | Stato |
|---|---|---|
| PC Principale | sviluppo, Git, documentazione, MkDocs, dashboard, portale, analytics, release, engineering governance | AS-IS / Transition |
| EAGLE | gestione osservatorio, acquisizione, controllo strumenti, telemetria, automazione, sincronizzazione, operazioni sul campo | AS-IS / Transition |

Il TO-BE mantiene questa separazione: il PC Principale non sostituisce il nodo operativo e l'EAGLE non diventa sorgente primaria della governance documentale.

## Relazioni tra domini

```text
Observatory -> Automation -> Data -> Analytics -> Web Portal
       |            |          |          |          |
       v            v          v          v          v
     Network ---- EAGLE ---- Documentation ---- Knowledge Graph
                                      |
                                      v
                                      AI
```

Il diagramma è concettuale. Interfacce, protocolli, frequenze di sincronizzazione e contratti telemetria sono `Da validare`.

## Relazioni con altri documenti

| Documento | Relazione |
|---|---|
| [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | Fonte gerarchica e roadmap congelata |
| [DSG-EAM-001](DSG-EAM-001-enterprise-architecture-meta-model.md) | Meta-modello |
| [DSRA-001](DSRA-001-reference-architecture.md) | Reference architecture operativa |
| [DSG-GOV-001](../enterprise/governance.md) | Governance, quality gate, freeze policy |
| [DSRA Risk Assessment](../enterprise/DSRA-risk-assessment.md) | Rischi e controlli |
| [Assessment](../enterprise/assessment.md) | Valutazione maturità |

## Vincoli

- Non spostare responsabilità operative safety dall'EAGLE a componenti AI.
- Non creare nuove piattaforme oltre quelle previste da `DSG-MR-001`.
- Non pubblicare parametri di rete, credenziali o configurazioni sensibili.
- Non dichiarare implementato il Knowledge Graph.
- Non dichiarare operativa l'AI senza governance e use case approvati.

## Decisioni

| ID | Decisione | Stato |
|---|---|---|
| `DSRA-000-DEC-001` | La target architecture usa `DSG-MR-001` come fonte primaria | Approvata |
| `DSRA-000-DEC-002` | PC Principale ed EAGLE mantengono responsabilità separate | Approvata |
| `DSRA-000-DEC-003` | AI e Knowledge Graph sono TO-BE e richiedono governance dedicata | Approvata |

## Elementi TBD

| ID | Elemento | Stato |
|---|---|---|
| `DSRA-000-TBD-001` | Contratti dati per telemetria live | Da validare |
| `DSRA-000-TBD-002` | Modello Knowledge Graph | TBD |
| `DSRA-000-TBD-003` | Use case AI approvati | TBD |
| `DSRA-000-TBD-004` | Frequenza sincronizzazione EAGLE -> PC Principale / repository | Da validare |

## Riferimenti

- `docs/enterprise-roadmap/DSG-MR-001-master-roadmap.md`
- `docs/enterprise/governance.md`
- `docs/enterprise/sop.md`
- `docs/enterprise/DSRA-risk-assessment.md`
- `docs/chapters/05-infrastruttura-rete.md`
- `docs/chapters/06-eagle.md`
- `docs/chapters/15-automazione.md`
- `docs/chapters/28-gestione-dati-archiviazione.md`
- `docs/analytics/index.md`
