# BKL-046 · Contaminazione dei riferimenti TV4 a bordo campo

Il test usa due contrasti TV4 riservati alla verifica. Inietta un disturbo digitale di 2 o 8 DN soltanto in una o entrambe le strisce disgiunte che stimano la correzione. Il disturbo occupa 16 pixel lungo la direzione corretta e 8 o 64 pixel dei 256 disponibili nella direzione trasversale. Queste iniezioni sono collocate al bordo oppure al centro della regione, sia per righe sia per colonne. Il dato grezzo della regione bersaglio resta identico.

La misura è il massimo scarto indotto nel bersaglio, diviso per il picco iniettato nella striscia. Il 5% è un riferimento diagnostico di questa prova.

| Operatore | Casi entro il 5%, 8 pixel | Casi entro il 5%, 64 pixel | Massimo scarto, 64 pixel |
| --- | ---: | ---: | ---: |
| Grezzo | 160/160 | 160/160 | 0,0% |
| Media | 160/160 | 0/160 | 23,4% |
| Media troncata al 20% per coda | 160/160 | 0/160 | 22,5% |
| Mediana | 143/160 | 48/160 | 34,8% |

Con la contaminazione estesa, la mediana resta entro il 5% in 22 casi al bordo e 26 al centro, su 80 ciascuno. Il caso estremo raggiunge circa il 35% anche con la mediana. Il grezzo è un controllo di identità. Lo scarto integrato sull’intera regione resta nullo entro la tolleranza del test anche in presenza di alterazioni locali.

La prova conserva tutti i 1.280 esiti. Usa perturbazioni digitali e due contrasti della stessa acquisizione. Il confronto riguarda queste geometrie e questi estimatori. Rimangono aperte la risposta a sorgenti reali, la propagazione delle incertezze e la verifica nativa per DIFFUSE_BACKGROUND/3.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 21d001b2c83662c0aa238be05d31e247e36fb3501a37df49b55bfbabc73821 |
| Programma | 85b3c150cc3baf7b1cdd657302192ace522834aef1173236512456263fcc4ea6 |
| Riscontro replicato da H: | e4aadfededaacaa7cafa1b442b03d1d8cf35b0b308271f375092223b75b4fcf6 |
