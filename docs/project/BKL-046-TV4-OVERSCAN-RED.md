# BKL-046 · Verifica dell’overscan nei flat e BIAS TV4 RED

Il test verifica se i bordi di lettura spiegano lo scarto additivo di +29,03 DN osservato nel [confronto BIAS-flat](BKL-046-TV4-BIAS-RED-CONFRONTO.md). Il riferimento strumentale colloca i pixel di overclock ai bordi della matrice. La prova usa sottoinsiemi conservativi e simmetrici per quadrante, lontani dagli angoli e dalla mezzeria, e tratta separatamente righe e colonne. È una diagnostica dei bordi nei prodotti TV4, con geometria e metodo esplicitati nel programma. [Calibrazione Deep Impact, §4.3](https://pdssbn.astro.umd.edu/holdings/dif-m-hriv-2-epoxi-mars-v1.0/document/calibration_paper_draft.pdf)

La differenza fra il bordo di ciascun flat e il bordo mediano dei quattro BIAS viene aggiunta alla mappa BIAS per il quadrante corrispondente. La risposta spaziale viene stimata sui soli flat di calibrazione. I valori delle regioni attive delle pose riservate servono al punteggio.

| Modello | Scarto flat–BIAS nei bordi, DN | RMSE sui tempi riservati, DN |
| --- | ---: | ---: |
| Mappa BIAS con spostamento stimato dai flat di calibrazione | +29,03, comune | 0,58–2,13 |
| Mappa BIAS con correzione dalle colonne esterne | −2 a +3, mediana 0 | 20,67–27,62 |
| Mappa BIAS con correzione dalle righe esterne | +111 a +114, mediana +113 | 54,58–80,89 |

Nessuna delle due misure ai bordi riproduce lo spostamento comune o la capacità predittiva del modello ancorato ai flat di calibrazione. Il risultato riguarda i sottoinsiemi selezionati e lascia aperta l’origine fisica dello scarto, compresa la compatibilità con altri stimatori o con la procedura strumentale completa. I 42 esiti di confronto precedenti coincidono con quelli ricalcolati. DIFFUSE_BACKGROUND/2 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | f47264097253fabe58f3c1d78aa36f083b75651dc600ea30cd2846fddc7c1c09 |
| Programma | 29d0d2a1cef6d0e44d4c813b048a029ce11afdaea727b23d29a46365b53dbb33 |
| Riconciliazione appaiata | c9e41469181ddd2f79fcc6b9d1f101c98de53462969eada4140e2c00aee7ce61 |
| Riscontro replicato da H: | 2689ccc779e4c01ef843027534981f32a1659b4f89e8f54d73d84a1908498d4b |
