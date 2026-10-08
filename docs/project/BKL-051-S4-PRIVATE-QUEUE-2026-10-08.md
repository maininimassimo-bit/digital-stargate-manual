# BKL-051 S4 — Coda privata separata

| Campo | Valore |
|---|---|
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Candidato implementato; collaudo locale sintetico, non attivato |
| Decisione | [Trasporto Owner](evidence/BKL-051-OWNER-TRANSPORT-2026-10-08.json) |

## Decisione e risultato

L'Owner autorizza la proposta concreta: richieste e stato nel portale remoto, immagini e rapporto completo sul PC, identità worker dedicata, estensione separata del servizio HTTPS privato esistente. Nessuna nuova risorsa cloud, bucket o trasferimento di pixel/report completi. Le revisioni ARB/RQ dei successivi incrementi sono autorizzate per tutta BKL-051. Non è accettazione scientifica o operativa finale.

Il candidato aggiunge `TransientQueue` e il namespace HTTP `/v1/transient-analysis`, indipendenti dai job PIAI SESSION_ASSISTED. Il vecchio worker non può usare questo namespace; il nuovo non può usare il vecchio. Google Owner e origine esatta sono verificati dal server con lo stesso controllo esistente. Nessun token Google viene estratto o salvato dall'assistente.

## Contratto implementato

Il worker registra cinque riferimenti opachi immutabili: binding, input, riferimento, algoritmo, contratto. Il registro dettagliato locale deve legarli ai byte, versione, immagine, parent e parametri esatti prima di usarli; il server non attesta questi dati. Il browser invia esclusivamente `requestId` e `bindingRef`. Payload con path, URL, query, comandi, coordinate, campi aggiunti o identificatori sconosciuti sono rifiutati. Riuso identico restituisce lo stesso job `TRN_`; contenuto diverso confligge. Non viene eseguita alcuna analisi dalla sola richiesta.

Il claim lega una root privata e un tentativo alla prenotazione. La lease dura 900 secondi: limite operativo, non soglia scientifica. Un nuovo report RUNNING in sequenza rinnova la lease; un retry identico non la rinnova. Scadenza o regressione dell'orologio comporta RECOVERY_REQUIRED persistito; il tentativo resta conservato e blocca nuove assegnazioni, senza rilancio o riassegnazione automatica. Non esiste sblocco forzato in questo incremento.

COMPLETED è ammesso soltanto dopo RUNNING, con esatto binding, hash SHA256 del rapporto locale e tre conteggi aggregati chiusi. Il server verifica forma e correlazione della ricevuta, non i byte locali o la validità scientifica: ogni vista dichiara WORKER_REPORTED_NOT_ATTESTED e NOT_VALIDATED. Coordinate, misure individuali, immagini, History, maschere e rapporto completo non hanno una route di upload. La vista Owner omette lease e ultimo evento privato.

Cancel di un job queued impedisce il claim. Su un job attivo è una richiesta pendente: il worker deve fermarsi al punto nativo sicuro, conservare checkpoint e confermare CANCELLED o RECOVERY_REQUIRED. Dal cancel pendente non si può consegnare COMPLETED; dopo lo stato terminale sono ammessi soltanto retry identici. Le revisioni Owner KEEP_FOR_REVIEW / REJECT_CANDIDATE / FOLLOW_UP sono immutabili, legate all'hash esatto, e non accettano la milestone né pubblicano una fotografia.

Persistenza in `control/transient-analysis-state-v1.json`, con CAS e copie di recupero immutabili nei due bucket privati esistenti. Massimo 32 binding, 32 job, 32 revisioni/job, 128 report/tentativo e 1 MiB di stato; a capacità esaurita si rifiuta senza eliminare evidenze. Le copie precedono la CAS: una copia non committata resta candidato di recupero, mai current head. MemoryStore e HTTP loopback sono solo fixture; nessun fallback in produzione.

## Attivazione successiva ai gate

In assenza di `DSG_TRANSIENT_ACTIVATION` il namespace resta assente (404) e PIAI invariato. L'attivazione richiede OWNER_AUTHORIZED, nuovo workerId e digest diversi dai PIAI e revisione/test prima di deployment. Credenziale bearer casuale a 256 bit sul PC; solo digest al server, niente token nel portale o repository. Rotazione/revoca esplicita, nessuna creazione automatica. Il servizio usa l'identità runtime esistente; il suo permesso di mutazione dovrà essere verificato ed esteso soltanto alla nuova chiave di controllo. Il bearer applicativo non assegna IAM cloud al PC. Nessun secret, IAM, traffico o risorsa è stato modificato da questo incremento.

Restano da completare adapter e journal locale, verifica dei byte/report, esecuzione nativa, UI Owner e report/esportazione sul PC, IAM/credenziale e TLS reali, Google Owner reale e utenti negati, crash/recovery/cancel reali, accessibilità/regressioni, S2/S3 scientifiche, soglie approvate e S5. Le prove P6 non sostituiscono queste prove. Il percorso completo S4 non è consegnato da una coda.

## Validazione e rollback

Test Python sintetici del lifecycle e HTTP loopback reale: idempotenza/restart, binding e risultato esatti, CAS/concorrenza, backup failure, clock/expiry, cancel queued e RUNNING, immutabilità terminale, capacità, separazione credenziali/ruoli e assenza attivazione. Si eseguono insieme alle regressioni PIAI; CI anche su Windows/Linux. Le ricevute exact-head e post-merge restano nel package di rilascio; nessun PASS anticipato.

Rollback: non impostare o rimuovere l'attivazione transient e revocare il suo digest; ripristinare il digest immagine revisionato precedente, conservando chiave, recovery e archivio PC. Non toccare coda PIAI, fotografie o registri AP-013/AP-014. F4/F5, BKL-050 e S10/Safety invariati.
