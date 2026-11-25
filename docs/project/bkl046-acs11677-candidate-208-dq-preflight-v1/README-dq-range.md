# BKL-046 — Controllo parziale DQ prima dell'acquisizione FITS

Per due ulteriori esposizioni pubbliche ACS sono state acquisite solo le testate FITS pertinenti e una fascia del piano DQ. Le letture con HTTP Range sono vincolate alla versione dell'oggetto e all'ETag. Le testate collegano il piano DQ all'estensione SCI del chip 2. La posizione è quella nominale calcolata dall'headerlet, senza una qualifica geometrica sui pixel della posa.

A raggio 10 pixel dalla previsione nominale, `jbbf01hxq` ha 10 pixel con DQ non nullo e `je5v02rhq` ne ha 18. A raggio 13 i conteggi salgono a 14 e 32. Il preflight non ha richiesto i campioni SCI o l'immagine completa. Una posizione nominale con flag non decide da sola l'ammissibilità dopo un'eventuale registrazione. Con le informazioni disponibili, nessuna delle due esposizioni ha una finestra nominale DQ zero e il flusso resta da misurare.
