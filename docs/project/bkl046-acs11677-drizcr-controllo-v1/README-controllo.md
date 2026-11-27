# BKL-046 — Controllo AstroDrizzle con Driz_CR disattivato

Sul mosaico ACS/WFC F606W `jb6v01010` sono stati elaborati gli stessi sei FLC con AstroDrizzle 3.11.0. Il braccio storico replica i parametri MAST. Nell'altro braccio l'unica variazione all'invocazione è `driz_cr=False`. Il log confronta 85 parametri effettivi comuni, tutti coincidenti. I 25 payload intermedi confrontati prima di Driz_CR coincidono byte per byte. La griglia WCS e l'ordine dei 12 ingressi CTX coincidono.

Sulla griglia di 20.480.144 celle differiscono 4.520.619 valori SCI finiti, 4.519.732 valori WHT e 949.006 codici CTX. Il confronto dei pesi positivi dà 18.871.410 celle con supporto comune, 1.301 con supporto solo nel controllo e 1.607.433 senza supporto in entrambi i bracci.

Il confronto sulle aperture congelate è riuscito in 335 dei 340 centri. Il controllo dà un segnale integrato più alto in 322 aperture, più basso in 12 e identico in una. La mediana delle variazioni assolute è 119,71 elettroni/s, il 90º percentile 298,87 elettroni/s e il massimo 2.676,93 elettroni/s. Cinque aperture sono escluse per copertura incompleta. I segnali sono somme nel mosaico sui centri di componenti sature, con sottrazione di fondo locale e supporto comune. Per stimare l'errore sul flusso stellare resta da qualificare un riferimento indipendente non saturo.

Questa prova quantifica la sensibilità alla disattivazione di Driz_CR per questa associazione. Il criterio di chiusura scientifica della famiglia resta aperto.
