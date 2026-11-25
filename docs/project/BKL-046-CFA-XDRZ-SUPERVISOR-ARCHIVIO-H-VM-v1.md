# BKL-046 · Pubblicazione CFA su H: prima del rilascio R4

Nel collaudo su DSG-Shared, il supervisore crea su H: una directory esclusiva per la prenotazione. Scrive e sincronizza 17 oggetti: dieci FITS, log, marker di batch, ricevuta del comparatore, schermata, ricevuta di chiusura e due record R4. Dopo la prima rilettura scrive ARCHIVED.json e verifica nuovamente l'insieme degli oggetti e le loro impronte prima di chiedere il rilascio. Il marker attesta l'archiviazione verificata al momento della scrittura. La ricevuta R4 rimane l'autorità sul rilascio.

Le due esecuzioni hanno prodotto rapporti identici su undici scenari. Il caso valido ha ottenuto il rilascio da R4 sul registro di prova. Dieci casi respinti hanno conservato la prenotazione, tra cui una directory preesistente lasciata intatta e una schermata alterata dopo la scrittura del marker. In quest'ultimo caso la rilettura ha impedito il rilascio. Le impronte dei 30 file canonici sono rimaste identiche.

Le uscite e il log sono sintetici, la finestra è di un testimone e l'inventario processi è simulato. Resta da integrare la pubblicazione nel launcher scientifico con percorso qualificato, protezione dei file e riconciliazione della ricevuta R4. PixInsight è rimasto chiuso. Esecuzioni native e chiusure scientifiche a zero.
SHA-256 archivio H: 4bdc9adc4dece79c1bc9e741119ffc92f9ad80ff9aa1f23617501b0d154a1e62.
