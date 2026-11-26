# Passaggio dei prodotti CFA dal batch all’archivio

Il batch esporta i dieci FITS, la trascrizione e il marcatore nella sottocartella `products` della prenotazione. I file del launcher e le risposte del supervisore restano al livello superiore e in `control`. Il confronto accetta soltanto i dodici prodotti attesi e lega la ricevuta alla prenotazione, al kit, al componente e al marcatore attesi. La rilettura verifica di nuovo ogni impronta. Un risultato numerico irrisolto resta registrato e blocca il passaggio al percorso di completamento.

L’archiviazione usa il formato della ricevuta di confronto e controlla le singole impronte prima di creare il marcatore d’archivio. Il collaudo con trascrizione e FITS simulati ha verificato 17 membri, oltre al marcatore d’archivio. Respinge una prenotazione con componente estraneo, un secondo archivio allo stesso indirizzo, una modifica dopo il confronto e una modifica dopo la pubblicazione nell’archivio.

Il kit comprende i tre driver di collaudo. `collaudo-export.cjs` controlla il batch con l’API PJSR simulata. `collaudo-confronto.py` produce i prodotti simulati nel proprio laboratorio. `collaudo-passaggio.cjs` riceve Python, pacchetti, kit, laboratorio, una nuova directory e un nuovo rapporto. Esegue il verificatore e il pubblicatore con file isolati.

Per integrare il componente, il parent deve creare `products` nella sua directory di prenotazione, leggere lì il marcatore e passare quella stessa directory alla pubblicazione. I tre percorsi devono essere legati al contesto del figlio originale. Il collaudo usa una copia isolata del registro. L’integrazione operativa richiede ancora la prova della catena completa, le revisioni e l’ammissione del coordinatore.
