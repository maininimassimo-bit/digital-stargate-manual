# BKL-046 · Comparatore XDRZ integrato nella prova isolata R4

La prova usa il coordinatore installato con un registro temporaneo e il comparatore CFA effettivo, con il suo SHA-256 congelato. I dieci FITS e i messaggi console sono generati dalla fixture. Il parent Windows originale resta quello legato all'handle custodito da R4. Dopo la sua uscita zero, l'operatore confronta i risultati e rilegge gli hash di ogni FITS, del log e della ricevuta prima di chiedere il rilascio.

| Caso | Riscontro |
| --- | --- |
| FITS e log conformi, parent originale uscito a zero | Comparatore e rilettura passano. R4 rilascia la prenotazione di prova. |
| Uscita non zero del parent | Il custode conserva la prenotazione di prova. |
| FITS difforme | Il comparatore respinge l'uscita e il rilascio non viene chiesto. |
| FITS modificato dopo l'esito favorevole | La rilettura rileva la modifica e il rilascio non viene chiesto. |
| Prenotazione precedente presente | Nessun nuovo parent viene creato. |

Le due esecuzioni producono la stessa ricevuta. I 30 file del registro operativo hanno conservato le impronte. Il confronto degli hash riguarda il registro e i prodotti temporanei. Restano da verificare la produzione dei FITS e della console da PixInsight, la custodia della sua finestra originale e la pubblicazione dei risultati sotto il binding revisionato. Zero esecuzioni native.

Ricevuta SHA-256 `4649af04104dd1847a2a26a3d4fe80f25b6ae67f98c7e194e2a74dc3dd94761c`.
