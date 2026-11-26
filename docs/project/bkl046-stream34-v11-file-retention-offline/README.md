# BKL-046 · Stream34 v11, lettura e ritenzione su Node

Il collaudo esegue due membri JavaScript del soggetto v11 già congelato, dopo averne verificato le impronte. Node usa sostituti di `File`, `CryptographicHash` e `ImageWindow`. Viene omessa la direttiva `#include` del preprocessore PJSR. Le operazioni di lettura usano gli otto input originali in sola lettura. L'impronta di ogni file coincide con il piano.

- **Caso completo.** 139.469.422 byte, 139 letture, richiesta massima di 1 MiB e otto chiusure. La seconda invocazione sullo stesso stato viene respinta.
- **13 guasti simulati.** Errori di apertura, posizione, dimensione, lettura, hash e chiusura. Il codice conserva l'oggetto originale con la fase raggiunta e rifiuta una seconda lettura con lo stesso contenitore. Una chiusura che solleva un errore dopo aver chiuso il file nella fixture resta incerta per il chiamante.
- **Cinque piani non ammessi.** Record duplicato, percorso alterato, totale incoerente, immagine già aperta e tipo dati inatteso. Nessuna allocazione di `File` in questi casi.

Per replicare, estrarre `candidata-v11.zip` dal fascicolo fissato nel protocollo, quindi estrarre la candidata in una directory di prova con gli otto ingressi disponibili nei percorsi del piano. Eseguire `node collaudo.cjs <candidata-estratta> protocollo.json riscontro-replica.json`.

Restano da osservare in PixInsight le semantiche effettive di lettura, hash, chiusura e uso della memoria. Il rapporto termina al corpo JavaScript. L'uscita del processo, il rilascio della prenotazione e la validazione scientifica richiedono le rispettive evidenze. Nessuna richiesta di ammissione.
