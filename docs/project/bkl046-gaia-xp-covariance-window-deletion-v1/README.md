# BKL-046 · Esclusione diagnostica della banda Gaia XP 632–646 nm

La verifica elimina righe e colonne degli otto campioni fissati a 632–646 nm e controlla l'intero spettro degli autovalori della correlazione residua. Il controllo è ripetuto sulla sorgente v571 e sulle tre sorgenti archiviate, tutte dello stesso catalogo e modello. La tolleranza di rifiuto è −1e−8.

| Campione | Modi negativi prima → dopo | Altre esclusioni di otto campioni che passano |
| --- | ---: | ---: |
| v571 | 1 → 0 | 7 su 335 |
| Coorte 1 | 1 → 0 | 6 su 335 |
| Coorte 2 | 1 → 0 | 6 su 335 |
| Coorte 3 | 1 → 0 | 5 su 335 |

Nessuna esclusione disgiunta dalla banda fissata passa. I minimi delle matrici residue sono dell'ordine di −4e−15. Le quattro correlazioni formali condizionate superano il controllo dopo la stessa esclusione. Questo risultato localizza il difetto in relazione alla maschera di otto campioni. L'idoneità scientifica della maschera resta aperta, in particolare la perdita di informazione e gli effetti su flussi e incertezze nelle bande d'interesse. Nessuna misura di calibrazione indipendente e nessuna prova nativa.

Per riprodurre con Python e NumPy 2.3.5 impostare OPENBLAS_NUM_THREADS=1. Passare protocollo, directory del riscontro di supporto della coorte, estrattore della coorte, directory del supporto v571, directory delle fonti della coorte, ZIP v571 restaurato e nuovo percorso di uscita. Il protocollo fissa le impronte.
