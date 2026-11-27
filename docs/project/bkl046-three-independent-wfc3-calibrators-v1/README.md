# BKL-046 · Verifica delle aperture di tre calibratori WFC3 indipendenti da GD153

Ho interrogato MAST senza limite di epoca per un elenco esplicito di alias di GD71, G191‑B2B e GRW+70°5824. Il catalogo restituisce 26, 21 e 198 visite candidate rispettivamente, con almeno un record pubblico in ciascuna delle bande F438W, F606W e F814W. Le visite sono raggruppate per programma e identificativo. La presenza delle tre bande nel catalogo non verifica modalità, geometria, qualità o disponibilità dei singoli FLC. [API MAST](https://mast.stsci.edu/api/v0/_services.html) · [Calibratori UVIS](https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/photometric-calibration/uvis-photometric-calibration.html)

Il protocollo fissa dieci visite prima di aprire i prodotti. Per GD71 e G191‑B2B include tutte le visite candidate nei quattro abbinamenti stella e programma indicati. Per GRW+70°5824 include quattro ranghi equidistanti nella sequenza temporale del programma 11907. I 30 record di catalogo portano a 48 FLC distinti. I FITS appartengono ai bersagli e alle bande attesi e risultano a puntamento fisso con metadati nominali.

| Stella | Visite | FLC | DQ nel nucleo | Supporto insufficiente | Scarto del picco | Terne valide |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GD71 | 4 | 24 | 24 | 0 | 0 | 0 |
| G191‑B2B | 2 | 12 | 12 | 0 | 0 | 0 |
| GRW+70°5824 | 4 | 12 | 1 | 4 | 7 | 0 |

Il bit DQ 16 è presente in tutti i 37 nuclei respinti. Le sette pose GRW+70°5824 respinte per scarto superano il limite di 4 pixel fra il picco locale e la posizione prevista dal WCS. Il test per le pose ammesse richiede entrambe le aperture da 5 e 10 pixel e terne con lo stesso chip, dither e visita entro 0,05 giorni. I rifiuti restano nel rapporto.

Nessuna di queste dieci visite fornisce una terna utile al trasferimento della correzione cromatica di GD153. La verifica limita le coorti riutilizzabili e lascia disponibili altre visite del catalogo. Zero esecuzioni PixInsight e zero chiusure scientifiche.

Per ripetere dalla copia archiviata, eseguire `catalogo.py` sulla directory estratta che contiene le risposte MAST. Passare poi a `misura.py` quella directory, la directory con NumPy 2.3.5 e Astropy 7.2.0, il nuovo percorso di risultato e lo SHA-256 dell'acquisizione `f79146dee9da7a903d488c295548a5f6c0940137da696182bbb9642a5b7b767d`. Il kit H/K conserva le risposte del catalogo e dei prodotti, i FITS e le mappe PAM.