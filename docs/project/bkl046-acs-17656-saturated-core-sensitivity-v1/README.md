# BKL-046 · Sensibilità dell'unico nucleo saturo misurabile nella visita ACS 17656/02

Ho ripreso l'unica sorgente ammessa nella posa da 150 s jfdp02vfq. L'analisi perturba il centro della sola posa lunga di ±1 px lungo entrambi gli assi e applica tre anelli per il fondo. Il confronto usa supporto comune nelle tre immagini. Il protocollo richiede tutti gli 11 pixel DQ 256 della componente nell'apertura e almeno il 97% di supporto comune. [Misura originaria e criteri di preselezione](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/83da4269ab90b9c66632d932c523339e1b253405/docs/project/bkl046-acs-17656-gain2-saturation-trails-v1)

| Raggio | Combinazioni utilizzabili | Minimo e massimo dello scarto lungo / breve |
| --- | ---: | ---: |
| 5 px | 27/27 | −1,73% – +3,55% |
| 8 px | 27/27 | +2,28% – +3,41% |
| 10 px | 27/27 | +2,74% – +3,24% |
| 12 px | 27/27 | +2,84% – +3,13% |
| 15 px | 9/27 | +2,77% – +2,97% |

La replica jfdp02vdq ha una sola componente corrispondente entro 3 px. Anche lì gli 11 pixel riportano solo DQ 256. L'apertura circolare di 10 px ha però supporto comune in 303 pixel su 317, pari al 95,58%. I 14 pixel esclusi sono nella seconda posa lunga e nessuno appartiene alla scia. Il protocollo originario respinge la replica. [Flag CALACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)

L'escursione a 10 px misura la sensibilità alle perturbazioni dichiarate. Lo scarto rispetto alle pose brevi persiste in tutte le combinazioni ammesse a quel raggio. Le combinazioni riusano le stesse immagini e non stimano un intervallo di confidenza. La replica fra pose lunghe e il recupero delle scie oltre l'apertura restano da qualificare.

Per ripetere, eseguire `verifica.py` con runtime Astropy e SciPy, directory estratta dello studio originario con i FITS brevi e la PAM, protocollo di sensibilità e percorso di uscita nuovo.
