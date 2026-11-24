# BKL‑046 · Registrazione della guida da pixel non saturi

La stima usa solo una corona valida della posa lunga e un costo con contributo del rumore sottratto. Le coppie di immagini e la maschera di saturazione sono le stesse della prova precedente. Il protocollo confronta bilineare e cubica di Keys, applicate con spostamento stimato e con spostamento noto dal generatore. I 1.776 confronti senza correzione riproducono esattamente gli esiti archiviati per bordo e picchi. [Controllo precedente](BKL-046-SATURAZIONE-PICCHI-MASCHERA.md)

| Scarto della guida | Interpolatore | P90 errore della stima dello spostamento | Sostituzione netta entro il 5%, stimata / spostamento noto | Sostituzione sfumata entro il 5%, stimata / spostamento noto |
| --- | --- | ---: | ---: | ---: |
| 0 | Bilineare | 0,127 px | 79/148 / 132/148 | 53/148 / 96/148 |
| 0 | Cubica | 0,130 px | 68/148 / 132/148 | 36/148 / 96/148 |
| 0,25 px | Bilineare | 0,127 px | 50/148 / 101/148 | 33/148 / 64/148 |
| 0,25 px | Cubica | 0,135 px | 61/148 / 137/148 | 45/148 / 122/148 |
| 0,50 px | Bilineare | 0,125 px | 24/148 / 57/148 | 17/148 / 33/148 |
| 0,50 px | Cubica | 0,137 px | 45/148 / 139/148 | 33/148 / 127/148 |

Con 0,25 e 0,50 pixel di scarto, entrambe le stime recuperano casi entro il 5% rispetto alla posa non registrata, che ne aveva zero per ciascun metodo. La cubica con spostamento noto conserva più casi della bilineare. Con guida già allineata, stimare di nuovo lo spostamento perde casi entro soglia. Il P90 dell’errore di stima supera 0,1 pixel in tutti i gruppi.

Le otto geometrie doppie risolte nel riferimento restano risolte e non compaiono picchi non abbinati. Il confronto riguarda sostituzioni idealizzate e non verifica aloni sotto soglia, righe di spillamento o registrazione su esposizioni reali. L’asse `SATURATION_BLEND/4` resta aperto.

SHA‑256 della ricevuta `718e714bf463435915084a02e7f9efa13a71f98a4c8758b8a5c3e82b67186146`.
