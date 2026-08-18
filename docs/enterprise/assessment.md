# DSG-ASMT-001 - Enterprise Assessment Baseline

| Campo | Valore |
|---|---|
| Documento | Enterprise Assessment Baseline |
| Identificativo | `DSG-ASMT-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.1 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |

## 1. Scopo

Valutare la maturita della baseline `DSG-MR-001` rispetto a documentazione, architettura, rischi, operativita, governance, dati, release e visione.

Il documento separa evidenze, analisi, conclusioni e raccomandazioni. Le informazioni non confermate sono marcate `TBD` o `Da validare`.

## 2. Ambito

Sono inclusi technical assessments, operational assessments, documentation assessment, release readiness assessment e governance/registry assessment. Sono escluse misure operative non presenti nel branch o non verificabili nel runtime.

## 3. Metodo

| Punteggio | Significato |
|---:|---|
| 0 | Non presente |
| 1 | Presente in forma frammentaria |
| 2 | Presente ma non governato |
| 3 | Adeguato per uso operativo |
| 4 | Maturo e tracciabile |
| 5 | Baseline completa, verificabile e mantenibile |

## 4. Evidenze

| ID | Evidenza | Fonte | Data | Stato |
|---|---|---|---|---|
| `DSG-ASMT-EVD-001` | Master Roadmap pubblicata | [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md) | 26/07/2026 | Verificato |
| `DSG-ASMT-EVD-002` | Meta-modello e reference architecture | [DSG-EAM-001](../enterprise-architecture/DSG-EAM-001-enterprise-architecture-meta-model.md), [DSRA-001](../enterprise-architecture/DSRA-001-reference-architecture.md) | 26/07/2026 | Verificato |
| `DSG-ASMT-EVD-003` | Portfolio, registry e governance | [Portfolio](program-portfolio.md), [Registri](registries/index.md), [Governance](governance.md) | 26/07/2026 | Verificato |
| `DSG-ASMT-EVD-004` | SOP e handbook | [SOP](sop.md), [Handbook](handbook.md) | 26/07/2026 | Verificato |
| `DSG-ASMT-EVD-005` | Manuale tecnico esposto in MkDocs | Capitoli tecnici in `mkdocs.yml` | Da validare | AS-IS via navigazione |
| `DSG-ASMT-EVD-006` | Build MkDocs locale | Runtime corrente | 26/07/2026 | Non eseguito, MkDocs non disponibile |

## 5. Technical Assessment

| Area | Score | Analisi | Rischi | Raccomandazioni |
|---|---:|---|---|---|
| Architecture baseline | 4 | Meta-modello, target e reference architecture presenti | Drift tra TO-BE e implementato | Mantenere ADR per decisioni reali |
| Warehouse/Data | 3 | Documentazione warehouse presente in MkDocs; contratti dati finali non verificati | KPI non confrontabili | Versionare schema e data catalog |
| Portal/MkDocs | 4 | Navigazione enterprise aggiornata | Build non eseguito nel runtime | Eseguire build su PC/GitHub Actions |
| Configuration | 3 | Configuration Registry presente | Mapping asset-config incompleto | Audit configurazioni pubblicabili |

Conclusione tecnica: baseline idonea alla review, con dettagli quantitativi e configurazioni da validare.

## 6. Operational Assessment

| Area | Score | Analisi | Rischi | Raccomandazioni |
|---|---:|---|---|---|
| Operations | 4 | SOP enterprise e capitoli operativi collegati | Evidenze reali dipendono dalle prossime sessioni | Collegare checklist e log |
| Safety | 4 | Safety-first e stato conservativo documentati | Feed live non validati | Non usare Live/AI per safety senza ADR |
| Incident/DR | 3 | SOP incident e DR presenti | RTO/RPO non definiti | Pianificare test restore e post-mortem |
| Security | 4 | Security governance e controlli presenti | Tooling scanning non definito | Formalizzare scansione automatica |

Conclusione operativa: adeguata per baseline documentale; maturita operativa piena richiede evidenze sul campo.

## 7. Documentation and Governance Assessment

| Area | Score | Evidenza | Valutazione |
|---|---:|---|---|
| Roadmap | 5 | `DSG-MR-001` | Completa |
| Portfolio | 5 | `DSG-PRG-001` | Completa |
| Registri | 5 | `DSG-REG-001` | Completa per baseline |
| Governance | 5 | `DSG-GOV-001` | Completa per baseline |
| ADR | 4 | ADR Index e ADR esistenti | Nessun ADR inventato |
| SOP | 4 | `DSG-SOP-001` | Completa per baseline |
| Handbook | 4 | `DSG-HBK-001` | Completa per workflow |
| Release | 4 | `DSG-REL-001` | Struttura pronta |
| Knowledge | 4 | Knowledge Index e Appendici | Completa per baseline |

Score medio baseline: `4,2 / 5`.

## 8. Gap e raccomandazioni

| ID | Gap | Impatto | Raccomandazione | Priorita |
|---|---|---|---|---|
| `DSG-GAP-001` | Evidenze operative reali future | Medio | Collegare checklist dopo sessioni | Media |
| `DSG-GAP-002` | Test failover/rete non verificato nel runtime | Medio | Pianificare registro test rete | Media |
| `DSG-GAP-003` | Data catalog e metadata scientifici finali | Alto | Definire schema quando approvato | Alta |
| `DSG-GAP-004` | Build MkDocs non disponibile nel runtime | Medio | Eseguire su PC Principale/GitHub Actions | Alta |
| `DSG-GAP-005` | RTO/RPO DR non confermati | Medio | Definire dopo test restore | Media |

## 9. Criteri di accettazione

La baseline e idonea alla review quando documenti pubblicabili sono in MkDocs, registry e traceability matrix coprono i deliverable, ADR non inventano decisioni, SOP includono gestione errori e rollback, TBD residui sono espliciti e security check non trova contenuti sensibili.

## 10. Elementi TBD

| ID | Elemento | Stato |
|---|---|
| `DSG-ASMT-TBD-001` | Evidenze operative da sessioni reali | Da validare |
| `DSG-ASMT-TBD-002` | Soglie quantitative KPI | TBD |
| `DSG-ASMT-TBD-003` | RTO/RPO e test DR | Da validare |
| `DSG-ASMT-TBD-004` | Tooling automatico build/link/security | TBD |

## 11. Riferimenti

- [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [Planning](planning.md)
- [Governance](governance.md)
- [SOP](sop.md)
- [Release documentation](release-documentation.md)
