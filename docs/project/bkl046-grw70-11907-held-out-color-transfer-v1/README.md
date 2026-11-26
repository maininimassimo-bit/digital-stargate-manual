# BKL-046 · Trasferimento della correzione di apertura su GRW+70°5824

Ho completato il censimento delle 74 visite del programma 11907 con tre esposizioni individuali pubbliche nel catalogo fissato. Il controllo precedente comprendeva 12 visite esplorative e un lotto di 20. In questo studio ho acquisito e verificato tutti i 126 FLC esatti delle 42 visite rimanenti, mantenendo la selezione Gaia, il limite sul picco, i veto DQ e le aperture a 5 e 10 pixel. [Primo lotto fissato](../bkl046-grw70-aperture-visit-replication-v1/README.md)

Il controllo astrometrico assoluto Gaia ammette una terna completa, `ibbsc0` su UVIS2. Con la previsione del centro dalle altre due bande, distinta da quella assoluta, cinque delle 42 visite consentono tutte le misure. Insieme alle due del primo lotto, risultano cinque visite su UVIS2 e due su UVIS1. Le 12 visite esplorative restano fuori dalla stima.

La correzione è la mediana del cambiamento di colore da 5 a 10 pixel in almeno due altre visite dello stesso chip. Ho effettuato due verifiche. Nella prima ho lasciato fuori ogni visita a turno. Nella seconda ho fissato la mediana delle due visite utili del primo lotto e l'ho applicata alle tre visite UVIS2 utili del lotto riservato. Il confronto usa il medesimo insieme di visite per il metodo con e senza correzione.

| Colore | Errore assoluto mediano sulle tre visite riservate, senza → con correzione | Errore massimo con correzione |
| --- | ---: | ---: |
| F438W − F606W | 10,00 → 2,59 mmag | 3,02 mmag |
| F438W − F814W | 27,01 → 7,92 mmag | 8,02 mmag |
| F606W − F814W | 12,83 → 6,33 mmag | 10,94 mmag |

La correzione riduce tutti e nove gli errori del lotto riservato. Lasciando fuori una visita alla volta sulle cinque UVIS2, riduce 13 errori su 15 e ne peggiora due. Il massimo residuo è 18,36 mmag. Su UVIS1 mancano due visite di stima per ciascuna previsione. Tutti gli esiti, incluse le esclusioni di centro e DQ, sono conservati.

Il risultato fornisce una verifica fra visite sullo stesso bersaglio e chip nel dominio selezionato. Restano aperti il trasferimento ad altre stelle e chip, la quantificazione dell'incertezza e il confronto nativo. Nessun avvio PixInsight e nessuna chiusura scientifica.

Per ripetere, passare a `misura.py` il kit, il kit dei tre calibratori, la directory con NumPy 2.3.5/Astropy 7.2.0, un nuovo risultato e lo SHA-256 di acquisizione `229491f064feec06e5cef1cc01605fa89bbb3755839af082def9bc794d10eb5b`. Passare a `misura-centro.py` i tre percorsi iniziali, i due rapporti del centro relativo precedenti nell'ordine esplorativo e primo lotto, il nuovo risultato, lo SHA-256 dell'acquisizione e quello del rapporto primario `dc50a0ed1ca637f00ccb7ef214b476e891c20616748bac8c66aa7511cc747360`.