# BKL-046 · Impronte delle etichette IA prima della valutazione

Un digest calcolato sulle sole quattro etichette binarie lascia 16 combinazioni da provare. Il controllo ha recuperato le etichette di tutti i 32 ticket sintetici da quel tipo di digest.

La candidata lega ogni insieme di etichette al ticket, all'impronta della richiesta, al protocollo e a un valore casuale segreto di 256 bit distinto per ticket. Prima di rivelare le etichette registra una seconda impronta per il manifesto delle risposte terminali. Questa seconda impronta dipende dalla prima. I due riferimenti sono fissati dal collaudo, senza usare firme o marche temporali esterne. Le chiavi aperte e i valori casuali di prova restano in memoria.

La verifica convalida 32 ticket, tra cui uno privo di risposta e uno con risposta malformata. Respinge etichette modificate, una chiave trasferita tra ticket, la scomparsa di una risposta terminale, il riferimento a un altro manifesto, un digest di risposta cambiato e il riutilizzo del valore casuale anche quando si aggiornano i digest. Il rapporto registra le verifiche e non conserva i segreti.

La prova riguarda la coerenza della catena locale. L'ancoraggio indipendente nel tempo, la custodia con accessi separati e la validazione sulle risposte reali rimangono aperti. Nessun provider è stato interrogato e le unità indipendenti confermative restano zero.

Per ripetere usare Python 3.12 con il protocollo, la directory delle richieste sintetiche bilanciate e un nuovo percorso per il rapporto. I valori casuali cambiano a ogni esecuzione. Il rapporto descrive gli invarianti e si riproduce byte per byte.
