# BKL-046 · Varianza in apertura con covarianza dipendente dal segnale

Il test conserva i 90 confronti del [ricampionamento dei flat TV4 RED](BKL-046-TV4-COVARIANZA-RICAMPIONAMENTO-RED.md). Al modello con covarianza normalizzata fissa e scala della varianza variabile affianca due modelli che stimano un andamento affine per ciascun ritardo. Il primo usa i tre livelli positivi di calibrazione. Il secondo fissa l’intercetta alla covarianza media misurata nelle due coppie BIAS. Entrambi prevedono la varianza delle somme ai due livelli riservati, usando gli stessi pesi equivalenti.

| Modello | Casi entro il 15% | Errore mediano mezzo pixel orizzontale, 33,5 ms | Errore mediano mezzo pixel orizzontale, 303,5 ms |
| --- | ---: | ---: | ---: |
| Covarianza normalizzata fissa | 45/90 | 16,98% | 15,78% |
| Affine per ritardo | 38/90 | 23,52% | 13,00% |
| Affine per ritardo con intercetta BIAS | 46/90 | 19,00% | 14,06% |

Entrambi i modelli affini migliorano la mediana orizzontale al livello alto e la peggiorano al livello basso. L’ancoraggio BIAS aggiunge un solo caso entro il riferimento sul totale. Le varianze previste sono positive per tutte le aperture provate. La positività per queste aperture lascia da verificare la validità della matrice di covarianza su supporti generali. Le 90 varianze osservate e le previsioni dei modelli precedenti coincidono con la ricevuta di riferimento. Il campione conserva le stesse pose e i due ricampionamenti espliciti. NOISE_FLUX/3 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 5dd46aace8e19e0e3f4067d80191bd2fb6ec182502ffc0e58410e01526532e5f |
| Programma | b65b4605bf114ce915602552fa7c33fd00e782fafd0457b8e587a50fe7a703be |
| Verifica appaiata | c1b1f8c2b063847d3bf03d8c6be6d30267a28594de96a907dd889162e82e0365 |
| Riscontro replicato da H: | 920891932cbea7b7e8f1a5acf5ee7a47b4bdc53629cd635e69f8358d1cdba116 |
