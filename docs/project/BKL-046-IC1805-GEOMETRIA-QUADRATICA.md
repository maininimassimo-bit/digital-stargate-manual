# BKL-046 · Modello quadratico per la registrazione di IC 1805

Sulle 38 pose di IC 1805 oltre il riferimento, il campo quadratico aggiunge i termini x², xy e y² al campo affine. I due modelli usano gli stessi centroidi verdi misurati sui RAW, le stesse stelle di addestramento e la stessa ripesatura di Huber. La verifica conserva le precedenti 40–71 associazioni per posa, su regioni escluse dall'addestramento. La riesecuzione verifica i residui affini già archiviati e un controllo sintetico verifica il recupero dei coefficienti quadratici.

| Modello | P90 complessivo (px nativi) | Pose con P90 ≤ 0,30 px |
| --- | ---: | ---: |
| Affine robusto | 0,463 | 0/38 |
| Quadratico robusto | 0,466 | 0/38 |

Il quadratico riduce il P90 in 17 pose su 38 e peggiora leggermente il P90 complessivo. I termini aggiuntivi non danno un miglioramento riproducibile sulle regioni di verifica di questo campo. Rimane possibile che altri modelli o errori nei centroidi, nell'associazione e nella PSF influiscano sui residui. Il confronto non consente di attribuire il residuo a una causa unica, e non qualifica la geometria per la replica CFA a scala comune. Zero chiusure scientifiche e zero avvii PixInsight.

SHA-256 della ricevuta `0b46f893cf58fd7476a57e03911569f9172285aa7d4c1aef1dd26a85304ddf3a`.
