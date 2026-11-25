# ACS 11677 · Preselezione astrometrica a due bande sullo stesso amplificatore

Il programma GO-11677 ha osservato 47 Tucanae in F606W e F814W con ACS/WFC a orientamenti differenti. Per il controllo sono state fissate sei visite pubbliche, distribuite lungo la campagna. Il catalogo MAST lega due associazioni per visita. Per associazione è stato scelto il primo membro in ordine lessicografico che dispone di RAW, FLT, FLC e headerlet FLT, prima di leggere il WCS. Le risposte MAST a due pagine e a pagina singola coincidono per 1.272 record di prodotto nel confronto di associazione, nome, URI e dimensione. [Descrizione osservativa GO-11677](https://arxiv.org/abs/1112.1426) · [MAST CAOM](https://mast.stsci.edu/api/v0/_services.html)

Il controllo usa i 12 headerlet CALACS con modelli SIP e tabelle di distorsione. Proietta una griglia interna di 8.001 punti per chip sulle quattro immagini di ogni coppia di visite. Sono richiesti la presenza in tutte e quattro le proiezioni, lo stesso chip, la stessa metà X e almeno 550 pixel di differenza Y in **entrambe** le bande. Il risultato è preliminare e sarà confrontato con i WCS e le dimensioni delle immagini complete. [Riferimento WCS HST](https://hst-docs.stsci.edu/drizzpac/chapter-4-astrometric-information-in-the-header/4-5-absolute-astrometry)

Nove coppie di visite soddisfano i criteri in almeno un chip, per 15 combinazioni coppia/chip. La copertura massima è 1.852 punti per jb6v01/jb6v24 sul chip 1, con riferimenti astrometrici misti. Per la prima prova sono fissate **jb6v01/jb6v04 sul chip 1**, la combinazione con maggiore copertura fra quelle con riferimento Gaia EDR3 comune nei quattro headerlet.

| Visita | F606W | F814W |
| --- | --- | --- |
| jb6v01 | jb6v01dfq | jb6v01dqq |
| jb6v04 | jb6v04a4q | jb6v04aeq |

La selezione contiene 1.791 punti di griglia nella regione utile e conserva nome, URI e dimensione dei quattro FLT/FLC corrispondenti. I punti sono geometria campionata. Servono immagini complete, attribuzione delle stelle, telemetria, DQ, saturazione, supporto di apertura, tempi e calcolo di incertezza per un confronto fotometrico. Non viene applicata alcuna correzione CTE. Zero misure fotometriche, zero avvii nativi e zero chiusure scientifiche.

Replay dagli archivi su H: identico byte per byte. SHA-256 riscontro `cd17e2d9e73a3e116f5036a764c8b2192659c98a0391e092ddcf449aaa7a2512`. SHA-256 selezione `ff2f4fab143049b6437bda12a7a79fdd07881798b21ea71318ae76f8cec142cc`. SHA-256 archivio `ae8c4245ddb00c134a72bc13cbc3409d789335860ed0962cb48bab1d0414992c`.

[Controllo precedente sul campione 17979](BKL-046-ACS-17979-47TUC-INCROCIO.md).
