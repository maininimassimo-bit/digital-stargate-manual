# BKL-046 · Adattatore con chiamata di funzione obbligatoria

Il collaudo esercita `research_provider.generate`, la decodifica JSON, la costruzione dello schema e il contratto decisionale originali del commit fissato in `protocollo.json`. La procedura verifica le impronte di sette sorgenti prima di caricare le definizioni necessarie, senza inizializzare l'applicazione. Il trasporto e la guida di conoscenza sono fixture locali. Non vengono elaborate immagini.

Su 24 casi, il codice accetta le tre decisioni valide STOP, TEST e SELECT e le due osservazioni riportate sotto. Respinge gli altri 19 casi, due dei quali prima del trasporto. Nei 22 casi che raggiungono il trasporto simulato, registra un solo invio e respinge il riuso della stessa prenotazione nella stessa istanza. Il precedente collaudo di recupero copre il riavvio e la concorrenza separatamente.

- Una risposta con una sola chiamata completata viene accettata anche senza `call_id`. La ricevuta registra l'ID della risposta. L'identità della singola chiamata non è un vincolo di ammissione di questo adattatore.
- Una motivazione di 301 caratteri ASCII supera il limite indicato nel prompt ed è accettata dal contratto. Un testo di 1.502 byte viene rifiutato. Il limite di 300 caratteri è un'istruzione al modello, mentre il controllo locale applica il proprio limite in byte.

Per riprodurre il risultato, collocare in `fonti` i sette file di `tools/pixinsight/local_pilot` al commit nel protocollo e invocare:

```text
python -I -B -S collaudo.py protocollo.json fonti riscontro-replica.json
```

Il collaudo non misura il comportamento del provider, il trasporto HTTP effettivo o la qualità di un'elaborazione PixInsight. Non modifica l'adattatore installato e registra zero chiusure scientifiche.
