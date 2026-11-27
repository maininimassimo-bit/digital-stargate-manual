# BKL-046 · Correzione del launcher CFA prima della revisione

La verifica interna ha rilevato che il launcher v1 imponeva la coppia detector / shear-edge05, mentre il piano congelato chiede di discriminare separatamente la coordinata della maschera e la convenzione geometrica. Questo poteva trattenere la prenotazione anche con risultati sintetici coerenti ma con una convenzione diversa.

Il launcher v2 accetta detector o reference e richiede la corrispondenza con una sola ipotesi geometrica. La ricevuta deve contenere il risultato specifico di ogni caso, le impronte del piano e del manifest e i tre valori enumerati. Tutti e quattro gli incroci fra le due scelte hanno prodotto il rilascio R4 nel registro di prova. Finestra non reattiva, FITS incompatibile e collisione nell'archivio hanno trattenuto le rispettive prenotazioni. Due esecuzioni hanno prodotto lo stesso rapporto.

Il soggetto per ARB è ora SHA-256 `ea2411fda0125521edc7ab987aea78fe52a4880dc8e91423341cd93b26bfd2da`. I risultati sono sintetici e non determinano quale convenzione usi PixInsight. Le approvazioni indipendenti e l'ammissione restano pendenti. PixInsight è rimasto chiuso.
SHA-256 archivio H: e342813d9bab3ff540a30a1629809d0e6b99c7d941e5c1e64e6e2824d0889e61.
