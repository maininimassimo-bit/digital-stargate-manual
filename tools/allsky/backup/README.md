# Snapshot di configurazione Allsky

Copia del produttore di backup usato sul Raspberry il 24 novembre 2026, non un ripristinatore automatico. Richiede il layout Allsky e i privilegi locali autorizzati. [Perimetro, separazione privato/pubblico, download e limiti](../../../docs/operations/allsky-configuration-backup.md).

Produce un archivio privato con configurazione e credenziali locali e un export pubblico separato tramite allowlist/sanificazione. Non versionare mai il privato o gli stati dei candidati. I database sotto config sono acquisiti tramite API SQLite; i due settings mantengono il relativo hardlink quando presente. Include codice/unit della revisione manuale ma non candidati o registro delle decisioni. Non ferma servizi, non aggiorna Allsky e non esegue un ripristino.

Ogni nuovo export richiede verifica dei manifest e un controllo di riservatezza prima della pubblicazione. Un successo dei checksum non dimostra un ripristino integrale riuscito. Il timestamp `meteor_manual_review.new_after` nel metadata rappresenta l’attivazione autorizzata del 24 novembre e non una finestra scorrevole.
