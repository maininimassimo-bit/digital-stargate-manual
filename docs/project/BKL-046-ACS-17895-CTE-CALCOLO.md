# ACS 17895 · Confronto delle correzioni CTE parallele FLT e DRZ

L'equazione 2 di ACS ISR 2022-06 è stata valutata localmente con logaritmi decimali e i coefficienti pubblicati dal ciclo 17 al 32 per aperture a 3 e 5 pixel. I coefficienti e gli errori standard sono estratti dalla pagina STScI archiviata. Un secondo calcolo con raggruppamento algebrico e aritmetica decimale verifica ogni risultato. Controlli aggiuntivi verificano perdita nulla a zero trasferimenti e proporzionalità a Y. Il confronto è una riproduzione locale dell'equazione. L'API non è stata utilizzata come oracolo. [ACS ISR 2022-06](https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/acs/documentation/instrument-science-reports-isrs/_documents/isr2206.pdf) · [Coefficienti aggiornati STScI](https://www.stsci.edu/hst/instrumentation/acs/performance/photometric-cte-corrections)

Il confronto copre le due visite in tre bande di WDFS0458-56 e WDFS0122-30. Per i 12 FLT validi a raggio 3 si calcola la correzione alla data, al flusso, al fondo e al numero di trasferimenti di ogni singola posa. La combinazione somma i conteggi corretti. Per i sei DRZ si usa il conteggio totale, il suo fondo e la media dei trasferimenti pesata per tempo. Il raggio 5 è valutato solo per DRZ perché i FLT hanno pixel mascherati in quell'apertura. [Prescrizioni del calcolatore DRZ](https://acsphotometriccte.stsci.edu/) · [Uso FLT descritto da ACSTOOLS](https://acstools.readthedocs.io/en/latest/acsphotcte.html)

| Perdita prevista a raggio 3 | Intervallo nelle sei coppie visita/filtro |
| --- | ---: |
| Correggendo i FLT separatamente | 41,41–59,96 mmag |
| Correggendo il DRZ combinato | 41,80–48,64 mmag |
| FLT separati meno DRZ combinato | −2,77 a +13,74 mmag |

Il massimo scarto sulle correzioni di colore è 14,09 mmag per F435W−F814W nella visita jfjv17. Lo scarto comprende anche differenze nelle stime di flusso e fondo tra i prodotti, oltre alla risposta non lineare del modello. I valori sono previsioni di perdita parallela con il modello pubblicato, senza CTE seriale, verifica su FLC/CRC, fattori di encircled energy o propagazione della covarianza dei coefficienti. Gli errori standard marginali non sono usati per costruire un intervallo di confidenza. Il confronto da solo non stabilisce quale stima riproduca meglio il flusso di riferimento. Zero avvii nativi e zero chiusure scientifiche.

Replay byte per byte con i tre archivi riletti da H:. SHA-256 riscontro `73787d84eaabb2fe59b645ed20716bd50fa4e8e4e629efb96030ea2c22e32321`. SHA-256 archivio `c3d7b79891c7286b0f91e7ee2dadcc0a3b8206e08cf63f84ee881fc2a4a23eb5`.

[Verifica dei FLT e del puntamento](BKL-046-ACS-17895-FLT.md) · [Provenienza e misure DRZ](BKL-046-ACS-17895-CTE-DRZ.md).
