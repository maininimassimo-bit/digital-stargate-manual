# BKL‑046 · Centro libero e controllo circolare

Il protocollo confronta gli stessi 1.350 adattamenti su 54 immagini Moffat sintetiche senza rumore, alla scala maggiore di 0,65 pixel. Il centro iniziale è perturbato fino a 0,10 pixel. Il profilo ellittico e quello circolare ottimizzano separatamente il centro. [Prova a centro imposto](BKL-046-PSF-ORIENTAZIONE-CENTRAGGIO.md)

| Scarto iniziale | Fuori criterio a centro imposto | Fuori criterio a centro libero | Fuori criterio dopo il raffinamento circolare |
| --- | ---: | ---: | ---: |
| 0 | 0/54 | 16/54 | 0/54 |
| 0,025 pixel | 352/432 | 97/432 | 0/432 |
| 0,05 pixel | 389/432 | 102/432 | 0/432 |
| 0,10 pixel | 407/432 | 111/432 | 0/432 |

Il controllo con gradiente analitico conferma i 326 arresti originari e raffina ciascuno di questi punti. La norma massima del gradiente finale è 9,99 × 10⁻¹¹, sotto la soglia congelata di 10⁻¹⁰. La curvatura locale risulta positiva per tutti i confronti circolari. I 326 arresti restano nella ricevuta precedente. La nuova ricevuta conserva entrambi gli esiti per riga.

L’angolo rimane indeterminato nei controlli circolari. La decisione di orientazione, il fit ellittico e le sue misure di centro e rapporto assiale coincidono con quelli della prova precedente. L’errore angolare massimo osservato resta inferiore a 0,000030° negli adattamenti ellittici.

La prova qualifica il comportamento numerico locale su questa griglia deterministica, con profilo di generazione e di adattamento della stessa famiglia e scala intrinseca nota. Restano aperti rumore, profili fuori famiglia, incertezza e misure native. L’asse `PSF_PIXEL/2` resta aperto.

| Ricevuta | SHA‑256 |
| --- | --- |
| Adattamento congiunto | `d58665a35562580ac274387d8ce3ea72702786061bc5dee2bb63113f76a8cbdf` |
| Raffinamento del confronto circolare | `5c204733172b58df26569e62c1a7a83618bb0b061584b884fe72413917789197` |
