# Layout System

| Campo | Valore |
|---|---|
| Documento | Layout System |
| ID | `DSG-DS-LAY-001` |
| Stato | Controlled Baseline |
| Fonte | `mkdocs.yml`, `docs/styles/extra.css`, `docs/styles/analytics.css`, portale corrente |

## Purpose

Il layout system definisce la struttura visiva standard del portale Digital StarGate. Conserva Material for MkDocs e le estensioni `dsg-*` esistenti.

## Grid

Il portale usa la griglia fluida Material con larghezza estesa:

| Elemento | Baseline |
|---|---|
| Pagina | `md-grid` con massimo esteso a `92rem`. |
| Card grid | `repeat(3, minmax(0, 1fr))` su desktop quando coerente. |
| Analytics link cards | Tre colonne desktop, una colonna sotto `900px`. |
| Dashboard shell | Larghezza piena del contenuto disponibile. |
| Tabelle | Larghezza contenuto, scroll controllato se necessario. |

## Responsive Behavior

| Viewport | Regola |
|---|---|
| Desktop | Griglie a 2-3 colonne, dashboard estese, navigazione completa. |
| Tablet | Riduzione colonne, toolbar flessibili, card piu larghe. |
| Mobile | Colonna singola, tabelle scrollabili, toolbar verticali, azioni compatte. |

Il comportamento responsive deve prevenire sovrapposizioni, tagli di testo e layout shift rilevanti.

## Desktop

Su desktop il portale deve offrire densita informativa controllata:

- hero o header solo quando utile alla pagina;
- dashboard con KPI sopra grafici e dettagli;
- card grid coerenti;
- tabelle ampie ma leggibili;
- contenuto centrale non eccessivamente stretto.

## Tablet

Su tablet:

- ridurre colonne a 1-2;
- mantenere pulsanti e badge leggibili;
- evitare iframe o dashboard con altezza insufficiente;
- mantenere header e tab scrollabili.

## Mobile

Su mobile:

- layout a colonna singola;
- azioni una sotto l'altra se necessario;
- card full width;
- tabelle con scroll orizzontale se inevitabile;
- testi lunghi spezzati prima di ridurre eccessivamente il font.

## Sidebar

La sidebar resta quella di Material for MkDocs. Nuove sezioni devono essere introdotte in `mkdocs.yml` in modo coerente con la tassonomia documentale.

Regole:

- non duplicare sezioni equivalenti;
- non creare profondita eccessiva;
- usare label brevi e descrittive;
- mantenere l'ordine di governance quando la sezione e documentale.

## Header

L'header e parte identitaria del portale:

- logo DSG;
- gradiente navy/indigo;
- sottotitolo operativo;
- ricerca Material;
- tabs scrollabili.

Non deve essere sostituito da header specifici di singola pagina.

## Content

Il contenuto deve seguire:

1. titolo;
2. descrizione sintetica;
3. metadati quando governati;
4. contenuto principale;
5. riferimenti o collegamenti.

Le sezioni enterprise e knowledge usano tabelle di metadati. Le dashboard usano toolbar, KPI, grafici e note qualità.

## Footer

Il footer resta gestito da Material for MkDocs. Non creare footer locali salvo pagina speciale approvata da design governance.

## Widget Spacing

| Widget | Spacing baseline |
|---|---|
| KPI card | Gap `1rem` nelle griglie. |
| Dashboard toolbar | Margine inferiore compatto, stato e azione separati. |
| Alert panel | Spazio prima e dopo l'admonition. |
| Log viewer | Altezza stabile e scroll interno se necessario. |
| Timeline | Distanza costante tra eventi. |

## Card Spacing

Le card devono avere padding sufficiente per lettura tecnica e raggio coerente con il portale corrente.

Baseline osservato:

- link card analytics: padding circa `1.1rem 1.2rem`;
- border radius circa `.7rem`;
- shadow `--dsg-shadow-soft`;
- hover leggero senza cambiare struttura.

## Layout Anti-Patterns

- Card dentro card senza necessita.
- Hero promozionali su pagine operative.
- Griglie rigide che rompono mobile.
- Testo sovrapposto a grafici o immagini.
- Pannelli decorativi non collegati a dati o navigazione.
- Footer o header personalizzati che rompono identita Material/DSG.