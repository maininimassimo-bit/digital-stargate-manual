# BKL-046 · Accordo delle parità verdi M8/M20 per zona

Nel campione di 19 stelle, otto dispongono di un angolo qualificato in entrambe le parità verdi. Tutte e otto concordano entro 15 gradi. Ho riletto gli angoli dei rapporti originali e contato tutte le assegnazioni degli angoli G2 alle stelle G1. L’angolo è assiale e riferito al reticolo di 7,5 gradi già prodotto dal fit. I valori numericamente vicini a un nodo sono arrotondati soltanto entro 10⁻¹⁰ unità di reticolo. [Fit delle parità verdi](../bkl046-m8-m20-psf-cfa-green-parities-v1/README.md)

| Assegnazioni considerate | Totale | 8 accordi su 8 entro 15° | Somma degli scarti pari o inferiore a quella osservata |
| --- | ---: | ---: | ---: |
| Fra tutte le otto stelle | 40.320 | 48 | 16 |
| Solo fra stelle della stessa zona | 48 | 48 | 16 |

Le zone contengono rispettivamente una, una, due e quattro stelle. Entro la stessa zona, ogni assegnazione conserva tutti gli accordi alla soglia di 15 gradi. La distanza angolare totale osservata è 45 gradi e 16 assegnazioni su 48 la eguagliano o la riducono. I conteggi pesano le assegnazioni delle etichette, anche quando due stelle hanno lo stesso angolo.

Le due calibrazioni producono gli stessi conteggi e riusano le esposizioni. Il confronto è condizionato alle otto stelle qualificate e ai loro angoli. Serve a valutare quanto l’accordo distingua le singole stelle entro zona. Restano da verificare l’orientazione fisica, la selezione delle stelle e il trasferimento cromatico. Nessuna esecuzione nativa e nessuna chiusura scientifica.

Per replicare, passare a `misura.py` il protocollo, la directory estratta del kit delle parità verdi e un nuovo rapporto. Il programma verifica il riepilogo e i risultati di dettaglio per impronta.