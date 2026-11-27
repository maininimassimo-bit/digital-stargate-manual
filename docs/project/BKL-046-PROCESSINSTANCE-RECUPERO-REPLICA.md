# BKL-046 · Blocco e recupero della replica ProcessInstance v601

Il collaudo su DSG-Shared usa una replica isolata su O: del registro v600 e la proposta v601 già archiviata. Due processi distinti si contendono lo stesso intervallo di un byte impiegato dal publisher storico. Il secondo processo viene respinto finché il primo detiene il blocco. Il file torna acquisibile dopo il rilascio e conserva l’impronta del padre.

| Interruzione del processo di prova | Stato trovato | Esito del recupero |
| --- | --- | --- |
| Prima del journal di intento | Padre integro | Padre conservato |
| Dopo il journal, prima della scrittura | Padre integro | Padre conservato |
| Dopo 4.096 byte della proposta | Prefisso della proposta e coda del padre | Ripristino dei byte del padre |
| Dopo scrittura completa, prima della ricevuta | Proposta integra | Proposta conservata e ricevuta emessa |

Una seconda esecuzione del recupero produce la stessa ricevuta. Un caso con byte estranei a entrambe le versioni è stato respinto e conservato senza alterazioni. La replica lanciata dal programma archiviato su H: produce un riscontro identico. La rilettura del registro autorevole su J: conferma ancora v600.

La verifica riguarda lo specifico schema di scrittura interrotta riprodotto su O:. Restano da verificare sul percorso di pubblicazione la contesa SMB fra tutti i writer e l’integrazione del journal con il commit di registro, matrice e manifest. La prova non simula un arresto del server SMB o una perdita di alimentazione.

| Evidenza | SHA-256 |
| --- | --- |
| Programma | 8e78cf73c21cd092842f778318cdf6c6e7769ac204fb9268923babbb834d3b22 |
| Riscontro replicato | 4f3b17bcb63c3667e839f56e8091e35a0253e7ea105ad1adf2210063600afd8f |
