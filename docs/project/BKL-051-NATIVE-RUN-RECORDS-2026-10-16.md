# BKL-051: registri monouso e commit Owner

`native_run_records.py` collega controllo di avvio e bootstrap verificato al
budget originale e ai registri V5 S5/S7. Non avvia, osserva o chiude processi;
non prepara grant e non autentica un consenso. Il futuro supervisore deve aver
ottenuto consenso fresco e conservare un solo contesto privato vivo, con budget
creato prima dell'I/O di preparazione. Ricostruire questo componente con un nuovo
budget non dimostra continuità ed è vietato alla futura composizione.

`NativeRunRecords` richiede le tre directory private esistenti, binding a cinque
impronte, sessione bootstrap viva e l'esatto tipo `LiveNativeBudget`. Prima di
scrivere verifica parent-intent V2, identità delle directory, pin del controllo,
attestazioni bootstrap, input sigillati, parametri V2, codice e grant. Non prova
la freschezza o autenticità del grant con il solo hash. Richiede lo stesso
termine UTC del budget e rifiuta prodotti, Owner o registri di tentativi già
presenti, anche parziali. Il retained deve essere vuoto.

Il componente riutilizza i controlli di pubblicazione per schema, pin,
identità, limiti e sorgenti. Riserva i byte del pacchetto Owner massimo canonico,
ready e 1 MiB per annullamento entro il limite di 200 MiB degli input.
I metadati del genitore restano entro 16 MiB. Il chiamante deve ancora tenere
gli handle in sola lettura sulle copie private prima del Popen: questi controlli
di documenti non sostituiscono i blocchi dei file o la prova PJSR.

`consume(createdUTC)` tenta una sola scrittura di `start-consumed.json` con
schema chiuso, impronte e sessione del controllo e permesso
`ONE_ATTEMPT_NO_REPLAY`. La data canonica, fornita dal chiamante fidato, deve
essere successiva o uguale al parent-intent e precedente alla scadenza. Il testo
non dimostra da solo l'ora reale: il budget vivo resta il gate. La scrittura
esclusiva comprende flush, fsync e rilettura con identità originale; l'impronta
è conservata in memoria e verificata prima dei passi successivi.

Dopo che il supervisore ha assegnato l'esatto Popen e catturato l'identità,
`write_owner(held)` conserva subito il riferimento a `HeldNativeProcess` e
ricontrolla la sua identità. Scrive una sola volta `held-process.json`, Owner
nel lavoro, la stessa copia nel registro e ready nel registro. Soltanto alla
fine scrive ready nel lavoro: il nativo può vedere il commit dopo che entrambe
le copie del genitore sono già conservate. Hash e identità sono ricontrollati
prima e dopo ogni scrittura, insieme a sorgenti, budget, directory e segnali.
Un Owner non deriva mai da un PID letto da file.

Prima del commit nativo, il lavoro deve contenere esattamente gli input e i
controlli già scritti. Dopo ready sono ammessi i nomi runtime fissi del wrapper;
completezza, limiti runtime e contenuti appartengono al publisher e al futuro
supervisore. Un errore dopo la scrittura di ready può lasciare quel file presente
mentre il componente è fallito: la presenza non dimostra commit accettato o
sicurezza di chiusura.

Ogni operazione consuma il proprio tentativo in memoria prima di I/O fallibile.
Un errore durante una verifica o un'operazione imposta lo stato fallito e mantiene
riferimenti e file, senza sovrascrittura, cancellazione o ritentativo. Un replay
respinto dal gate iniziale, dopo un'operazione riuscita, non cambia lo stato
precedente e non avvia altre scritture. La diagnostica è solo memorizzata e
restituisce sempre `newNativeStartAllowed:false` e
`processClosureAuthorized:false`. Il supervisore deve propagare l'incertezza e
tentare il proprio registro d'errore; questo componente non lo scrive e non
sostituisce la macchina a stati. Se la prima creazione fallisce senza lasciare
file, l'assenza non permette di ricostruire il contesto o ripetere il tentativo.

Le prove usano bundle opachi sintetici, bootstrap dichiaratamente finto e
interrogazioni del processo simulate. Non sono prove di consenso, caricamento
reale, handshake PJSR o validazione scientifica. Restano integrazione operativa,
gestione dell'incertezza, annullamento e chiusura comprovata del processo.
Rollback tramite revert, preservando tutti i registri e i tentativi precedenti.
