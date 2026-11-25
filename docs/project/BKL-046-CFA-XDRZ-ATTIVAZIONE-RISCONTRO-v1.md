# BKL-046 — Verifica dell’attivazione del launcher CFA v3

Su DSG‑Shared sono stati verificati i 21 file del soggetto CFA v3, lo ZIP archiviato su H: e le sei impronte del coordinatore R4 installato. La PR #627 non presenta ricevute di revisione. Il soggetto verificato ha SHA‑256 d7da70e4fcbcc5ea92d54bb4390577d95cdba116447c350b9860b5f9d90c6727.

Per la messa in servizio resta da dimostrare la provenienza dell’autorizzazione. Il launcher riceve dal chiamante l’impronta del documento che contiene le chiavi dei revisori. Il collaudo delle firme verifica la coerenza interna del documento, inclusa la relazione tra RQ e ARB. Serve anche la verifica che il contesto di lancio riceva l’autorizzazione da una fonte gestita separatamente e riconosca le chiavi iscritte per i rispettivi ruoli.

Prima della richiesta di ammissione, la verifica deve includere il rifiuto di una chiave non iscritta, di un’identità di collaudo in produzione e di un’impronta fornita dal chiamante senza autorizzazione gestita. Restano obbligatori il legame al soggetto esatto e il legame della ricevuta RQ alla ricevuta ARB approvata.

Il riscontro su H: ha SHA‑256 0bfaf23107f3ee7302830398a780c3ca52a6ddcba452993cca1612c23166b20b. Nessuna ammissione richiesta e nessun avvio di PixInsight.
