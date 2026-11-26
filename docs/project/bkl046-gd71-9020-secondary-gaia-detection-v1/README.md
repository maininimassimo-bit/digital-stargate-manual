# BKL-046 · Riferimento Gaia secondario per GD71 nel programma 9020

L'integrazione 5×5 individua un candidato brillante ripetuto nelle otto pose che il controllo astrometrico originale aveva escluso. I suoi centri differiscono al massimo di 2,24 pixel nella visita j8c103 e di 0,92 pixel in j8c104. Le coordinate del candidato nel WCS originale distano circa 2,9–3,8 secondi d'arco dalla posizione Gaia di GD71 all'epoca.

Nel WCS originale il cono Gaia archiviato non fornisce altri riferimenti nelle immagini. Applicando una traslazione ricavata dal candidato GD71 si proietta un secondo riferimento Gaia, di magnitudine G 20,29, vicino al bordo delle otto pose. La fotometria forzata in quella posizione supera la soglia diagnostica in entrambe le pose F660N di j8c103 e in entrambe le pose di ciascuna banda di j8c104. Il rapporto segnale/rumore diagnostico va da 12,8 a 15,1. Le due F658N di j8c103 restano escluse dal controllo per supporto DQ o cielo.

La posizione provata dipende dal candidato brillante. La rilevazione ripetuta sostiene l'ipotesi di traslazione. Restano da misurare il centro del riferimento secondario senza usare il candidato brillante e l'errore astrometrico fuori campione. Le otto esclusioni precedenti conservano il proprio stato. Nessun rapporto fotometrico 9020 è promosso. [Servizio Gaia ARI](https://gaia.ari.uni-heidelberg.de/) · [Registri di puntamento HST](https://hst-docs.stsci.edu/hstdhb/5-observation-logs/5-1-observation-log-files)

Per ripetere usare i FITS e la ricevuta GD71-9020, la ricevuta delle esclusioni, il CSV Gaia del cono archiviato e le dipendenze ACS. Il primo verificatore produce riscontro.json. Il secondo rilegge quel risultato e controlla il riferimento debole con la posizione fissata dal protocollo.
