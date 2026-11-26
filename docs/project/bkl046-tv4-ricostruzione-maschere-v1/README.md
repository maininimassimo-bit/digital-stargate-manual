# BKL-046 · Effetto della scelta della maschera sulla ricostruzione TV4

Il controllo riproduce la prova di taglio artificiale e mantiene la stessa previsione per la ricostruzione. Cambia soltanto la selezione dei pixel. Confronta il limite osservato, tre soglie sulla previsione e l'intersezione delle due condizioni. La sostituzione non può produrre un valore sotto il limite artificiale. Le regioni con saturazione originale rimangono escluse.

| Sei pose centrali, taglio all'80%, modello dopo riallineamento con overscan | Pixel misurabili sovrascritti | Pixel con segnale perso esclusi dalla maschera | Riduzione dell'errore assoluto rispetto al taglio |
| --- | ---: | ---: | ---: |
| Limite osservato | 0 | 0 | 91,04% |
| Previsione al limite | 1.165 | 3.984 | 90,83% |
| Intersezione al limite | 0 | 3.984 | 91,04% |
| Previsione con margine di 128 DN | 0 | 22.404 | 86,49% |
| Previsione con margine di 256 DN | 0 | 36.307 | 75,19% |

L'intersezione al limite produce lo stesso errore assoluto della maschera osservata. Nelle posizioni escluse, il valore previsto e limitato inferiormente era infatti il valore di taglio. Un conteggio di pixel non marcati va quindi interpretato insieme all'errore dei valori effettivamente ricostruiti.

Il risultato dimostra sul controllo artificiale il costo di sostituire pixel ancora misurabili usando la sola previsione. La soglia fisica, il recupero del flusso nella saturazione reale e la ricomposizione nativa restano aperti. Non è stata selezionata una soglia sulle pose di verifica. [Controllo precedente con maschera osservata](../bkl046-tv4-ricostruzione-taglio-artificiale-v1/README.md)

Eseguire `misura.py` con il protocollo, la directory congelata della ricostruzione artificiale, la directory della previsione TV4 e una nuova directory per i risultati.
