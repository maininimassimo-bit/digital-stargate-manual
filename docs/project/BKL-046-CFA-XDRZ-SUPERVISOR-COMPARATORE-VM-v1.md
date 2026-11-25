# BKL-046 · Supervisore CFA e comparatore su DSG-Shared

Il supervisore Node/Python usa il comparatore CFA con impronta verificata, cinque casi e dieci esportazioni FITS sintetiche. Il comparatore rilegge i parametri e gli esiti dal log, mentre il supervisore verifica che il marker appartenga alla prenotazione del test. Prima della chiusura e prima del rilascio rilegge marker, ricevuta, FITS e log.

Due esecuzioni hanno prodotto lo stesso rapporto su nove scenari. Il caso valido ha raggiunto il rilascio simulato dopo la chiusura ordinaria del testimone. Un FITS scientificamente incompatibile è stato respinto dal comparatore. Un FITS modificato dopo il confronto ha bloccato la chiusura. Una modifica al log dopo la chiusura ha impedito il rilascio. Anche i cinque casi negativi già introdotti per identità, cattura e autorizzazione alla chiusura hanno impedito il rilascio.

I 30 file del registro canonico hanno mantenuto le rispettive impronte. I FITS e il log provengono dalla fixture, la finestra appartiene a un testimone Windows e il rilascio è simulato. Restano l'integrazione con il custode reale, l'archiviazione delle uscite nel percorso di produzione, le revisioni e la prova PixInsight ammessa. Esecuzioni native e chiusure scientifiche a zero.
SHA-256 archivio H: 0a750cbc17dd293f915f49002fa1057eec3ade7fd8f0b1d5eaad7c15d537c696.
