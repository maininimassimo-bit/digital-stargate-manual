# BKL-046 · Ingressi XDRZ diagnostici M8–M20

Il pacchetto diagnostico per la stella 14-1-0 conserva 28 FITS CFA calibrati delle 14 pose. Contiene 336 descrittori XDRZ che coprono due calibrazioni, due geometrie, le due serializzazioni dell'origine e tre condizioni: rigetto in coordinate del rivelatore, rigetto in coordinate del riferimento e controllo senza rigetto.

Il verificatore ha riletto matrici, origine, fase RGGB, percorsi sorgente e tutti i byte dei piani di rigetto. Il manifest indica la regione di 29 × 29 pixel da confrontare con il riferimento numerico e registra gli scarti esterni al reticolo per l'ipotesi del riferimento. Due generazioni hanno prodotto lo stesso SHA-256 `eb8d6ef7a82808d5c55c2f9276e5de934097d273c2ddef91d955ebb7606e3637`.

Gli RGB ausiliari sono immagini marcatrici costanti e richiedono che il controllo sintetico confermi l'uso effettivo della sorgente CFA e l'assenza di normalizzazione. Il pacchetto attende quel risultato per scegliere l'origine e il tipo di mappa. Le ipotesi restano distinte e nessuna è stata eseguita in PixInsight. Esecuzioni native e chiusure scientifiche a zero.
SHA-256 archivio H: cd8219fc8ba7354d6eed071bc3fcd60fbb44fde8f3158ecf540dbaa3c8212315.
