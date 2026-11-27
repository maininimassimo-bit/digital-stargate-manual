# BKL-046 · Covarianza Roman stimata su coppie separate

La prova usa dieci coppie disgiunte di rampe GAIN, due fasce esterne, 32 canali e tre livelli di segnale. Per ogni coppia esclusa stima la forma della covarianza dei nove pixel di ingresso sulle altre nove coppie, nello stesso canale, fascia e livello. Usa blocchi 3 × 3 disgiunti e la maschera comune degli estremi di rappresentazione. Entrambi i modelli usano la stessa varianza scalare della coppia esclusa e gli stessi pesi bilineari. I 1.920 confronti riproducono prima la varianza di riferimento. [Prova sulle tre fasce](../bkl046-roman-gain-spatial-band-covariance-v1/README.md)

| Fascia e lettura | Errore mediano, ingresso indipendente | Errore mediano, covarianza stimata |
| --- | ---: | ---: |
| Inferiore, 1 | 21,9% | 5,6% |
| Inferiore, 5 | 13,4% | 4,1% |
| Inferiore, 10 | 12,0% | 3,7% |
| Superiore, 1 | 27,9% | 7,5% |
| Superiore, 5 | 14,3% | 4,1% |
| Superiore, 10 | 12,7% | 3,6% |

La stima riduce la mediana di ogni canale e di 59 delle 60 mediane per coppia, fascia e lettura. Riduce il P95 in tutte e sei le combinazioni. Il fascicolo sui flat ASI2600MC registra un esito diverso con lo stesso principio di separazione delle coppie. [Verifica ASI2600MC](../bkl046-asi2600mc-flat-held-out-covariance-v1/README.md)

Il campione Roman riguarda due fasce della stessa serie di laboratorio, un solo spostamento e acquisizioni condivise fra le letture. Il risultato riguarda la trasferibilità fra coppie nella stessa serie. Restano da verificare la trasferibilità fra sessioni, la dose calibrata e l’operatore nativo.

Per riprodurre, passare a `misura.py` il protocollo, i kit estratti Roman delle fasce e dei canali, la directory con NumPy 2.3.5 e una nuova directory di uscita. Usare Python 3.12.