# BKL-046 — Esposizioni ACS con soluzioni Gaia e controlli GO-14949

Sono state verificate sette testate astrometriche ACS/WFC F606W nell'archivio pubblico MAST. Per una ottava esposizione il catalogo non restituisce il prodotto headerlet. La soluzione Gaia e la proiezione con le distorsioni dei chip selezionano due esposizioni vicine nel tempo. A 30 secondi, `jbbf01i3q` copre 316 centri e precede il riferimento di 176,92 giorni. A 40 secondi, `jbb502ijq` copre 296 centri e lo precede di 163,36 giorni. Entrambe dichiarano Gaia eDR3 sui due chip con la stessa famiglia di riferimento IDC del FITS sorgente. La verifica geometrica richiede ancora i pixel dei FLC completi.

Sono stati misurati i due FLC da 40 secondi di GO-14949 già in custodia. Il primo, con soluzione Gaia eDR3, copre 287 centri e produce 67 ancoraggi complessivi nelle quattro coppie di chip, da 12 a 23 per coppia. Il secondo, con GSC 2.4.2, copre 286 centri e produce un solo ancoraggio. Nessuna coppia raggiunge il minimo di 24 stelle per partizione. Le due pose sono osservazioni distinte, quindi la differenza di conteggio non isola l'effetto del catalogo astrometrico. Nessun centro è qualificato per misurare il flusso stellare.

[Prodotti MAST](https://mast.stsci.edu/api/v0/)
