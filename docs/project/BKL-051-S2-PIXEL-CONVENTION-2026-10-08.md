# BKL-051 S2 — Convenzione dei pixel e riconciliazione delle misure

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S2-PIXEL-CONVENTION |
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Proposed offline contract; scientific operating acceptance pending |
| Baseline | PR #506, merge `14d53228a7ab4a34e90070fea99033a1f84360f6`, post-merge/Pages verified |

## Problema verificato

Confrontare un centro espresso come indice del campione con un centro geometrico senza normalizzarne l'origine sposta coordinate e aperture. Tre fixture Gaussiane native PixInsight, conservate con checkpoint, script e History, verificano separatamente il comportamento di `StarDetector` con `fitPSF=true` e del fit PSF separato. Non sono immagini astronomiche generate, iniezioni per completezza o misure di falsi positivi.

In questa installazione, il centro fitted `StarDetector.pos` è espresso nell'indice del campione a base zero; `PSF.x/y/c0` del fit separato è geometrico, indice + 0,5. Il percorso nativo ImageSolver usa centri PSF geometrici. Per il WCS nativo convertire la posizione fitted aggiungendo 0,5 **esattamente una volta**; un centro PSF separato non riceve nuovamente l'offset. Per un lettore FITS con origine zero si usa l'indice del campione. Le coordinate FITS a base uno sono indice + 1. Origine e orientamento devono essere dichiarati dal chiamante, mai dedotti dal nome del file.

| Coordinate dichiarate | Indice del campione | Geometriche native | FITS a base uno |
|---|---|---|---|
| Indice `p` a base zero | `p` | `p + 0,5` | `p + 1` |
| Geometriche `g` | `g − 0,5` | `g` | `g + 0,5` |
| FITS a base uno `f` | `f − 1` | `f − 0,5` | `f` |

Le tre fixture non attestano automaticamente altre versioni/API o la convenzione del detector senza fit. La vecchia diagnosi separata sui ritagli forti conserva soltanto distanze scalari dal centro raw, senza le sue due coordinate: non è possibile ricostruire una correzione vettoriale sottraendo una costante alla distanza. I conteggi reali rimangono storici; attribuzioni causali restano esplorative.

## Incremento puro offline

`tools/scientific_transients/pixel.mjs` espone `inspectPixelPosition` per un oggetto passivo già materializzato con `x`, `y`, `width`, `height`, `convention` e `axes`. Origini ammesse: `SAMPLE_INDEX_ZERO`, `NATIVE_GEOMETRIC`, `FITS_ONE_BASED`; assi espliciti `X_RIGHT_Y_DOWN`. Origine/assi/coordinate nulli producono `INCOMPLETE`, senza punti o footprint inventati. Assi invertiti o convenzioni non supportate vengono rifiutati: il modulo non corregge orientamento, crop, rotazione o registrazione.

Schema chiuso; geometria intera positiva e sicura, coordinate finite; conversioni che perdono il mezzo pixel per limiti numerici rifiutate. La tolleranza di arrotondamento è soltanto numerica, mai raggio di associazione o soglia astrometrica. L'estensione continua dell'immagine è `[0,width) × [0,height)` nel sistema geometrico: è distinta dagli indici interi dei campioni. Centri fuori campo non vengono troncati o sostituiti; `insideImage` non è un giudizio sulla qualità o sulla validità del rilevamento.

Gli output immutabili riportano `DECLARED_NOT_ATTESTED`, `NOT_VALIDATED`, `NOT_EVALUATED`: nessun WCS, misura, significatività, covariance propagation, lettura dei pixel, rete o consenso. Il chiamante deve verificare API/versione, byte, immagine, orientamento e provenance; il futuro parser raw deve rifiutare chiavi duplicate prima della materializzazione. Accessori/proxy non fidati non sono un boundary supportato. Questo helper non è ancora inserito nel worker o nel portale operativo.

Undici test nuovi coprono origini e round-trip, assenza di doppio offset, coordinate frazionarie, bordo continuo, dati mancanti, tipi/schema/assi invalidi, precisione e immutabilità. Suite offline totale: 55 test; nessuna dipendenza aggiunta. Le tre fixture native sono evidenza separata dalla CI numerica.

## Evidenze private riconciliate

- Due nuove epoche pubbliche dello stesso evento noto sono selezionate con criteri temporali/qualità dai metadati prima della lettura dei flussi. Sei prodotti e originali preservati; due importazioni native senza clipping/stretch/interpolazione verificate sui pixel. Il WCS TPV del provider non è interpretato da PixInsight: soluzione Gaia nativa su derivate con originali e tentativi falliti conservati. La soluzione già riuscita è recuperata dal checkpoint, senza ripeterla. Questi dati ampliano le epoche, non i campi indipendenti o la ricerca cieca.
- Conversione delle 463/496 coordinate delle nuove epoche dai checkpoint nativi esistenti, senza ridetezione, nuova soluzione o modifica dei pixel. Residui rispetto al WCS provider sono descrittivi: riferimenti/covarianze possono essere condivisi. Non attestano una precisione indipendente o il tasso di falsi positivi.
- Sei export M27 dai checkpoint già salvati: 12.463 posizioni convertite, byte genitori, posizioni dei campioni e flussi invariati. Le associazioni storiche restano le stesse dopo correzione. Il raggio storico esplorativo non è promosso a policy.
- La vecchia funzione di apertura usava `xx + 0,5 − x` rispetto a un centro fitted nell'indice del campione. La revisione in sola lettura usa `xx − x`, anche nella maschera dei vicini. Due prove numeriche speculari al bordo dell'apertura verificano il flusso noto; nuove misure conservate in un ramo additivo, senza sovrascrivere le precedenti.
- Il confronto sulla medesima popolazione di sei esposizioni ricostruisce le identità originali: 786 associazioni comuni; ensemble esplorativi di 193/46/12 sorgenti per le tre aperture storiche, identità ed eleggibilità invariate. Aggregati corretti e precedenti sono confrontati sulle stesse sorgenti nel dossier privato. Non confondere questi ensemble con quelli più ampi di singole coppie/tre epoche. Dispersione della popolazione non è incertezza certificata della singola sorgente.

Immagini, coordinate e misure individuali, calibrazione Owner, percorsi/hash dei parent restano privati. History e tentativi falliti conservati. I manifest collegano gli archivi genitore; nessun replay autonomo dell'intera acquisizione dichiarato. [Ricevuta minimizzata](evidence/BKL-051-S2-PIXEL-CONVENTION-2026-10-08.json).

## Residui e consegna

Il trasferimento condizionale di unità della calibrazione già verificato non viene rifatto. Rimangono da riconciliare i budget dipendenti dalle aperture e da validare covarianze di dark/flat condivisi, cosmetica, fondo mediano e rumore correlato, PSF, selezione del centro, normalizzazione e banda. Varianze/covarianze sconosciute rimangono unknown; non aggiungere due volte il rumore di lettura già incluso nel fondo empirico. Le vecchie diagnostiche astrometriche esterne con origini non esplicite non certificano S2.

S1/S2 aperte, S3 parziale, worker/journal/UI S4 e collaudo S5 ancora incompleti. I [requisiti di segnalazione](BKL-051-SCIENTIFIC-REPORTING-PLAN-2026-10-08.md) rimangono inclusi nella milestone, senza invio attivato. Soglie, policy autonoma e accettazione finale Owner ancora richieste; P6/F4/F5/BKL-050/S10/Safety invariati.

Gate di rilascio: CI exact-head → ARB → RQ → merge protetto → post-merge/Pages, da attestare nella PR. Rollback del solo helper/documenti con revert e rigenerazione delle projection; non ripristinare implicitamente vecchie coordinate come validate, non sovrascrivere o cancellare dossier.

Documentazione nativa consultata nell'installazione: PJSR StarDetector/StarData, PSF, ImageWindow e sorgenti ImageSolverEngine/WCSmetadata. Le conclusioni API sono limitate alle fixture e all'installazione verificata; prima di un adapter operativo, attestare nuovamente versione e contratto. Per i dati pubblici: [IRSA/ZTF API](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_api.html).
