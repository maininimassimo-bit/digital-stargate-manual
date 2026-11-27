# BKL-046 · Controllo fattoriale dell'origine XDRZ

Il controllo incrocia le due matrici serializzate dello shear con le due origini dichiarate 0 e 0,5. Mantiene gli stessi tre ingressi CFA, deposito, immagini attese e predicato numerico. Le quattro combinazioni generano tre classi di mappe distinguibili. Le tre ipotesi danno sequenze diverse.

| Matrice | Origine dichiarata | Usa origine dichiarata | Usa sempre zero | Usa sempre 0,5 |
| --- | ---: | --- | --- | --- |
| Centro zero | 0 | Riferimento | Riferimento | Matrice zero letta a 0,5 |
| Centro zero | 0,5 | Matrice zero letta a 0,5 | Riferimento | Matrice zero letta a 0,5 |
| Variante 0,5 | 0 | Matrice 0,5 letta a zero | Matrice 0,5 letta a zero | Riferimento |
| Variante 0,5 | 0,5 | Riferimento | Matrice 0,5 letta a zero | Riferimento |

Rispetto alla mappa di riferimento, i due controlli incrociati cambiano rispettivamente 44 e 52 campioni del supporto RGB. Tra loro ne cambiano 82. I 12 XDRZ di prova conservano le matrici originarie e variano l'origine dichiarata. Il kit contiene i sei FITS attesi. Per una futura prova nativa si classifica ogni mappa rispetto ai tre riferimenti. Una classificazione mancante, multipla o una sequenza estranea alle tre ipotesi resta da risolvere, mantenendo le evidenze.

I valori derivano dal modello poligonale archiviato e riguardano le tre ipotesi definite. La candidata CFA v4 e il suo criterio geometrico restano congelati. Il controllo costituisce una proposta separata per un piano nativo revisionato. Nessuna ammissione richiesta, nessuna esecuzione PixInsight. [Verifica dell'equivalenza](../bkl046-cfa-oracle-margin-v1/README.md)

Il programma riceve la directory del protocollo, la directory dello studio dei margini, la directory degli ingressi CFA a tre pose, il file verifica.py, la directory delle dipendenze e una directory di uscita nuova. Le impronte del generatore precedente e dei prodotti sono nel protocollo e nella ricevuta. Kit di origine SHA-256 107ab838a53abd70ffe4774985714b634c27811e7c91042e914182d6a88bf3c1.