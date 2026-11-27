# Recupero di una prenotazione IA BKL-046

Collaudo offline su DSG-Shared del ramo `API_RESERVED` di `ResearchFlowMixin.research_decision` e `_research_complete`. Il protocollo fissa il commit e le impronte delle fonti utilizzate. Il programma estrae i metodi originali e li esegue in processi distinti con una fixture SQLite.

- Se manca la prenotazione o il risultato persistito, il flusso conserva lo stato e rifiuta di ripetere l'invio.
- Una decisione con associazione alterata o una prenotazione pendente cambiata viene respinta.
- Con una decisione STOP valida già persistita, il recupero dopo il riavvio applica una sola transizione. Il caso di cancellazione esercita la chiusura per revisione.
- Due processi sincronizzati prima della mutazione producono una sola decisione applicata. La fixture serializza la mutazione con una transazione SQLite.

Il contatore iniziale della fixture rappresenta una chiamata storica simulata. Le nuove chiamate al provider sono zero. Il collaudo non esercita GCS, il trasporto reale o PixInsight e registra zero chiusure scientifiche.

Per replicare il risultato, usare il file originale `tools/pixinsight/local_pilot/research_flow.py` del commit nel protocollo e la directory di fonti estratta da `BKL046-IA-adattatori-fonti.zip` (SHA-256 `f231dccab0d78d5b2451bbe965fb0af7c70cc2bdb31a0acc1b8d8ea8f944d9ff`).

```text
python -I -B -S recupero.py test protocollo.json research_flow.py <directory-fonti> riscontro-replica.json
```
