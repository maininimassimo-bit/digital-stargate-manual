# Scala delle mappe di peso CFA in DrizzleIntegration

La documentazione installata di DrizzleIntegration descrive la mappa di peso come normalizzata tra 0 e 1. WBPP legge la finestra identificata da `weightImageId` e la salva come `drizzle_weights`. Le fonti fissate in `fonti.json` documentano quel percorso e il modulo installato. L’esportazione di quella finestra da sola non attesta pesi assoluti.

Il controllo a tre ingressi ha massimi attesi R, G e B di 1, 2 e 1 prima della normalizzazione. Il comparatore confronta la mappa completa di ogni braccio con tre predizioni: scala del modello grezzo, divisione per il massimo dell’intera mappa e divisione per il massimo di ciascun canale. Conserva tutti i riscontri e richiede un profilo coerente nei cinque bracci. Gli esiti della maschera e del pixel azzerato restano leggibili quando una sola convenzione è compatibile. Nessuna convenzione compatibile lascia il caso aperto.

Una stessa mappa normalizzata può derivare da pesi grezzi che differiscono per un fattore positivo. Il rapporto conserva l’eventuale compatibilità con un modello di scala e non dichiara che i pesi grezzi siano stati recuperati. Per la misura assoluta serve una fonte indipendente del fattore o dei pesi originali, da verificare con la prova nativa. Nessun modello di normalizzazione è attribuito al runtime sulla base del collaudo offline.

Per replicare eseguire `classifica.py <pacchetti-Python> <kit-a-tre-ingressi> <nuovo-rapporto.json> --self-test`. Il confronto di mappe fornite usa `--exports <directory-esportazioni>` al posto di `--self-test`.
