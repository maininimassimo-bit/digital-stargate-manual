# BKL-046 · Catena integrata con un testimone Windows

Il collaudo usa R4 sul registro temporaneo, il messaggio FD3 del parent, la preparazione dell'invocazione CFA, l'handle originale del child e il comparatore effettivo. Il child è un testimone Python. Produce i dieci FITS sintetici, il log e il marcatore con la prenotazione. Il parent verifica l'identità del child mentre è vivo, osserva la sua uscita sullo stesso handle e confronta il marcatore con il contesto R4. Il rilascio avviene solo dopo l'uscita zero del parent, il comparatore e la rilettura dei file e del log.

La prenotazione di prova viene rilasciata nel solo caso conforme. Resta trattenuta nei sei casi negativi, fra cui disponibilità attribuita a un altro PID, marcatore legato a un'altra prenotazione, FITS discordante, modifica dopo il confronto e prenotazione preesistente. Le due esecuzioni coincidono. I 30 file del registro canonico hanno conservato le impronte.

La catena verifica il comportamento con un testimone di Windows privo di finestra PixInsight. La creazione dell'applicazione, il controllo della finestra originale e la produzione di esportazioni native richiedono il launcher definitivo, la revisione indipendente e l'ammissione R4. Nessuna esecuzione PixInsight e nessuna chiusura scientifica.

Ricevuta SHA-256 `4119ce2a771ebb463ecf3223e4517e636e31bd54639c3ea8344ef26055585b14`.
