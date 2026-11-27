# BKL-046 · Flat TV4 RED a esposizione comandata zero

Il test usa otto pose FLBB24/RED MRI a esposizione comandata zero. L’indice PDS specifica un’integrazione di 3,5 ms. Sono state selezionate otto pose nella stessa directory in ordine di acquisizione. Quattro fissano una mappa osservata a 3,5 ms e quattro intercalate servono per verificarla. Tutte sono distinte dai BIAS e dai flat a esposizione comandata positiva delle prove precedenti. [Archivio NASA PDS TV4](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

Nelle quattro pose di verifica, i blocchi dei flat a comando zero superano in media i BIAS schermati di **42,51–42,59 DN**. La mappa misurata a zero comando li predice con **0,31–0,39 DN RMS**. Il modello stimato sui soli flat a comando positivo, valutato a 3,5 ms, dà **5,42–5,49 DN RMS**. La mappa BIAS dà **42,52–42,60 DN RMS**.

Fissando il modello alla mappa osservata a 3,5 ms e stimando la risposta sui sei flat positivi di calibrazione, l’RMSE a 33,5 e 303,5 ms è **5,01–5,43 DN**. Il modello con intercetta e risposta spaziali stimate sui soli flat positivi conserva **0,53–2,02 DN** su quelle stesse pose. Il controllo diretto mette in evidenza una differenza di regime a comando zero. La sua causa fisica e la separazione dei contributi di illuminazione, ottica e rivelatore restano aperte. I 42 esiti del confronto precedente sono riprodotti senza modifiche. DIFFUSE_BACKGROUND/2 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Inventario delle pose | 9deab4926ee7711d6f5848186cd0b0b69f47d602e9b97d222cdd16330afc61a8 |
| Protocollo | af680df9d74e6fc645496d9c20a3439491e64b4e5fc32b9cc67c3c46a67e8716 |
| Programma | d54155a938ed624ba1a79754fd162797826e4d082f5084af23f4cf2c95367671 |
| Riscontro replicato da H: | 3d11929dc4a54c08e69499ba228f96938d7e5e5268702a385be684f9be55ba2a |
