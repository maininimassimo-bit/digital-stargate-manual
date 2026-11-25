# ACS 11677. Prodotti intermedi comuni ai due bracci

Le invocazioni di AstroDrizzle 3.11.0 usano gli stessi sei FLC in F606W, nello stesso ordine, con la stessa MDRIZTAB. L'unica differenza negli argomenti è `driz_cr=False` nel braccio di controllo. I log attestano che le fasi comuni sono terminate e che Driz_CR è stato disattivato nel controllo.

Ho confrontato le impronte SHA-256 dei dati FITS per dodici immagini di elaborazione separata, il mediano e dodici immagini `blot`. I dati dei **25 prodotti** coincidono byte per byte. Per ogni voce il rapporto conserva anche le impronte dei file FITS completi, le dimensioni, il tipo dei dati e le unità dichiarate.

Questa verifica fissa l'accordo degli intermedi prima del rigetto. Il controllo del mosaico SCI, WHT e CTX resta in elaborazione. La misura delle aperture userà la coorte già congelata.
