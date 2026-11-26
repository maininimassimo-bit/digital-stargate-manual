# BKL-046 · Riferimento F606W indipendente per G191B2B

La ricerca CADC ha restituito 387 righe con i nomi del bersaglio e 465 per l'intersezione con un cono di 0,01° intorno alle coordinate della posa storica. Le righe descrivono prodotti e includono rappresentazioni multiple della stessa osservazione. La ricerca MAST filtrata ha restituito un errore applicativo e la ricerca MAST per cono è andata in timeout. Le durate qui sotto provengono dagli header FITS dei singoli prodotti FLT recuperati da MAST. [TAP CADC](https://www1.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/doc/tap/) · [API MAST](https://mast.stsci.edu/api/v0/)

| Programma e visite | Posa | Configurazione | Pixel DQ 256 entro 5 px |
| --- | ---: | --- | ---: |
| 9661, j8mj90pmq | 0,5079 s | WFC1-2K, B, gain 4 | 0 |
| 9661, j8mj90pnq | 3 s | WFC1-2K, B, gain 4 | 13 |
| 10374, j97e04rlq / j97e04rmq | 0,7955 s | WFC1-1K, B, gain 2 | 2 / 1 |
| 10054, j8v604xdq / j8v604xeq | 0,7955 s | WFC1-1K, B, gain 2 | 1 / 1 |

La ricerca WCS trova un solo candidato entro 1,25″ per ciascun FITS. Nella posa da 0,5079 s il picco è a 0,38″ dalla posizione cercata e DQ 0. Entro 5 px non risultano flag di saturazione del CCD, saturazione ADC o altre esclusioni oltre alla classe ammessa dal protocollo. Questa posa è un candidato di riferimento da confrontare con la posa satura da 3 s del programma 9661, che ha lo stesso gain e la stessa apertura. Il trasferimento alle pose 10054 richiede una verifica indipendente del cambio di configurazione. Questa selezione non misura un flusso recuperato. [Definizioni dei flag CALACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)

Per ripetere, eseguire `verifica.py` con runtime Astropy, directory dei FITS, protocollo e nuovo file di uscita. Il protocollo vincola i sei FITS per SHA-256. L'archivio su H: conserva risposte, richieste e FITS.
