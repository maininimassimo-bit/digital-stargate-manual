# BKL-046 · Trasferimento della maschera dai dati su M8/M20

Il controllo ripete le stesse iniezioni a 2 ADU. La maschera usa solo le mediane osservate nelle celle. Stima un piano sulle celle pari, esclude i residui sopra tre scale robuste e dilata le esclusioni di una cella. Prima e dopo l'iniezione ricalcola la maschera e verifica il supporto del fit. La forma iniettata entra solo nella valutazione finale. Una cella supera la soglia di contaminazione se contiene almeno il 2% del picco iniettato.

| Profilo | Celle contaminate mantenute, mediana | Perdita di flusso mediana con piano | Prove entro 5% su flusso e forma con piano o offset |
| --- | ---: | ---: | ---: |
| Filamento corto | 32 su 32 | 35,0% | 0/148 per ciascun modello |
| Filamento lungo | 32 su 32 | 46,6% | 0/148 per ciascun modello |
| Diffuso largo | 189 su 192 | 50,4% | 0/148 per ciascun modello |

La maschera procede in tutti i 148 scenari per ciascun profilo. Nei 27 controlli a scala unitaria, l'offset preserva un caso per ciascun filamento e il piano non ne preserva alcuno. Il profilo largo fallisce anche nei controlli. Il confronto a profilo noto aveva mostrato che i filamenti erano recuperabili su questa griglia con una maschera accurata e che il profilo largo richiedeva astensione per assenza di supporto pulito.

La soglia non è stata adattata dopo aver visto gli esiti. Lo studio riguarda un campo, una geometria e tre iniezioni digitali di contrasto prefissato, con riuso di pose e stime. Per una regola operativa rimangono da verificare una fonte indipendente per la maschera, un criterio di astensione applicabile ai dati e il comportamento in PixInsight.

Per replicare il programma riceve protocollo, kit della maschera a profilo noto, kit delle iniezioni, protocollo storico, kit di riferimento M8/M20, rapporto congiunto completo, dipendenze e nuova directory di uscita. [Controllo a profilo noto](../bkl046-m8-m20-scale-edges-known-profile-mask-v1/README.md)