# Verifica congiunta della trascrizione e delle mappe CFA

Il verificatore collega il marcatore di fine batch alla prenotazione attesa e alle impronte del kit e del componente. Controlla l’ordine delle riletture e delle esportazioni, i parametri dichiarati, i percorsi dei dieci FITS e l’identificativo della finestra dei pesi. L’impronta di ciascun FITS consumato dal comparatore deve coincidere prima e dopo il confronto. Un esito numerico incoerente viene conservato come irrisolto.

Eseguire `confronto.py <manifest-componente> <classificatore> <pacchetti-Python> <kit> <uscite> <nuova-ricevuta> <prenotazione> <sha256-marcatore>`. Il collaudo riproducibile usa `collaudo.py <manifest-componente> <kit> <classificatore> <pacchetti-Python> <verificatore> <nuovo-laboratorio> <nuovo-riscontro>`. Le mappe del collaudo sono predizioni offline, accompagnate da una trascrizione simulata.

La verifica conferma la coerenza dei file presentati. L’ingresso operativo deve ancora ottenere il digest del marcatore e l’identità della prenotazione dalla catena ammessa, verificare console e provenienza delle esportazioni, e attestare l’uscita del figlio originale. La ricevuta del comparatore non conferisce ammissione né autorizza un rilascio.
