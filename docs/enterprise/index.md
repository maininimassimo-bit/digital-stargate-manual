# Enterprise DSG-MR-001

| Campo | Valore |
|---|---|
| Raccolta | Documentazione enterprise Digital StarGate |
| Roadmap approvata | `DSG-MR-001` |
| Stato | Approvata per revisione |
| Versione | 1.1 |
| Responsabile | Massimo Mainini |
| Data baseline | 26/07/2026 |

## Scopo

Questa sezione raccoglie la baseline enterprise prevista dalla roadmap `DSG-MR-001`.

La baseline collega architettura, rischi, requisiti, decisioni, procedure operative, governance, planning, knowledge management e release management in un unico sistema di tracciabilita.

## Ambito

La documentazione copre roadmap, architecture baseline, program portfolio, registri, ADR, assessment, SOP, handbook, planning, governance, release, project history, knowledge index, vision e appendici.

## Mappa dei documenti

| Documento | ID | Scopo | Stato |
|---|---|---|---|
| [Master Roadmap](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | `DSG-MR-001` | Obiettivi, milestone, deliverable e criteri di completamento | Approvata |
| [Enterprise Program Portfolio](program-portfolio.md) | `DSG-PRG-001` | Portfolio programmi, capability, controlli, rischi e KPI | Approvato per baseline |
| [Enterprise Planning Framework](planning.md) | `DSG-PLAN-001` | Release, milestone, sprint, roadmap 2026-2030, dipendenze, rischi e KPI | Approvato per baseline |
| [Enterprise Architecture](enterprise-architecture.md) | `DSG-EA-001` | Vista integrata di domini, componenti, dati e deployment | Approvata per revisione |
| [DSRA](DSRA-risk-assessment.md) | `DSG-DSRA-001` | Registro rischi, controlli e mitigazioni | Approvata per revisione |
| [ADR Index](adr/index.md) | `DSG-ADR-INDEX-001` | Indice e governance degli Architecture Decision Records | Approvato per baseline |
| [ADR-004](adr/ADR-004-enterprise-documentation-baseline.md) | `DSG-ADR-004` | Decisione sulla baseline documentale enterprise | Approvata |
| [Registri](registries/index.md) | `DSG-REG-001` | Registry e tracciabilita enterprise | Approvata per revisione |
| [Handbook](handbook.md) | `DSG-HBK-001` | Engineering workflow e quality gates | Approvato per baseline |
| [SOP](sop.md) | `DSG-SOP-001` | Procedure standard con error handling e rollback | Approvato per baseline |
| [Assessment](assessment.md) | `DSG-ASMT-001` | Evidenze, analisi, conclusioni e raccomandazioni | Approvato per baseline |
| [Governance](governance.md) | `DSG-GOV-001` | Framework di governance e Roadmap Freeze Policy | Approvato per baseline |
| [Release documentation](release-documentation.md) | `DSG-REL-001` | Readiness, release notes e rollback | Approvato per baseline |
| [Project History](project-history.md) | `DSG-HIST-001` | Storia documentale e milestone baseline | Approvato per baseline |
| [Knowledge Index](knowledge-index.md) | `DSG-KNW-INDEX-001` | Indice documentale, traceability matrix, glossario e riferimenti | Approvato per baseline |
| [Long-Term Vision](vision.md) | `DSG-VISION-001` | Vision 2030, Vision 2035 e Continuous Evolution | Approvato per baseline |
| [Appendici](appendices.md) | `DSG-APP-001` | Glossario, template, mapping e riferimenti | Approvato per baseline |

## Gerarchia documentale

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

## Principi di coerenza

Ogni documento della baseline usa identificativi stabili, richiama `DSG-MR-001`, collega requisiti/rischi/controlli/evidenze/decisioni, mantiene continuita con il manuale tecnico, evita contenuti sensibili e usa `TBD` o `Da validare` quando un dato non e confermato.

## Collegamenti con il manuale tecnico

La sezione enterprise non sostituisce i capitoli tecnici esistenti. Li governa.

| Area manuale | Collegamento enterprise |
|---|---|
| Capitoli 1-15 | Contesto, architettura e domini tecnici |
| Capitoli 16-19 e 25-31 | SOP, sicurezza, manutenzione e incident management |
| Capitoli 20-24 e 32-34 | Governance, versioning, backup, sicurezza informatica e release |
| Capitoli 35-44 | Allegati tecnici, requisiti, FMEA, ruoli e accettazione |
| Analytics, Warehouse e Release Notes | Architettura dati, qualita, readiness e tracciabilita release |

## Stato della baseline

La baseline e considerata completa per review quando tutti i documenti in tabella sono pubblicati in MkDocs, la navigazione include la sezione enterprise, i registri contengono riferimenti a `DSG-MR-001`, i link interni principali sono risolti o i limiti sono documentati e la PR verso `main` contiene il riepilogo delle milestone.
