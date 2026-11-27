# BKL-046 · Stabilità dell'impronta full well in due pose ACS

Il controllo usa i 63 centri comuni del sensore 2 nelle due pose GO14949 F606W da 400 s. Verifica il digest dei FITS e dei rapporti originali, poi rilegge soltanto il piano DQ. Il bit 256 indica full well e viene valutato separatamente dal bit 2048 dell'ADC. [Definizione dei flag DQ di ACS](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/dq-flag-definitions)

| Sorgente | Pixel full well in comune / unione nel raggio di 3 px | Stato sui centri originali, raggio 5 px | Stato sui centri originali, raggio 7 px |
| --- | ---: | --- | --- |
| 2 | 4 / 5 | Flag misti in entrambe | Flag misti in entrambe |
| 10 | 3 / 3 | Flag misti in entrambe | Flag misti in entrambe |
| 11 | 1 / 1 | Solo full well in entrambe | Flag misti in entrambe |

Al raggio originale di 3 pixel la sorgente 2 passa a flag misti in una delle nove perturbazioni di ±0,25 pixel del centro in ciascuna posa. Le altre due mantengono la classificazione a quel raggio. Le perturbazioni sono controlli di sensibilità e non stimano la distribuzione dell'errore di registrazione.

L'impronta full well è ripetibile nei tre casi preliminari. La purezza del supporto dipende dal raggio e può cambiare se cambia il pixel centrale. Resta valido il criterio di prequalifica geometrica dei protocolli precedenti, che aveva ammesso zero casi. Questa prova non legge i valori scientifici per la fotometria e non ricostruisce flussi.

Per il replay passare a `misura.py` il protocollo, le due directory dei rapporti originali, le due pose congelate, Astropy 7.2.0 con NumPy 2.3.5 e un nuovo percorso di uscita.
