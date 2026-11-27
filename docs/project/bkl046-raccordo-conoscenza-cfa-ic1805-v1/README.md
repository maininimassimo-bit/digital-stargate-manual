# IC 1805 nel file di conoscenza BKL‑046

L’asse CFA_DITHER_DRIZZLE/3 richiede evidenze su buchi di copertura, pesi variabili e propagazione dei pixel mancanti. Le prove IC 1805 misurano la copertura geometrica e la sensibilità alla perdita di pose sulla stessa coorte di 72 stelle e 38 pose. Le due metà intercalate condividono campo e acquisizione.

| Deposito | Stelle con due contributi positivi | Stelle con numero effettivo almeno due | Stelle che conservano il numero effettivo dopo ogni rimozione locale | Pose che fanno scendere almeno una stella sotto soglia |
| --- | ---: | ---: | ---: | ---: |
| 1,00 px | 72/72 | 71/72 | 69/72 | 2/38 |
| 0,70 px | 71/72 | 66/72 | 59/72 | 13/38 |

Per documentare la robustezza, riportare insieme celle vuote, conteggi positivi, numero effettivo e transizioni in entrambe le direzioni. Una perdita può ridurre la copertura di alcune stelle anche quando il totale delle stelle sopra soglia sale. Nel caso da 0,70 px una posa lascia una cella vuota. Le variazioni tra stelle dipendono dalla stessa posa e vanno analizzate a livello di posa o campo quando si stima l’incertezza.

Due contributi effettivi è una soglia diagnostica. Per chiudere l’asse restano la misura riproducibile dei pesi effettivi dell’operatore nativo, la propagazione di pixel mancanti e maschere a parità di ingresso, e controlli indipendenti con incertezza predefinita. I limiti nominali IC 1805 non forniscono tolleranze universali. `conoscenza.json` lega le tre evidenze alla baseline v1.171 e conserva l’asse aperto.
