# BKL-046 · Chiusura ordinaria del testimone Windows

Il candidato rilegge l'identità della finestra e del processo originale subito prima dell'azione. Invia una sola richiesta ordinaria WM_CLOSE e respinge una seconda richiesta. Il test con due testimoni invisibili e omonimi ha osservato la scomparsa dell'handle originale e l'uscita zero dello stesso processo. L'altra finestra è rimasta aperta. Le due esecuzioni coincidono.

Il controllo di cattura ha rifiutato la finestra nascosta. Il messaggio WM_PRINT diretto non ha prodotto pixel validi e PrintWindow non ha restituito un'immagine utilizzabile. Il test attesta quindi il rifiuto del risultato, senza una cattura riuscita. PrintWindow è sincrona. Il suo uso nel supervisore richiederebbe un contesto di osservazione che consenta di trattenere la prova in caso di attesa o errore. La cattura e la chiusura di PixInsight restano da verificare dopo revisione e ammissione. [Microsoft Learn, PrintWindow](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-printwindow)

Ricevuta SHA-256 `ffe3b3051b01c24042ac7e55d0877f8c3b5970b8eaed3f9f170d8bbfec57e0ad`. Nessuna esecuzione PixInsight.
