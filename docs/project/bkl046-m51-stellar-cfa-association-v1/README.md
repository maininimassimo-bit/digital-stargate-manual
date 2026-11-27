# Associazioni stellari nel mosaico CFA di M51

Il confronto usa i centroidi sulla media delle due parità verdi delle tre pose originali. I triangoli nelle zone di stima inizializzano la corrispondenza. Le altre zone del riferimento contribuiscono solo alla verifica. Le associazioni di verifica sono confermate con prossimità reciproca e dipendono dalla previsione affine. I tre modelli vengono confrontati sugli stessi abbinamenti. Un controllo con rotazione nota verifica il verso della trasformazione.

| Posa | Stelle in verifica | Rotazione stimata | P90 Traslazione | P90 Similarità | P90 Affine |
| --- | ---: | ---: | ---: | ---: | ---: |
| Centrale | 122 | 0,160° | 6,70 px | 0,59 px | 0,61 px |
| Ultima | 114 | 0,346° | 13,77 px | 0,78 px | 0,83 px |

I residui sono in pixel nativi. La similarità contiene rotazione, scala e traslazione. Per l’ultima posa lo spostamento orizzontale stimato al centro è circa 767 pixel, oltre il limite di ricerca orizzontale di 720 pixel del controllo precedente. Questo fornisce una spiegazione compatibile con il mancato aggancio precedente. Nei due casi l’affine non migliora il P90 rispetto alla similarità sul campione analizzato.

L’analisi dimostra il limite della traslazione semplice per queste associazioni. Il P90 della similarità rimane sopra 0,30 pixel e non qualifica una fase subpixel globale. L’asse resta aperto perché mancano un riferimento astrometrico indipendente, un riscontro nativo e i log di acquisizione per attribuire gli spostamenti al dither.

Per replicare eseguire `misura.py protocollo.json <acquisizione-M51> <rapporto-registrazione-precedente> <rawpy-estratto> <pacchetti-Python> <directory-DLL-VC> <nuovo-riscontro.json>`. Il protocollo verifica le impronte della serie e del controllo precedente.
