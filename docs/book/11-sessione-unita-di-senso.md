# Capitolo 11 - La sessione come unità di senso

## Il limite della cartella

All'inizio una notte osservativa può sembrare contenuta in una cartella. Il nome indica una data o un target, i file si susseguono secondo la numerazione prodotta dal software di acquisizione e la struttura appare sufficientemente chiara a chi era presente. Finché il volume è limitato e la memoria dell'operatore è recente, questa convenzione funziona.

Il problema emerge quando il tempo passa, le notti aumentano e il patrimonio viene interrogato da persone o sistemi che non possiedono quel contesto. Una cartella può dire dove si trovano i file, ma non spiega con certezza quale fosse l'intento, quale configurazione fosse effettivamente in uso, quali condizioni abbiano influenzato la raccolta, quali frame siano stati esclusi o se la sessione sia terminata correttamente.

Digital StarGate incontra questo limite durante l'evoluzione degli analytics. Alcuni componenti ricavavano la sessione esclusivamente dal nome della directory. L'analisi di un dataset mostrò che immagini appartenenti alla notte precedente potevano essere incluse nel perimetro successivo. Non era un errore spettacolare. Era più istruttivo: dimostrava che una convenzione fisica era stata usata come se fosse identità logica.

La risposta registrata nell'ADR-001 introduce un Session Layer e una sorgente comune dei metadati. La decisione non riguarda soltanto il riuso del software. Stabilisce un principio più ampio: la sessione non coincide con il contenitore in cui sono stati depositati i file.

La cartella è un luogo. La sessione è un significato.

## Dalla notte tecnica all'oggetto governato

Una sessione osservativa è l'unità che tiene insieme intenzione, tempo, strumenti, condizioni, acquisizioni ed esito. Permette di rispondere non soltanto a “quali file sono presenti?”, ma a domande più importanti:

- quale obiettivo era perseguito;
- quale osservatorio e quale configurazione erano coinvolti;
- quando è iniziata e terminata la raccolta;
- quali sequenze e filtri sono stati usati;
- quali eventi hanno interrotto o degradato il lavoro;
- quali dati sono stati prodotti;
- quale qualità è stata rilevata;
- quale stato è stato assegnato alla sessione;
- quali evidenze sostengono quello stato.

Questa trasformazione è centrale nel modello Digital StarGate. L'osservatorio non produce una successione anonima di immagini. Produce episodi scientifici ricostruibili. Ogni episodio può attraversare acquisizione, trasferimento, validazione, elaborazione, confronto e pubblicazione senza perdere il legame con la propria origine.

Il termine “governato” non significa appesantito da procedure. Significa che identità, confini e responsabilità non dipendono soltanto dalla memoria informale. Una sessione possiede un identificatore stabile, una provenienza, uno stato e relazioni esplicite. Può essere incompleta o contenere valori sconosciuti; proprio per questo rimane affidabile, perché non nasconde l'incertezza.

## Tre tempi diversi

La sessione riunisce almeno tre concezioni del tempo.

La prima è il tempo astronomico dell'osservazione: la notte può attraversare la mezzanotte civile pur restando un unico episodio. Se si usa soltanto la data del calendario, una sequenza coerente rischia di essere spezzata in due.

La seconda è il tempo operativo: apertura, stabilizzazione, acquisizione, eventuali pause, chiusura e recovery. Questo tempo racconta ciò che il sistema e l'operatore hanno fatto.

La terza è il tempo informativo: scoperta dei file, importazione, registrazione, misurazione della qualità, processing e pubblicazione. Può continuare per giorni o mesi dopo la notte osservativa.

Confondere questi tempi produce errori silenziosi. La data della cartella non è necessariamente l'inizio fisico della sessione. Il timestamp di copia non è quello di acquisizione. La pubblicazione di un report non coincide con la conclusione della raccolta. Digital StarGate separa gli eventi e li collega attraverso identificatori e correlazioni.

Questa distinzione rende possibile seguire un dato lungo il suo ciclo senza riscrivere la storia. Un nuovo controllo di qualità può aggiungere informazione a una sessione esistente; non deve far sembrare che quel controllo fosse disponibile durante la notte.

## Identità prima del nome

I nomi dei file restano utili. Possono contenere tipo di immagine, binning, esposizione, gain, offset, target, telescopio, temperatura, filtro, numero del frame e timestamp. Sono una fonte ricca, ma non perfetta.

La sintassi può variare. Un campo può essere vuoto. Target e telescopio possono contenere spazi o alias. Un dato opzionale può mancare. Una correzione manuale può modificare il nome senza cambiare l'immagine. Un percorso può essere spostato durante una migrazione.

Per questo il modello DSDM distingue l'identità stabile dal locator fisico. Il nome e il percorso diventano attributi osservati, non fondamenta uniche dell'identità. Il parsing produce valori accompagnati dalla loro provenienza e dal loro stato: osservato, derivato, dichiarato, verificato, ambiguo o sconosciuto.

Il principio è semplice: un sistema affidabile non trasforma una buona ipotesi in un fatto silenzioso.

Quando l'alias non è risolvibile, la sessione non scompare e il sistema non inventa una corrispondenza. Registra l'ambiguità e la rende disponibile alla revisione. Quando il filtro è assente, usa un valore governato come `unknown`. L'incompletezza diventa una qualità visibile del dato, non una ragione per falsificarlo.

## La sessione e il progetto

Una singola notte raramente esaurisce un obiettivo. Lo stesso target può essere osservato in più occasioni, con filtri diversi, condizioni differenti o configurazioni aggiornate. Le sessioni devono quindi restare distinte e, nello stesso tempo, appartenere a strutture più ampie.

Digital StarGate introduce una catena concettuale che collega progetto scientifico, campagna, osservazione, sessione e acquisizione. Ogni livello risponde a una domanda diversa.

Il progetto definisce l'iniziativa. La campagna coordina un insieme di osservazioni. L'osservazione rappresenta l'intento verso un target o una regione. La sessione descrive l'episodio temporale e operativo. L'acquisizione raccoglie frame omogenei per configurazione, filtro ed esposizione.

Questa gerarchia evita due estremi. Nel primo, ogni file è isolato e il contesto deve essere ricostruito ogni volta. Nel secondo, tutte le notti dedicate allo stesso target vengono fuse, perdendo differenze che possono spiegare qualità e risultati.

Le sessioni multi-night restano quindi distinguibili, pur potendo essere collegate allo stesso progetto. Anche una sessione che attraversa la mezzanotte mantiene una propria identità, secondo una regola temporale canonica. Il modello conserva granularità senza rinunciare alla visione d'insieme.

## La configurazione effettiva

Il valore scientifico di una sessione dipende anche dalla configurazione realmente utilizzata. Non basta conoscere l'inventario generale dell'osservatorio. Occorre poter collegare la sessione alla combinazione effettiva di telescopio, camera, montatura, filtri, accessori, software e parametri rilevanti.

Questa configurazione è versionata perché l'impianto evolve. Un componente può essere sostituito, un driver aggiornato, un profilo corretto. Se la sessione viene collegata soltanto allo stato corrente dell'inventario, il passato viene inconsapevolmente riscritto.

La configurazione effettiva funziona come una fotografia logica dell'assetto. Non deve contenere ogni dettaglio possibile, ma quelli necessari a interpretare e confrontare i risultati. Permette di domandare se una variazione di qualità dipenda dalle condizioni, dallo strumento, dalla procedura o dal processing successivo.

La sessione diventa così il punto di incontro tra Configuration Management e Scientific Data. La prima conserva identità e versioni degli asset; la seconda registra quale combinazione ha partecipato a uno specifico episodio osservativo.

## Stato e qualità non sono la stessa cosa

Una sessione può essere completata dal punto di vista operativo e avere una qualità scientifica insufficiente. Può essere trasferita correttamente ma ancora non revisionata. Può contenere frame validi e altri da scartare. Può essere interrotta in modo sicuro e risultare comunque utile per analizzare il comportamento del sistema.

Per questo stato operativo, stato di importazione, integrità e qualità devono rimanere distinti.

Dire “completata” può significare che la sequenza è terminata. Non significa automaticamente che i dati siano accettati. Dire “trasferita” indica che una copia ha raggiunto la destinazione e ha superato il livello di verifica previsto. Non dimostra che il contenuto sia scientificamente valido. Dire “quality-reviewed” implica una valutazione ulteriore, con criteri e autorità propri.

La distinzione evita che una parola positiva si propaghi oltre il proprio dominio. Consente inoltre di conservare sessioni imperfette senza attribuire loro uno stato improprio. Anche una sessione fallita può essere patrimonio informativo se documenta condizioni, errori e recovery.

## Il primo vertical slice

Nell'evoluzione Digital StarGate, Observation Session diventa anche il primo vertical slice applicativo della Developer Foundation. La capability dimostra creazione, lettura, persistenza in memoria, pubblicazione di un evento e logging correlato.

Il suo valore storico non consiste nel numero di funzioni. Consiste nel portare un concetto enterprise attraverso più livelli, dai contratti all'evento. Allo stesso tempo, i limiti sono dichiarati: la persistenza è in memoria; non sono inclusi database, N.I.N.A., ASCOM, PixInsight o funzioni astronomiche avanzate.

Questa precisione è coerente con il metodo del progetto. Il vertical slice dimostra che la sessione può essere trattata come oggetto applicativo canonico. Non dimostra ancora l'intero ciclo scientifico. Diventa una fondazione sulla quale integrare discovery, manifest, catalogo e servizi successivi.

L'avanzamento non viene misurato chiedendo se “la sessione esiste”, ma quale parte del significato sia stata formalizzata e quale evidence sostenga la capacità corrente.

## Discovery senza appropriazione

Il passaggio dai concetti ai file reali avviene con una scelta prudente. Il Session Importer viene progettato dal PC principale verso una condivisione EAGLE in sola lettura. La prima attività è discovery: enumerare, interpretare, raggruppare e costruire un piano, senza trasferire o cancellare.

L'evidenza AP-013 registra un dry run su dati reali. Vengono individuate undici sessioni relative al target LDN 1320 e ai frame di calibrazione, comprese tra il 7 e il 17 luglio 2026. Il parsing e il raggruppamento producono zero finding bloccanti nel run finale; alcuni campi opzionali mancanti sono normalizzati come `unknown`.

Il risultato tecnico della discovery è dichiarato passato. Il trasferimento, però, non viene autorizzato da questa stessa evidence.

Questa separazione racconta molto del modello. Il sistema può conoscere la presenza dei dati senza acquisire automaticamente il diritto di copiarli. Può produrre un piano senza eseguirlo. Può dimostrare che il parser funziona senza dichiarare pronto lo storage di destinazione.

La discovery è un atto informativo. Il transfer è un atto operativo con rischi, permessi e controlli differenti.

## Il manifest come memoria portatile

Quando una sessione deve attraversare sistemi diversi, il contesto non può restare soltanto nel database o nel nome della cartella. I manifest rendono la memoria portatile.

Un Session Manifest descrive identità, stato, intervallo temporale, contesto osservativo, configurazione, conteggi e riferimenti. Un Asset Manifest descrive il singolo oggetto digitale, la sua classe, dimensione, locator e stato di integrità. Un Transfer Run Manifest registra pianificazione, copia, verifica ed esito.

Il manifest non sostituisce l'evidence. Descrive un oggetto o una run; non prova da solo che il comportamento sia avvenuto. Lo stato `TRANSFER_VERIFIED`, per esempio, richiede un riferimento alla verifica. Questa regola impedisce che una dichiarazione interna al documento si auto-certifichi.

I contratti sono versionati e tollerano l'evoluzione. I campi sconosciuti non vengono eliminati per rendere l'oggetto apparentemente completo. La storia viene estesa con nuove versioni, non riscritta.

La portabilità non è soltanto compatibilità tecnica. È la possibilità di spostare il significato insieme ai dati.

## La sessione come contratto tra mondi

La sessione collega il mondo fisico dell'osservatorio, il mondo operativo delle procedure e il mondo informativo della piattaforma.

Dal mondo fisico riceve strumenti, condizioni e vincoli. Dal mondo operativo riceve sequenza, authority, eventi e stato. Nel mondo informativo diventa identità, manifest, relazioni, metriche e fonte per catalogo, Warehouse e conoscenza.

Questa posizione la rende un contratto naturale. I sistemi a monte possono produrre eventi e dati senza conoscere tutti i consumer futuri. I sistemi a valle possono analizzare il patrimonio senza comandare gli apparati. La separazione protegge entrambi.

Una dashboard può mostrare una sessione. Un motore analytics può calcolarne indicatori. Un catalogo può renderla ricercabile. Un'AI può riassumerne le evidenze. Nessuno di questi consumer acquisisce per questo autorità sulla cupola o sulla camera.

Il significato viaggia; l'autorità non viene trasferita implicitamente.

## Lezione trasferibile

Ogni organizzazione che raccoglie dati attraverso episodi operativi può trarre beneficio da questo modello. Una sessione può essere una campagna di misura, un turno di laboratorio, un'ispezione, una missione o una finestra di produzione.

Il criterio è riconoscere quando il contenitore fisico non basta più. Se per comprendere un file occorre ricordare chi era presente, quale configurazione fosse attiva e che cosa sia accaduto prima, l'organizzazione possiede già un oggetto logico non formalizzato.

Rendere quell'oggetto esplicito non richiede necessariamente una piattaforma complessa. Richiede un'identità stabile, un confine temporale, relazioni essenziali, stati distinti e fonti dichiarate.

La sessione è il primo passo con cui un archivio smette di essere una raccolta di file e comincia a diventare memoria scientifica.

## Verifica per il lettore

- Le sessioni sono identificate indipendentemente da cartelle e path?
- Una notte che attraversa la mezzanotte conserva un significato coerente?
- Progetto, osservazione, sessione e acquisizione sono distinti?
- La configurazione effettiva è ricostruibile nel tempo?
- Stato operativo, trasferimento, integrità e qualità restano separati?
- I valori mancanti sono espliciti o vengono corretti silenziosamente?
- Un manifest descrive l'evidence senza sostituirla?
- Discovery e autorizzazione al trasferimento sono trattate come decisioni differenti?

Quando una sessione esiste soltanto nel nome di una cartella, il sistema conserva i dati ma delega il loro significato alla memoria umana.

## Fonti del capitolo

- `ADR-001`, Session Layer;
- Capability 001, Observation Session;
- `DSDM-001`, Scientific Data Manager Conceptual Model;
- `DSDM-002`, Logical Data Model;
- `DSDM-003`, Contract and Manifest Model;
- `DSDM-004`, Session Importer Architecture and Safe Transfer Design;
- `E-AP013-SD-001`, Session Discovery Execution Evidence;
- `AP-013`, Scientific Image Repository Architecture;
- `AP-014`, Scientific Observation Catalog and Search.
