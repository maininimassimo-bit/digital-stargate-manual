# BKL-046 · Astensione per disaccordo fra riferimenti TV4

La regola confronta i profili centrati delle due strisce disgiunte. Per ogni operatore e direzione fissa la soglia al massimo disaccordo osservato nei due contrasti di calibrazione. Sui due contrasti riservati, se una delle direzioni supera la propria soglia la regola usa la regione grezza. Su dati riservati senza iniezioni entrambi gli operatori applicano la correzione in sette casi su dieci.

Con la contaminazione di 64 pixel su 256 dello [studio precedente](BKL-046-TV4-CONTAMINAZIONE-BORDI.md), una correzione accettata supera ancora il riferimento diagnostico del 5% nei casi seguenti.

| Operatore | Contaminata una striscia | Contaminate entrambe nello stesso modo |
| --- | ---: | ---: |
| Media | 9/80 | 56/80 |
| Media troncata | 11/80 | 56/80 |

Con due riferimenti contaminati allo stesso modo, il disaccordo della media rimane invariato entro la tolleranza numerica. In questa condizione il criterio di accordo non rileva la componente comune. Con 8 pixel contaminati in una striscia, la media passerebbe sempre il riferimento del 5% nella correzione senza veto. La commutazione verso il grezzo modifica comunque l'uscita oltre tale riferimento in 13 casi su 80. Il confronto attribuisce questo effetto alla scelta dell’operatore, distinta dall’alterazione indotta dentro la correzione.

I 640 esiti riguardano iniezioni digitali su una sola acquisizione. La regola da sola lascia esiti oltre il riferimento e richiede altre verifiche, compreso un riferimento esterno o un controllo della componente comune. L’asse DIFFUSE_BACKGROUND/3 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 77214d2927194437362ee89a61d455b0553710976ed95e34fc84cb593d58ca24 |
| Programma | 4c957eee67fbc54db59a01c262443c0b062a13a901c028d0b4e05caaf8488c4d |
| Riscontro replicato da H: | 2483067d28b832b69405ec62bcb96c538f987516f484b030b67f5f04fe3fdd6c |
