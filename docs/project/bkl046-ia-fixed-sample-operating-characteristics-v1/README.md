# BKL-046 · Potenza del disegno IA a campione fisso

Il calcolo riproduce le tre soglie storiche 721, 957 e 1.159. Con 70 limiti simultanei illustrativi, ognuno riceve errore unilaterale 1/1.400, pari a 0,05 diviso 70. Per ogni numero massimo di eventi il programma calcola la coda binomiale esatta al rischio limite dell'1%. Verifica con aritmetica razionale che un'unità in meno superi la soglia. Il numero 70 è compatibile con le tre soglie storiche. Questo riscontro aritmetico non approva il numero di endpoint o la loro composizione. [Limiti binomiali esatti](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm)

| Massimo numero di eventi | Unità indipendenti per endpoint | Potenza se il rischio è 0,10% | Se è 0,25% | Se è 0,50% |
| --- | ---: | ---: | ---: | ---: |
| 0 | 721 | 48,6% | 16,5% | 2,7% |
| 1 | 957 | 75,2% | 31,0% | 4,8% |
| 2 | 1.159 | 88,8% | 44,6% | 7,1% |

Per una potenza di almeno 80% per singolo endpoint, la ricerca a campione fisso restituisce rispettivamente 1.159, 1.849 e 5.046 unità, con limiti di 2, 6 e 29 eventi. Le alternative di rischio sono scenari di progetto e non stime osservate. La probabilità che passino simultaneamente tutti gli endpoint dipende anche dalla loro relazione, che qui non è stata specificata.

La prova richiede unità indipendenti, una probabilità comune entro ciascun endpoint e un numero di unità fissato prima degli esiti. Ciascuna unità assegnata entra nel denominatore secondo la definizione congelata. Le risposte parziali conservano sia le astensioni sia le eventuali affermazioni positive infondate. Il rischio di affermazione infondata e il rischio di esito irrisolto restano distinti. I 64 pacchetti storici e le partizioni già esaminate apportano zero unità confermative. Questi calcoli non introducono un nuovo criterio Owner.

Per ripetere usare Python 3.12 con il protocollo, il rapporto sulla provenienza delle partizioni, quello della contabilità Native64 e un nuovo percorso di uscita.
