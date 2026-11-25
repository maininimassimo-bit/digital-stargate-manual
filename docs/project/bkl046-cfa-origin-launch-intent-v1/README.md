# BKL-046 · Comando candidato per la prova di origine XDRZ

Il preparatore associa il batch a una prenotazione della specifica operazione, fissa gli argomenti di PixInsight e restituisce il comando e i byte dell'entrypoint. Verifica l'installazione tramite le tre impronte del piano CFA, il CURRENT.json di R4, piano e manifest, 12 XDRZ e sei FITS. Nei 12 XDRZ controlla anche che i due riferimenti a immagini puntino esattamente ai file previsti. Il percorso di esecuzione previsto è separato da quello del piano v4.

Due invocazioni con lo stesso contesto producono comando ed entrypoint identici. Otto controlli negativi respingono un'operazione o un batch estranei, una prenotazione invalida e cinque sostituzioni simulate dei byte di selettore, script, modulo, XDRZ e FITS.

Il componente legge le fonti e costruisce il comando in memoria. Non materializza l'entrypoint, non usa il registro canonico e non avvia processi. La stringa di prenotazione del test identifica una fixture. Per il lancio servono il parent originale già associato, custodia attiva degli ingressi, attivazione protetta, approvazioni e ammissione del coordinatore. [Catena R4 con testimone](../bkl046-cfa-origin-window-r4-chain-v1/README.md)

Collaudo con Python 3.12 su DSG-Shared. Il programma riceve la directory del kit e il percorso del rapporto nuovo. Rilegge le fonti installate e quelle di studio con le impronte fissate.