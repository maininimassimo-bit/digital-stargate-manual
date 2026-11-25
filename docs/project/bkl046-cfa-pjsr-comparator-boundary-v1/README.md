# BKL-046 · Dal batch PJSR CFA al comparatore

Il collaudo usa lo script PJSR fissato dalla candidata CFA v4. Un ambiente JavaScript di prova fornisce le API di PixInsight, le finestre e i FITS degli oracoli congelati. Lo script scrive sul file system. Il comparatore del launcher e il verificatore Python leggono i FITS, il log e il marcatore prodotti dallo script.

| Scenario | Marcatore scritto dal batch | Confronto |
| --- | --- | --- |
| Maschera in coordinate rivelatore e origine centro zero | Sì | Accettato |
| Maschera in coordinate riferimento e origine bordo 0,5 | Sì | Accettato |
| FITS dei pesi incompatibile con la maschera richiesta | Sì | Respinto |
| Entrambe le origini geometriche risultano compatibili | Sì | Respinto |
| Terzo caso del batch interrotto | No | Il batch si arresta prima del confronto |

La prova copre il passaggio dei file dal batch al comparatore. I primi due casi confermano che formato dei messaggi e marcatore sono leggibili dal comparatore. I due rifiuti con marcatore presente confermano che il completamento del batch, da solo, non qualifica le misure. Il test non esegue DrizzleIntegration né determina la convenzione in PixInsight. Restano aperte la risposta del runtime nativo, la provenienza dei prodotti dal processo originale e l'ammissione del coordinatore. [Soggetto CFA v4](../bkl046-cfa-v4-review-intake/README.md)

Per replicare, passare al driver Node la directory della candidata CFA v4, il file batch-cfa.js fissato dal soggetto, la directory dei controlli, il Python vincolato, una nuova directory di prova e il percorso del nuovo rapporto. Il driver controlla le impronte degli ingressi dichiarati.