# BKL-046 — Schede operative MLT e catena CFA

Guida tecnica intermedia per i requisiti di processo. Le schede descrivono le fonti installate su DSG-Shared e le prove sintetiche. I criteri di verifica nativa restano aperti.

## BKL-046 — MultiscaleLinearTransform

La riga `process:MultiscaleLinearTransform` dell'indice requisiti ha impronta `8f25420107ae5bce237323dee60bcac14dbfbeb03e5e646924e4798d9413f25a` e disposizione U. Questa scheda documenta il comportamento descritto nella guida installata e un controllo sintetico del criterio decisionale. La copertura nativa resta da dimostrare.

### Ingressi e scelta della trasformazione

Registrare se l'immagine è lineare o già stirata, la scala in pixel delle strutture da conservare e la regione usata per stimare il rumore. Separare il ramo `Luminance` sul canale CIE Y lineare dal ramo `Lightness` sulla componente CIE L* di un'immagine non lineare. `Chrominance` rielabora l'RGB e ripristina la componente Y originale. Per RGB/K si opera sui canali RGB o sul singolo canale grigio.

La guida descrive Starlet e Multiscale Linear Transform come due decomposizioni distinte. Per Starlet usare la sequenza di scale diadica. Per la trasformazione lineare multiscala i filtri gaussiani sono scelti dall'algoritmo e il controllo della funzione di scala è disabilitato. Il rumore si attenua sui livelli di dettaglio. Il residuo a grande scala serve come controllo separato.

### Sequenza operativa e decisioni

1. Salvare i riferimenti delle regioni fondo, stelle e segnale debole prima della prova. Con Layer Preview individuare i livelli che contengono rumore e quelli che contengono strutture da conservare. Registrare trasformazione, numero di livelli, scala, canale e maschera.
2. Provare soglia in unità sigma, amount e iterazioni per singolo livello su una copia o anteprima. Su dati lineari positivi, la maschera lineare invertita dà maggiore protezione alle regioni brillanti e ha una maschera per canale su immagini RGB. Controllare l'effetto dell'amplificazione e della sfocatura, perché la protezione delle stelle può lasciare esposto il segnale diffuso debole. Disattivare STF per interpretare l'anteprima della maschera. Il ramo con immagine non lineare usa una strategia di mascheratura distinta.
3. Misurare separatamente il residuo sul fondo, il flusso di apertura delle stelle e il segnale diffuso. Una riduzione del rumore che non soddisfa i limiti preregistrati per il segnale richiede una soglia inferiore, una protezione diversa o l'astensione. Prima dell'esecuzione nativa definire questi limiti, la geometria delle regioni, il controllo del residuo e i parametri conservati nell'istanza.

### Controllo sintetico

Su una fixture inventata, una soglia crescente ha abbassato la RMS di fondo da 0,00404 a 0,00046, ma ha portato l'errore del flusso del filamento a circa −27,7%. La maschera pensata per proteggere le stelle non ha ridotto quell'errore. Il programma usa un modello didattico di attenuazione delle scale. Nessun risultato sul codice nativo o sui limiti numerici dei parametri di PixInsight è inferito da questa fixture.

Fonte tecnica: guida `MultiscaleLinearTransform.html` installata con PixInsight 1.9.6, SHA-256 `e8c78a0853ec885f75bc1b57906dea78ff487ceaadd3716f9a3dcac6df27476d`, sezioni 2.1, 2.4, 2.5, 2.10 e 2.11. Esecuzioni native e chiusure scientifiche: zero.

## BKL-046 — Prerequisiti e diramazioni per dati CFA

Questa scheda collega quattro processi alle guide installate su DSG-Shared con PixInsight 1.9.6. L'indice a fianco fissa sorgenti, sezioni e righe dei requisiti. Le decisioni riportate sono da validare in una futura prova ammessa.

| Processo | Prerequisito e scelta | Controllo prima di passare allo stadio successivo |
| --- | --- | --- |
| ImageCalibration | Per i light CFA preservare mosaico e orientamento. Registrare bias, dark, flat e overscan effettivamente previsti. Se si ottimizza il dark, conservare la decisione e il fattore per la sessione. | Verificare dimensione, posizione del mosaico, geometria degli ingressi e residui. Un mosaico già interpolato esce dal ramo CFA. |
| Debayer | Nel ramo RGB ordinario applicare il demosaicing dopo la calibrazione CFA. `Auto` richiede proprietà CFA riconoscibili. Per X-Trans la guida indica che il pattern è ricavato dalle proprietà dell'immagine. | Conservare il pattern adottato. Pattern residuo e colori anomali richiedono verifica prima di proseguire. Tenere a parte le sorgenti CFA del ramo Bayer Drizzle. |
| LocalNormalization | Operare dopo l'allineamento al riferimento e prima dell'integrazione. La scala in pixel determina quanto è locale il modello. In batch includere il riferimento tra i target se partecipa all'integrazione e deve avere un proprio XNML. | Fissare riferimenti, immagini e metadati associati. Confrontare anche un controllo senza normalizzazione. Valutare residuo sul fondo e flusso del segnale diffuso, prima di accettare una correzione più locale. |
| DrizzleIntegration | Nel ramo Bayer Drizzle usare sorgenti CFA calibrate coerenti con i record di registrazione e di integrazione. Le gocce dei singoli pixel contribuiscono solo al canale colore corrispondente. | Predefinire copertura minima per colore e confrontare fotometria, struttura e rumore con un ramo di riferimento. Una copertura insufficiente o metadati incoerenti richiedono astensione. |

Archiviare gli ingressi, i parametri, gli artefatti di registrazione e normalizzazione e i criteri misurabili di accettazione. L'apporto del dithering, la conservazione della fotometria e le perdite sul segnale diffuso vanno verificati nel perimetro dei dati e della versione impiegata. Nessuna esecuzione nativa e nessuna promozione dei criteri.

## BKL-046 — StarAlignment e ImageIntegration nel flusso WBPP

La guida DrizzleIntegration installata descrive due passaggi distinti. StarAlignment registra le immagini su un riferimento comune e genera i record geometrici XDRZ. ImageIntegration associa alle immagini registrate gli XDRZ corrispondenti e li aggiorna con pesi, normalizzazione e rigetto. Il ramo Bayer Drizzle richiede ancora i light CFA calibrati sulle griglie originali. La guida precisa che per l'ultimo passaggio contano i dati aggiornati negli XDRZ. Il risultato integrato ordinario non è un ingresso di DrizzleIntegration.

La copia installata di WBPP usa la costante `BPP.Version.WBPP_VERSION` del file `BPP-global.js`, pari a **3.2.2**. Il commento nell'entry point riporta 3.1.2. Per identificare il comportamento studiato, conservare la costante usata dal programma e le impronte dei sorgenti.

### Controlli per gruppo di immagini

- Registrazione. Fissare riferimento, immagini di partenza e criteri di esclusione. WBPP configura la generazione di XDRZ in StarAlignment. Il ramo con correzione di distorsione attiva o canali RGB separati imposta un modello a spline. Controllare che al risultato di ogni registrazione corrispondano l'immagine registrata, l'XDRZ prodotto e la sorgente CFA attesa.
- Integrazione. Nel ramo ImageIntegration di WBPP, un XDRZ assente disabilita l'aggiornamento dei record drizzle per il gruppo di light. La normalizzazione locale è selezionata quando ogni frame attivo ha un'associazione XNML e usa impostazioni distinte per normalizzazione di uscita e rigetto. In questo ramo la sottrazione dei pedestal è disabilitata perché i modelli sono stimati con il pedestal presente. La semplice associazione nel codice è da verificare insieme con esistenza, impronte, riferimento e corrispondenza di ogni file.
- Drizzle. WBPP passa al processo il sottoinsieme con riferimento XDRZ e verifica la numerosità prima dell'integrazione. Tre frame rappresentano un controllo di ammissibilità del wrapper. La copertura sufficiente per colore e per geometria va misurata sul sottoinsieme effettivo. Registrare parametri di scala, drop shrink, kernel e uso della correzione locale. L'assenza di un record, la selezione di un sottoinsieme imprevisto o il mancato aggiornamento dei record impediscono di attribuire il risultato al piano originario.

Le fonti sono la guida DrizzleIntegration, sezione 4.1, e i sorgenti WBPP installati esplicitati nel riscontro. Il controllo ha riletto il codice e il manuale. L'esito nativo e la conservazione fotometrica restano da verificare sul candidato ammesso.

## Collaudo delle associazioni XDRZ e XNML

Il controllo offline ha riletto tre XDRZ del piano CFA e le rispettive sorgenti. Con gli XNML sintetici ha accettato tre associazioni corrette e scartato 15 associazioni errate. Le matrici di normalizzazione e i risultati in PixInsight restano da verificare. SHA-256 riscontro su H: 6933fc53f72a18f1fdc6ee01a2a2773417f988f459fb8720fa3f5e8f924d94ad.

## Indice delle fonti

Il riscontro su H: mappa 125 requisiti di processo. Sono state trovate 40 guide dirette della versione installata. SHA-256 indice: 8363ab428d5fa254341799034d1f4a84c21c0f1eb669de420218efbc3cc500be.
