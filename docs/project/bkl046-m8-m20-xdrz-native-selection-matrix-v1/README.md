# Selezioni candidate per la prova XDRZ M8–M20

Ricevute le convenzioni native, la prova diagnostica BKL-046 richiede otto configurazioni. Incrocia due geometrie, due calibrazioni e depositi da 1,00 e 0,70 pixel. Restano candidate quattro coppie possibili di origine e coordinate di rigetto. L’inventario fissa le 14 impronte dei descrittori per ognuna delle 32 selezioni. Nessuna convenzione è stata scelta.

Sul ritaglio reale, 8 dei 112 confronti fra piani di rigetto nelle coordinate del rivelatore e del riferimento hanno byte identici. Negli altri variano al massimo quattro campioni di maschera. Il cambio di serializzazione fra origine 0 e 0,5 incide sui termini di traslazione delle matrici da 0,000016 a 0,000194 pixel. Questa differenza è fra descrittori offline. Il comportamento del lettore rimane da verificare sul controllo asimmetrico dell’origine.

Il controllo dell’origine usa il soggetto fattoriale v3. Il batch fissato dal soggetto v6 per rigetto e mappe dei pesi usa solo il deposito da 0,70 pixel. La configurazione da 1,00 pixel richiede evidenza propria prima di estendere a entrambe le larghezze l’esito del controllo. Restano indispensabili le ricevute native autentiche, le revisioni del launcher scientifico e l’ammissione del coordinatore.

Per replicare eseguire `verifica.py <protocollo.json> <ingressi.zip> <soggetto-origine> <soggetto-pesi> <riscontro-classificatore.json> <oracolo-pieno.zip> <nuovo-riscontro.json>`.
