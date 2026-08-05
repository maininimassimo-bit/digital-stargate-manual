# Standard di stampa Amazon KDP

| Campo | Valore |
|---|---|
| Identificativo | DSG-BOOK-KDP-001 |
| Progetto | DSG-BOOK-001 |
| Stato | Baseline vincolante |
| Data | 5 agosto 2026 |
| Template | `templates/kdp/amazon-kdp-5.5x8.5-template.docx` |
| Destinazione | Amazon KDP paperback |
| Interno | Bianco e nero, senza bleed |

## 1. Formato definitivo

Il manoscritto usa il formato Amazon KDP:

- larghezza: 5,5 pollici / 13,97 cm;
- altezza: 8,5 pollici / 21,59 cm;
- orientamento: verticale;
- direzione di lettura: sinistra-destra;
- bleed interno: nessuno.

Il formato deriva direttamente dal template Amazon fornito per il progetto. Non coincide con A5 ISO, che misura 14,8 × 21 cm. Nei documenti editoriali il formato viene quindi indicato come **KDP 5,5 × 8,5 pollici**.

## 2. Margini

Il volume target è compreso tra 300 e 400 pagine. KDP richiede per 301-500 pagine un margine interno minimo di 0,625 pollici / 15,9 mm.

La baseline applica:

- margine interno speculare: 0,76 pollici / circa 19,3 mm;
- margine esterno: 0,60 pollici / circa 15,2 mm;
- margine superiore: 0,60 pollici / circa 15,2 mm;
- margine inferiore: 0,60 pollici / circa 15,2 mm;
- distanza intestazione e piè di pagina: circa 0,35 pollici.

I margini sono speculari. La misura interna passa automaticamente dal lato sinistro delle pagine dispari al lato destro delle pagine pari.

Se il volume finale supera 500 pagine, il margine interno deve essere rivalutato prima dell'esportazione: KDP richiede almeno 0,75 pollici per 501-700 pagine.

## 3. Tipografia

| Elemento | Specifica |
|---|---|
| Corpo | Garamond, 11 pt, giustificato |
| Interlinea | 1,05 |
| Rientro prima riga | 0,20 pollici |
| Primo paragrafo di sezione | Senza rientro |
| Titolo capitolo | Garamond, 16 pt, centrato |
| Titolo sezione | Garamond, 12 pt, grassetto |
| Fonti | Garamond, 9,25 pt |
| Intestazioni | Garamond, 8 pt |
| Numerazione pagina | Garamond, 9 pt |

Il corpo non usa spazio aggiuntivo tra paragrafi consecutivi. Il ritmo è affidato al rientro e alla gerarchia delle sezioni.

## 4. Struttura delle pagine

- front matter con numerazione romana;
- pagina del titolo senza intestazione o numero visibile;
- copyright e ISBN;
- sommario;
- eventuale dedica, prefazione e ringraziamenti;
- pagine Parte su pagina dispari;
- ogni capitolo inizia su nuova pagina dispari;
- prima pagina del capitolo senza intestazione o numero visibile;
- corpo con numerazione araba riavviata dal Capitolo 1;
- pagine pari con nome autore in intestazione;
- pagine dispari con titolo breve del libro;
- appendici e informazioni sull'autore nel back matter.

## 5. Figure, tabelle e linee

L'interno corrente non usa bleed. Nessun elemento deve raggiungere il bordo pagina.

Per i contenuti futuri:

- immagini: almeno 300 DPI alla dimensione di stampa;
- testo incorporato nelle immagini: da evitare quando può restare testo nativo;
- linee: almeno 0,75 pt, come raccomandato da KDP;
- grafica in scala di grigi: riempimento almeno 10% quando deve rimanere visibile;
- tabelle: larghezza entro l'area di testo, righe espandibili e intestazioni ripetute;
- didascalie: unite visivamente alla figura o tabella;
- diagrammi: leggibili anche in bianco e nero.

Qualunque futura scelta di bleed richiede una nuova geometria del documento e non può essere introdotta localmente in una singola pagina DOCX.

## 6. Regole redazionali

Il Markdown nel repository rimane la fonte semantica del contenuto. Il DOCX master è la proiezione tipografica per la stampa.

Durante la conversione:

- i link repository diventano citazioni leggibili, senza percorsi tecnici nel corpo;
- gli identificativi rimangono visibili solo quando sostengono la tracciabilità;
- elenchi puntati e numerati usano definizioni Word reali;
- i titoli usano stili Word, non formattazione manuale;
- le fonti sono separate dal testo narrativo;
- il codice e le configurazioni di dettaglio restano esclusi dal libro;
- il sommario e i numeri di pagina vengono aggiornati prima della release.

## 7. Quality gate per ogni milestone

Ogni aggiornamento editoriale deve:

1. aggiornare i file sorgente del libro;
2. rigenerare il DOCX dal template KDP;
3. verificare dimensioni pagina e margini speculari;
4. renderizzare tutte le pagine in PNG e PDF;
5. controllare visivamente copertina interna, front matter, aperture capitolo, elenchi, fonti e ultima pagina;
6. verificare assenza di clipping, sovrapposizioni, link Markdown visibili e numerazioni incoerenti;
7. registrare numero di pagine e parole;
8. conservare il DOCX master e il PDF print-ready come artefatti di release, non come fonti primarie.

## 8. Controllo finale KDP

Prima del caricamento:

- ricontare le pagine sul PDF definitivo;
- verificare il margine interno rispetto alla fascia KDP effettiva;
- incorporare i font nel PDF;
- controllare dimensione pagina 5,5 × 8,5 pollici;
- verificare assenza di crop mark, commenti e revisioni;
- verificare ISBN e pagina copyright;
- aggiornare sommario e riferimenti;
- usare il Print Previewer KDP;
- ordinare una prova di stampa prima della pubblicazione.

## 9. Riferimenti ufficiali

- [KDP - Set Trim Size, Bleed, and Margins](https://kdp.amazon.com/en_US/help/topic/GVBQ3CMEQW3W2VL6)
- [KDP - Paperback Submission Guidelines](https://kdp.amazon.com/en_US/help/topic/G201857950)
- [KDP - Format Your Paperback](https://kdp.amazon.com/en_US/help/topic/G201834190)
