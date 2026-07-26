# UI 6.1 — Release Notes

| Campo | Valore |
|---|---|
| Documento | UI 6.1 Release Notes |
| Identificativo | DSG-REL-UI-6.1 |
| Progetto | Digital StarGate |
| Release | 4.0 M1 Foundation |
| Versione documento | 1.0 |
| Stato | Draft |
| Responsabile | Massimo Mainini |
| Data | 26/07/2026 |

---

## 1. Panoramica

La release UI 6.1 consolida l’identità visiva e le regole di pubblicazione del portale Digital StarGate.

L’intervento non introduce una riscrittura grafica completa. La release formalizza e organizza quanto già presente nel progetto, mantenendo continuità con:

- struttura Material for MkDocs;
- modalità chiara e scura;
- palette Digital StarGate;
- componenti hero;
- card e pannelli;
- dashboard Analytics;
- navigazione responsive;
- fogli di stile esistenti.

---

## 2. Obiettivi

Gli obiettivi principali della UI 6.1 sono:

- definire un Design System ufficiale;
- introdurre linee guida di pubblicazione;
- ridurre la duplicazione di componenti e stili;
- mantenere coerenza tra documentazione e dashboard;
- formalizzare i controlli responsive;
- migliorare la governance delle nuove pagine;
- preparare il portale alle release 4.x successive.

---

## 3. Documenti introdotti

La release aggiunge i seguenti documenti:

```text
docs/ui/design-system.md
docs/developer/portal-publication-guidelines.md
docs/architecture/assessments/PAA-001-Project-Architecture-Assessment.md
docs/releases/ui-6.1.md
```

### 3.1 Digital StarGate Design System

Identificativo:

```text
DSG-UI-001
```

Contiene:

- principi di progettazione;
- palette e token;
- tipografia;
- hero;
- card;
- KPI;
- tabelle;
- pulsanti;
- immagini;
- dashboard;
- modalità chiara e scura;
- responsive design;
- convenzioni HTML, CSS e JavaScript;
- checklist di conformità.

### 3.2 Portal Publication Guidelines

Identificativo:

```text
DSG-DEV-001
```

Definisce:

- workflow di pubblicazione;
- convenzioni per file e cartelle;
- criteri di qualità;
- controlli pre-pubblicazione;
- validazione MkDocs;
- processo Git.

### 3.3 Project Architecture Assessment

Identificativo:

```text
PAA-001
```

Formalizza:

- architettura target;
- responsabilità dei livelli;
- qualità del repository;
- stato dei test;
- build documentale;
- rischi;
- raccomandazioni;
- criteri di accettazione della Foundation.

---

## 4. Componenti interessati

La release riguarda principalmente:

```text
mkdocs.yml
docs/styles/extra.css
docs/styles/analytics.css
docs/javascripts/page-enhancements.js
docs/javascripts/nav-scroll.js
docs/javascripts/homepage-effects.js
```

In questa milestone non è prevista una sostituzione completa di tali componenti.

Le modifiche future dovranno rispettare le regole definite dal Design System.

---

## 5. Compatibilità

### 5.1 Compatibilità visiva

La release mantiene compatibilità con:

- pagine documentali esistenti;
- home page;
- dashboard Analytics;
- navigazione Material;
- modalità chiara;
- modalità scura;
- dispositivi desktop;
- tablet;
- smartphone.

### 5.2 Compatibilità dei contenuti

Non sono previste modifiche distruttive ai percorsi delle pagine già pubblicate.

### 5.3 Compatibilità tecnica

La release è validata con:

```powershell
mkdocs build --strict
```

---

## 6. Miglioramenti introdotti

### 6.1 Governance

È stato introdotto un modello documentale per governare:

- nuove pagine;
- componenti UI;
- note di release;
- assessment architetturali;
- revisioni;
- quality gate.

### 6.2 Coerenza visiva

Sono state formalizzate le regole relative a:

- colori;
- gradienti;
- ombre;
- bordi;
- spaziature;
- gerarchia dei titoli;
- stati;
- tabelle;
- dashboard;
- responsive design.

### 6.3 Qualità

La pubblicazione delle nuove pagine richiede:

- controllo della navigazione;
- verifica dei collegamenti;
- build strict;
- verifica dark mode;
- verifica responsive;
- controllo del repository.

---

## 7. Modifiche alla navigazione

Al completamento della Release 4.0 M1, le nuove pagine saranno aggiunte a `mkdocs.yml`.

Struttura prevista:

```text
Architettura
  └── Assessment
        └── PAA-001

Sviluppo
  └── Portal Publication Guidelines

UI
  └── Design System

Release Notes
  └── UI 6.1
```

La posizione definitiva dovrà rispettare la struttura già presente nel file `mkdocs.yml`.

---

## 8. Impatto operativo

### Per gli autori

Gli autori delle pagine devono:

- utilizzare i template documentati;
- mantenere metadati coerenti;
- evitare stili inline;
- riutilizzare componenti esistenti;
- completare la checklist di pubblicazione.

### Per gli sviluppatori

Gli sviluppatori devono:

- utilizzare il prefisso CSS `dsg-`;
- centralizzare i token;
- evitare duplicazioni;
- separare logica e rendering;
- verificare la console JavaScript;
- mantenere la compatibilità responsive.

### Per i revisori

I revisori devono controllare:

- coerenza con il Design System;
- correttezza della navigazione;
- build strict;
- qualità dei collegamenti;
- conformità dei file Git.

---

## 9. Problemi noti

### 9.1 Avviso Material for MkDocs

Durante la build viene visualizzato un avviso relativo a MkDocs 2.0.

L’avviso:

- non blocca la build;
- non indica un errore del repository;
- riguarda una futura incompatibilità dell’ecosistema;
- deve essere monitorato nelle release successive.

### 9.2 Pagine non ancora in navigazione

Fino all’aggiornamento di `mkdocs.yml`, MkDocs segnala le nuove pagine come non incluse nella navigazione.

Il comportamento è previsto durante lo sviluppo della milestone.

---

## 10. Verifiche eseguite

### 10.1 Design System

- file presente;
- dimensione verificata;
- intestazione verificata;
- contenuto finale verificato;
- build MkDocs superata.

### 10.2 Portal Publication Guidelines

- file presente;
- dimensione verificata;
- intestazione verificata;
- build MkDocs superata.

### 10.3 PAA-001

- file presente;
- dimensione verificata;
- codifica UTF-8 verificata;
- intestazione verificata;
- parte finale verificata;
- build MkDocs superata.

---

## 11. Criteri di accettazione

La UI 6.1 è accettabile quando:

- tutti i documenti previsti sono completi;
- la codifica UTF-8 è verificata;
- `mkdocs.yml` contiene le nuove pagine;
- `mkdocs build --strict` termina senza errori;
- la navigazione è coerente;
- il repository contiene solo modifiche previste;
- la documentazione è revisionata;
- il branch è pronto per il commit.

---

## 12. Rollback

In caso di regressione:

1. rimuovere le nuove voci da `mkdocs.yml`;
2. ripristinare i file documentali precedenti;
3. eseguire nuovamente la build;
4. verificare la navigazione;
5. registrare la causa nella documentazione di release.

Poiché la milestone introduce prevalentemente documentazione e governance, il rollback non impatta i dati operativi dell’osservatorio.

---

## 13. Attività successive

Le attività successive previste sono:

1. aggiornamento di `mkdocs.yml`;
2. build finale della Foundation;
3. verifica del rendering locale;
4. controllo del working tree;
5. commit della milestone;
6. push della feature branch;
7. preparazione della merge request.

---

## 14. Stato della release

```text
IN VALIDAZIONE
```

La release è pronta per l’integrazione nella navigazione, ma non ancora per il merge definitivo.

---

## 15. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 26/07/2026 | Prima emissione delle note di release UI 6.1 |
