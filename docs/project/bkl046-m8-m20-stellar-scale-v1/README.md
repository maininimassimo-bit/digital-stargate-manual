# BKL-046 · Scala relativa da stelle appaiate su M8/M20

Sulle 27 coppie già usate per il fondo differenziale sono state accoppiate le stesse 53 stelle in entrambe le parità verdi. Il rapporto da applicare alla posa bersaglio è stimato con la mediana dei logaritmi flusso riferimento / flusso bersaglio. Si mantengono separate le due calibrazioni, le due convenzioni per il centro dell'apertura e le due parità. Ogni stima di controllo esclude a turno uno degli otto riquadri di stelle. Le stelle del riquadro escluso misurano la trasferibilità.

| Scostamento ammesso dalla scala 1 | Coppie con tutte le stime fuori banda da uno stesso lato | Coppie con tutte le stime dentro banda |
| ---: | ---: | ---: |
| ±0,5% | 9/27 | 0/27 |
| ±1,0% | 8/27 | 2/27 |

L'intervallo tra tutte le stime di scala è 0,9627–1,0495. Per 132 delle 216 combinazioni coppia-variante il P90 dell'errore assoluto sui rapporti stellari esclusi diminuisce dopo la correzione. La mediana dei P90 passa da 7,09% a 6,71%. Gli intervalli descrivono sensibilità a parità, calibrazione, centratura e riquadro escluso. Le coppie condividono pose e stelle. Gli intervalli non sono intervalli di confidenza. Il residuo include il comportamento delle aperture e della correzione di fondo locale, oltre a eventuali variazioni fotometriche.

La perturbazione di ±1% dello studio precedente non copriva interamente le stime empiriche di M8/M20. Il residuo sulle stelle escluse lascia aperta la qualificazione di un singolo fattore per posa. Il passaggio alla correzione del fondo esteso richiede una verifica separata prima di attribuire il residuo a un gradiente additivo. Questo studio non stima il flat spaziale, non misura il fondo assoluto e non chiude il criterio scientifico. [Test di sensibilità](../bkl046-diffuse-scale-sensitivity-v1/README.md)

Il generatore usa Python 3.12 e la libreria standard. Riceve la directory del protocollo, la ricevuta fotometrica, la ricevuta delle coppie e il percorso della nuova ricevuta. Le due fonti esatte sono nello ZIP di custodia.