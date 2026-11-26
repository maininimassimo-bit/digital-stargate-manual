# BKL-046 — Confronto ePSF a una e due componenti su Orione F555W

Il test usa la libreria empirica ufficiale STScI STDPBF_ACSWFC_F555W_SM3, con nove piani di fuoco e una griglia di PSF sovracampionate quattro volte. I riquadri SCI/ERR/DQ vengono dal precedente controllo delle pose ACS/WFC. L'interpolazione usa i nodi del chip 2 e le coordinate del massimo registrato. Il confronto usa pixel a DQ zero, pesati con ERR, e un fondo planare. La griglia di pixel viene suddivisa in due insiemi alternati. Posizioni, ampiezze, fondo e indice di fuoco sono ottimizzati sulla porzione di stima e valutati sull'altra. Le stime per tutti i modelli di fuoco si trovano nel rapporto.

| Sistema | Esito |
|---|---|
| H97 232 | Il modello doppio riduce il residuo in tre verifiche su quattro. Le separazioni stimate vanno da 0,35 a 3,99 px e raggiungono entrambi i limiti di ricerca. I residui pesati restano elevati. |
| H97 345 | Il vantaggio del modello doppio è pressoché nullo. Le separazioni stimate cambiano da 1,41 a 3,66 px, con rapporti di flusso instabili. |
| H97 488 | Escluso dal fit con il criterio congelato di almeno otto pixel puliti in ogni settore delle ali. |

Il controllo numerico senza rumore, costruito con la stessa libreria, riproduce 1,4734 px come 1,4769 px. Verifica l'implementazione su un caso noto. I pixel intercalati della stessa immagine condividono sistematiche strumentali. Non producono un test statistico indipendente di binarietà. Le immagini reali non forniscono una separazione o un rapporto di flusso riproducibili con questo confronto. Restano da verificare l'associazione del picco, la dipendenza dalla PSF e la conservazione di flusso nelle componenti, sulle immagini reali e nella prova nativa. Zero esecuzioni native e chiusure scientifiche.

Lo script accetta directory del dossier, directory runtime, dossier dei riquadri sul rivelatore e percorso di output. La libreria e tutti i riquadri vengono riletti per SHA-256 prima del calcolo.

[Librerie ePSF ACS/WFC](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/psf) · [Riquadri e supporto sul rivelatore](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/7ec7a542cd63deccbbe9e552e3e86b1981271744/docs/project/bkl046-orion-close-pair-detector-support-v1)
