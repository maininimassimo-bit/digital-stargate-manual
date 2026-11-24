# BKL-046 · Limite di correzione delle strisce TV4 per conservare i filamenti

Per ciascun estimatore della [prova precedente](BKL-046-TV4-STRISCE-ROBUSTE.md), il segnale corretto è il grezzo più una frazione fissa della differenza fra l'uscita a correzione piena e il grezzo. La perdita osservata nelle differenze appaiate scala con quella frazione. Il banco contiene 180 prove con filamenti per estimatore. Il limite retrospettivo usa il caso peggiore fra errore di flusso centrale e di forma L2. Le varianze al limite sono ricalcolate sulle acquisizioni originali.

| Operatore | Quota massima della correzione piena entro il 5% | Varianza mediana al limite, rispetto al grezzo | Varianza mediana a correzione piena |
| --- | ---: | ---: | ---: |
| Media | 6,88% | 0,9311 | 0,5216 |
| Media troncata | 6,84% | 0,9330 | 0,5255 |
| Mediana | 6,76% | 0,9342 | 0,6499 |

Il limite è determinato dalla forma, con errore di flusso centrale massimo di circa 3,65% alla quota indicata. La riduzione mediana di varianza al limite è fra il 6,6% e il 6,9%. Singole combinazioni di apertura, kernel, regione e contrasto possono invece aumentare la varianza fino al 3,4%. Le quote sono limiti per il banco osservato e richiedono una nuova verifica per altre acquisizioni o morfologie.

Un confronto usa una mappa di strisce fissa, media delle due mappe di calibrazione. La mappa si cancella nella differenza tra la prova digitale con e senza iniezione, quindi il segnale iniettato è conservato per costruzione. Sui contrasti riservati, la varianza mediana cresce del 17,0% rispetto al grezzo. La previsione per questo metodo usa in calibrazione la mappa dell'altro contrasto. Nessuna delle nove combinazioni di apertura e kernel raggiunge il limite del 15% di errore mediano di previsione per i metodi confrontati.

`DIFFUSE_BACKGROUND/1` e `NOISE_FLUX/3` restano aperti. Nessuna prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `c54f5e184ac3d4b8775dc1db97dc5d350b9dd8fcb9bd8693993f0c3417cd2eb6` |
| Programma | `171dc6a472bdfeab3caed6c575de033e230902a4fc33f120cad638b415a29544` |
| Ricevuta | `0a68109c52e4b20707717a985498421700879c02fd7e9997845c453e82284217` |
