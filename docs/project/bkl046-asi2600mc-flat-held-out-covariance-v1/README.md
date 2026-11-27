# BKL-046 · Covarianza dei flat stimata da coppie escluse dalla misura

Il confronto usa le sette coppie disgiunte di flat ASI2600MC da 3 s, le cinque fasi bilineari e i tre trattamenti del test precedente. Per ognuna delle sette coppie esclusa a turno, la forma della matrice di covarianza dei nove pixel di ingresso è stimata sulle altre sei coppie, nello stesso riquadro, parità Bayer, metà e trattamento. Entrambi i modelli usano la stessa varianza scalare misurata sulla coppia esclusa. La previsione senza covarianza tra pixel di ingresso include comunque la condivisione dei pesi del ricampionamento. [Prova precedente](../bkl046-asi2600mc-flat-bilinear-v1/README.md)

| Mezzo pixel su entrambi gli assi | Errore mediano, ingresso indipendente | Errore mediano, covarianza stimata | Misure entro il 10%, ingresso indipendente → covarianza |
| --- | ---: | ---: | ---: |
| Differenza grezza | 6,2% | 13,3% | 330 → 180 su 504 |
| Scala di illuminazione | 6,3% | 13,5% | 330 → 179 su 504 |
| Piano sottratto | 5,4% | 5,9% | 384 → 352 su 504 |

La mediana aggregata peggiora con la stima appresa in tutti i 15 confronti fra fase e trattamento. Sui dati grezzi a mezzo pixel, il P95 migliora dal 39,1% al 37,9%. Dopo la sottrazione del piano, quattro delle sette mediane per coppia migliorano a quella fase, mentre il P95 aggregato peggiora dal 17,8% al 19,5%. Il rapporto conserva gli esiti per coppia e le code della distribuzione.

Le misure condividono le stesse acquisizioni, e le sei coppie usate per l’addestramento si sovrappongono tra ripetizioni. Il risultato riguarda la trasferibilità di questa stima sulla sola serie di flat a 3 s. Restano aperti operatori nativi, dosi multiple e validazione scientifica.

Per riprodurre, passare a `misura.py` il protocollo di questo studio, la directory estratta dell’archivio della prova precedente, le dipendenze NumPy 2.3.5 e Astropy 7.2.0 e una nuova directory di uscita. Usare Python 3.12. L’archivio precedente ha SHA-256 `085ca830a9eb9c8f51fd4b94d878803f2918f8ec0129f3d1f7b644b8c093086c`.