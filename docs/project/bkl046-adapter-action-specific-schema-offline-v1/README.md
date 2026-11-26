# BKL-046 · Schema candidato per le azioni del contratto locale

La candidata separa TEST, SELECT, STOP e FINISH. Il ramo corrispondente vincola il checkpoint e il passo compatibili con l'azione, conserva il legame con lo stato e omette i passi già provati sullo stesso genitore. Il runtime archiviato resta il riferimento per la decisione applicabile.

Sulle 1.680 fixture fissate dello studio precedente, lo schema storico consente 43 forme che il runtime respinge. La candidata riduce questi disaccordi a zero e conserva tutte le 16 decisioni che il runtime accetta. Un controllo aggiuntivo rifiuta il legame con uno stato diverso. Tre controlli sulla saturazione VIVIDNESS verificano il limite nei due sensi e il valore ammesso alla soglia.

Una risposta con 751 caratteri a due byte supera il limite di 1.500 byte. Il controllo locale dello schema la lascia passare e il runtime la respinge. I 1.680 casi sono una regressione sulla matrice archiviata. Non costituiscono una prova generale di equivalenza. La candidata usa operatori verificati dal valutatore locale. La compatibilità con un provider e l'applicazione alla catena reale restano da verificare.

Il programma riceve protocollo, directory delle fonti archiviate delle due revisioni e un file di uscita nuovo. Nessun provider contattato, nessuna distribuzione e nessun avvio PixInsight. [Disaccordi dello schema storico](../bkl046-adapter-contract-pair-vm-replay-v1/README.md)