# Protocollo nativo e verifiche

## Inventario e ripartenza

Lavorare su copie o nuovi output. Conservare manifest SHA256 degli input, indici delle immagini XISF e collegamento all'ultima versione approvata. Alcuni master XISF contengono un'immagine scientifica e una maschera di autocrop: ispezionarle e selezionare l'immagine corretta, senza interpretare la maschera come un secondo master. La geometria nei nomi dei file può precedere autocrop/drizzle.

Un file RGB debayerizzato non è un master CFA monocromatico anche se la cartella contiene «CFA». Per il debayer serve il pattern effettivo, senza inferirlo dal solo marchio della camera. Per SHO dichiarare la mappatura SII→R, Hα→G, OIII→B e gli eventuali guadagni: colori di presentazione non sono fotometria. Hα stimata da RGB dual-band è una separazione empirica, non un canale Hα puro calibrato.

## Sequenza e parametri

La sequenza dipende dall'oggetto e dai master; prima verificare registrazione, fondo e difetti di acquisizione. Deconvoluzione appropriata ai dati lineari, denoise calibrato, eventuale separazione delle stelle, trasformazioni tonali/cromatiche, contrasto locale mascherato e ricombinazione vanno registrati separatamente. Non applicare BlurXTerminator a uno stretch non lineare per imitare una messa a fuoco migliore.

Per drizzle confrontare anche alla stessa scala angolare e campo. Misurare normalizzazione di flusso e fondo, rivedere i raggi dei processi spaziali quando la scala cambia. Il raddoppio delle dimensioni non prova il raddoppio del dettaglio reale. Non riutilizzare ciecamente i guadagni tra master di integrazioni diverse.

Un confronto denoise deve partire dallo stesso checkpoint con stessi stretch, maschere e stelle. Annotare se il checkpoint è già stato denoisato: allora si confronta una finitura, non una prova indipendente dei motori su dati grezzi. Conservare file modello, versione e impronta verificata con l'algoritmo esplicito. Non chiamare SHA256 un digest SHA1.

## History concreta

Conservare script effettivi e parametri, file di impostazioni, maschere e mappe di allineamento, checkpoint nativi, History esportate, log e terminal receipt. Un factory JavaScript di processi non è necessariamente un replay autonomo: documentare ordine, selezione delle viste e dipendenze esterne. Quando si riparte da un checkpoint pre-deconvoluzione, ereditare solo i suoi predecessori; non concatenare anche i passaggi successivi del vecchio ramo.

I manifest devono distinguere input originali, copie, intermedi, prove e consegne. Verificare gli archivi ed elencare i file grandi mantenuti fuori dallo ZIP. Non cancellare intermedi per liberare spazio senza preservare la riproducibilità richiesta dall'utente.

## Confronto e lettura scientifica

- Verificare orientazione, crop e scala prima del confronto. Rotazione di 180° senza interpolazione solo per le copie di confronto, se necessaria; non cambiare silenziosamente gli originali.
- Mostrare campo completo e ROI al 100% con filamenti, stelle e cielo. Una vista ridotta in HTML non è il 100%: permettere l'apertura del ritaglio nativo.
- Per isolare la nitidezza dai colori usare anche una luminanza di presentazione e una versione con contrasto normalizzato, etichettandole. Queste trasformazioni non misurano la risoluzione ottica.
- Rumore RMS, energia delle alte frequenze e contrasto contengono sia segnale sia rumore; non tradurre la loro variazione in percentuali di «dettaglio reale recuperato».
- Leggere TIFF 16 bit con uno strumento che ne conservi la profondità. Un caricamento PIL RGB può produrre 8 bit. Un memmap manuale è valido solo dopo verifica di compressione, endian, offset, strip e geometria; altrimenti usare un lettore appropriato/PixInsight.
- Misurare NaN/Inf, valori fuori intervallo e clipping per canale, senza nascondere pochi pixel saturi. Controllare anche aloni, ringing, rumore cromatico e perdita delle polveri deboli.
- Zero pixel saturi nel finale non dimostra assenza di saturazione all'acquisizione: ricomposizione stellare e trasformazioni tonali possono abbassare massimi già saturi. Distinguere il controllo numerico dell'output dalla qualità degli input.

## Documentazione ufficiale

Consultare la documentazione del processo installato e, se necessario, i siti ufficiali PixInsight e RC-Astro. Per aggiornamenti usare fonti correnti. Riferimenti utilizzati nel lavoro del 2026:

- https://www.rc-astro.com/blurxterminator-technical-manual/
- https://pixinsight.net/dev/index.php?articles/mldenoise-model-v42-released.26/
- https://pixinsight.net/dev/index.php?articles/pixinsight-1-9-5-lockhart-released.21/

Questi riferimenti non rendono v42 automaticamente l'ultima versione futura.
