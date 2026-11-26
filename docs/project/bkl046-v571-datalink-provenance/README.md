# BKL-046 · Provenienza dei prodotti Gaia DR3 di v571

La capsula locale v571 conserva i riferimenti congelati del prodotto Gaia DR3 4458990005388621952. Il riscontro copre le risposte `votable_plain` XP_CONTINUOUS e XP_SAMPLED di DataLink.

Le risposte archiviate contengono XML identici byte per byte ai riferimenti congelati. I contenitori ZIP archiviati hanno hash diversi. Ripristinando la data e l'ora DOS nelle intestazioni locale e centrale cambiano sei byte per prodotto. I due ZIP ricostruiti raggiungono ciascuno lo SHA-256 storico, verificato rileggendo i file prodotti.

La nuova interrogazione registrata in `riscontro-http.json` ha risposto HTTP 200 con HTML per entrambi i prodotti. La verifica dei byte usa le risposte archiviate. Restano aperte la verifica del contenitore ZIP restituito direttamente da una nuova interrogazione valida e la rilettura completa del supporto remoto della conoscenza.

## Riproduzione offline

Nell'archivio delle evidenze, eseguire con Python 3.

```powershell
python -I -B -S recover_bytes.py replay mirror readback-archiviato replay.json
python -I -B -S recover_bytes.py rebuild readback-archiviato ricostruzione-di-prova
Get-ChildItem ricostruzione-di-prova/*.zip | Get-FileHash -Algorithm SHA256
```

Confrontare `replay.json` con `riscontro-archiviato.json` e i digest dei file ricostruiti con `reconstructedZipSha256`.
