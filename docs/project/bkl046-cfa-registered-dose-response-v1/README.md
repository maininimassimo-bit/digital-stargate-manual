# BKL-046 · Risposta per fase su sequenze CFA a dose crescente

Ho confrontato le pose RAW Canon EOS 1000D delle due scene statiche Cambridge. Il protocollo richiede lo stesso riquadro ad ogni dose, correlazione almeno 0,80 e spostamento stimato entro 0,40 pixel nativi. Entrano 11/20 riquadri nella scena 1 e 6/20 nella scena 2. Le misure successive leggono i fotositi originali senza interpolazione. Per ogni fase, la risposta attesa deriva soltanto dalle pose da 0,125 e 0,25 s, con accordo dei tassi entro il 3% e un margine dal massimo osservato. [Origine delle sequenze](https://doi.org/10.17863/CAM.6881)

| Posa da 2 s, campioni con atteso almeno 5% sopra 3.651 DN dopo sottrazione del nero | Campioni | Codice esattamente 3.651 DN | Almeno al limite del decoder |
| --- | ---: | ---: | ---: |
| Scena 1 | 23.352 | 23.330 | 0 |
| Scena 2 | 255.749 | 255.724 | 255.749 |

Nella scena 1, per questi campioni la risposta mediana scende dal 28,3% al 60,6% sotto l'atteso secondo la fase. Nel gruppo con atteso sotto il 60% del massimo, lo scarto mediano rimane fra +0,72% e +1,78%. Il P90 assoluto è fra 4,19% e 5,77%. Le statistiche a bassa dose descrivono la dispersione nei riquadri selezionati. L'accumulo al codice 3.651 a dose più alta, in presenza di attesi diversi, documenta il limite del segnale registrato in questa acquisizione.

Il risultato è condizionato alla registrazione locale, all'accordo delle pose brevi e al modello lineare usato per la previsione. Non stima in elettroni la capacità del sensore e non applica ricostruzione ai pixel saturi. Le due scene sono di laboratorio. L'incertezza su dati astronomici, sul ripristino del flusso e sulla ricomposizione RGB resta aperta. [Controllo precedente dei codici RAW](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/e52b2a97e614eec921cdb69711d1f90ad29f628f/docs/project/bkl046-cfa-static-raw-exposure-brackets-v1)

Per ripetere, eseguire `verifica.py` con la directory di questo protocollo, la directory estratta dei CR2 Cambridge, la directory rawpy estratta dal wheel verificato, la directory SciPy, le DLL VCLibs e un nuovo file di uscita.
