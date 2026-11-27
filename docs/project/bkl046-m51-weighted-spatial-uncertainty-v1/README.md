# Incertezza spaziale della registrazione pesata di M51

Il confronto BKL-046 riesegue il calcolo dei pesi dallo studio precedente e verifica il rapporto byte per byte. Usa le medesime 57 e 51 stelle Gaia di verifica. Sul sensore visibile della prima posa le stelle occupano tutte le 12 celle della griglia 4 × 3. Il bootstrap campiona 10.000 volte le celle con reinserimento. Ogni estrazione usa le stesse stelle per i residui pesati e unitari e mantiene fisse le trasformazioni stimate.

| Posa rispetto alla prima | Centroidi | Differenza P90 pesato meno unitario | Percentili 2,5–97,5% della differenza | Intervallo togliendo una cella |
| --- | --- | ---: | ---: | ---: |
| Centrale | Preview | −0,163 | [−0,223, −0,061] | [−0,200, −0,152] |
| Centrale | G1/G2 | −0,011 | [−0,180, +0,192] | [−0,072, +0,037] |
| Ultima | Preview | −0,212 | [−0,392, −0,046] | [−0,243, −0,211] |
| Ultima | G1/G2 | −0,114 | [−0,533, +0,057] | [−0,211, −0,067] |

Le unità sono pixel nativi. Per la preview il miglioramento sopravvive all’esclusione di ciascuna singola cella. Gli intervalli marginali per G1/G2 attraversano lo zero in entrambe le coppie. Per la preview pesata, anche il percentile inferiore del P90 dei ricampionamenti supera 0,30 pixel in entrambe le coppie, con valori di 0,337 e 0,458 pixel. Gli intervalli sono condizionati alle trasformazioni già stimate e a questo campo. Tre pose non quantificano la ripetibilità su campi o camere indipendenti.

Per replicare eseguire `misura.py <protocollo.json> <studio-pesi> <studio-centroidi> <studio-Gaia> <acquisizione-RAW> <sorgente-matcher> <rawpy-estratto> <pacchetti-Python> <directory-DLL-VC> <nuovo-riscontro.json>`.
