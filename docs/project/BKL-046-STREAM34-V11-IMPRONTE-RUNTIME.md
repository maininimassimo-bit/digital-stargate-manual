# BKL-046 — Rilettura statica del runtime Stream34 v11

Su DSG-Shared ho riletto il soggetto `0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1` e verificato i 64 membri. Ho compilato senza eseguire i corpi dei moduli 44 sorgenti Python e 16 moduli CommonJS. Gli import letterali rilevati fanno riferimento al pacchetto o alla libreria standard del rispettivo runtime. Il controllo Node ha registrato tre invocazioni di require con argomento non letterale nei moduli di ingresso, nel caricatore verificato e nell'adattatore del coordinatore. La compilazione statica non esercita questi percorsi durante un avvio.

| Componente | Riscontro |
| --- | --- |
| Python 3.12.14, eseguibile PixInsight e due header PJSR | Corrispondenza con le quattro impronte già fissate dal launcher |
| Coordinatore comune R4 | Sei file canonici coincidenti con le impronte del pacchetto |
| Ricevuta terminale publisher v571 | Impronta coincidente con quella fissata |
| Node v24.22.3 x64 | SHA-256 osservato `66e43517e90be6151a17e2e739f001501a582214938477886281dd31113ffe54` |

Il controllo ha registrato l'impronta Node del runtime utilizzato. Nessuna approvazione separata di tale impronta è stata verificata in questo controllo. La lettura della ricevuta v571 attesta i byte conservati, nel perimetro della ricevuta. Il controllo non ha avviato PixInsight, coinvolto il supervisore interattivo o richiesto l'ammissione. Le revisioni autentiche del pacchetto, il deployment, la continuità della sessione e la prova nativa restano da verificare.

La copia su H: di `BKL046-Stream34-impronte-runtime-v11.zip` ha SHA-256 `27314195c244ffeee7463232f360497d6243f24b13a3d45490adbfd921128d72`. La riesecuzione dei programmi estratti ha riprodotto entrambi i riscontri byte per byte. SHA-256 del riscontro completo `657104bb0fa6ba47cd828e3142cad21f013644c85adf791470c584c1019845af`.
