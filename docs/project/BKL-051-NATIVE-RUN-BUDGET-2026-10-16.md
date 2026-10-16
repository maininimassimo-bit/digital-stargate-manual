# BKL-051: budget originale della sessione nativa

`native_run_budget.py` implementa il tempo vivo richiesto dal contratto del
supervisore V5 S4. Non esegue I/O, non prepara file o grant, non avvia processi
e non offre recupero da dati persistiti. Il bootstrap fidato deve creare un solo
`LiveNativeBudget` prima del primo I/O di preparazione e conservare lo stesso
oggetto fino alla conclusione del tentativo. Un nuovo oggetto creato dopo una
preparazione non dimostra continuità: la futura composizione deve impedirlo.

La prima lettura monotona fissa l'origine; la scadenza è origine più 180 secondi,
senza argomento di durata, reset o rinnovo. L'origine UTC viene acquisita nella
stessa costruzione. I callback sono fidati e devono leggere gli orologi effettivi;
la loro sostituzione in memoria non è una sandbox coperta da questo componente.
I valori monotoni devono essere numeri finiti non negativi, entro 2^40 secondi,
con differenza rappresentabile esattamente di 180 secondi. Booleani, NaN,
infiniti e stringhe non vengono convertiti silenziosamente.

`check()` legge monotono, UTC e nuovamente monotono, così anche il tempo speso
nel callback UTC resta contato. Richiede valori non decrescenti e datetime UTC
consapevoli del fuso. Un errore o arretramento rende l'orologio permanentemente
incerto e i controlli successivi falliscono. Il recupero apparente dell'orologio
non azzera l'incertezza. Le scadenze raggiunte restano registrate separatamente
per monotono e UTC; l'uguaglianza alla scadenza significa già scaduto.

`deadline_utc` usa il formato canonico a secondi richiesto dal controllo di
avvio. Eventuali frazioni vengono arrotondate verso il basso: il limite UTC può
essere fino a meno di un secondo più stretto, mai più lungo. La scadenza monotona
originale rimane indipendente e non viene ricostruita dal testo UTC.

`require_running()` impedisce ulteriore calcolo se uno dei due limiti è scaduto.
Un superamento noto non è di per sé un guasto dell'orologio: `check()` può ancora
essere usato per conservare prove e svolgere il cleanup ammesso dal supervisore.
Per la conservazione opaca, il chiamante passa `publication_clock` insieme a
`deadline_monotonic` dello stesso oggetto; non crea una nuova scadenza di fase.
Il solo flag monotono del publisher non sostituisce il controllo UTC e tutti gli
altri gate prima di un'eventuale accettazione tecnica.

`diagnostic()` restituisce una copia di fatti già osservati: non aggiorna gli
orologi e non è una prova fresca. Dichiara sempre `newNativeStartAllowed:false`
e `processClosureAuthorized:false`. Non prova arresto, consenso, conservazione,
esecuzione corretta o validazione scientifica. Le proprietà numeriche sono per
il chiamante locale vivo, non istruzioni per riaprire una sessione da JSON.

Le prove usano soltanto orologi sintetici, senza attese o processi: scadenza
cumulata, UTC fermo, avanzamento UTC, callback lento, arretramento, valori
invalidi e separazione tra superamento noto e incertezza. La macchina a stati,
registri monouso e composizione operativa devono ancora integrare questi gate.
Rollback tramite revert del codice, preservando registri e prove precedenti.
