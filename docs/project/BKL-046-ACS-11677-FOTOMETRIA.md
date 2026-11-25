# BKL-046 — Colori ACS nelle visite 01 e 04 del programma HST 11677

La selezione geometrica iniziale fissava la prima esposizione disponibile per associazione. Nei FITS completi, la posa F606W della visita 01 durava 1 s e quella della visita 04 durava 1.490 s. Il test ha trovato due candidati iniziali e zero candidati proiettabili nella geometria richiesta. Il censimento dei sei membri della prima associazione ha anche escluso un sostituto entro lo 0,1% se si conserva la posa da 1.490 s.

Un nuovo censimento di 68 esposizioni dalle 12 associazioni delle sei visite ha trovato 15 coppie di visite con almeno una corrispondenza di durata in ciascun filtro. Mantenendo fisse le visite 01 e 04, abbiamo scelto prima della fotometria la posa di durata comune maggiore in ciascun filtro, con ordinamento deterministico. Gli otto FITS FLT/FLC confermano 1.457 s per le quattro esposizioni. Gli headerlet collocano 855 punti della griglia sullo stesso semichip WFC1 con almeno 550 trasferimenti di differenza in entrambi i filtri. Le quattro esposizioni condividono la soluzione Gaia e i log di guida riportano FINE LOCK. Per i prodotti ACS e il trattamento dei pixel si applicano le definizioni STScI. [Prodotti ACS](https://hst-docs.stsci.edu/acsdhb/chapter-2-acs-data-structure/2-1-types-of-acs-files) · [Mappe di area dei pixel](https://hst-docs.stsci.edu/acsdhb/chapter-5-acs-data-analysis/pixel-area-maps)

Dei 13.712 candidati iniziali, 1.468 si proiettano nell'area utile e 133 passano i controlli geometrici dopo il ricentraggio. Sette superano anche i controlli fotometrici in tutte e quattro le esposizioni a raggio 3 px. Per questi sette oggetti la mediana del valore assoluto di Δ(F606W−F814W) tra visite è 40,15 mmag per FLT, 39,57 mmag per FLC e 52,83 mmag per FLT con correzione fotometrica CTE parallela. Il valore assoluto diminuisce rispetto a FLT in 7 casi su 7 per FLC e in 5 su 7 per la correzione parallela. Il campionamento privilegia un massimo per cella e il confronto riguarda solo gli oggetti che passano tutti i filtri. [Correzioni fotometriche CTE STScI](https://www.stsci.edu/hst/instrumentation/acs/performance/photometric-cte-corrections)

A raggio 5 px, tutti i 133 candidati geometricamente ammessi hanno almeno un’apertura con pixel esclusi dalla maschera DQ. Il confronto tra raggi e una verifica indipendente su altre visite restano aperti. Il replay sugli stessi byte produce lo stesso SHA-256. Stato BKL-046 invariato con zero chiusure scientifiche e zero esecuzioni native per questo incremento.

| Evidenza | SHA-256 |
| --- | --- |
| Archivio del primo confronto respinto | b6d4ae01fbe1b63fdcc44836a409cd473f3b586800b653d0330fba661c576241 |
| Censimento delle durate | f767afda06343a0594c5c02189e712298bee355c4bc8829db0587b6edb5cf236 |
| Selezione e controllo geometrico delle pose abbinate | 37e1da9f5880304e9d9b67572f82e38b0759b3601150751288c7f3b46bee2ea3 |
| Riscontro fotometrico e replay | 03e227728e6dfad09f717fafcd9e42b6a74e26835146d772a554b8764ea794de |
| Archivio del nuovo confronto | 748ba2c11bfe61c9fe0dd2c25c8c80eefa4565031343b2581b75054752b3f3bd |
