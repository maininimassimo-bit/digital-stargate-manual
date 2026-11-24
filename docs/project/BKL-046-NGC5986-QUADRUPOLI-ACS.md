# BKL‑046 · Ripetibilità dei quadrupoli ACS/WFC in NGC 5986

Il confronto usa due esposizioni F606W da 350 s del programma HST 10775. Misura quadrupoli pesati negli stessi 117 abbinamenti stellari, con centri predetti in precedenza da esposizioni di riferimento separate. Le estensioni SCI, ERR e DQ sono quelle dei prodotti ACS/WFC `flc.fits`. La proiezione locale usa il WCS alternativo A in FK5 J2000. [Struttura dei file ACS](https://hst-docs.stsci.edu/acsdhb/chapter-2-acs-data-structure/2-2-acs-file-structure) · [Prova di trasferimento della fase](BKL-046-PSF-PIXEL-2-CONOSCENZA.md)

| Chip fisico | Associazioni | Coppie di momenti valide | Coppie con angolo proiettato definito | Entro 5° fra gli angoli proiettati definiti |
| --- | ---: | ---: | ---: | ---: |
| 1 | 49 | 7 | 6 | 4 |
| 2 | 68 | 3 | 3 | 2 |
| Totale | 117 | 10 | 9 | 6 |

Il filtro esclude una misura se almeno un pixel del riquadro centrale 9 × 9 ha un flag DQ. I flag DQ sono l’unica causa di esclusione osservata. Su 234 misure, 178 vengono escluse. Per 71 stelle il filtro esclude entrambe le esposizioni, per 36 ne esclude una. Tra le nove coppie con angolo proiettato definito, il P90 della differenza è 9,55°. Sul rivelatore sette coppie sono definite e tutte e sette rientrano in 5°. La proiezione e le soglie di disponibilità cambiano il campione, quindi i due conteggi non misurano lo stesso denominatore.

Il rapporto conserva stato, fase, chip e risultati per tutti i 117 abbinamenti. L’incertezza propagata da ERR assume pixel indipendenti e tiene fissi centro e fondo. Questo è un confronto della forma osservata in due esposizioni, con copertura fortemente selezionata dal filtro. Rimangono aperte la prova su più campi, una caratterizzazione dei flag per i quadrupoli e la misura nativa. L’asse `PSF_PIXEL/2` resta aperto.

SHA‑256 della ricevuta `27bf61b5c65b48175dcaa2e4b90b796b8f587d29cebd7f0b2d057863d286a597`.
