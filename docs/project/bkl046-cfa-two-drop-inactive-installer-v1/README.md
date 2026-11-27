# Installatore inattivo del launcher CFA a due depositi

L’installatore verifica l’impronta dello ZIP del soggetto BKL-046, i 34 file del launcher e i 3.824 file del runtime. Prepara i file in una directory sorella, rilegge nomi e impronte e rinomina la directory solo a verifica riuscita. Se la destinazione esiste, si ferma prima di creare la copia di staging.

La destinazione prevista è `C:\Program Files\DigitalStarGate\BKL046-CFA-XDRZ-two-drop-v1`. La modalità amministrativa crea oggetti con proprietario Administrators e DACL protetta. SYSTEM e Administrators hanno pieno controllo. Users dispone di lettura ed esecuzione. Il codice rilegge proprietario e regole prima e dopo la rinomina. La modalità di verifica successiva richiede il token ordinario e rilegge tutti i file e tutte le directory.

Il collaudo su copia isolata ha verificato 3.858 file, il rifiuto della destinazione esistente e la costruzione dei descrittori Windows. Il tentativo con token ordinario si è fermato prima di creare la destinazione. La posa amministrativa e la verifica sotto il token ordinario dell’installazione effettiva restano da eseguire. Il pacchetto dichiara l’attivazione nulla e l’installatore non richiede una prenotazione.

La sintassi è `installa-inattivo.py <self-test|install-inactive|verify-installed> <archivio-esatto> <nuovo-riscontro.json>`. Il rapporto va scritto fuori dalla directory di installazione.
