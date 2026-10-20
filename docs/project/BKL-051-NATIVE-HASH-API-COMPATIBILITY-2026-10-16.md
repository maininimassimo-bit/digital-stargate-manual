# BKL-051 — Compatibilità dell'algoritmo hash PJSR

## Esito dei gate verificato il 20 ottobre 2026

Sul commit `ee40d7a91b2a804d005f19f79306fa1ecbbc3e0d` sono conclusi 64 test sintetici PASS, MkDocs strict PASS, 24 controlli CI SUCCESS e revisioni indipendenti ARB poi RQ APPROVED sui sei file dell'incremento. Le revisioni non approvano l'intera PR né l'accettazione scientifica. Nessun nuovo avvio nativo sul codice corretto. [Stato consolidato, ricevute e attività successive](BKL-051-TECHNICAL-ALIGNMENT-2026-10-20.md). Il presente aggiornamento documentale è successivo al commit revisionato.

## Evidenza reale e limite

La prova locale autorizzata `92ce87c7f93d4dcdbe99b933d0a64c1a`, sul pacchetto congelato `5508e955`, ha consumato una preparazione e un avvio. La preparazione è riuscita. La console di PixInsight 1.9.5 build 1706 ha segnalato la proprietà inesistente `CryptographicHash.SHA256` nel launcher, seguita dall'errore generico `NATIVE_LAUNCH_UNCERTAIN`. Il processo ha scritto `NATIVE_LAUNCH_API_FAILURE`; il supervisore ha rifiutato il seguito con `RUN_RECORDS_UNCERTAINTY_OR_CANCEL` prima di Owner-ready. Nessun calcolo, History, checkpoint o ritorno causale è stato prodotto. Non è stato raggiunto il limite originale di 180 secondi prima di questo errore.

Il precedente errore di carattere illegale nell'inclusione non si è ripresentato: questa esecuzione ha raggiunto il codice del launcher. Non è una prova completa della compatibilità PJSR.

La causa principale indicata dal warning è l'accesso alla costante statica. Il gestore generico non espone l'eccezione originale del costruttore, quindi non si attribuisce al registro una diagnosi più precisa di quella osservata. Una controprova sintetica senza la proprietà statica riproduce il fallimento del launcher prima della correzione.

## Contrasto tra documentazione e runtime

La pagina locale `doc/pjsr/objects/CryptographicHash/CryptographicHash.html` descrive la proprietà statica e il costruttore con parametro intero. Il runtime effettivo non espone quella proprietà. L'header installato `include/pjsr/CryptographicHash.jsh`, datato 15 settembre 2026, dichiara invece la macro `CryptographicHash_SHA256` con valore 256. I loro SHA256, acquisiti in sola lettura, sono rispettivamente:

- pagina: `253d0ea4a641ed38da4245a957d40f31105adc341b81dc65e6d88546462492aa`;
- header: `868bec41a588a09c9a68fd52b6772f101377555439416778ccae92da613bcaea`.

Il nuovo codice passa esplicitamente 256 al costruttore nelle sei chiamate di ownership, wrapper, launcher e adattatore di apertura. Non introduce include esterni, rilevamenti automatici, algoritmi alternativi o fallback. Resta SHA-256: stesso algoritmo e stesso controllo integrale dei byte. La compatibilità del costruttore nel percorso completo resta da verificare con una nuova prova distinta.

## Correzione dei test e della dichiarazione di funzione

I mock precedenti inventavano una proprietà statica con valore 1 e non verificavano l'argomento del costruttore. I mock aggiornati non espongono la proprietà e accettano soltanto 256. La nuova regressione controlla anche il digest SHA-256 noto di `abc`, rifiuta identificatori diversi e percorre il launcher con i soli dati inventati. Non sostituisce una prova crittografica del runtime nativo.

La console ha inoltre emesso un warning sulla dichiarazione di `finalChecks` nel blocco `try`. La funzione è stata spostata al livello immediatamente interno al wrapper, ricevendo il terminale come parametro. Restano gli stessi controlli e lo stesso ordine delle due chiamate, prima e dopo la ricevuta ready. Nessun controllo di tempo, byte, cancellazione, identità o conservazione viene rimosso.

## Riconciliazione e autorizzazioni

L'istanza originale è stata chiusa normalmente con consenso separato dopo osservazione di Ready, nessuna immagine, console conservata e riferimento originale verificato. Il primo tentativo UI ha restituito un errore di geometria senza uscita osservata; una seconda autorizzazione ha permesso un solo nuovo tentativo, riuscito. L'uscita con codice zero è stata provata dall'handle originale prima di rilasciare i blocchi e chiudere il parent. Nessuna terminazione forzata o ripetizione dell'analisi. Tutti i file e i tentativi sono conservati.

Le autorizzazioni relative a questa prova e alla sua chiusura sono consumate. L'incremento ha modificato solo sorgenti, test e documentazione: nessun nuovo grant, preparazione o avvio nativo, cloud, credenziale, query provider o invio astronomico. CI esatta e ARB poi RQ sui sei file sono concluse sul commit indicato sopra; una nuova proposta eseguibile resta da predisporre e verificare separatamente. Le approvazioni restano riferite ai propri hash.

BKL-051 resta `OPEN / NOT_VALIDATED`. Restano zero nuovi controlli scientifici qualificati, il modello fisico completo non è attestato e i requisiti R01–R14 non sono chiusi da questa correzione. Rollback tramite commit ordinario, conservando tutte le prove.
