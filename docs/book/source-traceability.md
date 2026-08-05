# Matrice delle fonti e tracciabilità

| Campo | Valore |
|---|---|
| Identificativo | DSG-BOOK-TRACE-001 |
| Collegamento | DSG-BOOK-001 |
| Stato | Attivo |
| Data baseline | 5 agosto 2026 |
| Funzione | Controllo dell'aderenza storica ed editoriale |

## 1. Regola

Il libro è un'opera narrativa e interpretativa basata su un repository tecnico. Questa matrice impedisce che la semplificazione editoriale alteri lo stato del progetto.

La prevalenza delle fonti segue `AI_BOOTSTRAP.md`:

1. Architecture Package, ADR, capability e standard approvati;
2. assessment ARB, validation record, execution evidence e gate;
3. roadmap autorevole `AMP-002`;
4. release note e commit pubblicati;
5. contratti machine-readable;
6. dataset e dashboard come proiezioni;
7. Project Governance Center;
8. conversazioni e memoria.

`DSG-MR-001` rimane la baseline storica della trasformazione enterprise 2026-2030. `AMP-002` rappresenta il successivo riallineamento architetturale autorevole sul ramo principale.

## 2. Timeline minima verificata

La ricostruzione estesa, con commit e limiti interpretativi, è disponibile nella [Cronologia verificata del progetto](verified-timeline.md).

| Data | Passaggio | Fonte | Uso nel libro |
|---|---|---|---|
| 13/07/2026 | Configurazione Docs-as-Code e completamento progressivo dei capitoli 1-44 | Commit `cf4535f`, `57de947`-`93ba824` | Nascita verificabile della baseline documentale nel repository |
| 15-17/07/2026 | Report di sessione, reporting automatico e validazione analytics | Commit `d96150a`, `9d976b9`, `b87700e` | Collegamento tra osservazione, reporting e dati |
| 19/07/2026 | Prima architettura della piattaforma | Commit `10e0edf` | Passaggio dal manuale al disegno di piattaforma |
| 23-24/07/2026 | Dataset Warehouse, assessment EA-001/EA-002 e architettura dati | Commit `8669bb4`, `5128a72`, `cc98567` | Consolidamento della data platform |
| 26/07/2026 | Approvazione della Master Roadmap `DSG-MR-001` | Master Roadmap e `DSG-HIST-001` | Svolta enterprise e separazione AS-IS/Transition/TO-BE |
| 26/07/2026 | Baseline EAM/DSRA, portfolio, registri e governance | `DSG-HIST-001` | Fondazione enterprise |
| 31/07/2026 | Preparazione ed esecuzione progressiva della campagna ENV-011 | PR e documenti `ARB-012-C04-W06` | Esempio di evidence entro perimetro isolato |
| 03/08/2026 | Allineamento dell'evidenza tecnica ENV-011 | PR #37 e documenti di traceability | Distinzione tra risultato tecnico e accettazione |
| 04/08/2026 | Pubblicazione baseline AP-013 e pilot scientifico protetto | PR #38 | Passaggio da file a patrimonio scientifico governato |
| 04/08/2026 | Integrazione Enterprise Portal e command center | PR #39 | Evoluzione della documentazione in piattaforma |
| 04/08/2026 | Baseline del Project Governance Center e Knowledge Map | Documenti `docs/project/` | Memoria istituzionale |
| 05/08/2026 | Decisioni operative di continuità e delega AI registrate | Decision Log v1.1 | AI come collaboratore governato |

La cronologia precedente al 13 luglio e la storia dell'osservatorio fisico restano da ricostruire. Le motivazioni personali saranno raccolte come testimonianza dell'autore e non confuse con le evidenze repository.

## 3. Matrice capitoli-fonti

| Capitolo o tema | Fonti primarie | Fonti di stato/evidence | Classificazione editoriale |
|---|---|---|---|
| Prima dell'enterprise | Manuale tecnico 1-44 | `DSG-HIST-001` | Ricostruzione con date non note |
| Cambio di prospettiva | `DSG-MR-001`, Project Governance Center | Commit e PR di pubblicazione | Fatto verificato e lettura editoriale |
| Modello DSG-EOM | Tutto il corpus | Questa matrice | Sintesi editoriale dichiarata |
| Architettura come linguaggio comune | `DSG-EAM-001`, AP-001, Enterprise Metamodel | ARB-003, ABC-001, traceability register | Baseline approvata e sintesi editoriale |
| Repository come memoria istituzionale | `AI_BOOTSTRAP.md`, Enterprise Architecture Context, Knowledge Map | Decision Log, commit e cronologia verificata | Capacita organizzativa attiva |
| Decisioni tracciabili | ADR, Decision Log, AP-001 | Assessment, ARB, ABC-001 e traceability register | Metodo di governance verificato |
| Architettura enterprise | `DSG-EAM-001`, DSRA, AP-001 | Assessment e ABC-001 | Baseline approvata |
| Automazione | AP-003, ADR-004 | review ed evidence applicabili | Baseline più stato dimostrato |
| Osservabilità | AP-004 | ARB ed execution evidence | Baseline più stato dimostrato |
| Identity e security | AP-005 | ARB-007 e controlli | Baseline con condizioni |
| Asset e configurazioni | AP-006 | ARB-008 | Baseline con gap verificati |
| Operations | AP-007 | procedure e release | Modello operativo |
| Integrazione | AP-008 | cataloghi e test | Baseline architetturale |
| Infrastruttura | AP-009 e manuale | ARB-009 | AS-IS e target distinti |
| Safety | AP-010, ADR-005 | ARB-010 e test | Invarianti non negoziabili |
| Analytics | AP-011, warehouse | ARB-011 e quality gate | Capacità e maturity separate |
| Operations Center | AP-012 | ARB-012, ENV-011 | Evidenza limitata, non runtime generale |
| Repository scientifico | AP-013, DSDM-001/004 | discovery evidence e readiness gate | Pilot `COPY_ONLY` |
| Catalogo scientifico | AP-014 | roadmap `AMP-002` | Pianificato |
| Knowledge Platform | AP-015 e knowledge vision | roadmap `AMP-002` | Pianificato |
| BootAI | `AI_BOOTSTRAP.md`, Decision Log | commit e governance | Capacità organizzativa attiva |
| AI scientifica | vision e contratti AI | evidence future | Visione, non capacità dichiarata |

## 4. Affermazioni protette

Le seguenti formulazioni richiedono particolare controllo.

### “Operativo”

Usare soltanto quando il repository dimostra non solo pubblicazione, ma esecuzione e accettazione nel perimetro dichiarato. Per portale, simulatori e apparati fisici il termine può avere significati differenti e deve essere qualificato.

### “Approvato”

Una baseline approvata non è necessariamente implementata. Una review “approved with conditions” mantiene aperte le condizioni finché evidence e re-review non le chiudono.

### “AI”

Distinguere:

- uso dell'AI come collaboratore di engineering;
- contratti o predisposizioni architetturali;
- scientific intelligence nel portale;
- futura AI Platform o Scientific Knowledge Platform;
- comando autonomo, che non è implicitamente autorizzato.

### “Automazione”

Distinguere:

- sequenze operative già documentate;
- simulazione;
- orchestrazione;
- suggerimento;
- autorizzazione;
- comando fisico.

### “Repository scientifico”

Distinguere:

- inventario e discovery;
- catalogo/proiezione nel portale;
- trasferimento protetto `COPY_ONLY`;
- trasferimento massivo;
- cancellazione alla fonte;
- conservazione autorevole.

## 5. Registro delle sintesi editoriali

| ID | Sintesi | Stato | Vincolo |
|---|---|---|---|
| BOOK-SYN-001 | Digital StarGate è interpretabile come osservatorio enterprise | Adottata | Non sostituisce la classificazione ufficiale |
| BOOK-SYN-002 | Il sistema governa cinque continuità | Adottata | Tesi editoriale |
| BOOK-SYN-003 | `DSG-EOM` usa sette domini e tre cicli | Adottata | Modello del libro, non Architecture Package |
| BOOK-SYN-004 | L'autorità sicura è il centro del modello | Adottata | Derivata da AP-003, AP-005, AP-010 e AP-012 |
| BOOK-SYN-005 | BootAI è continuità cognitiva | Adottata | Interpretazione della funzione di governance |
| BOOK-SYN-006 | Roadmap in quattro orizzonti | Proposta | Strumento didattico da validare nel manoscritto |

## 6. Questioni ancora da ricostruire

| ID | Questione | Metodo |
|---|---|---|
| BOOK-TBD-001 | Cronologia precedente alla baseline enterprise | Analisi commit, release e registri revisioni |
| BOOK-TBD-002 | Prime motivazioni personali e operative del progetto | Intervista all'autore, distinta dalle fonti repository |
| BOOK-TBD-003 | Evoluzione esatta del warehouse e dell'analytics | Commit, assessment EA-002 e release |
| BOOK-TBD-004 | Sequenza completa AP-001/AP-013 | Architecture Master Plan, PR e certificate |
| BOOK-TBD-005 | Risultati osservativi rappresentativi | Session report verificati e selezione editoriale |
| BOOK-TBD-006 | Stato finale AP-012/AP-013 al momento della chiusura libro | Verifica sulla baseline di pubblicazione |
| BOOK-TBD-007 | Evoluzione AP-014/AP-015 | Trattare come pianificata finché priva di evidence |

Questi elementi non sono placeholder nel testo pubblicato. Sono il backlog di ricerca per i capitoli futuri.

## 7. Controllo prima della pubblicazione

Per ogni capitolo:

1. identificare le affermazioni sullo stato;
2. collegarle a una fonte primaria;
3. verificare data e branch;
4. confrontare roadmap, release ed evidence;
5. marcare chiaramente la sintesi editoriale;
6. rimuovere dettagli tecnici che non sostengono il ragionamento;
7. controllare che nessuna visione sia narrata come realtà;
8. aggiornare questa matrice.
