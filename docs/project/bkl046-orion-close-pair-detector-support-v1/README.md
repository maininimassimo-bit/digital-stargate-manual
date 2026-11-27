# BKL-046 — Esposizioni F555W per le coppie strette di Orione

Il test rilegge sei esposizioni ACS/WFC FLC individuali da 385 s di GO‑10246. I tre sistemi sono fissati nel catalogo NACO precedente. Per ogni posa verifica il chip che contiene la coordinata H97, individua il massimo registrato entro 8 pixel e conserva un riquadro 41 × 41 con SCI, ERR e DQ. Il massimo serve a contare il supporto sul rivelatore. La posizione di una singola componente della coppia richiede una misura distinta.

| Sistema | Radici FLC | Pixel full well in raggio 3 px | Pixel DQ zero nell'anello 4–9 px, su 208 |
|---|---|---:|---:|
| H97 232 | j93k28hcq / j93k76hiq | 7 / 5 | 190 / 197 |
| H97 345 | j93k09o4q / j93k58lnq | 0 / 0 | 200 / 206 |
| H97 488 | j93k0ap3q / j93k57noq | 28 / 29 | 34 / 0 |

Il bit 256 è quello del full well. Nessuna delle sei aperture da 3 px mostra il bit 2048 del convertitore A/D. Tutte le pose coprono le coordinate H97 sul chip 2. Le posizioni WCS dei massimi fra repliche differiscono di circa 0,25, 0,22 e 0,40 arcsec per H97 232, 345 e 488. In due esposizioni il massimo cade vicino al bordo della finestra di ricerca. Questi valori richiedono una registrazione locale, soprattutto perché superano le separazioni NACO di 58, 56 e 131 mas.

H97 232 conserva ali in tutti i settori di entrambe le pose e può entrare in un confronto di recupero con riferimento indipendente. H97 345 offre un caso senza saturazione di full well. H97 488 documenta un caso con perdita estesa di supporto. Restano da verificare l'identità e il flusso delle singole componenti, la corrispondenza tra epoche, la PSF, la registrazione e l'eventuale recupero. Zero esecuzioni native e chiusure scientifiche.

Lo script accetta directory del dossier, directory delle dipendenze, dossier del catalogo, percorso di output, modo replay e una nuova directory per i riquadri. Il replay usa blocchi FITS fissati per ETag e SHA-256. Il rapporto conserva l'impronta di ogni riquadro.

[Catalogo di confronto](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/d5ab8cd34511f50b97f504e06b7e6cb83e2c4920/docs/project/bkl046-orion-close-pair-reference-catalogs-v1) · [Flag DQ ACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)
