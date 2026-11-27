# BKL-046 · Orientazione PSF propria e di zona sui verdi M8/M20

Ho mantenuto i pixel Bayer nativi, i centri proiettati, le maschere e la griglia Moffat del controllo precedente. Per ciascuna delle 19 stelle, ho stimato un angolo locale dalle altre stelle della stessa zona sulla metà di stima. Ho poi scelto larghezza, profilo delle ali e rapporto assiale della stella allo stesso angolo locale. Il confronto valuta questa scelta con quella dell’angolo della singola stella sulle sette pose tenute da parte. Ho scambiato i ruoli delle due metà. Il riferimento è il fit circolare. [Controllo precedente per zona](../bkl046-m8-m20-psf-green-zone-permutation-v1/README.md)

| Calibrazione e parità | Casi | Angolo proprio migliore | Angolo di zona migliore | Pari entro la tolleranza numerica |
| --- | ---: | ---: | ---: | ---: |
| A, G1 | 38 | 11 | 10 | 17 |
| A, G2 | 38 | 13 | 8 | 17 |
| B, G1 | 38 | 11 | 10 | 17 |
| B, G2 | 38 | 16 | 5 | 17 |

La differenza mediana appaiata tra i guadagni rispetto al fit circolare è zero in tutte e quattro le combinazioni. I due modelli possono comunque differire per singola stella o metà di esposizione. Il profilo specifico della stella ha più vittorie in G2. Le due calibrazioni riusano le stesse pose. I 152 casi sono confronti dipendenti su un solo campo. Restano da verificare altri campi, l’orientazione fisica e la validazione nativa.

Il programma rilegge dal rapporto precedente i 76 fit delle parità verdi. Richiede identità di decisioni e forme, accordo degli angoli entro 10⁻¹⁰ gradi e dei guadagni entro 10⁻¹². Per ripetere, passare a `misura.py` il protocollo, le directory dei kit di parità, modelli estesi e pose disgiunte, lo ZIP dei mosaici, la ricevuta delle larghezze, le dipendenze e una nuova directory di uscita.