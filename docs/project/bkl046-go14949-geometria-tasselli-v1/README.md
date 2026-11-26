# BKL-046 · Sensibilità della prequalifica geometrica GO14949 ai tasselli

Il controllo riproduce integralmente i rapporti delle due pose F606W da 400 s. Sul sensore 2 ricalcola il P90 dopo avere tolto, solo per diagnosi, un tassello di verifica alla volta. I modelli e le partizioni di stima restano congelati. Il limite originale è 0,1 pixel.

| Posa e modello | P90 completo | Intervallo P90 togliendo un tassello |
| --- | ---: | ---: |
| Prima, affine | 0,10157 | 0,09671–0,10806 |
| Seconda, affine | 0,10428 | 0,09950–0,11400 |
| Prima, traslazione | 0,09570 | 0,09242–0,09940 |
| Seconda, traslazione | 0,08172 | 0,08117–0,09004 |

Fra i 39 riferimenti comuni alle pose, quattro degli scarti sopra soglia dell'affine compaiono in entrambe. Per la traslazione sono tre. Il risultato mostra una componente di sensibilità al supporto di verifica e scarti che ricorrono fra pose. La ripetizione usa la stessa visita e lo stesso metodo di registrazione.

La traslazione resta un confronto diagnostico. Il piano congelato prevede il modello affine sui tasselli completi. Nessuna esclusione è stata applicata per la prequalifica, che rimane a zero casi ammessi. Eseguire `misura.py --help` per gli argomenti del replay. Le pose, i rapporti, il registro degli assi e i programmi originali rimangono vincolati dagli SHA-256 dei protocolli.
