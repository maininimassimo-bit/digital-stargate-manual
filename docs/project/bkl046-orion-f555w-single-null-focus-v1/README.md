# BKL-046 — Controlli a stella singola e compagna iniettata, ACS/WFC F555W

Lo stesso motore del fit sulle coppie pubblicate è applicato a 18 confronti appaiati. Si usano le posizioni sul rivelatore, le maschere DQ e i valori ERR dei nove riquadri osservati in GO10246. I valori SCI rientrano nel controllo della maschera, mentre le intensità sottoposte al fit sono simulate. Ogni coppia di simulazioni condivide rumore gaussiano, gradiente di fondo e primaria. Il profilo usato per simulare è la media di due livelli adiacenti di fuoco, mentre il fit sceglie fra i nove livelli discreti della stessa libreria. Per ciascuna geometria si usa una sola realizzazione del rumore, riutilizzata a entrambi i livelli di rapporto segnale-rumore nominale (SNR).

L'iniezione usa 100 mas nominali e rapporto di flusso 0,33. La colonna «anche separazione e flusso» richiede guadagno positivo e accordo con i valori dell'iniezione in entrambe le partizioni. Per i casi a stella singola si applica lo stesso criterio per contare le coincidenze spurie con quella specifica iniezione.

| SNR nominale | Stella singola, due guadagni positivi | Stella singola, anche separazione e flusso | Compagna iniettata, due guadagni positivi | Compagna iniettata, anche separazione e flusso |
|---|---|---|---|---|
| 150 | 1/9 | 0/9 | 9/9 | 8/9 |
| 500 | 1/9 | 0/9 | 9/9 | 8/9 |

Questi conteggi valgono per le geometrie, il rumore e la libreria fissati. Le simulazioni condividono riquadri, livelli di fuoco e realizzazioni di rumore, quindi il conteggio non stima il tasso di falsi positivi su un campione stellare indipendente. Mancano controlli negativi osservati e una misura dell'incertezza che tenga conto delle dipendenze. Esecuzioni native e chiusure scientifiche in questo incremento: zero.

Il pacchetto dipende dal dossier positivo F555W (archivio H: SHA-256 de1d88c03411d06bc814f76871c4aea5246a4bd32fdbc87b312c6bf5f3394979) e dalla libreria ePSF separata, la cui impronta è vincolata nel protocollo. [Dossier positivo](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/100daf1b1e1d0d4397870483c73f3a5da6b2ba81/docs/project/bkl046-orion-f555w-published-pair-controls-v1)
