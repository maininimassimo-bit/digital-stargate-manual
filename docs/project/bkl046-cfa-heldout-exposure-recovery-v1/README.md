# BKL-046 · Recupero della risposta CFA con una posa di verifica indipendente

La prova usa i riquadri già verificati delle due scene Cambridge. La stima usa solo le pose da 0,125 e 0,25 s. La posa da 0,5 s, con fotositi lontani dal limite e sopra il minimo di segnale, fornisce un riscontro indipendente in DN/s. Le pose da 1 e 2 s sono confrontate come registrate, con sostituzione al limite del decoder, con sostituzione al codice osservato di 3.651 DN e con una transizione lineare nel 5% dell'intervallo prima di quel codice. [Dataset Cambridge](https://doi.org/10.17863/CAM.6881) · [Registrazione e risposta a dose crescente](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/7e27bf81d101de702fb546de1239bd1a2c39f730/docs/project/bkl046-cfa-registered-dose-response-v1)

| Posa da 2 s | Riquadri | P90 per fase dei campioni al limite, registrato → sostituzione al codice osservato | Celle con solo alcune fasi al limite | P90 R/G medio → dopo sostituzione | P90 B/G medio → dopo sostituzione |
| --- | ---: | ---: | ---: | ---: | ---: |
| Scena 1 | 11 | 52,83–71,18% → 2,75–3,79% | 855 | 154,72% → 27,30% | 161,24% → 20,90% |
| Scena 2 | 6 | 19,22–65,43% → 2,23–2,60% | 17.290 | 111,02% → 13,45% | 86,74% → 10,05% |

Nella scena 1 i limiti del decoder sono sopra il plateau osservato. La sostituzione basata solo sul decoder lascia invariati gli errori della tabella. La transizione lineare porta il P90 R/G medio della scena 1 da 27,30% a 26,87%, e quello B/G medio da 20,90% a 20,29%. I rapporti sono tra campioni nativi nelle celle Bayer e usano la media dei due verdi. Non sono immagini RGB ricostruite.

Il miglioramento sui fotositi riconosciuti al plateau è misurabile. Il recupero delle proporzioni tra fasi resta meno accurato sulle celle parzialmente sature. Le scene statiche di laboratorio, la selezione dei riquadri e l'assunzione di linearità del riferimento a 0,5 s limitano il risultato. Non sono stati recuperati flussi astronomici né qualificato un processo nativo.

Per ripetere, eseguire `verifica.py` con la directory del protocollo, la directory estratta dello studio registrato, la directory estratta degli originali Cambridge, i pacchetti rawpy del wheel verificato, le DLL VCLibs e un nuovo file di uscita.
