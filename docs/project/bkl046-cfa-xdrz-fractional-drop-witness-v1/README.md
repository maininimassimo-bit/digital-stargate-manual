# Controllo XDRZ della larghezza effettiva del deposito

Il controllo riusa i tre FITS CFA sintetici. Nel descrittore del secondo ingresso sostituisce la traslazione intera con una traslazione frazionaria di (1,30, −1,20) pixel. Le matrici restano traslazioni pure. Un calcolo separabile delle intersezioni del deposito e il calcolo poligonale concordano entro 3,34 × 10⁻¹⁵ nelle mappe accumulate.

Le mappe attese a 0,70 e 1,00 pixel presentano uno scarto massimo di almeno 0,133 per ogni confronto fra larghezze, anche confrontando scale diverse. Le sei coppie sintetiche FITS a 32 bit identificano univocamente larghezza e scala tra le ipotesi di peso grezzo, massimo globale e massimo per canale.

Il controllo frazionario serve a distinguere le larghezze osservando i prodotti. I cinque casi con traslazioni intere rimangono il riferimento per rigetto e campioni a zero. I nuovi ingressi e le mappe attese sono nel kit offline. La prova in PixInsight richiede un launcher che leghi parametri, console e FITS, con revisione e ammissione del coordinatore.

Per replicare eseguire `misura.py <protocollo.json> <kit-a-tre-ingressi> <codice-baseline.py> <pacchetti-Python> <directory-output-vuota>`.
