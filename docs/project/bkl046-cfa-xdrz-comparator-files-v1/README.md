# BKL-046 · Verifica del comparatore CFA v4 con file su disco

Il collaudo invoca il modulo Node fissato dal soggetto CFA v4 e il verificatore Python previsto da quel modulo. Gli ingressi sono file FITS e righe di console sintetiche. I due controlli validi producono le distinte conclusioni attese per maschera e convenzione geometrica.

| Fase | Esito |
| --- | --- |
| Confronto completo | Due raccolte sintetiche accettate e verificate alla rilettura. |
| Confronto iniziale negativo | Respinti FITS mancanti o in eccesso, evento duplicato o mancante e pesi FITS incompatibili con il controllo. |
| Rilettura negativa | Respinte modifiche distinte al FITS, al log, al marcatore e alla ricevuta dopo un confronto riuscito. |

Le ricevute riguardano la verifica dei file forniti. La provenienza da PixInsight e il legame con una prenotazione reale richiedono il collaudo della catena di custodia durante una prova ammessa. Gli identificativi degli enumeratori usati qui sono valori della fixture. Il collaudo invoca direttamente il comparatore con il verificatore Python già fissato e non ripete l'inventario del runtime effettuato dal preflight. Nessuna attivazione, nessuna richiesta al coordinatore e nessun avvio PixInsight. [Preflight e soggetto v4](../bkl046-cfa-v4-review-intake/README.md)

Per replicare, passare al driver Node la directory della candidata CFA v4, la directory dei controlli XDRZ, il Python fissato dal soggetto, un percorso di lavoro inesistente e un percorso per la nuova ricevuta. Il driver controlla le impronte dei file prima di invocare il comparatore.