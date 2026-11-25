# BKL-046 · Trasferibilità del fondo differenziale di IC 1805

Una prova istruita prima di rileggere i pixel usa 27 pose escluse dal primo confronto, appartenenti alla stessa sequenza. Sei ulteriori pose sono escluse dal limite sul P90 astrometrico. La prima, la mediana e l'ultima delle 27 pose ammissibili diventano riferimenti. Le altre 24 sono confrontate con ciascun riferimento. La griglia comune mantiene il 99,91% dei campioni e tutte le 192 celle.

| Indice riferimento | Coppie che superano il criterio in entrambe le partizioni | Coppie |
| ---: | ---: | ---: |
| 2 | 14 | 24 |
| 17 | 11 | 24 |
| 35 | 20 | 24 |

Il criterio richiede una riduzione di almeno il 10% dell'errore mediano assoluto sulle celle escluse dal fit e un P90 non superiore a quello dell'offset. Si scambiano le parità della scacchiera fra fit e verifica e si richiede il risultato in entrambe. Solo 6 pose bersaglio su 24 superano il criterio con tutti e tre i riferimenti. Il riferimento ha quindi un effetto operativo anche con dimensione del campione, supporto spaziale, modello e criterio fissati. Le 72 coppie condividono pose e sono misure ripetute di una sequenza.

Per la conoscenza BKL-046, il miglioramento rilevato con una posa di riferimento va riportato insieme alla sensibilità al riferimento. Un risultato favorevole con una sola ancora non basta a qualificare la correzione per nuovi dati. I valori sono residui relativi in ADU. Restano da verificare scala fotometrica, acquisizioni indipendenti, verità di fondo e prestazioni native. [Regole sul fondo diffuso](../bkl046-diffuse-background-knowledge-v1/README.md)

Per replicare, usare le stesse dipendenze e la stessa struttura degli argomenti dello studio differenziale. Il kit degli ingressi originali è l'archivio BKL046-IC1805-fondo-differenziale.zip, SHA-256 3224baae8a04403ac67ffde9565c9b883c4b562b57be2eae9644848d6ce78826. [Studio e dipendenze](../bkl046-ic1805-differential-background-v1/README.md)