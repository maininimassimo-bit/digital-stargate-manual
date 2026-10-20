# BKL-051: annullamento cooperativo e incertezza persistente

`native_supervision_signals.py` collega il contesto vivo dei registri ai segnali
S5/S7 del contratto V5. Non avvia, riapre, enumera o chiude processi e non
autentica consenso. Il futuro supervisore deve creare un solo componente sul
contesto originale prima dell'eventuale Popen. Una seconda costruzione sullo
stesso oggetto dei registri è respinta, anche se un'apertura fallita non ha
lasciato file. La futura composizione deve impedire anche la ricostruzione di
registri, budget e contesto dopo un errore: questo componente non è una sandbox
contro codice ostile nello stesso processo.

`adopt_held` mantiene il riferimento a `HeldNativeProcess` prima di diagnostica
fallibile, dopo il consumo del registro di avvio. Non interroga l'identità e non
autorizza una cattura o un avvio. Il futuro supervisore deve adottare l'esatto
oggetto appena creato prima di chiamarne `capture`. Se il writer dei registri
contiene già un riferimento, gli oggetti devono essere identici.

`request_cancel()` consuma il proprio tentativo in memoria e scrive una sola
volta `cancel.json` con protocollo, operationRef e requested:true. Usa creazione
esclusiva, flush, fsync, rilettura e identità originale. Un file preesistente,
anche identico o parziale, non viene sostituito. La richiesta non prova arresto,
fine delle immagini, completamento o sicurezza di chiusura.

`mark_uncertain(reason)` imposta subito incertezza viva e stato fallito dei
registri, poi tenta una sola ricevuta `supervision-uncertain.json` con schema
S7 chiuso. La ragione è un codice ASCII maiuscolo di massimo 96 caratteri;
percorsi o testi arbitrari non sono serializzati. I binding provengono dal
contesto originale, senza rileggere un PID da disco. Il digest start è null
quando non è disponibile un consumo completato e verificato.

Senza un riferimento adottato, l'osservazione è NO_HANDLE_AMBIGUOUS con exitCode
null: non afferma che non esista un processo. Con un riferimento, viene usata
la sua osservazione sull'handle originale, distinguendo HELD_RUNNING e
HELD_EXITED. Un'uscita osservata non è nascosta da identità incerta e non produce
accettazione. Se l'osservazione fallisce, non viene inventato uno stato: la
ricevuta non viene scritta, ma incertezza, riferimenti e tentativo consumato
rimangono vivi. Il supervisore deve conservare il contesto per riconciliazione.

Queste sono scritture conservative di stop e diagnosi. Possono essere tentate
anche se budget o attestazione del codice sono già falliti; non riattivano il
calcolo. Richiedono comunque identità originali delle directory private, limiti
di metadati e integrità della propria nuova scrittura. Il ruolo del grant aveva
già riservato 1 MiB per cancel; i metadati del genitore sono controllati prima e
dopo la scrittura entro 16 MiB, profondità 8 e 256 voci.

`verify_records()` controlla tutte le ricevute conservate con hash e identità
originali; un cambiamento mantiene l'incertezza. Il fallimento di una ricevuta
precedente non impedisce da solo di tentare un altro segnale conservativo ancora
disponibile: per esempio un cancel alterato può essere segnalato con una nuova
ricevuta d'incertezza senza essere riabilitato come cancel valido.

Un errore operativo lascia il tentativo consumato e l'incertezza in memoria
anche se il file non può essere scritto. Nessuna ripetizione, cancellazione o
riparazione automatica. I replay respinti prima dell'operazione non cambiano lo
stato precedente. La diagnostica descrive fatti memorizzati, non una verifica
fresca, e restituisce sempre newNativeStartAllowed:false e
processClosureAuthorized:false. L'incertezza non viene mai cancellata.

Le prove usano bundle opachi sintetici, bootstrap finto e interrogazioni
simulate; nessun processo è avviato o chiuso. Restano macchina a stati completa,
retention e chiusura comprovata, composizione approvata e preflight PJSR con
consenso fresco. Rollback tramite revert preservando registri e tentativi.
