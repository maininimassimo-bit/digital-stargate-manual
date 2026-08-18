# DSG-HBK-001 - Engineering Handbook

| Campo | Valore |
|---|---|
| Documento | Engineering Handbook |
| Identificativo | `DSG-HBK-001` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvato per baseline |
| Versione | 1.1 |
| Owner | Massimo Mainini |
| Data | 26/07/2026 |
| Fonte gerarchica | `DSG-MR-001` |

## 1. Scopo

Definire le regole operative per sviluppare, revisionare, validare e rilasciare documentazione e artefatti enterprise Digital StarGate.

Il documento si colloca nella gerarchia `DSG-MR-001 -> DSG-EAM-001 -> DSRA-000 -> DSRA-001 -> ADR -> Assessments -> SOP -> Engineering Handbook`.

## 2. Ambito

L'handbook copre repository workflow, branch strategy, commit convention, Pull Request workflow, review, testing, documentation, release, configuration management, gestione dei contenuti sensibili, quality gates e gestione delle eccezioni.

Non definisce configurazioni operative private o parametri tecnici non confermati.

## 3. Principi

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-HBK-PRN-001` | Docs-as-Code | Markdown e `mkdocs.yml` sono fonte pubblicabile |
| `DSG-HBK-PRN-002` | Roadmap-first | Ogni modifica enterprise richiama `DSG-MR-001` |
| `DSG-HBK-PRN-003` | No duplication | Aggiornare documenti esistenti prima di crearne di nuovi |
| `DSG-HBK-PRN-004` | Evidence | Validazioni, commit e review producono evidenza |
| `DSG-HBK-PRN-005` | Safety and security | Nessuna automazione o pubblicazione supera safety e security |

## 4. Repository workflow

1. Leggere `mkdocs.yml` e documenti enterprise correlati.
2. Identificare se l'ambito e gia coperto.
3. Aggiornare la fonte esistente se appropriato.
4. Creare nuovi file solo quando manca una fonte coerente.
5. Aggiornare registry e navigation quando il documento e pubblicabile.
6. Eseguire controlli statici disponibili.
7. Creare commit logico e tracciabile.

Input: richiesta, roadmap, documenti esistenti. Output: file aggiornati, validazioni, commit.

## 5. Branch strategy

| Branch | Uso | Stato |
|---|---|---|
| `main` | Base stabile | AS-IS |
| `docs/dsg-master-roadmap` | Branch lavoro `DSG-MR-001` | AS-IS / Transition |
| Branch temporanei | Non previsti per questa baseline | Da validare |

Regola: la milestone corrente lavora su `docs/dsg-master-roadmap` e non apre PR se l'utente lo vieta esplicitamente.

## 6. Commit convention

| Tipo | Uso |
|---|---|
| `docs(adr)` | ADR e indici decisioni |
| `docs(assessment)` | Assessment tecnici/operativi |
| `docs(operations)` | SOP e procedure |
| `docs(handbook)` | Engineering Handbook |
| `docs(planning)` | Planning, roadmap operativa, KPI |
| `docs(knowledge)` | Indici, traceability, glossario, riferimenti |
| `docs(vision)` | Visione lungo periodo |

Ogni commit deve avere scope coerente e non mescolare modifiche non correlate.

## 7. Pull Request workflow

1. Preparare riepilogo per milestone.
2. Elencare file principali.
3. Riportare validazioni eseguite.
4. Indicare limiti noti e TBD residui.
5. Collegare `DSG-MR-001`.
6. Non fare merge senza richiesta esplicita.

La PR verso `main` e parte del workflow finale, ma non viene aperta quando il task lo vieta.

## 8. Review

Il reviewer controlla coerenza con `DSG-MR-001`, rispetto Roadmap Freeze Policy, assenza di nuovi programmi non approvati, link relativi, YAML valido, registry aggiornato, `TBD` per dati non confermati e assenza di contenuti sensibili.

## 9. Testing e validazione

| Controllo | Strumento | Evidenza |
|---|---|---|
| YAML | Parser YAML disponibile | Esito sintassi |
| Link Markdown | Script/static check | Link mancanti o confermati via nav |
| MkDocs | `mkdocs build --strict` quando disponibile | Log build |
| Contenuti sensibili | Ricerca statica termini sensibili | Nessun finding |
| Duplicazioni | Confronto ID, nav e titoli | Nessun duplicato bloccante |
| Gerarchia | Controllo riferimenti | Matrix coerente |

Se MkDocs non e disponibile per vincoli runtime o proxy, il build viene rinviato a PC Principale o GitHub Actions.

## 10. Documentation workflow

Ogni documento enterprise deve includere identificativo, stato, versione, owner, data, scopo, ambito, riferimenti gerarchici, riferimenti incrociati, dipendenze, rischi, controlli, KPI o evidenze, e `TBD` o `Da validare` quando necessario.

## 11. Release workflow

La release segue [Release documentation](release-documentation.md): confermare deliverable, validare navigazione e link, aggiornare registry, aggiornare release notes, documentare rollback, riportare commit e limiti noti.

## 12. Configuration management

| Classe | Regola |
|---|---|
| Pubblicabile | Markdown, `mkdocs.yml`, template sanitizzati |
| Sensibile | Credenziali, parametri privati, accessi remoti |
| Da validare | Parametri non confermati |
| TBD | Configurazioni non ancora definite |

Le configurazioni pubblicabili sono registrate in [Enterprise Registry](registries/index.md). Le configurazioni sensibili non devono essere inserite nel repository.

## 13. Gestione dei contenuti sensibili

Regole: non pubblicare credenziali, chiavi o parametri privati; usare esempi sanitizzati se necessari; rimuovere immediatamente un contenuto sensibile se rilevato; bloccare la release finche il finding non e risolto; registrare la correzione nel change log se impatta una milestone.

## 14. Quality gates

| Gate | Applicazione |
|---|---|
| `QG-DOC` | Documentazione, link e navigazione |
| `QG-SEC` | Assenza contenuti sensibili |
| `QG-ARCH` | Decisioni e ADR |
| `QG-DATA` | Dataset, KPI e analytics |
| `QG-OPS` | SOP e safety |
| `QG-REL` | Release readiness |
| `QG-AI` | AI assistiva |
| `QG-DR` | Disaster Recovery |

## 15. Gestione delle eccezioni

Un'eccezione e ammessa solo se non viola safety o security, e motivata nel documento o nel riepilogo commit, ha owner funzionale o stato `Da validare`, ha follow-up tracciato e non introduce programmi o piattaforme fuori roadmap.

## 16. Dipendenze e rischi

| ID | Elemento | Stato/controllo |
|---|---|---|
| `DSG-HBK-DEP-001` | `mkdocs.yml` | AS-IS |
| `DSG-HBK-DEP-002` | Enterprise Registry | Transition |
| `DSG-HBK-RSK-001` | Commit troppo ampio | Commit logici |
| `DSG-HBK-RSK-002` | Duplicazione documentale | Review e registry |
| `DSG-HBK-RSK-003` | Pubblicazione contenuti sensibili | `QG-SEC` |
| `DSG-HBK-RSK-004` | Build non eseguito nel runtime | Evidenza e build su PC/GitHub Actions |

## 17. Elementi TBD

| ID | Elemento | Stato |
|---|---|
| `DSG-HBK-TBD-001` | Automazione completa dei controlli link | TBD |
| `DSG-HBK-TBD-002` | Policy branch temporanei | Da validare |
| `DSG-HBK-TBD-003` | Tooling dedicato alla scansione dei contenuti sensibili | TBD |

## 18. Riferimenti

- [DSG-MR-001](../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- [DSG-GOV-001](governance.md)
- [Enterprise Registry](registries/index.md)
- [SOP](sop.md)
- [Release documentation](release-documentation.md)
- [Knowledge Index](knowledge-index.md)
