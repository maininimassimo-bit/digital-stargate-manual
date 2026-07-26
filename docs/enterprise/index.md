# Enterprise DSG-MR-001

| Campo | Valore |
|---|---|
| Raccolta | Documentazione enterprise Digital StarGate |
| Roadmap approvata | `DSG-MR-001` |
| Stato | Approvata per revisione |
| Versione | 1.0 |
| Responsabile | Massimo Mainini |
| Data baseline | 26/07/2026 |

## Scopo

Questa sezione raccoglie la baseline enterprise prevista dalla roadmap `DSG-MR-001`.

La baseline collega architettura, rischi, requisiti, decisioni, procedure operative, governance e release management in un unico sistema di tracciabilità per il portale Digital StarGate e per l'Osservatorio Astronomico Remoto di Manciano.

## Ambito

La documentazione copre:

- governo del programma documentale `DSG-MR-001`;
- architettura enterprise del portale, dell'osservatorio e della pipeline dati;
- Digital StarGate Risk Assessment;
- decisioni architetturali e registri di controllo;
- handbook per contributor, maintainer e stakeholder;
- procedure operative standard;
- assessment di maturità e readiness;
- governance documentale, tecnica e di rilascio;
- appendici, glossario e mapping.

## Mappa dei documenti

| Documento | ID | Scopo | Stato |
|---|---|---|---|
| [Master Roadmap](DSG-MR-001-master-roadmap.md) | `DSG-MR-001` | Obiettivi, milestone, deliverable e criteri di completamento | Approvata |
| [Enterprise Program Portfolio](program-portfolio.md) | `DSG-PRG-001` | Portfolio programmi, capability, controlli, rischi e KPI | Approvato per baseline |
| [Enterprise Architecture](enterprise-architecture.md) | `DSG-EA-001` | Vista integrata di domini, componenti, dati e deployment | Approvata per revisione |
| [DSRA](DSRA-risk-assessment.md) | `DSG-DSRA-001` | Registro rischi, controlli e mitigazioni | Approvata per revisione |
| [ADR-004](adr/ADR-004-enterprise-documentation-baseline.md) | `DSG-ADR-004` | Decisione sulla baseline documentale enterprise | Approvata |
| [Registri](registries/index.md) | `DSG-REG-001` | Requisiti, rischi, controlli, decisioni, deliverable e change log | Approvata per revisione |
| [Handbook](handbook.md) | `DSG-HBK-001` | Regole operative per autori, maintainer e revisori | Approvata per revisione |
| [SOP](sop.md) | `DSG-SOP-001` | Procedure standard per gestione documentale e operativa | Approvata per revisione |
| [Assessment](assessment.md) | `DSG-ASMT-001` | Metodo di valutazione e score di maturità | Approvata per revisione |
| [Governance](governance.md) | `DSG-GOV-001` | Ruoli, responsabilità, review e change management | Approvata per revisione |
| [Release documentation](release-documentation.md) | `DSG-REL-001` | Readiness, note di release e criteri di pubblicazione | Approvata per revisione |
| [Appendici](appendices.md) | `DSG-APP-001` | Glossario, template, mapping e riferimenti | Approvata per revisione |

## Principi di coerenza

Ogni documento della baseline:

- usa identificativi stabili;
- richiama `DSG-MR-001`;
- collega requisiti, rischi, controlli, evidenze e decisioni;
- collega programmi e capability al portfolio `DSG-PRG-001`;
- mantiene continuità con i capitoli del manuale tecnico esistenti;
- evita dati sensibili, credenziali o parametri non verificabili;
- prevede owner, stato, criteri di controllo e manutenzione.

## Collegamenti con il manuale tecnico

La sezione enterprise non sostituisce i capitoli tecnici esistenti. Li governa.

| Area manuale | Collegamento enterprise |
|---|---|
| Capitoli 1-15 | Contesto, architettura e domini tecnici |
| Capitoli 16-19 e 25-31 | SOP, sicurezza, manutenzione e incident management |
| Capitoli 20-24 e 32-34 | Governance, versioning, backup, sicurezza informatica e release |
| Capitoli 35-44 | Allegati tecnici, requisiti, FMEA, ruoli e accettazione |
| Analytics, Warehouse e Release Notes | Architettura dati, qualità, readiness e tracciabilità release |

## Stato della baseline

La baseline è considerata completa per revisione quando:

- tutti i documenti in tabella sono pubblicati in MkDocs;
- la navigazione include la sezione enterprise;
- ogni registro contiene riferimenti a `DSG-MR-001`;
- non sono presenti marcatori operativi aperti;
- i link interni principali sono risolti;
- la Pull Request verso `main` contiene il riepilogo delle milestone.
