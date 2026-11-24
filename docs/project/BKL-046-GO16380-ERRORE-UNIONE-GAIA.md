# BKL-046 · Errore Gaia nell'unione delle coppie dirette e spostate GO16380

Sul sensore 2, l'[unione per sorgente](BKL-046-GO16380-SPOSTAMENTO-CALIBRATO.md) contiene 25 stelle in 13 tasselli di calibrazione e 28 stelle in 12 tasselli di verifica. Per ogni sorgente il protocollo usa la media dei due centroidi della coppia diretta, se disponibile, oppure la media della coppia spostata riportata nel sistema A40. La rimisura della coppia spostata riproduce le distanze fra i centroidi della ricevuta precedente. Il sensore 1 rimane sotto il minimo di copertura.

| Modello stimato sui tasselli pari | P90 sulle 28 stelle di verifica | Riferimenti entro 0,1 pixel |
| --- | ---: | ---: |
| Affine comune | 0,244604 px | 10 |
| Affine con traslazione distinta per le pose spostate | 0,104057 px | 24 |

Con la traslazione distinta, il P90 è 0,093897 pixel sui 20 riferimenti diretti e 0,128140 sugli otto ricavati dalle pose spostate. Questi conteggi per sottogruppo sono descrittivi. Il P90 della popolazione di verifica resta superiore a 0,1 pixel. Con il raggio di associazione fissato a 0,4 pixel, nessuna delle 28 stelle coincide con le 40 sorgenti appaiate nelle esposizioni profonde. Il confronto con Gaia non può quindi attribuire lo scarto ricorrente di quel campione.

La misura riguarda l'accordo con Gaia nel sistema A40, condizionato dai filtri di selezione, dalle incertezze del catalogo e dai modelli di proiezione. L'asse `SATURATION_BLEND/4` resta aperto. Nessuna sostituzione di pixel, prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `b9ba1b31ea0e5b5254493012095026e1610eebfe55f699691fcc87ac8359db7f` |
| Programma | `78d7c41c291766050c02d66103afa22833f87aa00b0cd75a5b0fba20ecbca48c` |
| Ricevuta con residui per sorgente | `2a4dd5e2c6849889fe159caac47a4b99a739fb2e2899ab2a1828bd9ef2ec4a8d` |
