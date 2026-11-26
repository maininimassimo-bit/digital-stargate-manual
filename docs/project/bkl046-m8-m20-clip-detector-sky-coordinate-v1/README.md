# BKL-046 · Clipping M8/M20 alle coordinate del sensore e del cielo

Nelle 105 coppie di pose da 180 secondi, a un raggio di 1,5 pixel la percentuale di siti CFA al limite che hanno un vicino della stessa parità passa dal 46,32% alle coordinate del sensore all'85,77–85,79% dopo le due proiezioni al cielo. Entrambe le proiezioni migliorano il conteggio di 100 coppie su 105. Nelle altre cinque il totale resta uguale.

| Raggio in pixel nativi | Sensore | Affine su anteprima a metà scala | Affine su mosaico CFA |
| ---: | ---: | ---: | ---: |
| 1 | 46,32% | 56,95% | 57,30% |
| 1,5 | 46,32% | 85,77% | 85,79% |
| 2 | 79,57% | 93,45% | 93,46% |

Il denominatore è 831.404 confronti direzionali, uguale fra i tre modelli. Ogni sito può essere contato in più coppie e un vicino può servire più siti. La selezione esclude le 15 occorrenze del fotosito rosso al limite anche nei dark e 299 occorrenze presso i bordi. Le posizioni sono filtrate allo stesso modo per tutti i modelli. La distanza fra fotositi della stessa parità sulla griglia del sensore è almeno due pixel, quindi a 1 e 1,5 pixel il conteggio sul sensore è identico. A 1 pixel, le affini peggiorano il totale in 36 e 35 coppie rispettivamente. A 2 pixel lo peggiorano in 19 e 18.

Il controllo usa le inverse di due stime affini congelate e verifica i punti di controllo per posa. La maggiore coincidenza aggregata dopo proiezione è coerente con una parte del clipping che segue il campo osservato. Le due stime riusano le stesse pose e la stessa regione di cielo. Il confronto rimane sensibile alla fase del reticolo, alla forma delle zone saturate e alla precisione geometrica. Non attribuisce la causa di singoli campioni, non misura la carica fisica e non verifica il recupero fotometrico.

Per ripetere, passare a `misura.py` protocollo, ZIP delle pose, ricevuta delle pose, ZIP dei dark, ricevuta dei calibratori, rapporto sulla geometria affine, rapporto sull'incrocio con i dark, directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo percorso di uscita. Gli ingressi sono bloccati per SHA-256. Zero avvii PixInsight e zero chiusure scientifiche.
