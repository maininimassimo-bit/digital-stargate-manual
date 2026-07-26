# DSG-REG-001 - Registri e tracciabilità

| Campo | Valore |
|---|---|
| Documento | Registri enterprise |
| Identificativo | `DSG-REG-001` |
| Roadmap | `DSG-MR-001` |
| Versione | 1.0 |
| Stato | Approvata per revisione |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## 1. Scopo

Questo documento centralizza i registri minimi richiesti dalla roadmap `DSG-MR-001`: requisiti, decisioni, rischi, controlli, deliverable, change log e release readiness.

I registri sono progettati per essere leggibili in MkDocs e revisionabili in Pull Request.

## 2. Stati standard

| Stato | Uso |
|---|---|
| Proposto | Elemento identificato ma non ancora approvato |
| Approvato | Elemento valido e applicabile |
| In trattamento | Azione o controllo in corso |
| Verificato | Evidenza disponibile e accettata |
| Sospeso | Elemento valido ma temporaneamente non applicato |
| Superato | Elemento sostituito da decisione o requisito successivo |

## 3. Registro requisiti

| ID | Requisito | Categoria | Priorità | Stato | Fonte | Verifica |
|---|---|---|---|---|---|---|
| `DSG-REQ-DOC-001` | Ogni documento enterprise deve richiamare `DSG-MR-001` | Documentale | Alta | Verificato | Roadmap | Revisione contenuti |
| `DSG-REQ-DOC-002` | Ogni pagina enterprise pubblicata deve essere raggiungibile da MkDocs | Documentale | Alta | Verificato | Roadmap | `mkdocs.yml` |
| `DSG-REQ-ARC-001` | Ogni componente critico deve avere dominio, responsabilità e controllo associato | Architettura | Alta | Verificato | `DSG-EA-001` | Matrice componenti |
| `DSG-REQ-SAF-001` | Le procedure operative devono privilegiare lo stato conservativo in condizioni incerte | Safety | Critica | Approvato | DSRA, FMEA | SOP incident |
| `DSG-REQ-OPS-001` | Avvio e chiusura osservatorio devono essere supportati da checklist | Operativo | Alta | Approvato | Manuale tecnico | Registro sessione |
| `DSG-REQ-OPS-002` | Gli incidenti devono produrre log, decisione e azione correttiva | Operativo | Alta | Approvato | DSRA | Post-mortem |
| `DSG-REQ-GOV-001` | Ogni modifica strutturale deve passare da review e change log | Governance | Alta | Approvato | `DSG-GOV-001` | PR e registro |
| `DSG-REQ-ADR-001` | Le decisioni architetturali rilevanti devono essere registrate in ADR | Governance | Alta | Verificato | `DSG-ADR-004` | Registro decisioni |
| `DSG-REQ-REL-001` | Ogni release documentale deve avere criteri di readiness e rollback | Release | Alta | Approvato | `DSG-REL-001` | Checklist release |
| `DSG-REQ-QA-001` | Link, navigazione e marcatori aperti devono essere controllati prima della PR | Qualità | Alta | Approvato | Handbook | Validazione documentale |

## 4. Registro decisioni

| ID | Decisione | Stato | Documento | Impatto |
|---|---|---|---|---|
| `DSG-ADR-001` | Session Layer | Approvata | `architecture/ADR-001-Session-Layer.md` | Struttura dati sessioni |
| `DSG-ADR-002` | Analytics Quality Gates | Approvata | `architecture/ADR-002-Analytics-Quality-Gates.md` | Controllo qualità analytics |
| `DSG-ADR-003` | Warehouse Engine | Approvata | `architecture/ADR-003-Warehouse-Engine.md` | Consolidamento dati |
| `DSG-ADR-004` | Enterprise documentation baseline | Approvata | `enterprise/adr/ADR-004-enterprise-documentation-baseline.md` | Governance `DSG-MR-001` |

## 5. Registro rischi

| ID | Rischio | Classe | Stato | Controlli |
|---|---|---|---|---|
| `DSG-RSK-OPS-001` | Cupola o safety incoerente | Medio | Mitigato | `DSG-CTL-SAF-001`, `DSG-CTL-OPS-001` |
| `DSG-RSK-OPS-002` | Montatura non in park | Medio | Mitigato | `DSG-CTL-SAF-001`, `DSG-CTL-OPS-001` |
| `DSG-RSK-NET-001` | Perdita connettività o VPN | Medio | Mitigato | `DSG-CTL-NET-001` |
| `DSG-RSK-INF-001` | Indisponibilità EAGLE o USB | Alto | In trattamento | `DSG-CTL-INF-001` |
| `DSG-RSK-DATA-001` | Divergenza report/warehouse/dashboard | Alto | In trattamento | `DSG-CTL-DATA-001` |
| `DSG-RSK-DOC-001` | Documenti non raggiungibili | Basso | Mitigato | `DSG-CTL-DOC-001` |
| `DSG-RSK-GOV-001` | Decisioni non registrate | Medio | Mitigato | `DSG-CTL-ADR-001` |
| `DSG-RSK-REL-001` | Release senza readiness completa | Medio | Mitigato | `DSG-CTL-REL-001` |

## 6. Registro controlli

| ID | Controllo | Tipo | Frequenza | Evidenza |
|---|---|---|---|---|
| `DSG-CTL-DOC-001` | Navigazione MkDocs aggiornata | Preventivo | Ogni PR documentale | Diff `mkdocs.yml` |
| `DSG-CTL-QA-001` | Controllo link interni e marcatori aperti | Preventivo | Ogni PR documentale | Log validazione |
| `DSG-CTL-ADR-001` | ADR per decisioni strutturali | Preventivo | Quando necessario | ADR approvato |
| `DSG-CTL-SAF-001` | Verifica stato conservativo | Preventivo | Ogni sessione | Checklist |
| `DSG-CTL-NET-001` | Test VPN e failover | Detective | Periodico | Registro test |
| `DSG-CTL-DATA-001` | Quality gate dataset | Detective | Ogni aggiornamento dati | Report analytics |
| `DSG-CTL-REL-001` | Release readiness | Preventivo | Ogni release | Checklist release |

## 7. Registro deliverable

| ID | Deliverable | Stato | Percorso |
|---|---|---|---|
| `DSG-DEL-001` | Master Roadmap | Verificato | `docs/enterprise/DSG-MR-001-master-roadmap.md` |
| `DSG-DEL-002` | Enterprise Architecture | Verificato | `docs/enterprise/enterprise-architecture.md` |
| `DSG-DEL-003` | DSRA | Verificato | `docs/enterprise/DSRA-risk-assessment.md` |
| `DSG-DEL-004` | ADR-004 | Verificato | `docs/enterprise/adr/ADR-004-enterprise-documentation-baseline.md` |
| `DSG-DEL-005` | Registri | Verificato | `docs/enterprise/registries/index.md` |
| `DSG-DEL-006` | Handbook | Verificato | `docs/enterprise/handbook.md` |
| `DSG-DEL-007` | SOP | Verificato | `docs/enterprise/sop.md` |
| `DSG-DEL-008` | Assessment | Verificato | `docs/enterprise/assessment.md` |
| `DSG-DEL-009` | Governance | Verificato | `docs/enterprise/governance.md` |
| `DSG-DEL-010` | Release documentation | Verificato | `docs/enterprise/release-documentation.md` |
| `DSG-DEL-011` | Appendici | Verificato | `docs/enterprise/appendices.md` |

## 8. Change log

| ID | Data | Cambiamento | Tipo | Stato |
|---|---|---|---|---|
| `DSG-CHG-001` | 26/07/2026 | Creazione baseline enterprise `DSG-MR-001` | Documentazione | Verificato |
| `DSG-CHG-002` | 26/07/2026 | Aggiunta sezione enterprise in MkDocs | Navigazione | Verificato |
| `DSG-CHG-003` | 26/07/2026 | Collegamento DSRA, ADR e governance | Tracciabilità | Verificato |

## 9. Regole di manutenzione

- Un nuovo requisito deve avere categoria, priorità, fonte e verifica.
- Un nuovo rischio medio o superiore deve avere almeno un controllo.
- Un controllo deve produrre un'evidenza osservabile.
- Una decisione strutturale deve avere un ADR.
- Un deliverable è verificato solo se è raggiungibile da MkDocs o escluso in modo esplicito.
