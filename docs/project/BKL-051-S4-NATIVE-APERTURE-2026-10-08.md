# BKL-051 S4 — Produttore nativo di aperture

| Campo | Valore |
|---|---|
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Candidate native kernel adapter; science and operational OAT incomplete |
| Baseline verificata | PR #510 merge `53fb275a117b32adb4312d9672705c522670b2ff`: 19 CI, ARB/RQ, 17 workflow post-merge e sette HTTP/projection PASS |

## Perimetro del produttore

`native_aperture.jsh` usa `PhotometryPixels.FromImage` e `Measure` del motore AperturePhotometry 2.2.0 installato con PixInsight 1.9.5 build 1706. Legge un'immagine monocromatica scelta esplicitamente e coordinate geometriche native; apertura circolare fissa e fondo da annulus, senza PSF adattiva, cataloghi, calibrazione di magnitudini o query. Il motore pesa il bordo con quadratura 8×8: queste somme non sono intercambiabili con le precedenti aperture binarie Python. Non esegue il workflow completo dello script AperturePhotometry. Nessun codice vendor copiato: include la dipendenza installata, con hash verificato prima/dopo; dipendenze standard transitive non archiviate integralmente.

`native_aperture.py` prepara e raccoglie file locali scelti dal coordinatore fidato, senza subprocess, rete, credenziali o input di esecuzione dal portale. Nuova directory esclusiva, copia sorgente verificata, launcher fisso e parametri chiusi con runtime/hash; indice immagine esplicito, linearità solo dichiarata e non attestata. Massimo 1024 target, 100 milioni di pixel e limiti di geometria sono bounds di risorsa, non soglie scientifiche. Copie/manifest/runtime cambiati, replay, parziali e collisioni falliscono conservando i file. In ambiente operativo sono richiesti filesystem quiescente, ACL Owner e unico coordinatore: hash locali non attestano firma, isolamento o resistenza a riscritture coordinate.

## Risultati e conservazione

Ogni target lascia una riga esclusiva, anche se clipped o senza fondo disponibile. Senza fondo il flusso corretto resta null; flussi negativi sono conservati senza inventare un limite di non-rivelazione. Unità `NORMALIZED_SAMPLE_SUM`, rumore del cielo diagnostico; `fullVariance` e `significance` null, stato `NOT_VALIDATED`. Nessuna conversione ADU/elettroni, classificazione, discovery o misura scientifica accettata. I quality counts registrano zero measured, clipped excluded e gli altri incomplete.

Il produttore confronta il buffer dei pixel prima/dopo le letture, salva un checkpoint nuovo e quattro esportazioni History initial/current della vista aperta e del checkpoint. Le letture del kernel non inseriscono Process instances nella History: ricevute, script, runtime e parametri documentano separatamente l'operazione. History di acquisizione a monte non attestata; archivio genitore necessario. Il collector verifica identità, hash, unità, righe e file per target prima di creare un bundle History esclusivo; raccolta ripetuta ammessa solo a byte identici. Errori/cancel locali preservano checkpoint fallito e History quando disponibili. Il marker cancel è locale fidato e controllato ai punti sicuri, non è ancora un cancel remoto autenticato. Errori di parsing prima dell'avvio non possono produrre una receipt nativa: rimangono recovery del supervisore, senza replay implicito.

## Prove eseguite e limiti

Cinque controlli numerici del kernel eseguiti realmente in PixInsight: flusso positivo, negativo, bordo frazionario simmetrico e clipping. 20.480 pixel del buffer invariati, cinque checkpoint e dieci esportazioni History; errore massimo di flusso `3.885780586188048e-16`. Tolleranza `1e-12` per risposte numeriche note, non policy astronomica. Il primo tentativo fallito all'inizializzazione, prima di qualunque misura, resta nell'archivio privato.

Una seconda prova componente usa il produttore candidato e riutilizza il controllo numerico positivo, senza nuove epoche indipendenti: due aperture, un checkpoint, quattro History, cinque eventi journal e quattro ACK outbox in coda MemoryStore. Errore massimo identico, sorgente genitore invariata. Il tentativo iniziale è fallito nel preprocessore PJSR su una regexp contenente slash escape: la correzione conserva lo stesso controllo su path senza quella sequenza. Console osservata, recovery e ramo fallito conservati; nuova directory per la prova corretta. L'istanza creata dalla prova è stata arrestata soltanto dopo receipt/checkpoint o errore osservato conservato. Nessun'altra istanza o originale toccato.

10 nuovi test Node con mock PJSR e otto test Python con XISF/engine sintetici verificano schema, unità sconosciute, replay/cancel, mutazioni, file e History. Suite complessive attese: 65 Node, 68 Python (un test symlink può essere skipped localmente per privilegio Windows); esiti finali CI/review sul commit esatto sono gate, non anticipati. La prova nativa locale con MemoryStore non è OAT cloud autenticata, lifecycle operativo o validazione astronomica indipendente. Non ripete P6, elaborazioni approvate, solves o detection.

## Prossimi gate

Integrazione operativa con supervisore, cancel/crash/lease/recovery server, report scientifico completo e UI/PC/cloud OAT. S1/S2 richiedono ancora full variance/covariance/passband, riferimenti e precisione indipendente, calibrazione e policy Owner; S3 parziale, S4 incompleta, S5 non accettata. Reporting CBAT/TNS/VSX/MPC resta da implementare e autorizzare per l'invio. BKL-051 OPEN, P6 Accepted con limiti, F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva. Nessuna attivazione, credenziale, gallery, root C→F, dispositivo o Safety modificati.

Rollback: revert adapter/collector/test/docs e rigenerare projection, conservando tutti gli archivi senza replay. Gate CI → ARB → RQ sul commit esatto → merge expected-head → workflow post-merge e Pages. [Evidenza minimizzata](evidence/BKL-051-S4-NATIVE-APERTURE-2026-10-08.json).
