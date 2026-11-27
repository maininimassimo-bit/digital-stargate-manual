# BKL-046 — Rilettura delle versioni storiche dai contenitori locali

L'indice di consegna riportava già la rilettura locale di 181 versioni da v0.1 a v1.171. Ho verificato un secondo percorso di recupero per 45 versioni, prendendo le copie dagli ZIP locali del corpus v600. Per ogni versione il controllo lega alias, dimensione e SHA-256 al piano, verifica la ricevuta e il contenitore e ricalcola l'impronta del membro decompresso in streaming. Sono stati riletti 63.599.156.359 byte utili senza materializzare i JSON.

Due ricevute di prima generazione non contengono il campo relativo al piano. Il primo passaggio le ha respinte. Nel secondo passaggio sono state accettate solo dopo la verifica dell'impronta della ricevuta, della corrispondenza ad alias e job dell'indice e dei byte del contenitore e del membro. I due esiti iniziali rimangono nell'archivio.

Il nuovo inventario coincide con la riconciliazione precedente per versione, nome, dimensione e SHA-256 di tutti i 181 file. Le quattro versioni senza ricevuta diretta, v0.1, v0.9, v1.0 e v1.2, conservano l'attestazione tramite il riferimento nella versione successiva.

| Evidenza | Esito |
| --- | ---: |
| Versioni storiche con byte coerenti con impronta registrata | 177 |
| Di cui rilette nuovamente dai contenitori locali | 45 |
| Versioni con riferimento successivo e ricevuta diretta assente | 4 |
| Asset GitHub verificati | 0 |

Il criterio di recupero dello storico ha ora un riscontro aggiuntivo sui contenitori locali. La consegna GitHub richiede ancora l'autorizzazione di distribuzione, gli oggetti remoti e la rilettura effettiva. L'archivio su H: ha riprodotto la riconciliazione dei riscontri. La lettura dei 63,6 GB è stata eseguita sulle copie dei contenitori su O:.

| Evidenza | SHA-256 |
| --- | --- |
| Inventario riconciliato | `e2b5b0abfbe9ab57537a8ffeba91d7614917f7e7a49f3a6679f41a926d0d7e10` |
| Archivio `BKL046-storia-rilettura-carrier-v1.zip` | `1fea5288391b21245f6bdac7cd88a830467fdbc97ba8aa7af0016eced4b5fe41` |
