# Digital StarGate Design System

| Campo | Valore |
|---|---|
| Identificativo | DSG-UI-001 |
| Versione | 2.0 |
| Stato | Proposed |
| Data | 10/09/2026 |
| Ambito | GitHub Pages, MkDocs, dashboard e hub |
| Release | UI 7.0 |
| Responsabile | Massimo Mainini |

## 1. Design thesis

Digital StarGate deve sembrare un osservatorio scientifico contemporaneo, non un insieme di pagine tecniche scollegate. L'esperienza unisce una base editoriale leggibile a superfici operative compatte: molto spazio per orientarsi, dati densi solo dove servono, colore usato per significato e provenance sempre visibile.

## 2. Principi

1. **Task first** — la prima schermata porta subito a stato, sessioni o fonti.
2. **One source, many views** — i valori dinamici provengono da projection governate.
3. **Realtime is not history** — freshness e tipo di fonte sono espliciti.
4. **Read-only first** — nessun affordance suggerisce comandi non autorizzati.
5. **Progressive disclosure** — hub semplici, dettaglio tecnico raggiungibile.
6. **Accessible by default** — tastiera, contrasto, zoom e reduced motion.
7. **Stable URLs** — il redesign non rompe deep link o ricerca.

## 3. Information architecture

I percorsi principali sono:

- Home;
- Osservatorio;
- Scienza e Analytics;
- Operations;
- Architettura;
- Governance e documentazione;
- Manuale tecnico.

La navigazione desktop privilegia gli hub. Il drawer e la navigazione Material mobile espongono il catalogo completo.

## 4. Foundations

### 4.1 Color

| Token | Light | Dark | Uso |
|---|---|---|---|
| dsg-paper | #f6f9fc | #07111f | pagina |
| dsg-surface | #ffffff | #0d1a2b | card e pannelli |
| dsg-text | #102035 | #edf5ff | testo principale |
| dsg-text-muted | #53657a | #a8b8ca | testo secondario |
| dsg-blue | #1769e0 | #69a7ff | azioni e link |
| dsg-cyan | #16b8d4 | #53d7eb | dati e freshness |
| dsg-green | #168a67 | #57d4aa | stato valido |
| dsg-amber | #bd6b00 | #f1b45b | attenzione |
| dsg-red | #c33d4b | #ff7c89 | errore o rischio |

Il colore non è mai l'unico portatore di informazione.

### 4.2 Typography

- corpo pagina: equivalente ad almeno 16 px;
- label operative: almeno 14 px nel contesto Material;
- metadati secondari: mai sotto 12 px;
- line-height corpo: 1.6–1.75;
- heading compatti, peso 700, tracking leggermente negativo;
- percorsi, ID, unità e file in monospaziato quando utile.

Non vengono caricati font esterni.

### 4.3 Layout

- contenuto massimo: 88 rem;
- pagina documentale: colonna leggibile con side navigation;
- hub: griglia responsive a 12 colonne;
- spaziatura verticale di sezione: 2,8–6,5 rem;
- card: raggio medio, bordo sottile, ombra contenuta;
- tabelle: superficie separata e scroll controllato su mobile.

## 5. Components

### Portal shell

Gestisce pagina, tipografia, link, tabelle, admonition, breadcrumb e navigazione precedente/successiva.

### Primary navigation

Contiene brand, sei hub, package corrente derivato dalla roadmap, ricerca, tema e drawer completo. Deve essere idempotente con Instant Navigation.

### Hero

Usato soltanto negli hub principali. Titolo, sintesi e massimo due azioni. Non deve impedire l'accesso al contenuto primario.

### Governed snapshot

Mostra:

- nome della fonte;
- data o freshness;
- stato o valore;
- collegamento al dettaglio;
- fallback loading/error non ambiguo.

### Cards

Una card risponde a un'unica domanda e contiene una sola azione. Titolo e azione restano descrittivi; vietati link come “clicca qui”.

### Status

Ogni stato include testo, non solo colore. UNKNOWN, STALE, PARTIAL, UNAVAILABLE e NOT REPRESENTED restano distinti.

### Drawer

Requisiti:

- aria-hidden coerente;
- inert quando chiuso;
- chiusura con Escape e backdrop;
- focus spostato alla chiusura e poi restituito al trigger;
- gruppi basati sul modello mentale, non sui nomi delle cartelle.

## 6. Dynamic content

1. I consumer usano projection versionate.
2. I fetch di stato corrente usano cache no-store.
3. Le proprietà additive sconosciute sono tollerate.
4. Il dato mancante non diventa zero.
5. I fallback non contengono valori storici plausibili.
6. La homepage legge con no-store le projection pubblicate dopo ogni sessione importata.
7. Lo stato roadmap è aggiornato dalla pipeline di proiezione governata.
8. Nessun consumer scientifico aggira Scientific Data Engine quando il catalogo è coinvolto.

## 7. Responsive behavior

| Viewport | Regola |
|---|---|
| Desktop | custom navigation, griglie multi-colonna, side navigation |
| Notebook/tablet | brand compatto, griglie a due colonne |
| Mobile | navigazione Material nativa, singola colonna, controlli full-width |
| Zoom 200% | nessuna sovrapposizione o perdita di azioni |

## 8. Accessibility

- focus visibile con spessore 3 px;
- ordine heading coerente;
- landmark semantici;
- alt text per immagini informative, alt vuoto per logo duplicato;
- controlli raggiungibili da tastiera;
- stato comunicato testualmente;
- prefers-reduced-motion rispettato;
- target touch con altezza indicativa minima 44 px;
- contenuto statico utile senza JavaScript.

## 9. Motion

Animazioni limitate a feedback brevi, reveal non essenziali e transizioni di drawer. Nessun contenuto critico dipende dal movimento. Le animazioni vengono ridotte quando richiesto dal sistema.

## 10. Content design

- italiano chiaro per navigazione e istruzioni;
- termini tecnici inglesi mantenuti quando canonici;
- nessuna promessa generica di innovazione;
- distinzione costante tra current, historical, planned e superseded;
- date e source vicino ai dati che qualificano;
- niente contatori manuali quando esiste un generatore.

## 11. CSS and JavaScript rules

- prefisso dsg-;
- token centralizzati in theme-tokens.css;
- shell condivisa in portal-shell.css;
- CSS di componente separato;
- niente nuovi stili inline;
- JavaScript incapsulato, idempotente e compatibile con document$;
- loading, empty, error e degraded state;
- nessuna dipendenza aggiuntiva per il solo styling.

## 12. Validation checklist

- [ ] un solo H1;
- [ ] percorso primario riconoscibile;
- [ ] light e dark mode;
- [ ] desktop, tablet e mobile;
- [ ] tastiera, Escape e focus;
- [ ] zoom testo 200%;
- [ ] fallback senza dati stale;
- [ ] JavaScript syntax check;
- [ ] regression test dei generatori;
- [ ] mkdocs build --strict;
- [ ] link e nav coerenti;
- [ ] CI su exact head;
- [ ] Pages post-merge.

## 13. Governance

Una modifica significativa richiede aggiornamento coordinato di Design System, solution architecture, audit freshness quando applicabile, release note, navigation e validation evidence.

## 14. Revision history

| Versione | Data | Stato | Descrizione |
|---|---|---|---|
| 1.0 | 26/07/2026 | Superseded | Prima emissione UI 6.1 |
| 2.0 | 10/09/2026 | Proposed | Redesign UI 7.0, nuova IA e dynamic content contract |
