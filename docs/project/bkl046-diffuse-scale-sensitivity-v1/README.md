# BKL-046 · Sensibilità alla scala nel fondo differenziale

Si moltiplica il contrasto della posa bersaglio rispetto alla sua mediana sul supporto comune, lasciando fissi riferimento, maschera, registrazione e partizioni spaziali. I moltiplicatori +/-0,5% e +/-1% sono perturbazioni analitiche delle pose allineate. A scala unitaria si riproducono esattamente tutte le 198 metriche per partizione del confronto precedente. La decisione è favorevole quando il piano migliora la mediana assoluta di almeno il 10% rispetto all'offset e il P90 non cresce in entrambe le partizioni.

| Fattore applicato alla posa bersaglio | IC 1805, coppie che cambiano esito su 72 | M8/M20, coppie che cambiano esito su 27 |
| ---: | ---: | ---: |
| 0,990 | 3 | 4 |
| 0,995 | 2 | 1 |
| 1,005 | 2 | 4 |
| 1,010 | 1 | 1 |

Il massimo sui quattro scenari del P90, calcolato sulle variazioni assolute del P90 del residuo del piano per partizione, è 0,032 ADU su IC 1805 e 0,298 ADU su M8/M20. I conteggi includono sia passaggi verso l'esito favorevole sia la perdita di un esito favorevole. Le coppie condividono pose e non costituiscono osservazioni statisticamente indipendenti. I due campi usano scale ADU diverse.

Questo controllo identifica decisioni sensibili a scarti di scala scelti prima della misura. Non stima il guadagno, il throughput effettivo o la risposta spaziale del flat. Per separare additivo e moltiplicativo servono una scala stimata da riferimenti indipendenti con incertezza, il relativo bilancio d'errore e un test nativo. I confronti prossimi alla soglia richiedono che la decisione sia stabile nell'intervallo di scala effettivamente qualificato. Nessuna chiusura scientifica.

Gli script di confronto, i dati originali e le ricevute degli ingressi sono conservati nei kit collegati. Il programma qui aggiunto riusa soltanto il caricamento e la registrazione degli script archiviati dopo averne verificato le impronte. [IC 1805](../bkl046-ic1805-reference-transfer-v1/README.md) · [M8/M20](../bkl046-m8-m20-reference-transfer-v1/README.md)