# BKL-046 · Ripristino logico del corpus v600

Il verificatore ricostruisce in streaming gli oggetti del corpus v600, controlla lunghezza e SHA-256 e verifica che tutti gli alias logici risolvano a un oggetto del piano depositato. L'identità di un alias è la coppia ruolo e nome. Il rapporto registra l'impronta aggregata delle coppie oggetto/dimensione e quella delle associazioni alias/oggetto, ordinate e serializzate in JSON UTF-8 compatto.

Le verifiche comprendono l'appartenenza esatta al piano e ai pacchetti di trasporto, i nomi degli asset nella release, il contenuto esatto di ciascuno ZIP e l'ordine delle parti dei file suddivisi. Un esito positivo attesta la ricostruzione dei byte e della tabella logica in memoria. I file ricostruiti non vengono scritti su disco.

## Esecuzione

Usare Python 3.12. Passare a `replay_corpus.py` il percorso del piano completo e il relativo SHA-256, poi l'indice e il relativo SHA-256, poi l'inventario di trasporto e il relativo SHA-256. Completare con la directory contenente i soli 80 asset del corpus e il percorso di un nuovo JSON di esito. L'opzione `--local-mirror` crea invece una nuova directory di hard link NTFS a partire dalla replica locale indicata. Il collaudo locale adopera questa opzione e non contatta GitHub.

Per una consegna reale, prima eseguire il [verificatore di rilettura della release](../bkl046-delivery-release-readback-verifier-v1/README.md). Conservare il suo rapporto e la capsula della conoscenza. Predisporre una seconda directory con i soli nomi elencati in `inventario-trasporto.json`, usando copie o hard link sullo stesso volume. Lanciare il ripristino logico su tale directory. Verificare che le due impronte aggregate e tutti i conteggi coincidano con `riscontro.json`. La prova della consegna richiede entrambi i rapporti e il legame con lo stesso inventario. Il piano completo contiene percorsi locali e va conservato con gli altri metadati nella custodia autorizzata.

`test_replay.py` verifica un pacchetto valido e sette rifiuti con piccoli pacchetti autonomi. Il collaudo locale integrale riguarda la consegna documentale. La validazione scientifica e l'ammissione alle prove PixInsight hanno evidenze proprie.