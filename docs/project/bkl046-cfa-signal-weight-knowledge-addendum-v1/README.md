# BKL-046 · Addendum di conoscenza sulla pesatura stellare

L’addendum aggiorna l’asse CFA_DITHER_DRIZZLE/2 del rendiconto v64 e rimanda alla capsula di conoscenza v1.171. I quattro rapporti dell’addendum sono verificati sui commit GitHub e nelle copie archiviate sul volume della VM ospitato da K: e su H:.

| Acquisizione | Confronto | Riscontro sulle stelle riservate alla verifica |
| --- | --- | --- |
| M51, Canon EOS 6D | Similarità con centroidi della preview | P90 da 0,614 a 0,451 px e da 0,790 a 0,578 px. Il vantaggio rimane escludendo ciascuna delle 12 zone. Con i centroidi G1/G2 l’intervallo del bootstrap spaziale attraversa lo zero. |
| IC 1805, Canon EOS 40D | Affine sui centroidi medi G1/G2 | P90 da 0,378 a 0,366 px. Da 7 a 14 pose entro 0,30 px, su 38. |
| M8–M20, ZWO ASI2600MC Pro | Affine con centroidi della preview | P90 da 0,414 a 0,390 px. Con Huber, aggiungere i pesi abbassa il P90 aggregato e riduce da tre a una le pose entro 0,30 px. |
| M8–M20, stesse pose | Fotometria di apertura prima della ricostruzione | Lo spostamento dei centri è 0,150 px al P90. Le differenze di flusso al P90 restano tra 0,368% e 0,506% nelle due calibrazioni. |

La pesatura resta un comparatore candidato. Le riduzioni del P90 sono specifiche alle combinazioni di camera, campo e metodo dei centroidi. I valori complessivi della registrazione superano la soglia diagnostica di 0,30 pixel. Il risultato fotometrico è una sensibilità alla geometria dell’apertura e richiede ancora un riferimento assoluto indipendente. Per la chiusura dell’asse restano da misurare gli effetti della registrazione e della ricostruzione native a scala comune, dopo revisione e ammissione del launcher esatto.

Il rendiconto v64 conserva tutti i criteri aperti del v63. L’addendum è pubblicato con l’impronta della capsula a cui si riferisce. La capsula e il rendiconto integrale restano nello storage di progetto.
