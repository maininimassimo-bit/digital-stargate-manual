# BKL‑046 · Componenti lungo righe e colonne nei frame TV4

Le finestre di riferimento sono disgiunte dalle cinque regioni di misura. Due strisce orizzontalmente separate misurano la componente comune di ogni riga. Due strisce verticalmente separate misurano quella di ogni colonna. Si confrontano la sottrazione lungo ciascun asse e la sottrazione congiunta, usando gli stessi 90 casi su contrasti di verifica. Le 90 misure senza sottrazione riproducono il rapporto precedente. [Protocollo delle aperture TV4](BKL-046-TV4-RUMORE-APERTURE.md)

Tra riferimenti disgiunti la correlazione mediana è 0,704 lungo le righe e −0,012 lungo le colonne. Con la sola sottrazione della componente di riga, la varianza mediana relativa dell’apertura larga scende al 44–45% del valore iniziale nelle tre trasformazioni. Per l’apertura alta resta al 62–73%. La sottrazione della sola componente di colonna lascia le varianze mediane relative fra 1,001 e 1,007.

| Trasformazione | Rapporto mediano 4 × 16 / 16 × 4 originale | Dopo sottrazione di riga | Dopo sottrazione di colonna | Dopo entrambe |
| --- | ---: | ---: | ---: | ---: |
| Identità | 2,392 | 1,816 | 2,375 | 1,807 |
| Mezzo pixel lungo X | 2,517 | 1,933 | 2,491 | 1,929 |
| Mezzo pixel lungo Y | 2,172 | 1,634 | 2,162 | 1,626 |

La correzione di riga attenua l’anisotropia osservata e ne lascia una parte misurabile. Nessuna delle correzioni porta un gruppo di previsioni di varianza entro la soglia mediana del 15% sulle coppie temporali di verifica. La prova riconosce una componente comune fra strisce in questa sequenza di laboratorio. L’origine fisica della componente e la conservazione del segnale astronomico con l’operatore restano da verificare. L’asse `NOISE_FLUX/3` resta aperto.

SHA‑256 della ricevuta `875cf9cf976596027dca45b1528d8f83b48a7511e4c7da35a27b3a232582c059`.
