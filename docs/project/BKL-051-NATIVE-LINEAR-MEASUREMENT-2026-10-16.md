# BKL-051: adattatore nativo della misura lineare

`DSGNativeLinearMeasurement(runDirectory)` è definito in
`native_linear_measurement.jsh`. Il file definisce una funzione, senza avviare
PixInsight o elaborare immagini al caricamento. La sua implementazione usa le API
PJSR; le prove attuali le sostituiscono con oggetti simulati e byte sintetici.
Il comportamento dell'installazione reale, le prestazioni e il limite pianificato
di memoria devono ancora essere verificati da un collaudo nativo autorizzato.

L'adattatore legge soltanto il sottoinsieme FITS Float32 primario già definito
dal lettore revisionato. Altri formati non vengono convertiti silenziosamente;
gli ulteriori formati richiesti dal progetto restano da gestire. Il calcolo usa
supporto, pesi e fattori condizionali congelati, senza generare un modello fisico
o trasformare una dichiarazione in evidenza scientifica.

## Input e autorità

Il chiamante locale sigillato deve caricare le quattro dipendenze esatte:
core, parser passivo, lettore primario e adattatore. Il parent deve aver verificato
le revisioni, tutta la chiusura dei riferimenti esterni e un nuovo consenso per
un solo avvio; deve possedere il processo, preservarne il controllo e applicare
il proprio termine monotono. I vecchi consensi restano consumati. Questo modulo
non crea consensi o processi e non rende autorevole un JSON con `authorized:true`.

Sono controllati protocollo, identità, tempi, sigillo, versioni, hash grezzi e
dimensioni. I ruoli degli input sigillati corrispondono ai nomi letterali: otto
fissi più al massimo 64 carte; sigillo e consenso sono esclusi dalla lista del
sigillo, per un massimo di 74 input e 200 MiB. Il launcher resta nei metadati del
parent. Nella directory nativa non sono ammessi file iniziali estranei o prodotti
precedenti. Le voci devono risultare file, senza collegamenti o reparse point;
la verifica canonica di tutti gli antenati resta anche un obbligo del parent.

Le carte risolvono separatamente riferimenti semantici e hash grezzi delle carte.
Sono richiesti esattamente i ruoli applicabili di identità, base, budget e lineage,
legati anche all'intero kernel e alla sorgente. Le dichiarazioni di risposta
strutturalmente nulla restano nel modello condizionale e nella relativa carta
dei fattori: non attestano da sole la validità fisica degli zeri o l'origine dei
fattori. Nessuna applicabilità scientifica deriva dal loro hash.

Il parser passivo e i controlli del modello precedono l'allocazione delle immagini.
Il kernel di input non può includere campioni: il modulo li legge privatamente
dall'immagine nativa. Non vengono inseriti campioni fittizi per collaudare il core.

## Valori e cronologia

Il sorgente viene letto con limite e mantenuto aperto in sola lettura durante
misura e checkpoint. Il valore numerico 15 per il tipo ByteArray è quello del
file `DataType.jsh` installato, verificato con impronta
`503f8d097b7b7a6a1892cb7d00e782e1fbccecb6746987d52e9b758793a4e298`;
non viene incluso altro codice eseguibile. La versione PJSR resta da provare.

Il lettore primario decodifica i valori Float32 in Float64. Una sola nuova
finestra monocromatica Float64 riceve questi valori, senza aprire il FITS con
il modulo di importazione, riscalare o applicare WCS. Ogni campione è confrontato
con l'oracolo grezzo con `Object.is`, preservando anche il segno dello zero.
I confronti `Image.getSamples` percorrono righe e segmenti di massimo 65536
campioni; le letture puntuali del supporto sono verificate a loro volta contro
l'oracolo prima del calcolo. I campioni privati e il modello vengono congelati
prima di passare al monitor cooperativo del core.

Il modulo confronta l'intera immagine prima e dopo il calcolo e il checkpoint
riaperto. Esporta le History iniziali e correnti effettivamente disponibili,
senza inventare operazioni per il calcolo puro. L'History iniziale della sorgente
è esportata prima di `setSamples`; un nuovo checkpoint non ricostruisce una
History di calibrazione assente dal FITS. Source-lineage e carte restano necessari
e la provenienza fisica resta non verificata.

Le viste vengono chiuse soltanto dopo aver conservato checkpoint e History
richiesti per il loro percorso. Un errore di conservazione lascia la vista aperta
e il terminale incerto. Tutte le finestre restituite da una riapertura sono
tracciate prima di verificarne il numero. Se superano il massimo previsto di due,
il modulo conserva il conteggio nel log e le lascia aperte, senza falsificare il
conteggio del terminale o produrre ready. Il parent deve riconciliare questo caso
senza terminazione forzata o un nuovo avvio.

## Termine e conservazione

Il termine cooperativo copre l'intero tentativo di 180 secondi dalla creazione
del consenso, incluso l'avvio. Il tempo nativo parte all'ingresso della funzione,
prima delle letture, e usa il residuo calcolato rispetto al termine originale.
Controlli prima e dopo le API sincrone rilevano ritardi; non promettono di
interrompere una chiamata nativa bloccata. Dopo il termine proseguono solo
conservazione e riconciliazione. Il parent deve verificare il proprio tempo vivo.

Gli output vanno soltanto nella directory scratch nuova con un solo scrittore.
Il controllo di assenza non è una creazione atomica senza sovrascrittura PJSR:
la pubblicazione immutabile è compito del parent mediante la copia esclusiva.
Un tentativo di scrittura fallito non viene ripetuto. Si controllano rilettura,
hash, limiti per ruolo e complessivi; il terminale esclude se stesso e ready
dalla propria lista di prodotti. Ready fissa poi l'hash grezzo del terminale.

Vengono ricontrollati prodotti e input anche dopo le ultime scritture. Un errore
tardivo o l'attraversamento della scadenza conserva i file, tenta una sola
scrittura di `native-publication-uncertain.json` e genera un'eccezione. Questo
diciassettesimo nome runtime è un segnale di errore da massimo 1 MiB, non un
prodotto accettato; restano i limiti di 20 file e 192 MiB. Il publisher del parent
rifiuta anche un segnale parziale, prima di copiare e nelle verifiche finali.
L'assenza del segnale, se fallisce la sua scrittura, non dimostra successo:
esito effettivo, processo e diagnostica restano sotto supervisione.

Il ritorno massimo è `COMPLETED_CONDITIONAL_COMPUTATION`. Varianza fisica completa
e significatività rimangono null, applicabilità e provenienza false, stato
scientifico NOT_VALIDATED e zero controlli qualificati. Restano da completare
supervisore, preflight nativo e tutti i requisiti scientifici e operativi R01-R14.
