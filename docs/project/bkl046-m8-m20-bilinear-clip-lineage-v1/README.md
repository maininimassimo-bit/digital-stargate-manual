# BKL-046 · Clipping CFA e debayer bilineare su M8/M20

Nei 15 FITS grezzi RGGB congelati, 289.327 campioni RGB ricostruiti ricevono almeno un contributo da un fotosito al limite digitale 65.535. Alla soglia 62.000, 190.860 di questi campioni (65,97%) restano sotto soglia. Il conteggio somma campioni per canale e posa. Campioni adiacenti possono condividere fotositi.

| Canale | Con almeno un contributo al limite | Sotto 62.000 | Sotto 64.880 | Sotto 65.535 |
| --- | ---: | ---: | ---: | ---: |
| R | 98.479 | 74.394 | 75.713 | 75.958 |
| G | 103.052 | 56.248 | 58.808 | 59.276 |
| B | 87.796 | 60.218 | 61.820 | 62.173 |
| Totale | 289.327 | 190.860 | 196.341 | 197.407 |

Tra i campioni a soglia o sopra, 3.816 a 62.000 e 659 a 64.880 non ricevono contributi da fotositi a 65.535. Il riferimento per entrambi i conteggi è la provenienza dal limite digitale. Alla soglia 65.535, l'uscita bilineare raggiunge il limite esattamente quando tutti i contributi con peso positivo lo raggiungono.

La misura usa stencil bilineari espliciti, taglia due pixel CFA per lato e confronta numeratori interi senza arrotondare le medie. Verifica due stimoli sintetici isolati R e G, le impronte dei 15 FITS e i conteggi per parità dello studio precedente. Per ripeterla, passare allo script nell'ordine il protocollo, lo ZIP delle pose, la ricevuta di cattura, il riscontro precedente, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un percorso di output nuovo. Il protocollo fissa le impronte degli ingressi. I FITS originali restano nell'archivio di progetto.

Il risultato documenta un limite della soglia sull'immagine ricostruita per SATURATION_BLEND. Il modello descrive il clipping del codice memorizzato e lascia da verificare la risposta fisica del sensore, il recupero del flusso e il comportamento del debayer nativo di PixInsight. Chiusure scientifiche in questo incremento: zero.
