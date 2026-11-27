# BKL-046 · Interpolazione dei piani di fuoco WFC3/P330E

Con le 24 maschere reali P330E confrontiamo, sulle stesse immagini sintetiche, la selezione dei soli piani di fuoco di indice pari e l’interpolazione lineare fra quegli stessi piani. Entrambi stimano il centro sulla medesima griglia a ottavi di pixel. I profili usati per la verifica combinano al 37% coppie adiacenti, una delle quali esclusa dalla griglia di fit. L’interpolazione usa pesi in multipli di 1/8. Ogni fase sintetica è fuori dalla griglia di centratura. Il controllo con profilo e centro veri misura l’errore dato il rumore simulato.

| Banda | Fuoco discreto, P90 con maschera | Fuoco interpolato | Profilo esatto a 20.000 e⁻ | Profilo esatto a 200.000 e⁻ |
| --- | ---: | ---: | ---: | ---: |
| F438W | 4,02–4,14% | 2,77–2,91% | 1,74% | 0,49% |
| F606W | 5,01–5,05% | 3,43–3,47% | 1,71% | 0,51% |
| F814W | 5,34–5,65% | 3,64–3,70% | 1,71% | 0,51% |

I primi due intervalli coprono i due livelli di segnale. Il P90 di centratura con maschera è circa 0,092 px per entrambi i fit. Il confronto appaiato comprende 1.536 immagini sintetiche e 9.216 esiti considerando le due maschere e tre metodi. L’interpolazione riduce l’errore, con un residuo sopra il riferimento dell’1%. Anche il controllo con profilo esatto supera l’1% a basso segnale. Ad alto segnale scende sotto l’1% in tutte e tre le bande. Il controllo quantifica il rumore nel modello simulato. Gli errori residui dei fit includono congiuntamente forma e centro e il test non misura la fotometria reale delle visite P330E. Gli assi FILTER_COLOR/2 e FILTER_COLOR/3 restano aperti.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 71e54105094aa70c67af6c773adbf9da4c356d635d77157b0b3632472ba140e9 |
| Programma | b0e1f5c2b0a8b5d4c0ccba200243649cfb8b2e8edfedbf48acb98f455597f7e6 |
| Ricevuta riprodotta da H: | 04ef0d18a47a0e35b21ca10cfdd4be66d898412e660b773eb6407d0415a2587f |
