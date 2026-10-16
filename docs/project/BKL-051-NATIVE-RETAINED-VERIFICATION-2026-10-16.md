# BKL-051: composizione viva delle prove conservate

Stato: componente di preparazione del supervisore, non integrato in un percorso
di avvio o chiusura. Milestone R01–R14 aperta; `NOT_VALIDATED`, zero nuovi
controlli reali qualificati. Nessuna nuova autorizzazione nativa o cloud.

`native_retained_verification.py` collega gli oggetti originali
`NativeRunRecords`, `NativeSupervisionSignals`, `LivePublicationVerification`,
`HeldNativeProcess` e da uno a tre gruppi `NativeReadLocks`. Non ricostruisce
contesti da JSON o PID e non apre, termina, attende o rilascia processi e file.
La costruzione si può tentare una sola volta sul contesto. Ogni errore osservato
resta in memoria nel verificatore, nei segnali e nei registri: ripristinare un
file non riabilita il tentativo. Il chiamante deve conservare tutti questi
oggetti anche quando il costruttore non restituisce un nuovo verificatore.

Il controllo combina:

- identità delle directory originali, sessione bootstrap e budget originale;
- hash e identità originali di tutti i registri, compresi consumo dell'avvio,
  processo posseduto e copie parent dei due file Owner;
- controllo vivo della pubblicazione, con identità originali dei prodotti
  sorgente e conservati, codice e input, inventari, cancellazione e marker;
- identità corrente dell'handle originale, uguale a quella del collegamento
  Owner, senza ricerca o riapertura per PID;
- copertura esatta dei blocchi: tutti i file input originali nel lavoro,
  compresi seal, grant e Owner, più entry e launcher privati; nessun duplicato;
- metadati passivi riletti dai file conservati, marker e prodotti collegati
  agli hash effettivi, ritorno causale, Owner e ready, quindi la verifica S6
  dello stato, delle dichiarazioni native e dei rami di conservazione.

La verifica di preparazione `NativeRunRecords.verify()` non è usata dopo la
pubblicazione: vieta intenzionalmente publication-intent, cancellazione e
scadenza. Qui i suoi pin originali vengono riletti direttamente insieme alla
verifica viva di pubblicazione, senza cambiare o riabilitare quella guardia.
Una scadenza nota consente soltanto la verifica per la conservazione; inversione
o incertezza del tempo impediscono il risultato. Una cancellazione già presente
e fissata dalla pubblicazione viene riportata; una comparsa successiva invalida
la continuità. Nessun risultato autorizza accettazione o chiusura del processo.

Il futuro preparatore deve acquisire i gruppi statici prima dell'avvio e quello
Owner dopo il commit dell'handshake, conservandoli fino all'uscita verificata.
Questo componente ne verifica la copertura e gli handle attuali, ma non può
dimostrare da solo il momento dell'acquisizione. Le guardie dei gruppi devono
permettere l'osservazione dopo una scadenza nota (`budget.check` più sessione);
il preparatore deve applicare separatamente `require_running` durante la
preparazione e prima dell'avvio. Non modificare le guardie dopo un errore.

Le prove automatiche usano file sintetici opachi, un bootstrap fittizio e
interrogazioni simulate di processo e blocchi. Non provano la compatibilità
dei blocchi Windows con PJSR reale, la validità di XISF/History, la provenienza
astronomica o il modello fisico completo. Rimangono necessari preparatore,
supervisore, decisione di chiusura con handle originale, ricevuta di uscita,
revisione e consenso fresco sul pacchetto esatto prima di qualsiasi prova nativa.
Il confine è un lavoro privato e quiescente, non un isolamento contro codice
ostile eseguito dallo stesso utente. I risultati sono osservazioni del momento:
il supervisore dovrà verificarli di nuovo prima di una decisione sul processo.

Rollback: rimuovere questo componente e i suoi test/documentazione prima della
composizione. Non esistono cambiamenti runtime, risorse cloud o ricevute reali da
ripristinare. La rimozione non cancella prove né autorizza un altro tentativo.
