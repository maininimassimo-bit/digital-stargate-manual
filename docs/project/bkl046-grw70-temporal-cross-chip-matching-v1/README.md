# BKL-046 · Confronto delle epoche fra UVIS1 e UVIS2 per GRW+70°5824

Ho incrociato le 70 visite del programma 11907 per le quali è disponibile la stessa procedura di previsione del centro fra bande. Le quattro visite del primo controllo con una procedura diversa restano fuori. Per ogni finestra temporale ho abbinato UVIS1 e UVIS2 una sola volta per visita, massimizzando il numero di coppie e poi minimizzando la somma delle separazioni. L'epoca è la mediana dei tempi di inizio delle tre esposizioni.

| Dati richiesti per coppia | Entro 0,05 giorni | Entro 1 giorno | Entro 7 giorni |
| --- | ---: | ---: | ---: |
| Metadati di entrambe le visite | 14 | 21 | 24 |
| Tre colori a 5 pixel | 2 | 4 | 8 |
| Tre colori sia a 5 sia a 10 pixel | 0 | 0 | 1 |

Nell'unica coppia completa, `ibbsc5` su UVIS1 e `ibbsc0` su UVIS2 sono separate da **4,08 giorni**. La differenza UVIS2 meno UVIS1 nel termine di apertura da 5 a 10 pixel è **+5,40 mmag** in F438W − F606W, **+15,62 mmag** in F438W − F814W e **+10,23 mmag** in F606W − F814W.

Le due coppie entro 0,05 giorni con i soli colori a 5 pixel danno uno scarto F438W − F814W fra −24,46 e −16,46 mmag. Questa misura dipende dal raggio singolo. Le due visite di ciascuna coppia devono avere entrambe le aperture per stimare una differenza del termine di apertura. [Prova di trasferimento fra chip](../bkl046-grw70-cross-chip-aperture-transfer-v1/README.md)

L'abbinamento accorcia la distanza temporale e conserva tutte le esclusioni, ma lascia una sola coppia completa e non isola posizione, PSF e calibrazione. Il confronto non stabilisce quale contributo dipenda dal chip. Zero chiusure scientifiche e zero avvii PixInsight.

Per ripetere, passare a `misura.py` il protocollo, gli ZIP del controllo esplorativo GRW+70°5824, del primo lotto e del censimento rimanente, poi un nuovo file di risultato. Il programma verifica entrambi i rapporti di ogni archivio e controlla l'abbinamento con un caso in cui scegliere subito la coppia più vicina perderebbe una visita.