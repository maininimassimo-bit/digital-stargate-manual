# BKL-046 · Limite del processo Windows ristretto

Il controllo esegue la stessa operazione di lettura e scrittura con il contesto ordinario su un file sintetico. La risposta coincide con la richiesta. Nei primi due tentativi ristretti, il processo nasce sospeso con un token primario ristretto verificato e senza eredità degli handle. Dopo la ripresa termina con 0xC0000142 nella configurazione corrente e con un desktop temporaneo separato. Nessun file di risposta del test ristretto contiene la prova di accesso prevista.

La variante che crea una stazione Windows temporanea e separata si ferma con Win32 5. La verifica registra il punto di arresto. La causa precisa dell'errore di inizializzazione nelle prime due varianti resta aperta. I test usano file, processi e oggetti temporanei, con la sessione e la policy esistenti. [CreateProcessAsUserW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasuserw) · [Token ristretti](https://learn.microsoft.com/en-us/windows/win32/secauthz/restricted-tokens)

Il precedente controllo a livello di thread aveva verificato gli accessi NTFS. La separazione del rispondente in un processo effettivo resta da qualificare. Il risultato esclude chiamate a provider e avvii PixInsight. L'archivio H/K conserva le tre varianti e il verificatore del controllo ordinario.

Per ripetere usare Python 3.12 con `rileggi.py <nuovo-rapporto>` nella directory contenente le tre varianti. Il comando rilancia i casi, verifica le impronte degli script nel rapporto e respinge esiti diversi dagli arresti registrati.
