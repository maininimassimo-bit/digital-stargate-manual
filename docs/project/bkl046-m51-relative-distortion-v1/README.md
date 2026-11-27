# Confronto fra modelli di distorsione relativa nelle pose di M51

Il confronto riusa le tre pose RAW Canon EOS 6D e le associazioni Gaia DR3 Lite dello studio dei centroidi. L’analisi precedente viene rieseguita e il rapporto deve coincidere byte per byte. Le coppie conservano rispettivamente 55 e 54 stelle per la stima e 57 e 51 stelle per la verifica. I modelli sono stimati solo sulle stelle di addestramento, con i centroidi della preview a coppie e del fit congiunto G1/G2.

Il termine radiale usa la differenza fra il vettore radiale della posizione sorgente trasformata nel sistema di destinazione e quello della posizione di destinazione predetta dalla similarità. Il centro del rivelatore è fissato dal formato visibile. Il modello quadratico aggiunge tre termini per coordinata. I controlli sintetici confermano la riproduzione di una similarità pura con il termine radiale e il recupero di una trasformazione quadratica nota.

| Posa rispetto alla prima | Centroidi | P90 similarità | P90 affine | P90 con termine radiale | P90 quadratico |
| --- | --- | ---: | ---: | ---: | ---: |
| Centrale | Preview | 0,614 | 0,601 | 0,679 | 0,693 |
| Centrale | G1/G2 | 0,593 | 0,623 | 0,622 | 0,614 |
| Ultima | Preview | 0,790 | 0,846 | 0,793 | 1,134 |
| Ultima | G1/G2 | 0,847 | 0,851 | 0,854 | 0,965 |

Le unità sono pixel nativi. Il termine radiale e i modelli quadratici aumentano il P90 nei quattro confronti rispetto alla similarità. Il risultato riguarda le stelle comuni in tre esposizioni e lascia aperti la misura della distorsione assoluta, il contributo di altri errori locali e la verifica nativa PixInsight. Nessuna combinazione raggiunge il criterio diagnostico di 0,30 pixel.

Per replicare eseguire `misura.py <protocollo.json> <studio-centroidi> <studio-Gaia> <acquisizione-RAW> <sorgente-matcher> <rawpy-estratto> <pacchetti-Python> <directory-DLL-VC> <nuovo-riscontro.json>`.
