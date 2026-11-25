# BKL-046 — Replica del controllo sul fondo diffuso in IC 1805

Il protocollo di M8/M20 è stato applicato a tre pose grezze di un campo diverso, IC 1805. I 27 riquadri usano la media dei due verdi Bayer. Le coordinate dei riquadri sono scalate nelle proporzioni del nuovo rivelatore e arrotondate al pixel pari più vicino. Il raggio, le forme, le ampiezze, la scelta fra piano e quadratica e il criterio congiunto del 5% su flusso e forma riprendono il protocollo precedente. Le 729 iniezioni digitali riusano tre pose e non costituiscono altrettante acquisizioni indipendenti.

| Profilo | Casi | Senza maschera entro soglia | Maschera automatica entro soglia | Maschera con profilo noto entro soglia |
| --- | ---: | ---: | ---: | ---: |
| Filamento corto | 324 | 0 | 14 | 322 |
| Filamento lungo | 324 | 0 | 1 | 324 |
| Profilo diffuso largo | 81 | 0 | 0 | 0 |

Nel profilo largo, il modello adattivo senza maschera sottrae in mediana il 90,05% del flusso nell'apertura. La maschera automatica si astiene in 3 casi. Negli altri 78 la perdita mediana è 89,56%. La maschera che conosce il profilo si astiene in tutti gli 81 casi per supporto insufficiente. Questo conferma su un campo diverso il limite già osservato in M8/M20. La scelta del grado tramite errore predittivo può conservare un buon fit del fondo e rimuovere segnale diffuso.

I rapporti dei due test sono riprodotti byte per byte. Il risultato resta circoscritto ai modelli offline, all'iniezione digitale e alle immagini provate. La qualificazione del fondo astronomico e la prova nativa restano aperte.
