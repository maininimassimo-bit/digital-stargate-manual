# BKL-046 · Lettura verificata del puntatore ProcessInstance

Il lettore sperimentale su DSG-Shared legge il puntatore, verifica il manifest e i file previsti per quella versione, poi rilegge il puntatore. Una variazione tra le due letture interrompe l’accettazione della vista. Il controllo di v600 rilegge il registro canonico in sola lettura e verifica il registro requisiti v45 e la matrice v600. I controlli v601 usano le repliche su H: e J: e verificano tutti e tre gli artefatti nuovi della proposta.

| Stato osservato | Esito del lettore |
| --- | --- |
| Registro canonico corrente o replica ripristinata a v600 | Vista v600 accettata |
| Replica v601 con tutti i file conformi | Vista v601 accettata |
| Replica v601 con delta alterato | Lettura sospesa per impronta errata |
| Puntatore parziale o cambiato fra le letture | Lettura sospesa |
| Primo byte bloccato dal writer di prova via UNC | Lettura da J: sospesa, poi riuscita dopo il rilascio |

I dieci casi hanno prodotto lo stesso riscontro con due repliche e il programma conservato su H:. La verifica dei file ereditati oltre matrice e registro v45 è documentata nel [rapporto precedente](BKL-046-V600-ARTEFATTI-EREDITATI.md). Il lettore resta sperimentale. La verifica riguarda l’adozione su copie isolate della vista v601 e non prova che tutti i lettori storici adottino lo stesso contratto. Il registro canonico continua a indicare v600.

| Evidenza | SHA-256 |
| --- | --- |
| Programma di verifica | 15ecf972b852389a933a8291a9b8a04772a2129e41ef0b3485fcc49282055bbb |
| Riscontro replicato | 877b9f320722db44fbeff27c9a71b7f98b090650b57eb45f9ac1d95f19c87a5d |
