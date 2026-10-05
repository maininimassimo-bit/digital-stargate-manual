# P5 — richiesta scientifica e revisione privata PixInsight

| Campo | Valore |
|---|---|
| Versione | 1.0 |
| Stato | Implemented candidate; release/deployment/live Owner OAT pending |
| Data | 2026-10-05 |
| Perimetro | BKL-049-EXT-PIAI P5; M27, Owner PC, SESSION_ASSISTED |

## Procedura

La pagina [Elabora con PixInsight e IA](../pixinsight-pilot/index.md) è raggiungibile dalla navigazione Osservatorio e dalla galleria. L’Owner accede con Google, seleziona un gruppo di master M27 registrato dal PC, le sessioni già importate, titolo/data e, facoltativamente, l’esatta immagine/versione/workflow pubblicata di riferimento.

Il server verifica catalogo e relativa impronta, sessioni dello stesso target e identità della versione corrente. Conserva lo snapshot privato e crea il job con l’impronta del contesto nella stessa transizione CAS della coda. Il retry dello stesso identificativo conserva la selezione originaria anche se il catalogo cambia; un contenuto differente viene rifiutato. Il browser conserva solo la richiesta ambigua, mai la credenziale Google. Non aggiunge una scadenza.

Il worker riceve il contesto tramite autenticazione dedicata in uscita e confronta l’impronta del manifest locale: ricetta, parametri di background, hash dei quattro master, ruoli, indici immagine e geometria; percorsi e parametri integrali non vengono trasmessi. La verifica precede la preparazione delle copie. La ricetta resta quella M27 revisionata, non un’elaborazione arbitraria proposta da un file caricato. L’assistente attivo avvia lo script nativo preparato sotto supervisione.

La pagina mostra stato, conteggi e contatto PC su aggiornamento esplicito. OFFLINE conserva job/prenotazione; nessuna riassegnazione o elaborazione continua. L’annullamento viene applicato tra processi; quello in corso può terminare. La raccolta richiede conferma che l’esecuzione nativa sia arrestata.

## Consegna e revisione

Un’azione esplicita sul PC riconvalida originali/copie, runtime/journal/checkpoint e tutti i pixel finali, genera una preview JPEG dal checkpoint verificato e invia al servizio privato preview, workflow delle 29 azioni e correlazioni runtime. Il server richiede job COMPLETED verificato e binding worker/lease; valida JPEG, rimuove metadati, legge JavaScript come dati, verifica l’ordine dei processi della ricetta e il job/ordinale/variabili delle correlazioni. Non esegue il workflow.

La ricevuta immutabile collega job, manifest, snapshot catalogo/sessioni, versione di riferimento, hash originale sul PC e hash di preview/workflow/correlazioni. Gli identificatori IMG/VER/WF del risultato sono **identità private del pilota**, non record automaticamente ammessi all’archivio di pubblicazione. Il caricamento separato genera i propri identificatori e conserva i gate esistenti. Nessuna falsa equivalenza fra le due versioni è dichiarata.

Originale XISF e journal completo restano sul PC. Preview, workflow e correlazioni sono conservati soltanto nei due bucket privati esistenti, con backup prima delle scritture; nessun URL pubblico o download anonimo. Il server riporta `WORKER_REPORTED_NOT_ATTESTED`, non un’attestazione indipendente del desktop. Le sessioni rimangono `OWNER_DECLARED`; il workflow ha scope `RUNTIME_RECIPE_ONLY`, mentre la History a monte rimane `NOT_ESTABLISHED`.

L’Owner apre l’anteprima, consulta i 29 processi e scarica workflow, correlazioni e ricevuta. Accetta il risultato privatamente oppure registra il rifiuto, con decisione vincolata all’esatto hash della revisione. Una decisione o consegna diversa sulla stessa identità viene rifiutata: per una revisione nuova serve un nuovo job. La valutazione non pubblica, non ritira M27 e non avvia automaticamente un altro lavoro. L’accettazione scientifica reale resta una decisione Owner; non è simulata dai test.

## Comandi locali

Con la configurazione privata P4 e la credenziale DPAPI già autorizzata, caricata solo nell’ambiente del processo:

```text
python -m tools.pixinsight.local_pilot.scientific_delivery register --config <private-config.json>
python -m tools.pixinsight.local_pilot.transport --config <private-config.json>
# Avvio supervisionato del run.js preparato tramite PixInsight.
python -m tools.pixinsight.local_pilot.transport --config <private-config.json> --native-stopped
python -m tools.pixinsight.local_pilot.scientific_delivery deliver --config <private-config.json> --job <PIAI_job>
```

Registrazione limitata a otto gruppi immutabili, coda a 16 job e un root/worker nativo attivo. Preview ≤4 MiB, workflow ≤2 MiB, correlazioni ≤256 KiB, richiesta di consegna ≤9 MiB. Nessuna porta in ingresso, credenziale nuova, API IA, polling continuo o nuova risorsa cloud. Costi della stessa infrastruttura già approvata possono aumentare per i nuovi oggetti privati e le operazioni; nessun hard cap è dichiarato.

## Prove e gate

Test locali PASS: 43 Node e 77 Python Windows, MkDocs strict e consistenza roadmap. [Ricevuta minimizzata](evidence/BKL-049-PIAI-P5-2026-10-05.json). Test sintetici di selezione, idempotenza, parent/versione, integrità contesto, consegna/decisione immutabile, ordine dei processi, binding e privacy; HTTP loopback reale con identità sintetiche, distinto da Google/cloud/PixInsight. Test browser sintetici per risposta persa, richiesta congelata, account negato e OFFLINE senza mutazioni automatiche. CI, review ARB/RQ separate e sequenziali, deployment per digest e Pages sul merge SHA precedono il completamento operativo.

La prova reale richiesta è: comando scientifico Owner HTTP/UI → preparazione PC → nuova esecuzione nativa → raccolta verificata → consegna privata → anteprima/workflow/sessioni esatte. Finché questa prova non è registrata, P5 non è dichiarata completata. P6 mantiene errore/annullamento/crash recovery e acceptance complessiva; le prove P4 restano circoscritte ai perimetri già registrati.

## Rollback

Interrompere nuove richieste e cicli prima del rollback; non forzare lo sblocco di un job vivo. Conservare root, binding, prenotazioni, copie, journal, ricevute e bucket/backup. Ripristinare il digest P4 già verificato e ritirare il collegamento P5 tramite revert revisionato solo quando non ci sono job P5 attivi; un job scientifico non deve essere adottato da un worker privo del controllo del contesto. Non cancellare evidence né modificare M27 pubblicata. [Piano](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md), [P4](PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md), [handover](HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md).

Correzioni ARB: le registrazioni condividono il solo oggetto CAS già autorizzato `control/piai-state.json`; nessun ampliamento IAM. Un rifiuto HTTP 400 consente una nuova selezione solo dopo verifica autenticata `JOB_NOT_FOUND`; esiti ambigui conservano la richiesta. Le dipendenze dei master nelle correlazioni cloud sono riferimenti di ruolo associati al digest composto del manifest; il grafo originale con hash individuali rimane sul PC. Regressioni per seconda registrazione, minimizzazione e recupero del catalogo obsolete aggiunte.
