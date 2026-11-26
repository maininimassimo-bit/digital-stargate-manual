# BKL-046 · Ingressi ACS storici per i controlli F658N/F660N

Il censimento CADC in F658N e F660N ha restituito 116 righe per GD71, GD153 e G191B2B. I gruppi includono esposizioni, combinazioni e prodotti derivati. Per GD71 il programma 9020 aggiunge due visite con due FLT in ciascuna banda. I FITS completi MAST coincidono con le intestazioni già acquisite. [HST al CADC](https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/hst/) · [HST al MAST](https://archive.stsci.edu/hst/)

| Controllo | Geometria verificata | Saturazione DQ nell'immagine |
| --- | --- | --- |
| GD71, 9020, visita j8c103 | WFC1-FIX, chip 1, amplificatore A | Nessun flag nelle quattro pose |
| GD71, 9020, visita j8c104 | WFC2-FIX, chip 2, amplificatore C | Nessun flag nelle quattro pose |
| G191B2B, 10054 | WFC1-1K, chip 1, amplificatore B | Nessun flag nelle quattro pose strette. Un flag in ciascuna delle due immagini F606W |

Nelle 14 pose PCTECORR è OMIT. GD71 nel 9020 aggiunge due configurazioni e due epoche dello stesso programma. Il confronto con il 10054 cambia anche amplificatore e, per una visita, chip. G191B2B estende il confronto tra stelle del 10054. I dati consentono una successiva misura di fotometria e di sensibilità alla configurazione. L'acquisizione non isola la CTE e non stabilisce se il flag F606W cade nell'apertura stellare. La calibrazione ACS usa standard di questa famiglia. [Calibrazione fotometrica ACS](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/zeropoints)

Gli originali e i riscontri completi sono conservati nelle cartelle GD71-9020 e G191B2B-10054 dell'archivio. Per ripetere la verifica, usare Python, le dipendenze ACS archiviate e la modalità offline per ciascun verificatore. I due riscontri pubblici attestano l'identità e l'integrità degli ingressi. Nessuna nuova misura fotometrica o chiusura scientifica.
