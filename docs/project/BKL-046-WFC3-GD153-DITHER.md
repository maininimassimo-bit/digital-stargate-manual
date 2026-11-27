# GD153 · Identificazione per dither e fotometria a tre bande

L'Instrument Science Report WFC3 2009-31, §3 e tabella 2, identifica GD153 nelle visite 11–14 del programma 11450 e documenta il subarray UVIS1 sull'amplificatore A e il pattern di quattro dither. I 48 FLC già archiviati contengono 16 combinazioni visita/dither con una posa per ciascuna banda. Le immagini calibrate lette hanno dimensioni effettive 512 righe × 513 colonne. [STScI, WFC3 ISR 2009-31](https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/wfc3/documentation/instrument-science-reports-isrs/_documents/2009/WFC3-2009-31.pdf)

Per individuare la sorgente, l'analisi esplorativa cerca il segnale distribuito più alto su una finestra interna 3×3 di pixel finiti con DQ zero. Per ogni posa, la posizione viene predetta dalle altre due bande allo stesso `POSTARG`. La coerenza geometrica è verificata anche rispetto ai tre dither rimanenti della stessa visita, escludendo quello in esame dal fit. La distanza del picco dalla previsione a due bande è al massimo 1,42 pixel. La previsione del dither escluso differisce al massimo di 1 pixel. Il controllo usa un limite di 2,5 pixel per la coerenza tra bande, 3 pixel per il dither e almeno 1.000 elettroni nel pixel di picco. I limiti appartengono a questa analisi esplorativa.

Nell'esposizione `iaah11ddq_flc.fits`, il segnale concordante è a (218, 176) con 5.646 elettroni nel pixel di picco. Il valore precedente di 39,4221 elettroni/s proveniva dall'apertura centrata intorno a (255, 255) e viene ritirato come misura di GD153. La riapplicazione del misuratore, con il solo seme sostituito, restituisce 23.596,47 elettroni/s in F814W per quell'esposizione. Restano attivi i controlli DQ, PAM, fondo, apertura e risposta fotometrica.

| Visita | F438W valide | F606W valide | F814W valide | Terne allo stesso dither |
| --- | ---: | ---: | ---: | ---: |
| iaah11 | 2 | 1 | 2 | 0 |
| iaah12 | 2 | 2 | 2 | 2 |
| iaah13 | 1 | 1 | 1 | 0 |
| iaah14 | 2 | 1 | 1 | 1 |

Sono valide 18 aperture. Quattro pose sono escluse per DQ nel nucleo e 26 per supporto di apertura o fondo. Nella visita 12, le due terne differiscono di 13,06 millimagnitudini in F438W−F606W, 17,68 in F438W−F814W e 4,62 in F606W−F814W. Sono colori derivati dalle aperture, senza correzione differenziale di encircled energy. Le due terne condividono visita e calibrazione, e la visita 14 dispone di una sola terna. Occorrono una verifica indipendente delle misure, la riconciliazione delle aperture con la riduzione pubblicata e una prova confermativa. Il conteggio resta a zero chiusure scientifiche e zero avvii nativi.

La ripetizione dagli archivi riletti su H: ha riprodotto il JSON byte per byte. SHA-256 del riscontro: `b1d08b03e33f3579ad9f08aa49e4ff0c8e273faf379cf4f7488ecbc5b619728e`. SHA-256 dell'archivio: `07b2b84ebf0fb3a5239bd1f9c91b1fcf9dfdab20fd933b77b2ccbe99bdaa5ee7`.

Riscontri precedenti: [visite GD153](BKL-046-WFC3-GD153-VISITE-PUNTATE.md) e [confronto astrometrico](BKL-046-WFC3-GD153-ASTROMETRIA.md).
