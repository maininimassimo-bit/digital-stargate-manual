# BKL-046 — Rilettura R4 dopo una conferma di rilascio incerta

Il coordinatore R4 scrive la ricevuta di rilascio prima di rimuovere `active.json`. Una ricevuta accompagnata dalla stessa prenotazione ancora attiva indica quindi uno stato intermedio. Il verificatore classifica separatamente questo caso, un rilascio ordinario con record concordanti, una disposizione amministrativa e uno stato indeterminato.

Il controllo verifica l'impronta del coordinatore installato e confronta due letture stabili dello stesso insieme di file. Correlazione, istanti e identità sono verificati rispetto alla prenotazione richiesta. La doppia lettura è un'osservazione senza blocco e non garantisce che il registro non evolva in seguito. L'eventuale impronta del record del padre, già conservata in precedenza, si può richiedere come riscontro aggiuntivo. Il programma non decide nuove ammissioni e non ritenta un rilascio.

| Controllo su DSG-Shared | Esito |
| --- | --- |
| Prenotazione storica BKL-046 | Disposizione amministrativa, nessun rilascio ordinario attestato. Acquisizione e record attivo conservato coincidono. |
| Rilascio storico di controllo R4 | Acquisizione, padre originale e rilascio concordano. La stessa prenotazione non compare come attiva nelle letture. |
| Collaudo con record sintetici | 19 casi, incluso il rilascio scritto con `active.json` ancora presente, ricevute contraddittorie e padre assente o difforme. |

L'esito del controllo R4 riguarda i record della prenotazione storica, non la validazione scientifica. Il registro canonico è stato letto senza modifiche. La candidata Stream34 v11 resta in attesa delle revisioni e dell'ammissione.

| Evidenza | SHA-256 |
| --- | --- |
| Verificatore | `0f24b188df8d36a586b77080102e2fb7c2f763688b91080c914f227719a6aa38` |
| Collaudo | `8a4995329e1e4338c169ef22833e32a9fd7ace4b1d316af34f080e300168bf19` |
| Riscontro storico BKL-046 | `47fa2f66cf674d512e032190a02e2b475dff2718c62e9a38e47c926410c85de7` |
| Archivio riprodotto da H: | `e84d7126ab9ca70bf492c9a379612fc9e9544162a2c2d2d97160960caa66e2c1` |
