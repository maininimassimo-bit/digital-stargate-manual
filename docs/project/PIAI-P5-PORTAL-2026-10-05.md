# P5 — richiesta scientifica e revisione privata PixInsight

| Campo | Valore |
|---|---|
| Versione | 1.3 |
| Stato | Technical M27 Owner HTTP/UI/native/private-delivery OAT PASS; Owner private result accepted |
| Data | 2026-10-05 |
| Perimetro | BKL-049-EXT-PIAI P5; M27, Owner PC, SESSION_ASSISTED |

## Procedura

La pagina [Elabora con PixInsight e IA](../pixinsight-pilot/index.md) è raggiungibile dalla navigazione Osservatorio e dalla galleria. L’Owner accede con Google, seleziona un gruppo di master M27 registrato dal PC, le sessioni già importate, titolo/data e, facoltativamente, l’esatta immagine/versione/workflow pubblicata di riferimento.

Il server verifica catalogo e relativa impronta, sessioni dello stesso target e identità della versione corrente. Conserva lo snapshot privato e crea il job con l’impronta del contesto nella stessa transizione CAS della coda. Il retry dello stesso identificativo conserva la selezione originaria anche se il catalogo cambia; un contenuto differente viene rifiutato. Il browser conserva solo la richiesta ambigua, mai la credenziale Google. Non aggiunge una scadenza.

Il worker riceve il contesto tramite autenticazione dedicata in uscita e confronta l’impronta del manifest locale: ricetta, parametri di background, hash dei quattro master, ruoli, indici immagine e geometria; nella registrazione e nel contesto non vengono trasmessi percorsi o parametri integrali; il workflow runtime consegnato successivamente conserva i parametri dei processi. La verifica precede la preparazione delle copie. La ricetta resta quella M27 revisionata, non un’elaborazione arbitraria proposta da un file caricato. L’assistente attivo avvia lo script nativo preparato sotto supervisione.

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

Test locali PASS: 43 Node e 80 Python Windows, MkDocs strict e consistenza roadmap. [Ricevuta minimizzata](evidence/BKL-049-PIAI-P5-2026-10-05.json). Test sintetici di selezione, idempotenza, parent/versione, integrità contesto, consegna/decisione immutabile, ordine dei processi, binding e privacy; HTTP loopback reale con identità sintetiche, distinto da Google/cloud/PixInsight. Test browser sintetici per risposta persa, richiesta congelata, account negato e OFFLINE senza mutazioni automatiche. CI, review ARB/RQ separate e sequenziali, deployment per digest e Pages sul merge SHA precedono il completamento operativo.

La prova reale richiesta è: comando scientifico Owner HTTP/UI → preparazione PC → nuova esecuzione nativa → raccolta verificata → consegna privata → anteprima/workflow/sessioni esatte. Finché questa prova non è registrata, P5 non è dichiarata completata. P6 mantiene errore/annullamento/crash recovery e acceptance complessiva; le prove P4 restano circoscritte ai perimetri già registrati.

## Rollback

Interrompere nuove richieste e cicli prima del rollback; non forzare lo sblocco di un job vivo. Conservare root, binding, prenotazioni, copie, journal, ricevute e bucket/backup. Ripristinare il digest P4 già verificato e ritirare il collegamento P5 tramite revert revisionato solo quando non ci sono job P5 attivi; un job scientifico non deve essere adottato da un worker privo del controllo del contesto. Non cancellare evidence né modificare M27 pubblicata. [Piano](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md), [P4](PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md), [handover](HANDOVER_2026-10-05-BKL049-PIXINSIGHT-AI.md).

Correzioni ARB: le registrazioni condividono il solo oggetto CAS già autorizzato `control/piai-state.json`; nessun ampliamento IAM. Un rifiuto HTTP 400 consente una nuova selezione solo dopo verifica autenticata `JOB_NOT_FOUND`; esiti ambigui conservano la richiesta. Le dipendenze dei master nelle correlazioni cloud sono riferimenti di ruolo associati al digest composto del manifest; il grafo originale con hash individuali rimane sul PC. Regressioni per seconda registrazione, minimizzazione e recupero del catalogo obsolete aggiunte.

## Rilascio P5 del 5 ottobre — prova scientifica Owner ancora aperta

PR #485 integrata nel commit `f1a4650dfb8da54c498b763752fd4d5d2b8877ad`: 20/20 check sullo head revisionato, ARB e RQ AI-assistite sequenziali PASS con zero finding residui; 22/22 check post-merge e deployment Pages effettivo SUCCESS. Cloud Build del codice revisionato PASS con 77 test; digest `sha256:b6d14fa1934076f16f0c44721fdc2852dd5e49f68bd21bf3cae0cf54b38e1ee0`, revisione `dsg-pixinsight-pilot-p5-science-01`, traffico 100%. Nessuna nuova risorsa, credenziale o estensione IAM. Registrazione reale di un gruppo M27 dopo verifica dei quattro master e ripetizione idempotente PASS.

La pagina scientifica è pubblicata e aperta; il completamento tecnico P5 richiede ancora accesso Owner sulla nuova pagina, creazione scientifica HTTP/UI, nuova esecuzione nativa e consegna/revisione privata con sessioni esatte. Non sostituire questa prova con fixture amministrative, prove P4 o accettazione scientifica simulata. Le dipendenze dei master nelle correlazioni cloud usano i ruoli, mentre il grafo originale e gli hash individuali restano sul PC. P6 e accettazione scientifica Owner rimangono aperti. La M27 pubblicata non è stata modificata. Questa riconciliazione documentale richiede i propri gate di consegna.

## Compatibilità del target rilevata nel collaudo Owner

Il primo accesso Owner alla pagina scientifica è stato verificato, senza creazione di job: catalogo e galleria usano `M 27`, mentre il gruppo locale registrato usa `M27`. Il confronto letterale della prima versione nascondeva sessioni e parent. La correzione ammette esclusivamente questi due alias per il pilota M27, conserva target e identità originali nel contesto scientifico e non amplia i target o le ricette consentiti. Tre regressioni coprono parent/catalogo con nome spaziato, 16 sessioni e rifiuto di nomi ambigui. Verifica aggiuntiva dei profili pubblici reali in un broker locale sintetico: 16 sessioni e un parent corrente, target originale conservato; non è prova Owner HTTP/nativa. La correzione deve superare CI/ARB/RQ e distribuzione prima del collaudo scientifico; P5 rimane aperta.


## P5 — prova tecnica completa del 5 ottobre 2026

P5 è tecnicamente completata nel perimetro M27 del pilota: richiesta reale dalla pagina autenticata Owner, un gruppo di master registrato, tutte le 16 sessioni M27 e l'esatta versione pubblicata di riferimento; preparazione con verifica del contesto prima delle copie, nuova esecuzione supervisionata in PixInsight sul PC Owner, raccolta verificata e consegna privata. Sono state eseguite 29 operazioni, prodotti 15 checkpoint e verificati tutti i pixel finali del risultato RGB Float32 non lineare 4634×2808. I quattro master sono rimasti invariati. Anteprima privata e 29 passi del workflow sono stati consultati nell'interfaccia Owner. Workflow, correlazioni e ricevuta conservati dal servizio sono stati letti con la CLI amministrativa già autorizzata e confrontati con le impronte e i derivati locali: PASS. Questa lettura è distinta dal salvataggio sul PC tramite i pulsanti del browser. La M27 pubblicata conserva la stessa versione e lo stesso workflow.

La correzione dei soli alias `M27` e `M 27` è consegnata con PR #487: head revisionato `912d433345db0dc053f9e70466c1f2a340b23032`, 9/9 check exact-head, ARB e RQ AI-assistite separate e sequenziali senza finding; merge `85fea6c2955471427a50d93adf01aef2b4808350`, 10/10 check post-merge inclusa Pages effettiva SUCCESS. Cloud Build `60d5ab2b-a855-4da0-ac29-bb2e73d00835` SUCCESS con 80 test; revisione `dsg-pixinsight-pilot-p5-target-01`, digest `sha256:c6a4c7ead3035d896afda66b3f3580473418cb19f9ec92478f7cfb2ecbe9f993`, traffico 100%. Fonte e identità scientifiche originali conservate; nessuna nuova risorsa, credenziale o estensione IAM.

L'Owner ha accettato il risultato privato: `ACCEPT_PRIVATE` osservato nella pagina autenticata dopo la conferma umana del 5 ottobre. Nessun pulsante di accettazione/rifiuto è stato premuto dall'assistente e nessuna pubblicazione è avvenuta. Le sessioni restano `OWNER_DECLARED`, l'evidenza di esecuzione `WORKER_REPORTED_NOT_ATTESTED`, il workflow `RUNTIME_RECIPE_ONLY` e la History a monte `NOT_ESTABLISHED`. L'Owner conferma che entrambi i pulsanti workflow e collegamenti/ricevuta funzionano e salvano i file nella cartella Download (`PASS_OWNER_REPORTED_DOWNLOADS_FOLDER`). È una conferma umana del trasferimento browser → file locale, distinta dalla precedente verifica amministrativa degli asset e senza confronto indipendente degli hash dei file scaricati. La catena tecnica P5 richiesta → nativo → consegna privata → anteprima/workflow è provata. Dopo il ricaricamento della pagina, riaprire «Apri anteprima e workflow» nella sezione Stato delle elaborazioni per riabilitare i download. P6 deve completare acceptance operativa, casi errore/annullamento/offline/crash recovery e rollback secondo il piano, senza confondere i test sintetici con prove reali. SESSION_ASSISTED, zero nuove chiamate API IA; originali e journal completo sul PC. Le precedenti sezioni P5 pending sono snapshot storici superati da questo aggiornamento. La presente riconciliazione documentale conserva i propri gate CI → ARB → RQ → merge → Pages, registrati nella PR di consegna. [Procedura P5](PIAI-P5-PORTAL-2026-10-05.md), [evidenza minimizzata](evidence/BKL-049-PIAI-P5-2026-10-05.json).
