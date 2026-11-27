# BKL-046 — Adattatore PJSR per ImageAnalysis

Il codice candidato è una definizione da includere nell'entrypoint revisionato. Verifica il digest della configurazione, calcola quello dell'entrypoint e pubblica una richiesta che contiene entrambi. Avvia le misure solo dopo aver ricevuto dal padre una conferma per la richiesta esatta, con nonce e prenotazione associati. [Adattatore](ImageAnalysis-adapter.jsh)

Dopo le due misure, rilegge la conferma e scrive risultati e ricevuta nella directory dell'operazione. Rilegge entrambi i file e stampa il segnale di completamento solo dopo averne verificato le impronte. Un segnale assente lascia la prova senza ricevuta conclusiva. La ricevuta attesta il ritorno del produttore. L'uscita di PixInsight e il rilascio della prenotazione richiedono verifiche del padre.

Il collaudo ha riprodotto la sequenza con il parser esatto, quattro FITS reali del set sintetico e un ambiente PJSR simulato. Ha verificato un esito positivo e nove rifiuti, inclusi conferma alterata dopo le misure e rilettura incorretta. La scadenza viene controllata prima e dopo le chiamate al modulo. Il collaudo non ha misurato l'interruzione di una chiamata nativa in corso. [Riscontro](riscontro.json) · [Verificatore](verifica-adattatore.cjs)

Per l'integrazione manca il padre che custodisce la directory privata, i file e l'ammissione R4. In particolare l'adattatore controlla l'assenza dei file prima di scriverli. L'esclusione di altri scrittori dipende dalla custodia della directory, che il test simulato non qualifica.
