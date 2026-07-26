# PAA-001 — Project Architecture Assessment

| Campo | Valore |
|---|---|
| Documento | Project Architecture Assessment |
| Identificativo | PAA-001 |
| Progetto | Digital StarGate |
| Release di riferimento | 4.0 M1 Foundation |
| Versione | 1.0 |
| Stato | Draft |
| Responsabile | Massimo Mainini |
| Data | 26/07/2026 |

---

## 1. Scopo

Il presente assessment valuta lo stato architetturale del progetto Digital StarGate alla soglia della Release 4.0 M1.

L’obiettivo è:

- consolidare l’architettura esistente;
- identificare punti di forza e aree di miglioramento;
- definire criteri misurabili per le release successive;
- ridurre il rischio di regressioni;
- preparare il progetto alla separazione tra raccolta dati, reporting, analytics e portale.

---

## 2. Ambito

L’assessment comprende:

- repository principale `digital-stargate-manual`;
- documentazione MkDocs;
- moduli Analytics;
- Warehouse;
- Reporting;
- componenti di automazione EAGLE;
- pubblicazione del portale;
- qualità del codice e dei test;
- governance delle release.

Sono esclusi:

- valutazioni prestazionali dell’hardware astronomico;
- certificazioni di sicurezza formali;
- audit infrastrutturali di terze parti;
- penetration test.

---

## 3. Architettura di riferimento

Il flusso logico target è:

```text
EAGLE
  ↓
Automation / Collection
  ↓
Reporting
  ↓
Warehouse
  ↓
Analytics
  ↓
Renderer
  ↓
Portal
```

### 3.1 Responsabilità dei livelli

| Livello | Responsabilità |
|---|---|
| EAGLE | Acquisizione locale e integrazione con i sistemi dell’osservatorio |
| Automation / Collection | Raccolta, normalizzazione iniziale e pubblicazione dei dati |
| Reporting | Produzione di report tecnici e dataset di presentazione |
| Warehouse | Consolidamento, storicizzazione e controllo qualità |
| Analytics | Calcolo KPI, aggregazioni e analisi |
| Renderer | Trasformazione dei risultati in viste pubblicabili |
| Portal | Consultazione, navigazione e presentazione finale |

### 3.2 Principio di separazione

Ogni livello deve:

- avere responsabilità chiare;
- evitare dipendenze circolari;
- non duplicare la logica di altri livelli;
- esporre input e output identificabili;
- poter essere validato separatamente.

---

## 4. Metodo di valutazione

Ogni area è valutata su una scala da 0 a 100.

| Intervallo | Valutazione |
|---|---|
| 90–100 | Eccellente |
| 80–89 | Buono |
| 70–79 | Adeguato |
| 60–69 | Debole |
| < 60 | Critico |

Le valutazioni considerano:

- completezza;
- coerenza;
- testabilità;
- manutenibilità;
- documentazione;
- automazione;
- rischio operativo.

---

## 5. Risultati sintetici

| Area | Punteggio | Valutazione |
|---|---:|---|
| Repository | 98 | Eccellente |
| Architettura | 96 | Eccellente |
| Testing | 100 | Eccellente |
| Build documentale | 100 | Eccellente |
| Documentazione | 92 | Eccellente |
| Interfaccia utente | 97 | Eccellente |
| Analytics | 97 | Eccellente |
| Reporting | 95 | Eccellente |

### Valutazione complessiva

```text
96,9 / 100
```

Il progetto è considerato idoneo all’avvio della Release 4.0 M1 Foundation.

---

## 6. Repository

### 6.1 Punti di forza

- branch di sviluppo dedicata;
- working tree controllato;
- separazione tra ambiente PC Principale ed EAGLE;
- esclusione degli artefatti locali;
- backup verificato tramite SHA256;
- storia Git coerente;
- repository remoto sincronizzato.

### 6.2 Evidenze

Branch di sviluppo:

```text
feature/release-4.0-m1-foundation
```

Commit di riferimento:

```text
efea66b feat(analytics): add standalone analytics core module
```

### 6.3 Rischi residui

- presenza di file locali non classificati;
- possibile inclusione accidentale di artefatti tramite `git add .`;
- dipendenza da controlli manuali prima dei commit.

### 6.4 Raccomandazioni

- utilizzare sempre `git status --short`;
- aggiungere i file in modo selettivo;
- mantenere aggiornato `.gitignore`;
- non versionare esportazioni, backup o snapshot diagnostici;
- introdurre una checklist pre-commit.

---

## 7. Architettura applicativa

### 7.1 Punti di forza

- chiara evoluzione per release;
- introduzione del Warehouse;
- separazione del modulo Analytics;
- repository Reporting dedicato;
- progressiva riduzione dell’accoppiamento;
- documentazione tramite ADR e assessment.

### 7.2 Rischi residui

- confini tra Reporting, Analytics e Renderer da formalizzare completamente;
- dipendenze runtime da censire;
- interfacce dati non ancora governate da contratti formali;
- possibile crescita di logica condivisa non centralizzata.

### 7.3 Raccomandazioni

- definire input e output di ogni modulo;
- documentare gli schemi dati;
- introdurre versionamento dei dataset;
- evitare accessi diretti del portale ai dati grezzi;
- mantenere il Warehouse come fonte consolidata;
- usare ADR per ogni variazione strutturale.

---

## 8. Testing

### 8.1 Stato

Comando di validazione:

```powershell
python -m pytest -q
```

Esito registrato:

- 50 test superati;
- 40 subtest superati;
- nessun errore bloccante.

### 8.2 Valutazione

Il livello di copertura funzionale osservato è adeguato alla Foundation.

### 8.3 Raccomandazioni

- mantenere i test obbligatori prima del merge;
- aggiungere test per contratti dati e casi limite;
- introdurre test di integrazione tra Warehouse e Analytics;
- registrare i risultati nelle note di release;
- evitare modifiche non accompagnate da test quando impattano logica core.

---

## 9. Build documentale

### 9.1 Stato

Comando:

```powershell
mkdocs build --strict
```

Esito:

- build completata;
- nessun errore;
- pagine non ancora in navigazione rilevate correttamente.

### 9.2 Nota su MkDocs 2.0

L’avviso mostrato da Material for MkDocs non rappresenta un errore del progetto.

Deve essere trattato come rischio evolutivo esterno e monitorato, senza effettuare migrazioni non pianificate.

### 9.3 Raccomandazioni

- mantenere `mkdocs build --strict` come quality gate;
- verificare periodicamente compatibilità di plugin e tema;
- bloccare le versioni delle dipendenze quando necessario;
- evitare aggiornamenti major non testati;
- produrre una procedura di rollback.

---

## 10. Documentazione

### 10.1 Punti di forza

- manuale tecnico strutturato;
- navigazione per aree funzionali;
- ADR disponibili;
- documentazione Warehouse presente;
- capitoli operativi e di governance;
- introduzione del Design System;
- linee guida di pubblicazione in preparazione.

### 10.2 Aree di miglioramento

- alcune pagine non sono ancora registrate in `mkdocs.yml`;
- metadati non uniformi in tutti i documenti;
- mancano template obbligatori per alcune tipologie;
- criteri di stato documentale da applicare in modo sistematico.

### 10.3 Raccomandazioni

- uniformare intestazioni e metadati;
- collegare ogni nuovo documento alla navigazione;
- mantenere un registro revisioni;
- utilizzare identificativi univoci;
- aggiungere riferimenti incrociati tra documenti correlati.

---

## 11. UI e Design System

### 11.1 Punti di forza

- identità visiva consolidata;
- palette centralizzata;
- modalità chiara e scura;
- componenti hero e dashboard;
- navigazione Material;
- struttura responsive;
- CSS dedicato per Analytics.

### 11.2 Rischi residui

- crescita non governata delle classi CSS;
- duplicazione di componenti;
- uso eccessivo di HTML personalizzato;
- regressioni su dispositivi mobili;
- differenze tra pagine documentali e dashboard.

### 11.3 Raccomandazioni

- adottare `DSG-UI-001`;
- usare prefisso `dsg-`;
- evitare stili inline;
- centralizzare token e componenti;
- verificare desktop, tablet e smartphone;
- testare sempre modalità chiara e scura.

---

## 12. Analytics

### 12.1 Punti di forza

- modulo core separato;
- test automatizzati;
- dashboard integrate;
- qualità dati trattata come requisito;
- integrazione con storico e Warehouse.

### 12.2 Rischi residui

- indicatori non sempre accompagnati da metadati;
- necessità di formalizzare il concetto di dato non disponibile;
- dipendenza da dataset prodotti da processi esterni;
- possibile divergenza tra calcolo e visualizzazione.

### 12.3 Raccomandazioni

- associare periodo, unità e fonte a ogni KPI;
- usare `N/D` quando il dato manca;
- separare calcolo e rendering;
- registrare l’ultimo aggiornamento;
- esporre anomalie e record esclusi.

---

## 13. Reporting

### 13.1 Punti di forza

- repository dedicato;
- responsabilità separata dal portale;
- possibilità di riuso dei report;
- integrazione prevista nel flusso dati.

### 13.2 Rischi residui

- contratti dati da completare;
- naming e versionamento da uniformare;
- criteri di compatibilità tra versioni non ancora formalizzati;
- dipendenza dal formato di output.

### 13.3 Raccomandazioni

- definire schema e versione di ogni report;
- separare contenuto e presentazione;
- produrre output deterministici;
- validare i file generati;
- documentare input, output ed errori.

---

## 14. Sicurezza e configurazione

### 14.1 Stato

L’analisi degli artefatti EAGLE ha confermato l’assenza di:

- password;
- token;
- chiavi API;
- segreti.

### 14.2 Raccomandazioni

- non versionare configurazioni locali complete;
- usare template sanitizzati;
- mantenere segreti fuori dal repository;
- controllare i file prima del commit;
- includere solo percorsi e parametri non sensibili.

---

## 15. Gestione degli artefatti locali

I seguenti elementi non devono essere versionati salvo decisione esplicita:

- esportazioni di task Windows;
- snapshot dell’albero directory;
- cartelle `.venv`;
- file di backup;
- log temporanei;
- output di build;
- file generati localmente;
- configurazioni contenenti percorsi specifici della macchina.

Gli artefatti operativi utili devono essere:

1. salvati fuori dal repository;
2. verificati tramite hash quando necessario;
3. sostituiti da template o procedure documentate;
4. registrati nella documentazione tecnica.

---

## 16. Governance delle release

Ogni release deve essere organizzata come:

```text
Release
  └── Milestone
        └── Sprint
```

### 16.1 Quality gate minimo

Prima del merge devono essere verificati:

- test automatici;
- build documentale;
- documentazione aggiornata;
- changelog o release notes;
- assenza di file locali;
- verifica su PC Principale;
- verifica su EAGLE quando applicabile;
- architettura coerente con ADR e assessment.

---

## 17. Rischi principali

| ID | Rischio | Probabilità | Impatto | Azione |
|---|---|---:|---:|---|
| R-01 | Accoppiamento tra moduli | Media | Alto | Formalizzare interfacce |
| R-02 | Regressioni UI | Media | Medio | Test responsive e dark mode |
| R-03 | File locali nel repository | Media | Medio | Git add selettivo |
| R-04 | Incompatibilità MkDocs futura | Media | Alto | Version pinning e monitoraggio |
| R-05 | Divergenza degli schemi dati | Media | Alto | Versionamento dataset |
| R-06 | Documentazione non aggiornata | Bassa | Medio | Quality gate documentale |
| R-07 | Duplicazione logica Analytics/Reporting | Media | Alto | Confini di responsabilità |

---

## 18. Decisioni architetturali richieste

Le seguenti decisioni devono essere formalizzate nelle milestone successive:

1. contratto tra Reporting e Warehouse;
2. schema di versionamento dei dataset;
3. responsabilità del Renderer;
4. modalità di pubblicazione del portale;
5. standard per plugin futuri;
6. strategia di compatibilità tra release;
7. gestione centralizzata della configurazione.

---

## 19. Piano di miglioramento

### Priorità alta

- completare la documentazione 4.0 M1;
- aggiornare `mkdocs.yml`;
- formalizzare gli schemi dati;
- definire i confini tra Reporting, Warehouse e Analytics.

### Priorità media

- introdurre template per componenti e pagine;
- consolidare i token CSS;
- aggiungere test di integrazione;
- formalizzare il versionamento dei report.

### Priorità evolutiva

- plugin architecture;
- dashboard live;
- archivio astrofotografico;
- portale osservatorio;
- funzioni AI.

---

## 20. Criteri di accettazione della Foundation

La Release 4.0 M1 può essere approvata quando:

- tutti i documenti pianificati sono completi;
- `mkdocs.yml` è aggiornato;
- `mkdocs build --strict` termina senza errori;
- i test automatici risultano superati;
- il repository contiene solo file previsti;
- Design System e linee guida sono pubblicati;
- PAA-001 è revisionato;
- le release notes sono disponibili;
- il branch è pronto per il merge.

---

## 21. Conclusione

Digital StarGate presenta un livello di maturità architetturale elevato.

La Foundation della Release 4.0 non richiede una riscrittura, ma un consolidamento strutturale basato su:

- separazione delle responsabilità;
- contratti dati;
- governance documentale;
- quality gate;
- riuso dei componenti;
- controllo delle dipendenze;
- disciplina di release.

Il progetto è quindi valutato come:

```text
IDONEO CON RACCOMANDAZIONI
```

all’avvio della Release 4.0 M1.

---

## 22. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 26/07/2026 | Prima emissione per Release 4.0 M1 Foundation |
