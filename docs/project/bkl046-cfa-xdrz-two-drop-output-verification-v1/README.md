# Verifica dei prodotti del batch CFA a due depositi

Il verificatore BKL-046 rilegge il marcatore, gli eventi, la console e i 24 FITS dei 12 casi. Controlla ordine, parametri dichiarati, larghezza riletta e identità delle finestre di output. Per ogni larghezza confronta il prodotto frazionario con le sei ipotesi numeriche. Il risultato dei cinque casi interi deve concordare anche sulla scala dei pesi.

Il collaudo riconosce sia la normalizzazione globale sia quella per canale. Conserva un esito distinto se le due larghezze danno convenzioni differenti. Una mappa frazionaria da 0,70 presentata come 1,00 resta irrisolta. Console incompleta, larghezza di esportazione difforme e FITS mancante vengono respinti.

Il rapporto di file forniti resta numerico. Per attestare una prova nativa, la catena ammessa deve fornire il marcatore e la prenotazione, custodire le letture e verificare l’uscita del processo originale. La fase di esecuzione richiede revisione e ammissione del coordinatore.

Per l’autotest eseguire `verifica.py <protocollo.json> <batch> <oracolo-intero.zip> <kit-frazionario.zip> <classificatore.py> <pacchetti-Python> <nuovo-riscontro.json>`. Per leggere output forniti aggiungere `--outputs <directory> --reservation <UUID> --marker-sha256 <impronta>`.
