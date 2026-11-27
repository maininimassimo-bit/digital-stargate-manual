# BKL-046 · Ricostruzione di valori tagliati artificialmente su TV4

Il controllo rilegge gli stessi modelli congelati del test di estrapolazione. Conserva le regioni trattenute prive di valori realmente al limite digitale. Applica un taglio artificiale al 70%, 75% o 80% della soglia, quindi sostituisce soltanto i pixel marcati dal taglio con la previsione, limitata inferiormente dalla soglia applicata. I pixel esterni alla maschera restano identici. L'immagine originale conserva i valori con cui misurare l'errore.

| Taglio artificiale nelle sei pose centrali non sature | Pixel effettivamente cambiati | Riduzione dell'errore assoluto, modello dopo riallineamento con overscan | Riduzione dell'errore assoluto, modello prima del riallineamento con overscan |
| --- | ---: | ---: | ---: |
| 70% | 388.177 | 97,62% | 96,78% |
| 75% | 292.880 | 94,91% | 93,32% |
| 80% | 68.207 | 91,04% | 86,51% |

Il confronto di riferimento lascia intatti i valori tagliati. A ogni soglia, entrambi i modelli riducono l'errore assoluto in tutte e sei le pose. L'errore residuo della somma cambia segno fra le due calibrazioni. Questo limite resta importante quando si usa la previsione come misura integrata.

Il taglio è digitale e artificiale. I risultati hanno un riferimento osservato ma non includono la risposta fisica oltre il limite del rivelatore, il blooming o l'errore di una maschera prevista. Le regioni realmente censurate sono escluse e riportate nel conteggio. Nessuna soglia è stata scelta e nessuna chiusura scientifica è stata dichiarata. [Studio delle soglie della maschera](../bkl046-tv4-maschera-saturazione-soglie-v1/README.md)

Per riprodurre i risultati passare a `misura.py` il protocollo congelato, la directory della previsione TV4 con i FITS originali e una nuova directory di uscita.
