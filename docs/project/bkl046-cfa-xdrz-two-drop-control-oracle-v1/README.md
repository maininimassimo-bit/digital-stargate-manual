# Riferimento sintetico XDRZ per depositi da 0,70 e 1,00 pixel

Il controllo ricostruisce le mappe attese dei cinque casi CFA a tre ingressi a partire dai FITS e dalle traslazioni intere XDRZ congelate. Usa l’intersezione del deposito quadrato con ciascun pixel e assegna il canale a partire dalla parità RGGB del sensore. Verifica i modelli di rigetto nel rivelatore e nel riferimento e il comportamento dei campioni con valore zero.

Il calcolo riproduce le predizioni archiviate del controllo da 0,70 pixel. Con queste traslazioni intere, la sovrapposizione normalizzata non cambia passando a 1,00 pixel. Le mappe previste alle due larghezze coincidono. Per ciascuna larghezza, i cinque controlli distinguono le due ipotesi di coordinate di rigetto, i due comportamenti a valore zero e le tre scale dei pesi. Le combinazioni verificate offline sono 24.

Il confronto dimostra che il disegno sintetico può distinguere le convenzioni anche con il deposito da 1,00 pixel. Per attribuire l’esito a PixInsight servono un batch che verifichi il parametro effettivamente applicato, le revisioni sul soggetto esatto e l’ammissione. Il controllo nativo v6 resta fissato a 0,70 pixel.

Per replicare eseguire `misura.py <protocollo.json> <kit-a-tre-ingressi> <classificatore-v6.py> <pacchetti-Python> <directory-output-vuota>`.
