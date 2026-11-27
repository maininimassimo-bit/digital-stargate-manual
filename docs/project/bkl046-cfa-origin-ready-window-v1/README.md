# BKL-046 · Prontezza del processo originale per la prova di origine XDRZ

Il controllo attende il marcatore dei quattro casi nella directory della prenotazione. Ne verifica i campi e l'impronta, interroga l'handle del processo originale e cerca una sola finestra visibile dello stesso PID. Prima di restituire il contesto rilegge il marcatore, ricontrolla l'identità del processo e interroga di nuovo lo stato della custodia degli ingressi. Il contesto lega riscontro di batch, entrypoint ed eseguibile atteso alla finestra originale.

Nel collaudo una finestra Windows reale è stata associata al caso valido. I quattro controlli negativi hanno respinto un marcatore di un'altra prenotazione, il marcatore mancante fino alla scadenza, il processo originale già uscito e la perdita simulata della custodia degli ingressi. La chiusura ordinaria rimane affidata alla fase successiva del supervisore.

Il collaudo usa un processo testimone e un marcatore sintetico. Il modulo di prontezza presuppone l'handle del processo originale ottenuto dopo il lancio autorizzato. L'effettiva emissione del marcatore da PixInsight resta da verificare. Nessun uso del registro canonico e nessun avvio PixInsight. [Parent R4 e posa dello script](../bkl046-cfa-origin-bound-entry-v1/README.md)

Per replicare, eseguire collaudo.py in sessione interattiva con la directory del kit, il preparatore incluso e un nuovo percorso per il rapporto. Le fonti restano quelle già fissate dal preparatore.