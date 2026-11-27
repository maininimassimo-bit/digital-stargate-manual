# BKL-046 · Riconciliazione dei riscontri storici sui diritti v1.146

La verifica parte dal JSON integrale della conoscenza v1.146 nella capsula ricostruita, dall'indice degli incorporati e dall'inventario storico dei diritti. Controlla le quattro impronte e ogni candidato d'archivio, compresi i membri interni dello ZIP GaiaXPy. Confronta la struttura JSON e i valori con precisione decimale, rifiutando chiavi duplicate e valori numerici non conformi. L'ordine degli elementi negli array è significativo.

Tutti e 20 i candidati corrispondono ai digest dichiarati nell'inventario. I 14 rapporti incorporati corrispondono ai valori JSON restaurati. Nessuno ha la stessa serializzazione del file sorgente. Per ciascuna corrispondenza persistono quindi due digest distinti per la sorgente e per il valore incorporato. Tutte le voci dell'inventario conservano lo stato NOT_YET_QUALIFIED. L'equivalenza accertata consente di usare le stesse voci per la revisione dei contenuti, che resta aperta.

Per riprodurre con Python 3.12 passare lo ZIP v571 ricostruito, l'indice dei contenuti incorporati, l'inventario storico dei diritti e un nuovo percorso per il riscontro. I digest sono fissati nel verificatore. La ricevuta contiene solo ordinali, impronte, conteggi e stati. Nessun contenuto degli archivi sorgente è incluso nella ricevuta.
