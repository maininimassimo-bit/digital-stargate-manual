# Typography

| Campo | Valore |
|---|---|
| Documento | Typography |
| ID | `DSG-DS-TYP-001` |
| Stato | Controlled Baseline |
| Fonte | Material for MkDocs theme, `docs/ui/design-system.md` |

## Font Families

Il portale usa la tipografia fornita dal tema Material for MkDocs. Non sono autorizzati font esterni da questo baseline.

| Uso | Regola |
|---|---|
| Testo principale | Font predefinito Material for MkDocs. |
| Codice, percorsi, identificativi | Font monospaziato Material. |
| Titoli | Gerarchia Material, senza override non governati. |
| Tabelle e dashboard | Font Material con dimensioni compatte e leggibili. |

## Font Hierarchy

| Livello | Uso | Regola |
|---|---|---|
| H1 | Titolo pagina unico. | Uno solo per pagina, coerente con navigazione. |
| H2 | Sezioni principali. | Usare per blocchi stabili e scansionabili. |
| H3 | Sottosezioni. | Usare per dettagli tecnici, componenti e pattern. |
| H4 | Dettagli locali. | Evitare profondita eccessiva. |
| Body | Descrizioni e procedure. | Frasi brevi, lingua tecnica chiara. |
| Caption/meta | Stato, owner, versione, fonte, data. | Testo secondario ma leggibile. |
| Code | ID, path, token, comandi. | Sempre in monospaziato. |

## Titles

I titoli devono indicare esattamente il contenuto della pagina o sezione. Evitare titoli promozionali o generici.

Esempi coerenti:

- `Observation Session`
- `Executive Observatory Dashboard`
- `Architecture Decision Catalog`
- `Repository Quality Model`

## Cards

Le card devono usare titoli brevi e descrizioni concise. Una card deve rappresentare un solo oggetto o una sola azione.

Regole:

- titolo chiaro;
- descrizione massimo 2-3 righe;
- KPI o stato ben separato dal testo;
- link o azione primaria non ambigua;
- nessun blocco testuale lungo dentro card operative.

## Tables

Le tabelle sono componenti centrali del portale tecnico.

| Tipo contenuto | Allineamento |
|---|---|
| Testo | Sinistra |
| Numeri | Destra |
| Stati brevi | Centro o badge testuale |
| Codici e ID | Monospaziato |
| Date | Formato coerente e leggibile |

Ogni tabella deve avere intestazioni chiare e, quando applicabile, unita di misura.

## Dashboard

Le dashboard devono privilegiare leggibilita rapida:

- KPI con label, valore, unita e periodo;
- testi brevi;
- legenda e assi comprensibili;
- stato dati visibile;
- messaggio `N/D` quando il dato non e disponibile.

## Spacing

La spaziatura deve seguire Material e le classi esistenti:

| Uso | Regola |
|---|---|
| Sezioni | Spazio sufficiente tra H2 e contenuto. |
| Card grid | Gap coerente con `1rem` dove gia usato. |
| Dashboard toolbar | Gap compatto tra stato e azioni. |
| Liste | Evitare liste troppo lunghe senza raggruppamento. |
| Tabelle | Separare tabelle complesse con testo introduttivo breve. |

## Reading Rules

- Scrivere in modo tecnico-professionale.
- Preferire frasi dirette a periodi lunghi.
- Evitare buzzword non necessarie.
- Usare la terminologia del Knowledge Framework.
- Non duplicare contenuti architetturali dettagliati dentro pagine UI.
- Mettere informazioni critiche prima dei dettagli.

## Accessibility

- Mantenere ordine gerarchico `H1 > H2 > H3`.
- Non saltare livelli di heading per ragioni estetiche.
- Link descrittivi, non `clicca qui`.
- Ogni contenuto informativo importante deve essere leggibile senza dipendere solo da colore o posizione.