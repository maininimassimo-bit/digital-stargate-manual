# Digital StarGate Design System

| Campo | Valore |
|---|---|
| Documento | Digital StarGate Design System |
| Identificativo | DSG-UI-001 |
| Release di introduzione | 4.0 M1 |
| Versione documento | 1.0 |
| Stato | Draft |
| Ambito | Portale web, documentazione MkDocs e dashboard |
| Responsabile | Massimo Mainini |

---

## 1. Scopo

Il Digital StarGate Design System definisce le regole visive, strutturali e comportamentali da applicare a tutte le pagine del portale Digital StarGate.

Il documento garantisce coerenza grafica, riconoscibilità del portale, riutilizzo dei componenti, compatibilità tra modalità chiara e scura, comportamento responsive e continuità tra documentazione, osservatorio e analytics.

Ogni nuova pagina deve apparire come parte nativa del portale esistente e non come un modulo grafico indipendente.

## 2. Principi di progettazione

### 2.1 Continuità

Le nuove funzionalità devono estendere il linguaggio visivo esistente senza sostituirlo.

### 2.2 Chiarezza

Ogni pagina deve rendere immediatamente riconoscibili titolo, scopo, posizione nella navigazione, informazioni principali, azioni disponibili e stato operativo.

### 2.3 Gerarchia

Le informazioni devono seguire una struttura prevedibile:

1. contesto della pagina;
2. titolo;
3. sintesi;
4. contenuto principale;
5. approfondimenti;
6. azioni e collegamenti;
7. note operative.

### 2.4 Modularità

Le pagine devono utilizzare componenti riutilizzabili: hero, card, KPI, badge di stato, tabelle, callout, pannelli informativi, griglie, pulsanti e breadcrumb.

### 2.5 Accessibilità

Il design deve mantenere contrasto leggibile, testi alternativi per le immagini, titoli in ordine gerarchico, link descrittivi, elementi comprensibili anche senza colore e compatibilità con tastiera e dispositivi mobili.

### 2.6 Responsive design

Ogni pagina deve essere verificata su desktop, notebook, tablet e smartphone.

## 3. Fondamenti visivi

### 3.1 Palette primaria

| Token | Valore | Utilizzo |
|---|---:|---|
| `--dsg-navy` | `#07152f` | Sfondo principale scuro |
| `--dsg-navy-2` | `#0b2453` | Superfici e gradienti secondari |
| `--dsg-indigo` | `#4658d9` | Elementi primari e accenti |
| `--dsg-blue` | `#3078ff` | Collegamenti, azioni e indicatori |
| `--dsg-cyan` | `#55d9ff` | Evidenziazioni e dettagli luminosi |
| `--dsg-border` | `#dce4f3` | Bordi in modalità chiara |
| `--dsg-text-soft` | `#68738a` | Testi secondari |
| `--dsg-surface` | `rgba(255, 255, 255, 0.9)` | Superfici chiare |
| `--dsg-surface-dark` | `rgba(14, 24, 48, 0.92)` | Superfici scure |

Le variabili esistenti devono essere preferite ai valori colore inseriti direttamente nei nuovi componenti.

### 3.2 Colori di stato

| Stato | Significato |
|---|---|
| Verde | Operativo, completato o conforme |
| Giallo | Attenzione, verifica richiesta o condizione parziale |
| Rosso | Errore, indisponibilità o condizione critica |
| Blu | Informazione o attività in corso |
| Grigio | Stato non disponibile, inattivo o non applicabile |

Il colore non deve essere l’unico elemento distintivo: ogni badge deve contenere anche un testo esplicito.

### 3.3 Gradienti

I gradienti devono usare prevalentemente combinazioni di navy, indigo, blu e ciano. Sono ammessi per header, hero, pulsanti primari, card in evidenza e indicatori selezionati.

### 3.4 Ombre

```css
--dsg-shadow: 0 14px 36px rgba(12, 29, 70, 0.14);
--dsg-shadow-soft: 0 7px 22px rgba(12, 29, 70, 0.09);
```

### 3.5 Bordi e raggi

| Componente | Raggio indicativo |
|---|---:|
| Pulsante | `0.45rem` |
| Badge | `0.35rem` o forma pill |
| Card | `0.75rem` |
| Pannello principale | `0.9rem` |
| Hero | `1rem` |

## 4. Tipografia

Il portale utilizza la tipografia fornita dal tema Material for MkDocs. Non devono essere aggiunti font esterni senza una decisione architetturale specifica.

Una pagina deve contenere un solo H1 e rispettare l’ordine H1, H2, H3, H4.

Percorsi, comandi, nomi file, variabili e identificativi devono essere formattati in monospaziato.

## 5. Struttura delle pagine

Ogni nuova pagina deve adottare, quando applicabile, questa struttura:

```text
Breadcrumb
Titolo o hero
Descrizione sintetica
Indicatori principali
Contenuto
Approfondimenti
Azioni o collegamenti
Note operative
```

Il titolo deve essere unico, coerente con `mkdocs.yml` e accompagnato da una breve introduzione.

## 6. Hero

Il componente hero è destinato a home page, portali di sezione, dashboard principali e pagine di presentazione.

Classi esistenti:

```text
.dsg-hero
.dsg-hero__overlay
.dsg-hero__content
.dsg-hero__eyebrow
.dsg-hero__tagline
.dsg-hero__subtitle
.dsg-hero__actions
.dsg-hero__facts
.dsg-hero__fact
```

Le nuove varianti devono estendere queste classi.

## 7. Card

Le card devono avere uno scopo unico, evitare testi troppo lunghi, mantenere altezze coerenti nelle griglie e non contenere più di un’azione primaria.

Griglia desktop consigliata:

```css
grid-template-columns: repeat(3, minmax(0, 1fr));
```

Su schermi piccoli la griglia deve diventare a colonna singola.

## 8. KPI e indicatori

I KPI devono presentare nome, valore, unità di misura, periodo di riferimento e stato o confronto, quando disponibile.

Quando un dato non è disponibile utilizzare `N/D` e non `0`, salvo che zero sia realmente il valore misurato.

## 9. Tabelle

Ogni tabella deve avere intestazioni chiare, unità di misura, ordine logico delle colonne, allineamento coerente e comportamento responsive.

- testo: sinistra;
- numeri: destra;
- stati brevi: centro;
- codici: monospaziato quando opportuno.

## 10. Pulsanti e azioni

Una pagina deve avere normalmente una sola azione primaria visivamente dominante.

Le etichette devono descrivere l’azione. Evitare espressioni generiche come `Clicca qui`, `Vai` o `Altro`.

## 11. Admonition e callout

Tipologie raccomandate:

```text
note
info
tip
warning
danger
success
example
```

## 12. Icone

Le icone devono provenire prioritariamente dal set Material già disponibile nel tema e non devono sostituire completamente il testo.

## 13. Immagini e diagrammi

Le immagini devono essere archiviate sotto:

```text
docs/assets/images
```

Utilizzare nomi minuscoli, descrittivi, separati da trattini e privi di spazi.

Preferire SVG per diagrammi, WebP o JPEG per fotografie e PNG per schermate o trasparenze.

## 14. Dashboard Analytics

Struttura consigliata:

```text
Titolo dashboard
Periodo
Stato aggiornamento
KPI principali
Grafici
Tabelle di dettaglio
Note sulla qualità dei dati
```

Ogni grafico deve avere titolo, unità di misura, intervallo temporale, legenda quando necessaria e messaggio in assenza di dati.

## 15. Modalità chiara e scura

Ogni nuovo componente deve essere verificato in entrambe le modalità, controllando contrasto, bordi, ombre, icone, tabelle, stati e immagini.

## 16. Responsive design

Su desktop sono ammesse griglie a più colonne. Su tablet il numero di colonne deve ridursi. Su smartphone occorre usare prevalentemente una colonna e permettere lo scorrimento controllato delle tabelle.

## 17. Convenzioni HTML

L’HTML personalizzato deve essere usato solo quando Markdown e i componenti MkDocs non sono sufficienti.

Regole:

- usare elementi semantici;
- evitare stili inline;
- usare classi con prefisso `dsg-`;
- evitare JavaScript incorporato nella pagina;
- non duplicare componenti già presenti.

## 18. Convenzioni CSS

Le nuove classi devono usare il prefisso `dsg-`.

I valori ricorrenti devono essere definiti come custom properties.

Evitare `!important`, selettori eccessivamente specifici, stili inline, colori duplicati e dimensioni fisse non responsive.

## 19. Convenzioni JavaScript

Il JavaScript deve migliorare progressivamente la pagina, non impedire la fruizione del contenuto statico, evitare errori in console e separare dati, logica e rendering.

Gli script condivisi devono essere archiviati sotto:

```text
docs/javascripts
```

## 20. Navigazione

Ogni pagina pubblicata deve essere registrata in `mkdocs.yml` oppure esclusa esplicitamente dalla navigazione quando previsto.

## 21. Breadcrumb

Le pagine interne devono utilizzare breadcrumb coerenti con la navigazione.

Esempio:

```text
Home / Architettura / Assessment tecnici / PAA-001
```

## 22. Stati delle pagine

| Stato | Significato |
|---|---|
| Draft | Documento in preparazione |
| In review | Documento sottoposto a verifica |
| Approved | Documento approvato |
| Active | Documento operativo |
| Superseded | Documento sostituito |
| Archived | Documento storico |

## 23. Template minimo di pagina

```markdown
# Titolo della pagina

Breve descrizione dello scopo della pagina.

## Panoramica

## Contenuto principale

## Verifica

## Riferimenti
```

## 24. Template pagina tecnica

```markdown
# Titolo tecnico

| Campo | Valore |
|---|---|
| Identificativo | DSG-XXX-000 |
| Versione | 1.0 |
| Stato | Draft |
| Responsabile | Massimo Mainini |

## Scopo

## Ambito

## Prerequisiti

## Architettura o procedura

## Validazione

## Rischi e limitazioni

## Riferimenti
```

## 25. Checklist di conformità

### Contenuto

- [ ] Il titolo è chiaro e unico.
- [ ] La pagina ha uno scopo esplicito.
- [ ] I termini tecnici sono coerenti.
- [ ] I collegamenti funzionano.
- [ ] Le immagini hanno testo alternativo.
- [ ] I comandi sono completi e verificabili.

### Design

- [ ] La pagina utilizza la palette Digital StarGate.
- [ ] I componenti esistenti sono stati riutilizzati.
- [ ] La pagina funziona in modalità chiara e scura.
- [ ] La pagina è leggibile su smartphone.

### Navigazione

- [ ] La pagina è inserita in `mkdocs.yml`.
- [ ] La posizione nella navigazione è corretta.
- [ ] Il breadcrumb è coerente.

### Qualità tecnica

- [ ] `mkdocs build --strict` termina correttamente.
- [ ] Non sono presenti errori JavaScript nella console.
- [ ] Non sono presenti risorse mancanti.
- [ ] Non sono presenti file locali o temporanei.
- [ ] `git status` contiene solo le modifiche previste.

## 26. Governance del Design System

Ogni modifica significativa deve includere aggiornamento del documento, aggiornamento dei fogli di stile, verifica delle pagine esistenti, build MkDocs e registrazione nelle note di release.

## 27. Criteri di accettazione

Una nuova pagina è conforme quando mantiene l’identità visiva esistente, usa componenti documentati, supera la build MkDocs strict, funziona in modalità chiara e scura, è responsive e non introduce regressioni.

## 28. Riferimenti tecnici

```text
mkdocs.yml
docs/styles/extra.css
docs/styles/analytics.css
docs/javascripts/page-enhancements.js
docs/javascripts/nav-scroll.js
docs/javascripts/homepage-effects.js
```

Documenti correlati:

```text
docs/developer/portal-publication-guidelines.md
docs/architecture/assessments/PAA-001-Project-Architecture-Assessment.md
docs/releases/ui-6.1.md
```

## 29. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 26/07/2026 | Prima emissione per Release 4.0 M1 |
