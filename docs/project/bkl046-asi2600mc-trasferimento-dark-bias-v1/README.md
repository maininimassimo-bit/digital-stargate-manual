# BKL-046 · Trasferimento della covarianza fra dark e Bias ASI2600MC

Il test riproduce le misure congelate sui dark da 180 s e sui Bias da 3 s. Per ogni coppia esaminata, calibra la forma della covarianza sullo stesso riquadro e sulla stessa parità Bayer. Usa tutte le sette coppie dell'altra serie per il trasferimento oppure le sei coppie rimanenti della stessa serie per il confronto. Tutte le previsioni usano la varianza scalare della coppia analizzata e tengono conto della condivisione dei pixel nel ricampionamento.

| Mezzo pixel su entrambi gli assi | Mediana di errore, ingresso indipendente | Covarianza dell'altra serie al 25% | Covarianza dell'altra serie al 100% |
| --- | ---: | ---: | ---: |
| Dark 180 s, dalla serie Bias | 4,96% | 5,48% | 6,90% |
| Bias 3 s, dalla serie dark | 4,24% | 4,68% | 8,42% |

Nelle dieci combinazioni di direzione del trasferimento e fase, la matrice trasferita integralmente non migliora né la mediana né il P95. Il peso del 25% migliora la mediana in due combinazioni e il P95 in una. Il rapporto conserva le mediane per coppia. Le fasi, le parità e i riquadri riusano le stesse acquisizioni. Il confronto resta circoscritto a due serie senza illuminazione e non qualifica il trasferimento tra dosi ottiche, altri sensori o operatori nativi.

Per riprodurre il rapporto passare a `misura.py` il protocollo, le directory congelate del test dark bilineare e dei calibratori, la directory dei due ZIP FITS originali, NumPy 2.3.5 con Astropy 7.2.0 e una nuova directory di uscita.
