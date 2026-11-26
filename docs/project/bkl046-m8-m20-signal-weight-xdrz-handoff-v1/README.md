# Ingressi e oracolo offline XDRZ per la pesatura M8–M20

Il pacchetto BKL-046 lega la regione diagnostica 14-1-0 alle matrici ricavate dalla baseline a scala comune. Le matrici dirette dal riferimento al rivelatore sono trasferite nelle coordinate del ritaglio 48 × 48 a origine pari, conservando la fase RGGB. Il rapporto verifica che i 28 FITS CFA e i 28 RGB ausiliari siano identici ai corrispondenti file del pacchetto precedente.

I 336 descrittori formano 24 selezioni complete da 14 pose. Le selezioni distinguono calibrazioni A e B, geometria unitaria e pesata, origine 0 o 0,5 e rigetto assente, nel rivelatore o nel riferimento. Il programma rilegge le matrici, le maschere e i collegamenti XML. Gli RGB ausiliari sono immagini costanti e richiedono conferma dell’uso effettivo della sorgente CFA.

L’oracolo comprende intensità, pesi e supporto RGB per matrici e depositi, con i controlli offline per il rigetto e per i campioni azzerati a peso conservato. Sulla regione verificata, il massimo scarto numerico dei flussi dalla baseline a scala comune è 2,71 × 10⁻⁸ ADU. L’oracolo e il manifest sono legati dalla stessa impronta.

Il pacchetto riguarda un ritaglio diagnostico. Prima dell’uso nativo servono la ricevuta del controllo sintetico, un comparatore vincolato a questi due archivi, le revisioni sul nuovo soggetto e l’ammissione del coordinatore. I descrittori sono conservati nello ZIP. Nessun input è stato estratto nella directory di avvio.

Per replicare eseguire `prepara.py <protocollo.json> <riscontro-scala-comune.json> <studio-oracolo-precedente> <studio-ingressi-precedente> <directory-output-vuota>`.
