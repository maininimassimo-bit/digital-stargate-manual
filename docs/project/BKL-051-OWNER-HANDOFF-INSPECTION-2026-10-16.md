# BKL-051 — ispezione locale di un'esportazione handoff

Stato: candidato tecnico, **R09 aperto / NOT_VALIDATED**, zero controlli reali qualificati.

L'ispezione confronta il pacchetto registrato, le quattro operazioni Owner conservate, le ricevute, i tre file di esportazione interni e una copia esterna esistente. Rilegge le evidenze per rilevare cambiamenti durante l'osservazione. Non crea file, non elimina marker, non modifica il blocco di esportazione, non invia richieste e non avvia o termina processi.

`CONSISTENT_RETAINED_COPY` indica soltanto associazione locale coerente della copia osservata. Se esiste `unconfirmed.json`, il rapporto continua a indicare `needsAssistedRecovery:true`, anche in presenza di `completed.json`. Un file assente, alterato, inatteso, interno alle radici protette o non confrontabile produce `INCOMPLETE_OR_CONFLICT`. Nessuno stato autorizza reinvio, nuova esportazione o avvio. PID e altre tracce di processo non costituiscono proprietà del processo o prova di arresto.

## Verifica condivisa senza ricevute scritte

`LocalRegistry.inspect()` esegue le verifiche di schema e byte senza conservare una ricevuta, anche in errore. Il comportamento storico di `verify()` rimane invariato per default. L'opzione rigorosamente booleana `record_verifications=False`, inoltrata dai caricatori della configurazione e dei piani, sopprime esclusivamente le ricevute VERIFY, comprese quelle delle chiamate indirette durante i costruttori e i preflight.

Questa opzione non rende read-only l'intero oggetto: un'esplicita chiamata a `register()` continua a scrivere. L'ispettore ricostruisce piani con verifica senza ricevute prima di ogni controllo e usa soltanto metodi di lettura. Non modifica la policy degli oggetti originali né applica sostituzioni globali ai metodi di produzione.

## Comando

`python -m tools.scientific_transients.owner_handoff_inspection --help` descrive gli argomenti: configurazione privata e impronta, ricevuta di preparazione e impronta, tre coppie ordinate `--projection-receipt PATH SHA256`, percorso assoluto `--copy` della copia esterna esistente. Il rapporto minimizzato viene scritto sullo standard output, senza percorsi privati, credenziali o diagnostiche grezze. Il comando non salva automaticamente un rapporto.

Il controllo richiede un pacchetto registrato ancora compatibile con il caricatore pristine esistente. Non riapre o ricostruisce l'autorità di un tentativo nativo già avviato e non risolve il recupero dei processi dopo perdita dell'handle. La chiusura operativa della milestone richiede ancora il flusso completo e le sue prove.

## Prove

Le prove applicano un divieto di scrittura ai file e al registro durante l'ispezione e confrontano nomi, byte e tempi di modifica dei file prima e dopo. Coprono costruttori, esito valido, errore sulle sorgenti, marker incerto persistente, copia mancante o interna, modifica concorrente e artefatto PID non ammesso. I test del comando usano configurazione e piani sintetici reali senza iniettare il caricatore. Le regressioni verificano che le ricevute ordinarie e la registrazione esplicita mantengano il comportamento storico.

I test usano solo dati e trasporti sintetici; non attestano autenticazione reale, stato attuale del servizio, arresto nativo o validazione scientifica. Revisioni sul codice esatto e CI aggiornata restano gate separati.
