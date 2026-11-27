# BKL-046 · Replica su DSG-Shared del confronto di conoscenza v18–v20

Il confronto usa il lettore storico con impronta fissata e gli stessi identificativi su v18, v19 e v20. Per ogni versione verifica le impronte e rilegge identità, criteri e hash delle righe della matrice. Il controllo confronta 4.920 requisiti per ciascuna delle due coppie e ripete le 24 consultazioni in ordine crescente e decrescente delle versioni.

| Confronto | Variazione verificata | Decisioni registrate cambiate |
| --- | --- | ---: |
| v18 → v19 | Un riferimento aggiunto in DrizzleIntegration e collegato a CFA_DITHER_DRIZZLE/3 | 0 |
| v19 → v20 | Nuova evidenza per SATURATION_BLEND/1, nessuna riga dei requisiti modificata | 0 |

Le 12 coppie versione-richiesta producono gli stessi byte logici nei due ordini. La variante errata dell'identificativo viene respinta. Il risultato verifica la compatibilità documentale con un lettore fissato e riproduce il confronto storico sulla VM. Restano da verificare il confronto di decisioni prodotte da modelli, l'effetto di un cambio di adattatore e la prova stocastica. Nessun provider o PixInsight è stato invocato.

Il generatore riceve il protocollo di replica, la directory del corpus estratto e un file di uscita nuovo. L'archivio sorgente H/K conserva le tre versioni, il lettore e i rapporti storici. La pubblicazione GitHub contiene il rapporto e il verificatore.