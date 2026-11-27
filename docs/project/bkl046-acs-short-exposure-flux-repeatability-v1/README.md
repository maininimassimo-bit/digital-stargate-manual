# BKL-046 · Ripetibilità del flusso nelle pose ACS da 40 s

Confronto diagnostico fra jfdp02vwq e jfdp02w3q della visita 17656 e jfln02qzq del programma 17979, tutte a gain 2 e F606W. Ho tenuto lo stesso identificativo Gaia e lo stesso chip nelle tre pose. Le aperture usano centratura locale, pesi frazionari con griglia 8×8, correzione PAM, fondo mediano a 8–12 px e DQ 0/64. Un pixel escluso nell'apertura fa respingere la misura anziché imputarne il valore. [Riferimenti astrometrici e log di guida](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/0247c695c5370b4780ce726bf2eb51f00903981e/docs/project/bkl046-acs-17656-short-reference-qualification-v1)

| Raggio | Chip | Sorgenti utilizzabili / in verifica | P90 assoluto 17656, verifica | P90 assoluto 17979 rispetto alla media 17656, verifica |
| --- | --- | ---: | ---: | ---: |
| 3 px | 1 | 50 / 16 | 2,59% | 1,78% |
| 3 px | 2 | 56 / 11 | 1,98% | 2,41% |
| 5 px | 1 | 5 / 2 | 0,68% | 0,61% |
| 5 px | 2 | 2 / 1 | 0,16% | 1,14% |

I 234 abbinamenti geometrici producono 106 sorgenti utilizzabili a 3 px e sette a 5 px. A 3 px, 77 delle 106 misure rispettano il limite diagnostico del 2% in entrambi i confronti. I sottogruppi di verifica non sostengono un limite del 2% per l'intero campo. L'analisi usa i FLT e non isola CTE, differenza d'epoca, sorgenti vicine e risposta fotometrica. Le piccole numerosità a 5 px non supportano un confronto fra aperture. La fotometria di pose sature e la qualificazione delle scie a gain 2 restano aperte.

Per ripetere, eseguire `verifica.py` con runtime Astropy, runtime SciPy, directory delle due PAM, directory estratta dei riferimenti brevi (con jfln02qzq recuperato dal suo archivio), protocollo e due nuovi file di uscita per rapporto e dettaglio. Le impronte sono fissate nel protocollo e nei metadati vincolati della prova Gaia.
