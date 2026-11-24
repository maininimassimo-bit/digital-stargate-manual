# BKL-046 · Commit coordinato v601 su copie H: e J:

Il collaudo usa i cinque file della proposta ProcessInstance v601. Un processo separato scrive gli artefatti della replica su H: e usa un registro di prova su J:. Il journal fissa le impronte del padre, della proposta e dei quattro file su H:. La replica usa lo stesso blocco di un byte del test precedente. Il recupero acquisisce il blocco, confronta le impronte e decide se conservare v600 o riconoscere v601.

| Interruzione o anomalia | Esito |
| --- | --- |
| Copia incompleta del primo artefatto su H: | v600 conservato |
| Artefatti completi, puntatore ancora a v600 | v600 conservato |
| Puntatore scritto solo in parte | v600 ripristinato byte per byte |
| Puntatore v601 scritto, ricevuta assente | v601 riconosciuto dopo verifica di tutti i file e ricevuta ricostruita |
| Puntatore v601 scritto, delta alterato | Recupero respinto e nessuna ricevuta emessa. La replica resta preservata per l’analisi. |

Il test impedisce di attestare una copia danneggiata durante il recupero. La verifica del puntatore e la lettura da parte dei consumer di produzione restano da qualificare. La replica da H: ha prodotto lo stesso riscontro. Il registro autorevole su J: è stato riletto prima e dopo ed è rimasto v600. Il collaudo riguarda arresti di processi nella VM e lascia da verificare la contesa con il writer sul PC principale.

| Evidenza | SHA-256 |
| --- | --- |
| Programma | ca0506d444c42d4f04ec11ec1fc1a819486a0fe55f1aafd822ffa2854d07a754 |
| Riscontro replicato | 153f02ce7465b4513af9b6c15c9b89c400285d2a5ff639834a67c31dee7ceb5f |
