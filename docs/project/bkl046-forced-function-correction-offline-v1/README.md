# BKL-046 · Candidata per la validazione della risposta IA

La patch agisce al confine di ingresso delle nuove risposte. La chiamata completata deve avere un `call_id` opaco di 1–64 caratteri ASCII alfanumerici, trattino o underscore. La ricevuta registra `callIdSha256`, calcolato sulla codifica JSON canonica dell'identificatore. La Responses API documenta `call_id` per `function_call`. La sintassi qui applicata è una scelta locale che richiede verifica di compatibilità prima dell'attivazione. [Riferimento Responses API](https://developers.openai.com/api/reference/resources/responses/methods/create)

Sia la motivazione sia le limitazioni devono rientrare in 300 punti di codice Unicode, come indicato nelle istruzioni al modello. Il controllo in byte del contratto esistente rimane in vigore. La modifica lascia la rivalidazione dei record storici al contratto precedente. Il digest entra nell'impronta della nuova ricevuta, senza dipendenze da quel campo nelle decisioni già archiviate.

La replica ripete i 24 casi originali. Nei 16 confronti differenziali, sette input in precedenza accettati vengono rifiutati. STOP, TEST e SELECT validi conservano la decisione, compresi i valori ai limiti verificati. Il riuso della stessa prenotazione viene rifiutato da entrambe le versioni in ogni confronto.

Il protocollo fissa il commit sorgente, la patch, lo script di collaudo precedente e il file candidato. Estrarre l'archivio base con l'impronta indicata, copiare le sue fonti in una replica di lavoro sotto `tools/pixinsight/local_pilot` e applicare `research-provider.patch` con terminatori LF. Eseguire dalla radice del pacchetto:

```text
python -I -B -S collaudo-differenziale.py protocollo.json <base-estratta> <sorgenti-candidate> riscontro-replica.json
```

Patch candidata isolata. Il trasporto è simulato. Restano da verificare la compatibilità con risposte reali e la revisione del cambiamento prima di qualsiasi integrazione.
