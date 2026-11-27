# BKL-046 · Supervisore CFA con custode R4 su registro di prova

Su DSG-Shared, il custode R4 installato ha associato il processo padre Python originale tramite il canale FD3, PID e ora di creazione. Il padre ha verificato i record di acquisizione prima di creare il testimone. Il supervisore ha poi acquisito la finestra, usato il comparatore CFA e controllato di nuovo le impronte prima della chiusura e del rilascio.

Due esecuzioni su nove scenari hanno prodotto lo stesso rapporto. Nelle esecuzioni valide R4 ha scritto la ricevuta di rilascio con uscita del padre pari a zero. Negli otto rifiuti il registro di prova ha conservato i record originali e l'acquisizione attiva senza ricevuta di rilascio. La modifica del log dopo l'uscita regolare ha trattenuto la prenotazione anche con il padre già terminato a zero. Il collaudo ha verificato le impronte dei 30 file del registro canonico e dei tre file R4 controllati prima e dopo.

Il registro è di prova, l'inventario è simulato e la finestra appartiene a un testimone Windows. FITS e log sono sintetici. Il collaudo ha chiuso la pipe del custode nei casi di rifiuto e ha verificato che il registro restasse trattenuto. Il launcher scientifico deve ancora integrare il trasporto definitivo, la pubblicazione persistente e l'inventario effettivo, quindi passare le revisioni e ottenere l'ammissione prima di avviare PixInsight. Esecuzioni native e chiusure scientifiche a zero.
SHA-256 archivio H: 2a30c05e81fceea6f2e19910fea2708b3c7ccfe66663f963356419b79ec2f122.
