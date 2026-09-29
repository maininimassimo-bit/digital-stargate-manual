# BKL-043 F4 — attivazione separata del reporter GitHub

Stato: attivazione autorizzata dall'Owner il 29/09/2026; rilascio e verifica end-to-end da registrare nella PR dedicata. Non costituisce chiusura complessiva F4.

## Perimetro esatto

Il solo workflow `.github/workflows/bkl-043-f4-github-outcome-reporter.yml` proviene, senza modifiche, dal commit già esaminato `2b3f5a31d17868ae7c06696bf4bb676b60ba9649`. SHA-256 LF: `e3c92f1efbea2135719b5bc5219e16696b5b41f97cc90e43c35eb15fd8f35557`.

Massimo ha confermato in chat l'approvazione di Leonardo Di Egidio della versione finale per architettura, qualità e sicurezza/privacy; tale evidenza è owner-reported, non una review GitHub firmata. Massimo ha inoltre autorizzato esplicitamente l'attivazione del solo monitor attraverso una PR separata, lasciando la PR #428 draft. Nessun riavvio o aggiornamento del collector EAGLE è incluso.

Il reporter osserva gli eventi completed dei soli workflow `BKL-031 F9 MeteoHub Refresh` e `Analyze Observatory Session Automatically` sul branch predefinito. Mantiene distinte le conclusioni success/failure/cancelled/skipped e le altre conclusioni ricevute. Usa OIDC/WIF e un'identità invoker dedicata, senza chiavi persistenti, checkout del codice upstream, download dei suoi artifact o lettura dei suoi log.

## Configurazione e controlli

Prima del rilascio sono state lette la condizione WIF (repository/main/percorso esatto/evento workflow_run), la policy invoker priva di principal pubblici, la variabile receiver URL e la presenza dei nomi dei secret. I valori dei secret non sono stati estratti. La coerenza runtime si verifica solo con una consegna reale e un durable ACK.

`test-bkl043-f4-reporter-activation.py` verifica i byte approvati e dieci scenari offline: quattro conclusioni, duplicate ACK, errore rete, ACK non valido, ID discordante e due esclusioni di origine. Tutte le chiamate HTTP sono sostituite da test doubles. Il workflow di validazione non possiede credenziali cloud.

Il reporter non dispone di outbox locale e non ripete automaticamente il POST: un errore resta una run fallita da riconciliare, senza reinterpretare il risultato upstream. L'assenza di una run event-driven non è un guasto. La ricostruzione di gap e le prove end-to-end restano evidenze separate dai test sintetici.

## Rilascio, limiti e rollback

La pubblicazione su main abilita il reporting continuo per i futuri eventi idonei; non effettua un backfill dei run precedenti. Nessun dispatch scientifico, acquisizione manuale F9 o modifica del relativo workflow è incluso nell'attivazione del reporter.

L'evidenza operativa è conservata fuori dal repository pubblico. Qui non si pubblicano ricevute, log cloud o identificatori di telemetria. La chiusura generale F4 richiede la disposizione delle restanti prove e dei rischi residui del gate; non viene dedotta dal merge di questo workflow.

Rollback: disabilitare questo workflow o revert della PR di attivazione su main; conservare le ricevute già archiviate e l'outbox EAGLE. Verificare eventuali run già avviate, che potrebbero completarsi dopo la disabilitazione. Nessuna modifica al receiver o alle policy di conservazione è richiesta.
