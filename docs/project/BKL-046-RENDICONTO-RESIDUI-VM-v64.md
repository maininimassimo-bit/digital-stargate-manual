# BKL-046 · Rendiconto residuo v64

Ho confrontato l'indice della PR #627 con il rendiconto v63 e verificato 17 note, ciascuna al commit di introduzione e alla punta `6848f30750bb738804bc539ed59338574655a78b`. Le copie con impronta verificata contengono 22 ricevute referenziate: 12 note per FILTER_COLOR/3, 4 per DIFFUSE_BACKGROUND/1 e 1 per DIFFUSE_BACKGROUND/2. Il confronto non ha cambiato gli stati ereditati.

| Perimetro | Verifica |
| --- | ---: |
| Requisiti nel tracciato e nell'indice TSV | 4.920 |
| Criteri letterali | 14.521 |
| Famiglie scientifiche aperte | 7 |
| Assi scientifici aperti | 25 |
| Criteri Owner da soddisfare | 19 |
| Chiusure scientifiche | 0 |

Le disposizioni dei requisiti restano 4.887 con completamento da provare, 26 con evidenza parziale, 1 con esclusione API motivata in attesa di attestazione e 6 con contratto documentale circoscritto in attesa di attestazione. Il rendiconto conserva la mappatura e i criteri dei 25 assi. Le evidenze fotometriche e sul fondo di questo incremento sono offline.

## Vincoli di chiusura

- **Stream34 v11.** Sul fascicolo VM associato all'impronta `0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1` i file di revisione attesi erano assenti. L'ultimo collaudo dell'ingresso usava chiavi di prova. Servono il pin di fiducia autenticato, ARB firmata e RQ firmata che riferisca quella ARB, poi deployment e iscrizione del peer verificabili e ammissione del coordinatore. La lettura del percorso di stato ha osservato `active.json` assente e zero processi PixInsight. Nessuna ammissione richiesta.
- **Conoscenza e GitHub.** La ricevuta terminale archiviata del publisher v571, conoscenza 1.146, riporta codice 0. Impronta della capsula locale `16276ed6372b09cec3f600cb0a0f77359b95c47c6367b42d98e0dd09d4d345fd`. La ricevuta di rilettura identifica il file di conoscenza e gli artefatti dipendenti. L'indice GitHub resta un riferimento ai metadati e la consegna integrale richiede ancora l'approvazione del perimetro di distribuzione, l'oggetto GitHub effettivo e la verifica indipendente di scaricamento e ricostruzione. Nessun publisher riavviato.
- **Studio scientifico.** Per FILTER_COLOR/3 restano la risposta ottica reale, un confronto cromatico indipendente e il controllo spaziale di PSF e fondo. Per DIFFUSE_BACKGROUND/1 serve un riferimento indipendente per fondo assoluto e contrasto diffuso. Per DIFFUSE_BACKGROUND/2 serve una prova calibrata che separi effetti additivi e moltiplicativi. I prerequisiti ereditati per gli altri assi restano nel rendiconto.

## Riproduzione

L'accesso diretto agli archivi precedenti su H: è rimasto in attesa. Per il confronto ho usato le copie di lavoro su O:, controllando le impronte degli ZIP, delle ricevute e delle note di GitHub. Il nuovo rendiconto è stato archiviato su H: con i dati necessari per una riproduzione offline.

- Rendiconto `rendiconto-VM-v64.json`, SHA-256 `2a6817384f7caf22ba85b6563c86a58eb832ba6195766a40ddeabfdae610cb86`.
- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-rendiconto-v64-2a6817384f7c.zip`.
