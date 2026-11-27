# BKL-046 · Registrazione astrometrica fra le visite ACS 05 e 02

L'analisi usa le quattro pose FLT F606W del programma 17979 vincolate per SHA-256. La selezione usa massimi locali senza flag incompatibili nella finestra, un limite sul picco e un tetto di guide per tassello. Le guide della posa lunga vengono proiettate nei due chip di ciascuna posa breve. L'abbinamento richiede la scelta reciproca e una separazione dal secondo vicino. I tasselli di verifica sono esclusi dalle stime. La seconda variante cerca anche uno spostamento globale entro 80 px usando soltanto tasselli di stima.

| Posa | Guide chip 1 | Guide chip 2 |
| --- | ---: | ---: |
| jfln05ykq | 182 | 273 |
| jfln05ymq | 180 | 258 |
| jfln02qtq | 190 | 177 |
| jfln02qzq | 279 | 263 |

Su 16 combinazioni di pose e chip ci sono 12 abbinamenti reciproci complessivi con la preselezione WCS. Il massimo è due per combinazione. Nessun gruppo raggiunge i 18 abbinamenti di stima e i 12 di verifica previsti. La ricerca di offset non produce alcun picco con il supporto richiesto e quindi conserva gli stessi abbinamenti. Non risulta una trasformazione qualificata. Il limite riscontrato è l'abbinamento delle guide con queste soglie e queste immagini. Una registrazione con identificativi di catalogo indipendenti o guide più profonde resta da verificare.

Per ripetere, eseguire ciascun verificatore con runtime Astropy, runtime SciPy, directory dei quattro FITS, protocollo corrispondente e un nuovo percorso di uscita. I FITS sono conservati nei due archivi già verificati delle visite. [Preselezione delle scie](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/9540ff0ed65848ba762fddcc3ed546061229fbb8/docs/project/bkl046-acs-17979-visit05-gain2-cross-visit-screen-v1)
