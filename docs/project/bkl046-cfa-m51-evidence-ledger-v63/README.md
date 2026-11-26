# Riconciliazione BKL-046 dei riscontri CFA di M51

L’indice riconcilia sette rapporti conservati nella PR #627 con i rispettivi archivi sul volume della VM ospitato da K: e su H:. Per ogni rapporto registra il commit, l’identità del blob Git e l’impronta SHA-256. Il programma confronta i byte restituiti da GitHub con il rapporto locale e con il membro dell’archivio. Verifica anche l’integrità delle due copie di ciascuno ZIP.

| Asse | Evidenza aggiunta | Criterio ancora aperto |
| --- | --- | --- |
| CFA_DITHER_DRIZZLE/1 | RGGB confermato nei mosaici RAW completo e visibile in tre pose della Canon EOS 6D, su 159 pose disponibili. | Identità fisica delle parità su camere indipendenti e confronto con riduzione nativa. |
| CFA_DITHER_DRIZZLE/2 | Associazioni Gaia, residui con centroidi verdi, confronto dei modelli geometrici e similarità pesata. P90 pesato della preview pari a 0,451 e 0,578 pixel nativi. | Riscontro indipendente, incertezza di registrazione e misure native a scala comparabile. I P90 superano 0,30 pixel. |

Il rendiconto v63 aggiunge questi riscontri al v62 con un riferimento all’impronta del predecessore. Il perimetro documentato resta di 4.920 requisiti, 14.521 criteri, 25 assi aperti, 19 criteri Owner aperti e zero chiusure scientifiche. La PR ospita l’indice e i rapporti pubblici. Gli archivi delle prove e il rendiconto integrale sono conservati nello storage di progetto.
