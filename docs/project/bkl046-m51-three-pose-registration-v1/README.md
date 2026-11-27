# BKL-046 · Registrazione delle tre coppie M51 su stelle comuni

Il confronto riusa le tre pose Canon EOS 6D e le associazioni Gaia già verificate. Ripete il rapporto a monte byte per byte. L'intersezione delle identità nelle tre pose dà 54 stelle di stima e 51 stelle di verifica, disgiunte. Lo stesso insieme vale per tutte le coppie, i centroidi della preview e il fit congiunto G1/G2. Le tre strategie sono pesi unitari, pesi dal segnale e pesi dal segnale con riduzione iterativa dell'influenza dei residui elevati in stima. Un controllo sintetico verifica il recupero della trasformazione dopo lo spostamento artificiale di una stella di stima.

| Centroidi | Pesi | P90 prima → centrale | P90 prima → ultima | P90 centrale → ultima | P90 prima → centrale → ultima | P90 scarto diretto rispetto alla catena |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Preview | Unitari | 0,567 | 0,790 | 0,406 | 0,791 | <0,001 |
| Preview | Segnale | 0,397 | 0,578 | 0,373 | 0,592 | 0,013 |
| Preview | Segnale e residui | 0,377 | 0,709 | 0,392 | 0,676 | 0,045 |
| G1/G2 | Unitari | 0,539 | 0,847 | 0,416 | 0,847 | <0,001 |
| G1/G2 | Segnale | 0,457 | 0,733 | 0,363 | 0,741 | 0,008 |
| G1/G2 | Segnale e residui | 0,451 | 0,640 | 0,390 | 0,628 | 0,025 |

Le distanze sono in pixel nativi. La coppia centrale–ultima, valutata direttamente, rimane sopra la soglia diagnostica di 0,30 px anche nella combinazione migliore (0,363 px). Per la preview il peso robusto migliora la coppia prima–centrale e peggiora le due che coinvolgono l'ultima posa rispetto ai soli pesi di segnale. Le previsioni dirette e concatenate differiscono al P90 di meno di 0,045 px, mentre i residui rispetto alle misure sono maggiori. Poiché le trasformazioni condividono le identità di stima e verifica, il confronto della catena misura la coerenza interna. La registrazione astrometrica e l'accuratezza delle singole misure richiedono evidenza aggiuntiva.

Le tre pose non qualificano M51 come riferimento di rumore CFA a pari risoluzione. La fase fisica, la calibrazione e la registrazione nativa restano aperte. Zero avvii PixInsight e zero chiusure scientifiche.
