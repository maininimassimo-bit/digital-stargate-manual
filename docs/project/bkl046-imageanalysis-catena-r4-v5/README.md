# BKL-046 — Custodia delle evidenze fino alla decisione R4

La prova v5 su DSG-Shared aggiunge al collaudo ImageAnalysis il controllo delle misure, della ricevuta di ritorno e dell'interpretazione dopo l'uscita del padre. Il decisore apre i tre file in lettura esclusiva rispetto a scrittura ed eliminazione, confronta dimensioni e SHA-256 con i valori restituiti dal padre e mantiene gli handle fino alla decisione di rilascio.

Cinque casi sono passati con copie isolate del registro R4. Nel caso positivo, le tre aperture in scrittura sono state respinte durante la decisione ed è stata emessa una ricevuta di rilascio. La ricevuta alterata prima dell'uscita del padre ha conservato la prenotazione. Nei tre casi con un file alterato dopo l'uscita con codice zero, il controllo SHA-256 ha respinto la modifica e la prenotazione è rimasta attiva senza ricevuta di rilascio.

Una prima esecuzione di sviluppo ha rilevato che Python espone il rifiuto di scrittura come `EACCES` anche senza `winerror`. Il collaudo finale ha verificato per ciascun file che l'apertura in scrittura fosse permessa prima dell'acquisizione degli handle e respinta durante la custodia.

I processi e i file erano reali. Le misure ImageAnalysis erano simulate. Questo esito riguarda il passaggio di custodia nel collaudo isolato. Servono la revisione del launcher operativo e l'ammissione R4 prima della prova nativa.