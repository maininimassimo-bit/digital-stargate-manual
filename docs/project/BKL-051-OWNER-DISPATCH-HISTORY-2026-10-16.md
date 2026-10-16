# BKL-051 — cronologia tecnica nel candidato Owner

La UI candidata è integrata localmente con il backend `ed18a0a6`. Il registro
Owner conserva l'intera cronologia: nessun evento viene eliminato per adattarlo
al contratto precedente e l'impronta dell'ultimo evento resta quella del servizio.

Il nuovo validatore riconosce `DISPATCH_INTENT`, `START_ADMISSION`,
`FRAME_CLOSURE` e `UNRESERVED_FENCED_CLOSURE`. Verifica richieste e fatti esatti,
autorità e attori, contesto congelato e relativo hash, sequenza delle ammissioni,
chiusure, riferimenti di recupero e barriera senza attempt. Gli esiti con intento
vincolato devono corrispondere ai tre job, input e rapporti delle esatte chiusure.
Le dichiarazioni di arresto rimangono Worker-reported; una dichiarazione Owner di
quiescenza non diventa attestazione del processo né accettazione scientifica.
La prima ARB ha rilevato che un esito poteva precedere le prove a cui era legato.
Il candidato corretto richiede che intento, ammissioni e chiusure precedano
l'esito nella catena; cerca anche eventuali intenti futuri prima di applicare
l'eccezione storica senza intento. Rapporto e sorgenti respinti sono conservati.

Un ciclo completo comprende almeno 534 eventi: creazione e congelamento, 59
intenti, 177 ammissioni, 177 chiusure, 59 esiti, 59 revisioni e accettazione finale.
Il precedente limite di 512 era insufficiente. Il candidato ammette al massimo
1.024 eventi senza troncare la cronologia, conservando il limite del trasporto di
8 MiB. I limiti della coda (512 elementi) e del registro backend non cambiano.

Le prove generano ricevute attraverso gli effettivi servizi applicativi e la coda
in memoria, con sole fixture dichiarate. Comprendono il ciclo di 534 eventi,
campagna parziale, recupero, chiusura senza prenotazione e alterazioni di fatti,
autorità, ordine e legami con gli esiti, anche dopo il ricalcolo della catena.
Non sono prove native, controlli nulli reali o qualificazione di dati astronomici.

Questo incremento aggiorna soltanto il contratto di lettura e le etichette.
Restano la preparazione durevole delle operazioni Owner, i comandi di dispatch,
l'esportazione dell'handoff, il recupero assistito e la verifica visiva sul
candidato integrato. La memoria del browser non sostituisce fsync locale.
Build, ARB/RQ, CI, merge e verifica post-merge sono gate distinti: nessun rilascio
o servizio è attivato da questo documento. R09 e milestone restano aperti,
`NOT_VALIDATED`, con zero controlli reali qualificati.
