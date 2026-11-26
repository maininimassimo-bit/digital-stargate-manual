# BKL-046 · Copertura delle misure di colore GD153 con nucleo integro

Ho verificato se le lacune DQ proiettate sul nucleo dell'apertura permettono di escludere le terne con maggiori errori cromatici. Le regole sono fissate nel protocollo. Una terna supera il filtro geometrico soltanto se nessuna delle tre bande ha campioni mancanti entro 3 pixel dal centro. Il test aggiunge tetti da 0 a 10 campioni mancanti nell'apertura da 10 pixel per singola banda. La metrica è il massimo errore assoluto fra i tre colori della stessa terna.

| Copertura | Casi conservati su 28 | Somma parziale entro 10 mmag | Riscalatura per area entro 10 mmag | Mediana per anello entro 10 mmag | Peggior caso della mediana |
| --- | ---: | ---: | ---: | ---: | ---: |
| Pixel più vicino, tutti i casi | 28 | 25 | 24 | 26 | 26,82 mmag |
| Pixel più vicino, nucleo integro | 23 | 23 | 23 | 23 | 1,35 mmag |
| Quattro pixel, tutti i casi | 28 | 17 | 10 | 17 | 62,13 mmag |
| Quattro pixel, nucleo integro | 16 | 16 | 10 | 16 | 5,76 mmag |

Con quattro pixel di supporto, le due visite di riferimento conservano otto casi ciascuna. La mediana per anello rientra nei 5 mmag in 15 dei 16 casi. La somma parziale rientra nei 10 mmag per tutti i casi conservati, con un massimo di 8,60 mmag. Limitare a tre il numero di campioni mancanti per banda elimina tutti i casi con quattro pixel di supporto. La soglia di 10 mmag è descrittiva.

Il controllo usa quattro terne di una stella, da due visite, e maschere di sette visite. Gli stessi dati alimentano il confronto precedente sulle lacune cromatiche. Il risultato circoscrive il rischio sui campioni oscurati di questo controllo. Rimangono da verificare l'errore sulle pose realmente danneggiate, le dipendenze fra visite, il trasferimento ad altre stelle e la prova nativa. Zero chiusure scientifiche e zero avvii PixInsight.

Per ripetere, passare a `misura.py` il protocollo, gli archivi delle aperture integre, delle maschere e dello stress cromatico, poi un percorso di risultato nuovo. Il programma controlla le tre impronte degli ZIP, verifica i singoli membri, ricalcola gli errori di colore e li confronta con quelli archiviati prima di applicare il filtro. [Stress cromatico](../bkl046-gd153-heldout-dq-chromatic-stress-v1/README.md)