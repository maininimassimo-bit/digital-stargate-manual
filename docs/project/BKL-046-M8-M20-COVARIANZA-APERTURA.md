# BKL-046 · Covarianza e dispersione in apertura nei ritagli CFA

Le differenze fra le due metà da sette pose di M8 e M20 sono ricalcolate con le tre ricostruzioni a scala nativa e le calibrazioni A e B. Si usano otto finestre 7 × 7 a offset fissi da ciascuna stella, esterne all'apertura stellare. Sono ammesse soltanto finestre con tutti i pixel coperti in entrambe le metà per tutti i metodi. Restano 431 finestre R, 426 G1, 430 G2 e 428 B.

La misura somma i pixel del nucleo 3 × 3 o 5 × 5 e sottrae la media del bordo esterno moltiplicata per il numero di pixel del nucleo. Prima della stima della covarianza si centra ogni posizione relativa sulle finestre della stessa parità. Si confronta la deviazione standard empirica della somma compensata con quella ricavata dalle sole varianze per pixel. I controlli verificano la cancellazione di un piano e il rapporto unitario per campioni sintetici indipendenti.

| Nucleo | Riduzione della dispersione in apertura con bilineare rispetto a deposito da 1 px | Rapporto fra dispersione misurata e stima diagonale per il bilineare |
| --- | ---: | ---: |
| 3 × 3 | 23,8–51,5% | 1,49–1,98 |
| 5 × 5 | 44,5–56,0% | 1,23–2,04 |

Gli intervalli riportano il minimo e il massimo sulle quattro parità e due calibrazioni. Il vantaggio del bilineare rimane su queste somme, mentre l'ipotesi di indipendenza fra pixel sottostima la loro dispersione. L'ampiezza della riduzione dipende dalla dimensione dell'apertura. Le finestre condividono campo e pose e possono contenere struttura di fondo o sorgenti deboli. I valori misurano la ripetibilità dello stack e comprendono registrazione, PSF e fondo. L'allargamento del profilo stellare già misurato rende ancora necessario un confronto a risoluzione effettiva equivalente. Zero chiusure scientifiche e zero esecuzioni native.

SHA-256 della ricevuta `218ffd7a24a87da24798e76ee6165f212b96029394a11cbcb89ff6425690b15b`.
