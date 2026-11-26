# BKL-046 · Gaia XP, CALSPEC e rapporti ACS su GD71 e GD153

La catena ACS WFC1 viene ricostruita all'MJD di ciascuna delle dodici pose e verificata con PHOTFLAM. Le quadrature a quattro e otto nodi concordano. I rapporti osservati a tre pixel e le stime CALSPEC sulla griglia originale riproducono i risultati storici. Il confronto aggiunge Gaia XP e una stima CALSPEC ricampionata sulla stessa griglia. Il ricampionamento controlla gli effetti della griglia e della copertura. Non riproduce la risoluzione strumentale Gaia.

| Sorgente | F658N/F660N Gaia XP | CALSPEC su griglia Gaia | ACS a 3 px |
| --- | ---: | ---: | ---: |
| GD71 | 2,638386 | 2,537336 | 2,537887 |
| GD153 | 2,644750 | 2,562550 | 2,551130 |

Il rapporto Gaia è superiore a CALSPEC sulla stessa griglia del 3,98% e del 3,21%, rispettivamente. Le misure ACS sono inferiori al rapporto Gaia del 3,81% e del 3,54%. L'esclusione 632–646 nm abbassa il rapporto stretto Gaia dello 0,042% circa e alza F658N/F606W del 5,92–5,94%. La rimozione del modo negativo dal fascicolo precedente e l'accordo fotometrico sono quindi controlli distinti.

ACS e Gaia usano strumenti diversi. La misura ACS è ad apertura finita, la sintesi ad apertura infinita, e CALSPEC contribuisce alla calibrazione ACS. Il confronto conserva tali dipendenze, la copertura delle bande, il limite della risoluzione Gaia e l'assenza della covarianza completa. GRW+70 5824 resta nella raccolta Gaia XP, fuori dal confronto a tre bande con dodici pose fissato qui. Nessuna accettazione fotometrica assoluta o chiusura scientifica.

Per ripetere con Python e NumPy 2.3.5 e le dipendenze ACS archiviate, passare protocollo, spettri Gaia estratti, protocollo ACS, ricevuta delle pose, confronto storico e FITS CALSPEC di GD71, gli stessi tre ingressi per GD153 e un nuovo percorso per il risultato.
