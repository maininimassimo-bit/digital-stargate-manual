# BKL-046 · Propagazione della covarianza dopo ricampionamento dei flat RED

La prova conserva le coppie di flat e le tre aperture da 64 pixel del [confronto precedente](BKL-046-TV4-VARIANZA-APERTURE-RED.md). Usa un operatore identità e due medie a mezzo pixel, rispettivamente lungo colonne e righe. Le finestre sono disgiunte nel dominio di ingresso per ogni forma e operatore. Il programma verifica che la somma dei pixel ricampionati coincida con la somma ottenuta dai pesi equivalenti sulla griglia originale.

Sui tre livelli di calibrazione il modello stima la varianza per pixel in funzione del tempo e la covarianza normalizzata per ritardo e regione. Ai due tempi riservati confronta l’indipendenza dei pixel in uscita, l’ipotesi di ingresso bianco con sovrapposizione esatta dei pesi, e la propagazione della covarianza di ingresso. La tabella mostra l’errore relativo mediano sulle 15 combinazioni di regione e forma.

| Operatore e tempo | Uscita indipendente | Ingresso bianco con pesi condivisi | Covarianza di ingresso |
| --- | ---: | ---: | ---: |
| Identità, 33,5 ms | 34,87% | 34,87% | 13,72% |
| Identità, 303,5 ms | 20,92% | 20,92% | 13,77% |
| Mezzo pixel orizzontale, 33,5 ms | 67,22% | 38,75% | 16,98% |
| Mezzo pixel orizzontale, 303,5 ms | 56,38% | 21,97% | 15,78% |
| Mezzo pixel verticale, 33,5 ms | 65,36% | 40,40% | 12,49% |
| Mezzo pixel verticale, 303,5 ms | 57,80% | 23,03% | 14,32% |

La propagazione della covarianza porta 45/90 esiti entro il riferimento del 15%, contro 21/90 con ingresso bianco e pesi condivisi. Le mediane del mezzo pixel orizzontale restano sopra quel riferimento. I controlli riproducono le dieci previsioni per pixel e le 30 misure senza ricampionamento. Gli operatori sono quelli espliciti del protocollo. Le pose, le regioni e le aperture non costituiscono repliche indipendenti tra tutte le combinazioni. NOISE_FLUX/3 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 1f3a0f2b1fa0c20721c6f5dbd3d0de0ff34952fe976e024795b16b8c1d0bf666 |
| Programma | e42c17d9e9e4168a16b6e3ff6aa6b9c868de97de11f851aaf1f8170205942ae0 |
| Verifica appaiata | 21f96322b732b687cdda6fb0225896829d83616206e98d0c3c572cad912f321f |
| Riscontro replicato da H: | 14091d3c521efa0479a939b4b6c30298d4e38027655c79a45cb4b109910f428e |
