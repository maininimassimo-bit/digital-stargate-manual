# ACS 11677. Replica storica completata su DSG-Shared

AstroDrizzle 3.11.0 ha eseguito il braccio con MDRIZTAB riga 4 sui sei FLC in F606W dell'associazione `jb6v01010`. La replica ha usato il WCS incorporato e una lista ordinata in luogo dell'ASN originale. Il confronto dei log copre 93 parametri comuni. Gli 87 valori coincidenti comprendono tutti i 60 parametri scientifici controllati. Le sei differenze registrate riguardano lista di ingresso, nomi d'uscita e di log e conservazione degli intermedi.

| Piano FITS | Pixel confrontati | Differenze | Scarto assoluto massimo |
| --- | ---: | ---: | ---: |
| SCI | 20.480.144 | 263 valori finiti | 0,000003814697265625 elettroni/s |
| WHT | 20.480.144 | 150 valori | 0,0009765625 |
| CTX | 20.480.144 | 0 | 0 |

La griglia e l'ordine delle dodici associazioni tra bit e ingresso coincidono. La copertura con peso positivo e la posizione dei campioni SCI non finiti coincidono. Il massimo scarto WHT è 2 ULP. Negli SCI il massimo è 243 ULP, quindi l'accordo resta numerico e l'impronta dell'intero FITS della replica è distinta. Non è stata attribuita una causa ai residui.

Le dodici maschere trasferite hanno le impronte rilevate prima dell'esportazione e riproducono il bit archivistico DQ 4096 in tutti i 100.663.296 pixel. Nelle 340 scie sature della posa L1457, tutti i 14.372 flag archivistici sono riprodotti e non compaiono flag aggiuntivi. Per le 29.087 proiezioni fissate sul chip 2 si riproducono le 3.046 coincidenze tra pose e l'intera distribuzione descrittiva del controllo a rotazioni cicliche.

Il confronto dimostra la riproducibilità della configurazione storica per questo insieme di dati. Rimane da completare il confronto con Driz_CR disattivato. La ricorrenza del flag non stabilisce la natura astrofisica dei pixel. PixInsight non è stato avviato.
