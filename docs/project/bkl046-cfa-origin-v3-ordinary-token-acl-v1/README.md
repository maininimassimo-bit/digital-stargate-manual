# BKL-046 · Controllo del token ordinario per la posa CFA v3

Il verificatore ha ricontrollato le impronte di 56 file del soggetto v3 prima e dopo le prove. Usa aperture di handle su oggetti già esistenti, senza scrivere byte o cambiare ACL. Registra separatamente i diritti di scrittura, cancellazione, modifica del proprietario e dell'ACL. Controlla anche la cancellazione dei figli sulle directory. Una condivisione in conflitto o un altro errore inatteso lascia il diritto indeterminato.

Il token ordinario di DSG-Shared ottiene almeno un diritto di modifica su ciascuno dei 56 file della copia di lavoro. Il controllo su PixInsight.exe sotto Program Files ha ricevuto il rifiuto di tutti i diritti di modifica provati. La destinazione protetta DigitalStarGate sotto Program Files risulta assente.

Lo script verifica la copia inattiva e il token osservato. L'installazione effettiva richiede la stessa verifica sui file finali, sull'autorità di attivazione e sulla catena di avvio, oltre alle revisioni autentiche del pacchetto esatto. In questo controllo non sono state richieste ammissioni e PixInsight è rimasto chiuso.