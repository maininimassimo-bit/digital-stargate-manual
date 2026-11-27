# BKL-046 · Verifica congiunta dei controlli XDRZ

La verifica richiede i cinque casi del piano congelato, dieci FITS lineari di intensità e peso e i relativi messaggi di console con i parametri riletti. Controlla nomi, geometria, supporto RGB, pesi grezzi, membri XDRZ e impostazioni uguali fra i casi quando il piano le fissa. Il rigetto del verde deve corrispondere a una sola interpretazione. Il controllo geometrico richiede una sola variante compatibile con il riferimento offline. Se entrambe le origini concordano o nessuna concorda, il programma segnala l'ambiguità per la revisione.

Le due riesecuzioni dei controlli simulati producono lo stesso risultato. Il verificatore riconosce due serie complete e respinge otto esiti alterati, fra cui uscite o messaggi mancanti, maschera senza effetto, origini ambigue, cambi di parametro, ingressi difformi e pesi riscalati. Nel percorso di confronto con le esportazioni fornite, registra gli SHA-256 dei FITS e degli eventi. La provenienza dal processo originale, l'ammissione e l'uscita verificata competono al supervisore e al coordinatore.

Ricevuta SHA-256 `9e7db44d6dbc1114ddfb4c21c312edd3a03497b5684324ed0a5d12dd458c6f14`. Il controllo è candidato alla revisione insieme al piano e allo script PJSR. Zero esecuzioni native.
