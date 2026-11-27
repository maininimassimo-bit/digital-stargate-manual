# BKL-046 · Diagnosi della seconda posa breve e verifica con altro orientamento

L'header di `jdg302cvq_flc.fits` (40 s) registra il mancato riaggancio della stella guida e l'osservazione con i soli giroscopi nei campi QUALCOM1 e QUALCOM2. Il WCS primario riporta un fit GSC242. Nell'altra posa breve del gruppo, `jdg302ctq`, quei commenti sono vuoti e il fit è Gaia DR3. La diagnostica STScI documenta le anomalie di guida ACS. [STScI](https://www.stsci.edu/hst/instrumentation/acs/performance/anomalies-and-artifacts)

Sui soli tasselli di stima, la ricerca di una correzione intera alla semina WCS di B40 entro ±8 pixel per asse ha trovato al massimo 2 centri validi per ciascun sensore, su un minimo di 24. I migliori spostamenti erano diversi fra sensori e a pari merito con altre soluzioni. Nessuna correzione è stata applicata. La prova non misura lo spostamento effettivo del telescopio.

Le cinque pose di riserva hanno lo stesso puntamento nominale del gruppo B40 respinto, con orientamento PA_V3 diverso. Gli header delle due pose corte di riserva non riportano il problema di guida. Il programma originario ha scartato tutti i semi della prima posa corta, 6.086 per qualità e 58 per margine. Una seconda selezione ha applicato l'esclusione DQ del nucleo già prescritta prima di ordinare i picchi, preservando tutti i controlli successivi. Ha trovato 19 e 41 sorgenti fuori dal primo campo studiato, ma zero riferimenti validi in tutte e cinque le pose. Nessun P90 misurabile.

La ricerca successiva richiede un altro set di pose con verifica preliminare della guida e delle sorgenti comuni nelle due esposizioni brevi. L'asse `SATURATION_BLEND/4` resta aperto. Nessuna prova nativa o chiusura scientifica.

| Evidenza riprodotta e archiviata | SHA-256 |
| --- | --- |
| Ricerca della correzione B40 | `db74aa9a170d8cb1cefa281c11a7b8fab9703336f70c4ff16e0da6df082a73b4` |
| Riscontro header delle quattro pose brevi | `42d3465a0ed219976f4a8a0c62075bf446bc2f6c9d15b0ede3a861e8c4564257` |
| Altro orientamento, selezione originale | `f6fdde812e68834234f0880c3dba47f0aff0e10b024fe9abc030211001ea0fdd` |
| Altro orientamento, DQ prima dell'ordinamento | `2b0d8150cb55768cb658da399c43862ef1f3aaf1e86087847481a766872f9b49` |
