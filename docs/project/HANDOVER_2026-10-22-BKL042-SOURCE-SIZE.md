# BKL-042: blocco 503 e fonte compatta — 22 ottobre 2026

## Diagnosi osservata

Il 22 ottobre tre richieste del portale hanno raggiunto il relay privato, restituendo HTTP503. Gateway /health READY; revisione relay 00008-qat, quota 14/100. Il catalogo pubblico pesa 1.035.349 byte rispetto al massimo di lettura 1.000.000: retrieval v3 riproduce SOURCE_TOO_LARGE prima del provider. Tutte le altre quattro fonti sono sotto limite. Il gateway sostituiva il codice specifico con PRIVATE_RELAY_REQUEST_FAILED e il browser mostrava soltanto il numero HTTP.

## Correzione e aggiornamento automatico

Metodo v4: stessa allowlist di cinque classi di fonti e stessi campi sessione già ammessi, ma session-catalog legge docs/data/bkl042-session-catalog.json, derivato compatto del catalogo completo. Esclusi coordinate, percorsi, dettagli guida/meteo, seriali e altre proprietà non ammesse. Baseline 27 record e 7.297 byte; nessuna nuova classe di conoscenza o capability. Digest e path delle citazioni attestano i byte della nuova proiezione; i link restano al dettaglio della sessione. Nessuna certificazione scientifica aggiunta.

Il generatore canonico crea e verifica entrambi i cataloghi, con budget UTF-8 1.000.000 byte anche sulla fonte compatta. Lo stesso processo di aggiornamento scientifico include il nuovo file nei percorsi pubblicati: non è uno snapshot aggiornato a mano. Se la popolazione cresce oltre il budget, generazione/CI falliscono: non si alza il limite né si elimina la verifica di grandezza. Lettura HTTP resta bounded e fail-closed, con e senza Content-Length; nessuna fonte mancante viene nascosta.

Il gateway inoltra soltanto codici diagnostici pubblici allowlisted; corpi arbitrari del relay restano esclusi. UI distingue fonte grande, indisponibile/invalida, limite pilota, runtime, provider e accesso scaduto. Nessun dettaglio privato o segreto esposto. Quota, modelli, credenziali, autenticazione Google e authority immutati. Il runtime v4 richiede pubblicazione della nuova fonte prima del deployment del relay; gateway separato da aggiornare per la diagnostica.

## Perimetro e limiti

La fonte non comprende documentazione RTU o descrizione degli apparati della cupola: il rilascio risolve il blocco tecnico e non attesta copertura RTU. Le risposte devono restare nelle fonti disponibili. Nessuna richiesta IA di prova a pagamento necessaria per verificare retrieval; non consumare quota o resettare il contatore per aggirare errori. Read-only, tools disabilitati, command/execution/safety authority NONE.

## Verifica e rilascio

Test reali dei derivati, equivalenza dei campi ammessi, regressione catalogo oltre 1MB, limite anche senza header, codici gateway sanitizzati; suite minimizzazione e UI. Build, ARB indipendente poi RQ, CI exact-head, merge/postmerge/Pages. Deployment agli stessi due servizi esistenti con identità, secret binding, risorse, traffico e limiti preservati; nessuna nuova risorsa o espansione IAM. Evidenze finali, revisioni e verifiche sanitarie nella PR. Rollback su revisioni precedenti conservate; mantenere la fonte compatta pubblicata, nessuna cancellazione o modifica dei dati scientifici.
