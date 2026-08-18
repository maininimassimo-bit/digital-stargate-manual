# DSG-REL-001 - Release Documentation and Notes Structure

| Campo | Valore |
|---|---|
| Documento | Release Documentation and Notes Structure |
| Identificativo | `DSG-REL-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.1 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |

## 1. Scopo

Definire release strategy, release readiness, rollback e struttura delle release notes per la baseline documentale `DSG-MR-001`.

## 2. Ambito

Include release documentation, release notes structure, readiness checklist, rollback, evidenze, follow-up e collegamento a project history.

## 3. Release scope

La baseline include Master Roadmap, Enterprise Architecture baseline, Program Portfolio, Enterprise Registry, Governance Framework, ADR Index, Assessment, SOP, Engineering Handbook, Planning, Knowledge Index, Project History, Vision e Appendici.

## 4. Release notes structure

```markdown
# Release YYYY.N - Titolo

## Summary

## Scope

## Added

## Changed

## Validation

## Risks and TBD

## Rollback

## References
```

## 5. Readiness checklist

| ID | Controllo | Esito atteso |
|---|---|---|
| `DSG-REL-RDY-001` | Deliverable previsti presenti | Conforme |
| `DSG-REL-RDY-002` | `mkdocs.yml` aggiornato e valido | Conforme |
| `DSG-REL-RDY-003` | Link relativi principali verificati | Conforme o limite documentato |
| `DSG-REL-RDY-004` | Registry aggiornato | Conforme |
| `DSG-REL-RDY-005` | ADR Index presente e collegato | Conforme |
| `DSG-REL-RDY-006` | SOP e Handbook aggiornati | Conforme |
| `DSG-REL-RDY-007` | Assessment con evidenze/analisi/conclusioni | Conforme |
| `DSG-REL-RDY-008` | Security check senza finding | Conforme |
| `DSG-REL-RDY-009` | Build MkDocs strict | Da eseguire su PC/GitHub Actions se runtime non disponibile |

## 6. Release process

1. Confermare milestone e scope.
2. Aggiornare registry e traceability.
3. Verificare MkDocs YAML.
4. Verificare link Markdown relativi.
5. Verificare assenza contenuti sensibili.
6. Eseguire build MkDocs se disponibile.
7. Registrare limiti e TBD.
8. Creare commit logici.
9. Aprire PR solo quando richiesto.

## 7. Rollback

| Scenario | Azione |
|---|---|
| Errore in navigazione | Correggere o rimuovere voce `mkdocs.yml` |
| Link errato | Correggere link relativo e validare |
| Documento duplicato | Consolidare nella fonte corretta |
| Contenuto sensibile | Rimuovere immediatamente e registrare remediation |
| Build fallita | Correggere errore e ripetere build |

Il rollback documentale non modifica dati osservativi o procedure fisiche dell'osservatorio.

## 8. Evidenze di validazione

Le evidenze accettate includono diff dei file Markdown, diff di `mkdocs.yml`, controllo YAML, controllo link, controllo identificativi, scansione contenuti sensibili, log build MkDocs se disponibile, commit hash e PR summary quando aperta.

## 9. Collegamento a project history

Ogni release significativa aggiorna [Project History](project-history.md) con data, evento, evidenza e stato. Le date non confermate restano `Da validare`.

## 10. Follow-up non bloccanti

| ID | Follow-up | Motivazione |
|---|---|---|
| `DSG-FUP-001` | Collegare evidenze operative reali alle checklist | Le evidenze nascono dall'uso operativo |
| `DSG-FUP-002` | Riesaminare DSRA dopo test failover e safety | Migliora rischio residuo |
| `DSG-FUP-003` | Eseguire build MkDocs su PC Principale/GitHub Actions | Runtime corrente non include MkDocs |
| `DSG-FUP-004` | Formalizzare release notes future | Mantiene continuita governance |

## 11. Elementi TBD

| ID | Elemento | Stato |
|---|---|
| `DSG-REL-TBD-001` | Numerazione release formale | Da validare |
| `DSG-REL-TBD-002` | Automazione release notes | TBD |
| `DSG-REL-TBD-003` | Integrazione build GitHub Actions | Da validare |

## 12. Riferimenti

- [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [Planning](planning.md)
- [Project History](project-history.md)
- [Enterprise Registry](registries/index.md)
- [Governance](governance.md)
