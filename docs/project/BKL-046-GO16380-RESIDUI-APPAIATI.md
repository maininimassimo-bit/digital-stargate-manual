# BKL-046 · Residui affine appaiati nelle due pose GO16380

Il confronto usa soltanto le stelle dei tasselli dispari con margine di 56 pixel, valide in entrambe le [prove affine](BKL-046-GO16380-AFFINE-TASSELLI.md). L'abbinamento è esatto per sensore e coordinate A40. I residui e i fit originali sono letti dalle ricevute già congelate. Per valutare la stabilità dei coefficienti, ogni posa è stata valutata anche con il modello stimato sui tasselli pari dell'altra. Nessun coefficiente è stato stimato sui tasselli di verifica.

| Sensore | Stelle / tasselli appaiati | P90 residuo medio vettoriale | P90 metà della differenza | Sorgenti > 0,1 px in entrambe |
| --- | ---: | ---: | ---: | ---: |
| 1 | 40 / 14 | 0,163830 px | 0,037566 px | 9 |
| 2 | 40 / 14 | 0,102737 px | 0,023501 px | 4 |

Sul sensore 1, l'intervallo percentile del P90 del residuo medio, ricavato ricampionando 2.000 volte i tasselli appaiati, è [0,112920, 0,220529] pixel. Sul sensore 2 è [0,078121, 0,127580]. I P90 ottenuti scambiando i coefficienti fra le due pose sono 0,208659 e 0,177060 pixel sul sensore 1, 0,133050 e 0,092854 pixel sul sensore 2.

La componente che si ripete sulle stesse stelle è maggiore della variazione tra pose. Le due pose condividono guide, coppia breve, campo e procedura di selezione. La decomposizione non attribuisce la causa a uno di questi fattori. Non è stato valutato alcun recupero del flusso, e l'asse `SATURATION_BLEND/4` resta aperto. La prossima discriminazione richiede un riferimento geometrico con errori indipendenti dalle due guide.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `0ea36cf500bdd7760dd0df350e141aee50650eb55811e3bbe76406e5d42c19b2` |
| Ricevuta con residui vettoriali e intervalli | `14cd555bc8eaf01dd5794c392ff168d3c8db3085283a52c3e03ee61817a35a4d` |
