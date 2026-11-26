# BKL-046 · Direzione dello spostamento bilineare nel Roman H4RG

Ho riprodotto la prova delle due fasce esterne e mantenuto le stesse dieci coppie, gli stessi 32 canali e la stessa maschera di supporto. Ho confrontato cinque fasi, compresa l’identità, per 9.600 confronti complessivi. La fase di mezzo pixel sui due assi riproduce tutti i 1.920 valori di riferimento. A fase nulla i due modelli di propagazione coincidono. [Prova sulle tre fasce](../bkl046-roman-gain-spatial-band-covariance-v1/README.md)

Per uno spostamento di mezzo pixel su un solo asse, la mediana delle differenze appaiate fra errore in X e in Y è positiva in tutte e sei le combinazioni di fascia e lettura, da **0,89 a 2,36 punti percentuali**. Al livello più alto, nella fascia superiore, gli errori mediani con i pesi completi sono 11,8% in X e 10,6% in Y. I corrispondenti errori diagonali sono 41,2% e 40,4%. In ogni combinazione, il P05 della differenza appaiata è negativo e il P95 è positivo. Il verso della differenza varia fra i singoli casi.

Il modello con tutti i pesi ha errore mediano inferiore in ognuna delle 24 combinazioni di fascia, lettura e fase non nulla. Il confronto riguarda gli assi dei FITS e le stesse esposizioni Roman di laboratorio. Restano aperti il contributo causale della direzione di lettura, la dose calibrata e la prova nativa.

Usare Python 3.12 e NumPy 2.3.5. Passare a `misura.py` il protocollo, le directory estratte dei tre kit Roman delle fasce, della rampa e dei canali, la directory delle dipendenze e una nuova directory di uscita. Il dettaglio dei confronti è nel kit H/K.