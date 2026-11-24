# BKL-046 · Supporto DQ nelle visite P330E successive

Quattro visite successive di P330E, nei programmi 17681 e 17960, hanno fornito 24 esposizioni originali CALWF3. Il [protocollo precedente](BKL-046-WFC3-P330E-VISITE.md) è stato riapplicato agli stessi tre filtri e alle due pose per filtro. Ventitré esposizioni sono respinte per DQ nel nucleo e una per picco troppo distante dalla posizione prevista. Nessuna visita fornisce la fotometria ripetuta richiesta.

Ho controllato la possibilità di combinare le due pose. Il controllo riproietta una griglia circolare di 317 campioni nel sistema WCS della seconda posa. Ogni campione richiede DQ zero per tutti i pixel con peso bilineare non trascurabile. La tabella riporta il supporto dell'unione. La classificazione è la stessa nelle tre bande di ciascuna visita.

| Visita | Sensore | Campioni ancora scoperti nell'apertura | Campioni ancora scoperti nel nucleo |
| --- | ---: | ---: | ---: |
| ifi511 | 1 | 6 | 1 |
| ifi512 | 2 | 3 | 0 |
| ifqj11 | 1 | 5 | 2 |
| ifqj12 | 2 | 3 | 0 |

Le pose spostate rendono completo il nucleo nella proiezione nominale su UVIS2. Rimangono lacune nell'apertura su entrambi i sensori. Il controllo include anche la coppia con identità del picco non confermata e per quella coppia attesta soltanto la geometria delle maschere. Non sono stati riempiti pixel né stimato il flusso. L'asse `FILTER_COLOR/2` resta aperto.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo e impronte delle esposizioni | `c1c700b6e668a5fd6b4174a7b1016644a593880c87786cd33baa949ebdce17db` |
| Ricevuta delle 24 esposizioni | `71a6732a965b092c4bb87343311b45ab4b89ec334c21d44183ca6dddb87194f4` |
| Supporto DQ delle 12 coppie | `c11836dcc3bae058bd778ad52f7976c080a5cd0ed1e110bcd0700454a11387d1` |
