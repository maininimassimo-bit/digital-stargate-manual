# SpatialLag — Avvio dotnet nascosto e verifica del lotto 40

| Campo | Valore |
|---|---|
| Data | 12 novembre 2026 |
| Tipo | Correzione operativa locale della presentazione di un sottoprocesso |
| Componente | `spatial_lag_stdin_adapter_g_v1.py` nel workspace scientifico PixInsight |
| Esito osservato | Primo successivo lotto naturale avviato con il sorgente corretto; continuità iniziale verificata |
| Limite | Osservazione campionata e primi blocchi; non completamento del lotto o nuova validazione scientifica |

## Origine e modifica

La finestra intitolata `dotnet`, segnalata circa ogni minuto, è stata ricondotta
alle chiamate ripetute a `SpatialLag.dll` del controller
`continue_spatial_sessions38_45_h_v1.py`, eseguito con `pythonw.exe`.
Non è una seconda attività discovery/import né prova di un timer da 60 secondi.

Il `subprocess.run` dell'adapter aggiunge soltanto
`creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0`.
Il confronto AST conferma che questa è l'unica differenza di codice.
Comando, ambiente, stdin, stdout/stderr e gestione del risultato restano
invariati. Il binario scientifico e gli input non sono stati modificati.

| Artefatto | SHA-256 |
|---|---|
| Adapter precedente conservato | `61acbc6b6ff5dc4cd745ab77a6d91ba1b1e7ea893855fc697347fd1cc2b36a24` |
| Adapter corretto installato | `78c5ac18f7b79697b2543f889a49f3589e03d9437f2c5371d698083caccf4cfb` |
| `SpatialLag.dll`, invariato | `6fc539a880e4170ea2f9c03761195e46eb1e1977dbb6d0bdd09b5a2cf07570b3` |

Le cinque fixture `block-00`, `block-01`, `block-02`, `maximum-positive` e
`signed-lattice-edge` mantengono gli stessi risultati numerici conservati.
Due flussi malformati restano respinti. Il test del lancio conferma che cambia
soltanto il flag e restano preservati gli altri argomenti e il risultato.
Queste sono prove tecniche su fixture, non nuove misure scientifiche.

## Transizione del lotto 39

Il controller PID 77856 era già caricato prima dell'aggiornamento su disco.
Durante l'applicazione è iniziato il lotto 39: il suo protocollo ha registrato
l'hash del candidato presente su disco, mentre il codice precedente era quello
atteso in memoria. Non interpretare quel campo come prova che il controller
fosse già nascosto. Il protocollo originale non è stato riscritto.

La sequenza comprende un ripristino cautelativo intermedio e l'applicazione
finale, registrata alle 21:07:22.725818 Europe/Rome. Sono conservati entrambi
i sorgenti e `activation-and-session39-source-amendment.json`, che esplicita
la differenza tra hash su disco e versione attesa in memoria.
Non è stata eseguita iniezione nel processo, né un arresto o riavvio.
Il lotto 39 ha poi completato i propri 128 blocchi.

## Successivo avvio naturale e continuità

Orari del 12 novembre 2026, Europe/Rome (UTC+1).

| Riscontro | Risultato |
|---|---|
| Lotto verificato | `session-0040` |
| Nuovo controller | PID 32112, padre 84636 |
| Avvio naturale | 22:10:43.191202, successivo alla correzione |
| Hash adapter nel protocollo | Coincide con il sorgente corretto installato |
| SHA-256 protocollo lotto 40 | `493803294a70b3a92e58b2054e98d8453a30fe3efb60ba62d3d35c88f8e8e274` |
| Osservazione finestre | 22:11:49.649–22:17:24.904, 2.106 campioni |
| Finestre `dotnet` rilevate | 0; inventari disponibili, almeno 13 finestre complessive per campione |
| Blocchi controllati nel dettaglio | Primi tre, 8.192 campi ciascuno, stato `COMPLETE_ARCHIVE_MEASUREMENT_AND_RETIREMENT` |
| Controlli delle ricevute | Sequenza, campi, riferimenti hash, stato e margine di spazio non negativo |
| Riscontro successivo, 22:20:39.765026 | 7 blocchi completati, controller ancora attivo, stderr 0 byte |
| Interventi sui processi | 0 arresti, 0 riavvii imposti |

Il confronto temporale è ricavato dai timestamp ISO originali. Sostituisce
il booleano derivato erroneamente dal parsing delle date in PowerShell nel
record grezzo dei processi; entrambi i timestamp originali restano conservati.

## Limiti dell'evidenza

L'osservazione delle finestre è campionata, con intervalli tra le sessioni di
lettura; non è una registrazione continua. Il tentativo separato di catturare
i processi `dotnet` di brevissima durata non ha prodotto record: non dichiarare
una cattura dei singoli figli. Il riscontro combina nuovo avvio del controller,
hash, ricevute dei blocchi e inventari delle finestre.

Le tre ricevute sono state controllate per stato, sequenza e riferimenti;
non è stata ripetuta indipendentemente l'intera analisi scientifica o decodificato
l'intero archivio. I sette blocchi sono il conteggio osservato alle 22:20:39,
non un attestato di completamento dell'intero lotto. Non promuove acceptance,
conoscenza scientifica, milestone, qualità d'immagine o stato del portale.

## Bundle locale, pubblicazione e rollback

Il bundle `work/dotnet-hidden-launch-h-v1`, relativo al workspace scientifico,
conserva i sorgenti prima/dopo, `proposal.json`, `verification.json`,
`applied.json`, `deferred-activation.json`, la nota di provenienza,
`final-verification.json` e le evidenze della verifica successiva:

- `next-batch-watch.jsonl` e `next-controller-start.json`;
- `next-batch-window-observation.json` e `next-batch-process-observation.json`;
- `next-batch-final-verification.json` e `next-batch-continuity-last.json`;
- `VERIFICA-LOTTO-SUCCESSIVO.txt` e `LEGGIMI.txt`.

Questo documento pubblica il riepilogo curato e gli hash tecnici, non i log
grezzi, gli inventari delle finestre, gli input o i risultati scientifici privati.
L'aggiornamento GitHub è documentale: non ridistribuisce il runtime locale,
non ripete il calcolo e non autorizza ulteriori elaborazioni.

Per il rollback operativo seguire il [runbook](../../developer/local-background-launch.md):
verifica dell'hash corrente, ripristino atomico dei soli byte precedenti e
attivazione ai futuri import. Il rollback documentale è il revert della PR;
non implica il rollback dell'elaborazione scientifica.
