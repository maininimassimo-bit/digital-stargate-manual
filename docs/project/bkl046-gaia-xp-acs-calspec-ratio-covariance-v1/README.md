# BKL-046 · Covarianza formale Gaia XP nei rapporti ACS di GD71 e GD153

Il modello GaiaXPy fissato ricostruisce i flussi e gli errori marginali pubblicati con scarti relativi massimi inferiori rispettivamente a 1,15e−5 e 1,97e−6. Si usano gli stessi pesi ACS verificati alla data delle dodici pose. Per ogni banda si mediano i pesi delle due pose prima di propagare la covarianza, poiché entrambe usano lo stesso spettro Gaia.

| Sorgente | Deviazione standard relativa F658N/F660N, BP/RP indipendenti | Solo diagonale spettrale | Scarto osservato ACS rispetto a Gaia |
| --- | ---: | ---: | ---: |
| GD71 | 0,716% | 0,573% | −3,81% |
| GD153 | 0,598% | 0,471% | −3,54% |

Con le due covarianze marginali BP e RP fissate, una covarianza congiunta semidefinita positiva limita la deviazione standard di ciascun rapporto tra il modulo della differenza e la somma delle deviazioni standard dei contributi. Per il rapporto stretto il limite superiore cambia meno dello 0,004% in termini relativi rispetto al caso BP/RP indipendenti. Lo scarto osservato è 5,32 e 5,92 volte il rispettivo limite superiore della sola componente formale Gaia. Questi fattori non misurano una significatività statistica congiunta. Apertura, errori ACS, risoluzione spettrale e sistematiche restano aperti.

Nella correlazione ricostruita dal triangolo storico ricompare un autovalore negativo in entrambe le stelle. Per l'incertezza ACS il verificatore usa la propagazione lineare delle covarianze dei coefficienti. Conserva anche l'effetto della maschera 632–646 nm. Il buon accordo con flussi ed errori pubblicati è una verifica numerica. L'identificatore della soluzione del modello resta distinto da quello delle soluzioni nel catalogo. Zero nuove esecuzioni native o chiusure scientifiche.

Per riprodurre con NumPy 2.3.5 e le dipendenze della catena ACS, passare nell'ordine protocollo, directory dei coefficienti continui, spettri campionati, directory del confronto ACS, protocollo ACS, ricevuta delle pose GD71, ricevuta delle pose GD153, capsula v571 ricostruita e nuovo percorso di uscita.
