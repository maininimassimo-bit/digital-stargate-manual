# BKL-046 · Ripetibilità dei dark nelle celle di riferimento M8/M20

Quattordici dark da 180 secondi della serie già verificata sono divisi in due gruppi intercalati da sette. La quindicesima acquisizione resta esclusa. Nelle sei celle più vicine alle coordinate del disegno distribuito si mediano i due verdi Bayer. Si misura la media o la mediana dei campioni che soddisfano il supporto congelato. Le statistiche per cella sono poi mediate sulle sette esposizioni di ciascun gruppo.

| Statistica per cella | Massima differenza fra gruppi | Diffuso largo, variazione del flusso | Diffuso largo, errore L2 |
| --- | ---: | ---: | ---: |
| Media | 0,0997 ADU | 4,23% | 7,34% |
| Mediana | 0,3571 ADU | 7,05% | 15,78% |

Le ultime due colonne propagano la differenza fra i gruppi attraverso un piano sulle sei posizioni, confrontato con il profilo sintetico largo da 2 ADU. Anche i due filamenti superano almeno una tolleranza con entrambe le statistiche. Per il profilo largo, il bilancio teorico a riferimenti distribuiti ammetteva 0,0418 ADU di errore per riferimento. La differenza osservata fra metà è un indicatore di ripetibilità. Non stima l'errore di una delle due metà, del master completo o di un riferimento ottico. Le celle sono posizioni del rivelatore vicine alle coordinate del modello.

Il kit conserva le statistiche, le impronte dei dark letti e l'acquisizione di calibrazione esatta su H:. Restano da verificare la precisione effettiva del fondo ottico indipendente, l'effetto delle altre condizioni di acquisizione e la prova nativa. Nessun master è stato scritto. [Bilancio teorico](../bkl046-m8-m20-background-anchor-error-budget-v1/README.md)