# BKL-046 · Sessione candidata per i cinque controlli CFA

L'ingresso PJSR candidato esegue i cinque casi del piano nell'ordine congelato, nella stessa sessione e in una directory associata alla prenotazione. Ogni caso esporta l'intensità e i pesi, chiude le due finestre risultato che ha creato e restituisce il testo dei due eventi di console. Se i cinque casi terminano, il batch scrive e rilegge il log di dieci eventi e poi il marcatore di completamento con operazione, prenotazione e impronte del piano e del soggetto.

Il collaudo simulato ha verificato che resti aperta una finestra preesistente e che si chiudano le dieci finestre risultato. In nove casi negativi il programma si interrompe prima di emettere il marcatore. Fra i casi rientrano directory assente, risultati preesistenti, prenotazione invalida, piano diverso, fallimento di un caso, finestra trattenuta, scrittura FITS fallita e log alterato. Le ricevute delle due esecuzioni coincidono.

Il marcatore attesta il completamento della produzione dei file nel batch. L'origine del processo, la verifica scientifica degli output, la custodia della finestra PixInsight e il rilascio restano responsabilità del launcher revisionato e di R4. Lo script è candidato per una nuova revisione e non viene eseguito quando viene caricato nel simulatore.

Ricevuta SHA-256 `4a18fc32ff9adbeb02756f1fcd4e4678496bfcd318323009089a8ec5a06ee656`. Zero esecuzioni native.
