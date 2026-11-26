# BKL-046 · Confronto a tre livelli di segnale con Roman H4RG

La sequenza GAIN di laboratorio del rivelatore 21816 comprende 21 acquisizioni a 1400 nm. Ho letto gli header di tutte e 21 e segmenti di righe SCI a quattro indici nelle prime 20. Gli 80 segmenti sono stati acquisiti con HTTP 206 e con l’ETag dell’header della stessa esposizione. Gli hash coprono i byte acquisiti. [Sequenza Roman GAIN di MAST](https://archive.stsci.edu/missions-and-data/roman/wfi-triplet-test-data)

Ho confrontato dieci coppie disgiunte di esposizioni. Per ciascuna delle letture 1, 5 e 10 ho sottratto la lettura 0 della stessa esposizione e applicato uno spostamento bilineare di mezzo pixel su entrambi gli assi. Il protocollo fissa tre porzioni all’interno dei canali di lettura. Il canale con indice 15 contiene almeno un campione al limite di rappresentazione in ciascuna esposizione campionata. Ho conservato i 30 confronti esclusi dal calcolo e mantenuto gli altri 60.

| Lettura dalla rampa | Segnale mediano rispetto alla lettura 0 | Errore mediano con pesi completi | Errore mediano con stima diagonale |
| --- | ---: | ---: | ---: |
| 1 | 220 ADU | 24,5% | 66,5% |
| 5 | 1.082 ADU | 15,1% | 62,3% |
| 10 | 2.152 ADU | 13,9% | 61,7% |

La propagazione che include il supporto condiviso dal ricampionamento riduce l’errore mediano a tutti e tre i livelli. Entrambi i modelli usano come ingresso la varianza misurata nella stessa porzione. I livelli sono segnali del rivelatore, condividono la lettura iniziale e restano privi di una misura indipendente della dose. Il test riguarda il rivelatore Roman in modalità differenziale di laboratorio. Restano aperti la qualifica operativa di volo, la risposta ASI2600MC a più dosi, l’operatore nativo e la validazione scientifica.

Per riprodurre offline, estrarre il kit e invocare `misura.py` con la directory del kit, quella delle dipendenze, un nuovo rapporto e lo SHA-256 della cattura `6bf59ebdb660cbd1cd7a6b9d175fc849e61589fd8e47c6e3faf74633fa95bb07`. Il kit contiene tutti i 101 segmenti HTTP e i metadati usati. Il replay verifica i segmenti salvati e i relativi offset FITS.