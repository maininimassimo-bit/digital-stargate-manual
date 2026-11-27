# BKL-046 — Preselezione di scie estese e riferimenti brevi GO14949

Ho fissato prima della misura due puntamenti ACS/WFC F606W, ciascuno con una posa da 400 s e due pose da 40 s. Ho riletto i sei FITS per SHA-256. La selezione parte dalle componenti connesse nel DQ lungo con bit di full well e sviluppo verticale di almeno 21 pixel. Per ogni componente, la proiezione WCS del suo centro fornisce un punto di partenza nelle pose brevi. Il test richiede un picco locale, uno scarto limitato e un'apertura di 10 pixel con DQ nullo.

| Puntamento | Componenti lunghe | Prive di altri flag lungo la componente | Riferimenti brevi che superano la preselezione |
| --- | ---: | ---: | ---: |
| Secondo | 66 | 1 | 0 |
| Terzo | 102 | 0 | 0 |

Nel secondo puntamento, 43 delle 66 componenti ricadono su aperture della prima posa breve che mostrano già full well dopo il controllo del picco. La singola componente lunga con il solo bit di full well ha 55 pixel totali, due fuori dall'apertura standard. Nella prima posa breve, lo scarto del picco supera la soglia prescritta e l'apertura contiene due pixel di full well. Nella seconda posa breve il picco resta sotto il requisito di segnale.

La proiezione WCS e il massimo locale costituiscono una preselezione diagnostica. Un rifiuto per supporto del picco non stabilisce se la sorgente è assente o se mancano dati o precisione di registrazione. Il risultato riguarda queste sei pose e queste soglie. Rimane da trovare o acquisire un riferimento breve pulito per misurare il recupero del flusso. Nessuna fotometria sulle scie è stata qualificata. Il replay coincide byte per byte.

[Contesto strumentale STScI](https://spacetelescope.github.io/hst_notebooks/notebooks/ACS/acs_saturation_trails/acs_saturation_trails.html)