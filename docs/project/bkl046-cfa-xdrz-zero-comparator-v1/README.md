# Comparatore delle mappe CFA con maschera e pixel azzerato

Il comparatore legge cinque coppie di mappe FITS RGB lineari e pesi grezzi. Le prove richiedono un’esportazione per ciascun braccio denominato `unmasked`, `mask-green`, `mask-wrong-channel`, `zero-detector` e `zero-reference`. Per ogni braccio il nome dei file termina in `-rgb.fits` e `-weight.fits`.

Si confrontano il supporto RGB, i pesi grezzi su tutti i pixel e le intensità sui pixel supportati. Le tolleranze sono 10⁻⁸ per la presenza di supporto e 10⁻⁶ in valore assoluto per pesi e intensità. Le tolleranze si applicano al riferimento sintetico congelato. I risultati conservano gli esiti misti, mancanti o fuori modello. Un rigetto verde senza effetto non conferma la semantica della maschera. L’esito sui controlli azzerati distingue peso conservato, esclusione e risposta non risolta.

Eseguire `classifica.py <pacchetti-Python> <kit-congelato> <nuovo-rapporto.json> --exports <directory-esportazioni>`. Per riprodurre il collaudo usare `--self-test` al posto di `--exports`. Il confronto registra l’impronta dei dieci metadati FITS e dei pixel così come consegnati, tramite l’hash di ciascun file completo. La provenienza nativa deve essere verificata dal launcher con una ricevuta distinta che colleghi acquisizioni e uscite alla stessa prenotazione. La rilettura allegata usa mappe simulate.
