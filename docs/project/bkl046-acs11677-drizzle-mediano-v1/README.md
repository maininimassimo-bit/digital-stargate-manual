# AstroDrizzle ACS 11677. Verifica del fondo e supporto per la ricorrenza

Per l'associazione pubblica `jb6v01010`, il trailer MAST e la replica su DSG-Shared riportano la stessa MDRIZTAB, riga 4, e gli stessi sei valori di fondo usati nella costruzione del mediano. Il confronto usa le stringhe registrate nei due log. La dimensione, il pixel di riferimento, il centro celeste e la matrice CD calcolati nella replica concordano con la testata SCI del DRC ufficiale, entro 10⁻¹² per i valori di griglia non interi.

Il file `ricorrenza-chip2-fissata.npy` conserva le 29.087 proiezioni univoche già ammesse dalla geometria sul chip 2. Le colonne sono componente, coordinate X/Y nella posa di 1457 s e coordinate X/Y nella posa di 1456 s. Il congelamento riproduce le 3.046 coincidenze archivistiche del bit 4096 sulle 121 componenti. Il supporto potrà essere applicato alle due maschere della replica senza rifare la selezione.

Il riscontro riguarda i valori di fondo registrati, la griglia calcolata e la riproduzione del campione archivistico. Il confronto delle nuove maschere, dei dati SCI e dei pesi effettivi richiede i prodotti completi. La ricorrenza del flag da sola non determina la natura dei pixel respinti.
