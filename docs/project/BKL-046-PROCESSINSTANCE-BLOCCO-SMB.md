# BKL-046 · Contesa del blocco sullo storage SMB di J:

Su DSG-Shared due processi distinti hanno aperto un file di prova attraverso J: e il percorso UNC corrispondente. Identità, dimensione e contenuto confermano che i due percorsi portano allo stesso file. Il blocco copre il primo byte, come nel publisher storico.

| Titolare | Contendente | Esito durante il blocco | Esito dopo |
| --- | --- | --- | --- |
| J: | UNC | Secondo blocco respinto | Acquisito dopo rilascio esplicito |
| UNC | J: | Secondo blocco respinto | Acquisito dopo uscita del primo processo |

Il secondo byte è rimasto leggibile durante entrambe le contese. Il file di prova ha mantenuto gli stessi byte. La replica con il programma archiviato su H: ha prodotto una ricevuta identica. Il registro autorevole su J: ha mantenuto l’impronta v600 tra le riletture iniziale e finale.

La prova usa due processi nella stessa VM e un file separato sullo stesso storage del registro. Per qualificare la convivenza con un writer sul PC principale resta da osservare la contesa fra host e VM sullo stesso file di prova. Restano aperti il collaudo del commit coordinato e la pubblicazione canonica.

| Evidenza | SHA-256 |
| --- | --- |
| Programma | b21f8aa7144ff59d419668afe6fa19aa8587ff33069b3dd120d305c8fb14a478 |
| Riscontro riprodotto | f0059bda1ec17e8b7192cbfbb428e8b67988cdac08bbece36ee4c2012c07a1d7 |
