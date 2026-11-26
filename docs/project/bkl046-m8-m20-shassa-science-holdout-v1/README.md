# BKL-046 · Celle SHASSA su pose scientifiche M8/M20

Le tre disposizioni fissate a 4 arcmin stimano offset e piano sulle sei celle assegnate. La verifica usa 177 celle comuni, tutte esterne all'unione delle 15 celle di stima. Il test usa 27 differenze a scala unitaria fra pose registrate, con tre riferimenti e nove bersagli riutilizzati. Una coppia supera il criterio quando il piano riduce la mediana assoluta di almeno il 10% rispetto all'offset senza aumentare il P90.

| Disposizione | Piano favorevole rispetto al proprio offset | Mediana dei residui mediani del piano, ADU | Mediana dei P90 del piano, ADU | L2 mediano sul diffuso iniettato |
| --- | ---: | ---: | ---: | ---: |
| Originale | 7/27 | 0,814 | 1,976 | 22,4% |
| Sei celle con Hα minima | 6/27 | 1,094 | 2,599 | 71,2% |
| Una cella con Hα minima per settore | 8/27 | 0,810 | 1,948 | 59,6% |

La disposizione per settore ha residui del piano non superiori all'originale su entrambi gli indicatori in 18 confronti. Dopo l'iniezione del profilo diffuso da 2 ADU nella posa bersaglio registrata, tutti i modelli in tutte le disposizioni superano almeno una delle due tolleranze di errore del 5%. I due filamenti sintetici passano tutti i confronti con i centri e le larghezze fissati. Il test non generalizza a filamenti spostati, confronti indipendenti o una misura ottica coeva.

La selezione per settore è quindi utile come confronto diagnostico. I risultati sui residui e sulla conservazione del segnale diffuso danno indicazioni diverse e non qualificano la disposizione per la messa in produzione. Zero avvii PixInsight e zero chiusure scientifiche. [Misure su dark nelle stesse celle](../bkl046-m8-m20-shassa-dark-layout-repeatability-v1/README.md)

Per replicare, usare Python 3.12, NumPy 2.3.5 e Astropy 7.2.0. Passare il protocollo, il rapporto che fissa le disposizioni, la directory del protocollo di iniezione, la directory del fondo di riferimento con gli ingressi estratti, il rapporto completo scala e bordi, la directory delle dipendenze e una directory di uscita esistente e vuota. Le impronte dei quattro archivi sorgente sono in `fonti.json`.
