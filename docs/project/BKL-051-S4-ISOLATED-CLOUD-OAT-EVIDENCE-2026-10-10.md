# BKL-051 — evidenze del collaudo cloud isolato S4

La coppia concorrente autorizzata è stata eseguita con successo nel nuovo laboratorio isolato. Il servizio è stato arrestato e la sua assenza osservata. Il risultato non chiude l’intera S4 o BKL-051.

## Provenienza e autorizzazioni

Il candidato rilasciato con PR546 resta fissato al merge `c3942103366b0bccb20eb7a534877d96f2e2b4cf`, senza aggiornamento implicito alla main successiva. Dopo distinte autorizzazioni Owner: profilo CLI fresco isolato, preflight in sola lettura, valuta EUR e prezzi effettivi, una build e sole nuove risorse/IAM/policy sintetiche, quindi distinta attivazione/collaudo/arresto. Nessun vecchio profilo/token estratto o riutilizzato. Account Owner e payload privati non pubblicati.

Una sola build SUCCESS. Immagine effettiva vincolata al digest `sha256:fbe5d526a9a726b997a820c67894e0bc88e54348afbab78362b349e6b2edd83d`: manifest, configurazione e layer controllati per hash; metadata dei pacchetti reali google-auth2.61.0/google-cloud-storage3.17.0 e21distribuzioni osservate; 168file tools/sorgente corrispondono agli oggetti pubblici approvati. Verificato il marker overlay opaco della directory tools, non trattato come file sorgente inatteso. Non è scansione vulnerabilità o esecuzione dell’immagine durante l’audit.

## Prova reale e riscontro indipendente

Un deploy, runtime con una CPU/1GiB, concorrenza2 e massimo una istanza/minimo zero; gateway autorizza le operazioni di stato a livello applicativo. Owner completa personalmente Google e preme una sola volta il collaudo. Due esecutori A/B nello stesso container e quattro client GCS distinti: non due repliche Cloud Run. REGISTER e CREATE producono due binding, due job QUEUED, sei tentativi e quattro commit. Ripetizione delle richieste soltanto dopo entrambe le ricevute e conferma della fase, senza nuova scrittura della testa.

Il trasporto runtime conta due upload HTTP412 reali ricevuti dal client, 100invii provider su200 e24richieste HTTP su80 alla ricevuta finale Owner. È evidence del trasporto strumentato, non audit indipendente server del provider. La ricevuta browser e il rapporto TEST_HARNESS_REPORTED mantengono questo limite.

Letture dirette GCS dopo lo spegnimento verificano quattro versioni primarie con le generazioni dei commit, testa finale e relativo SHA256, due binding/due job QUEUED e sei backup letti per generazione e verificati per SHA256. Le due candidate respinte rimangono conservate: non sono teste pubblicate. Questo riscontro è distinto dal contatore interno.

## Arresto, costi e archivio

Processo esterno separato armato e verificato prima del deploy; richiesta finale di arresto, verifica di servizio/sessione/sorgente/immagine, una sola cancellazione del nuovo servizio e lista riuscita vuota dopo lo stop. La ricevuta è OBSERVED_ABSENT_AFTER_STOP senza risposta incerta. Nessun dato cancellato dallo stop. Un processo sullo stesso PC non protegge dal guasto totale dell’host. Nuova fase26invocazioni CLI su40; la build precedente aveva consumato il suo distinto grant40/40.

Prezzi EUR effettivi osservati e preventivo prudenziale complessivo5EUR, limite Owner10EUR. Non è costo fatturato verificato né hard cap Google Billing. Regole di eliminazione a7giorni dei soli nuovi dati sintetici, versioning/soft-delete e applicazione differita possono prolungare la conservazione pagata. Pulizia futura non già osservata; nessuna modifica del progetto condiviso per imporre un cap che interferisca con P6.

Archivio privato102elementi verificati CRC e ogni SHA256, hash `c20dec270e7e4b39881045fbf862d52713c2331edac9e47c97172fd84ba9cdd4`. Esclusi profilo credenziali e directory di payload/token runtime. I log build non restituiscono il testo di installazione e Cloud Logging solo due audit: non inventata una ricevuta pip. Il riscontro delle dipendenze viene dai file dell’immagine. Prima lettura GCS fallita con ambiente Windows ridotto conservata; dopo l’arresto, nuove letture esplicite con ambiente necessario/profilo isolato verificano i dati, senza replay di mutazioni o riattivazione.

## Residui e rollback

S4 complessiva incompleta, S5 non accettata, BKL-051 OPEN / NOT_VALIDATED. Restano copertura dell’intero servizio, pipeline/rapporto scientifici, calibrazione/rumore/provenienza IRSA, timing/frame/matching/covarianze, prove cieche/falsi positivi, oggetti mobili/tracklet, reporting autenticato e policy/accessibilità/accettazione S5. Non estendere questo risultato alla validazione scientifica o ad altre sessioni.

P6 Accepted nei limiti; F4 lifecycle pending, F5 dopo F4 e BKL-050 conclusiva. Nessun PixInsight nativo, fotografia, invio astronomico, dispositivo, Safety/Scheduler o collegamento C→F modificato. Nessuna accettazione piena S4 implicita. Rollback documentale mediante revert e rigenerazione delle proiezioni; dati/evidenze conservati e servizio lasciato spento.

[Evidenza pubblica aggregata](evidence/BKL-051-S4-ISOLATED-CLOUD-OAT-EVIDENCE-2026-10-10.json). [Handover](HANDOVER_2026-10-10-BKL051-ISOLATED-CLOUD-OAT.md). [Candidato e confini](BKL-051-S4-LAB-CLOUD-CANDIDATE-2026-10-09.md). [Mandato](DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md).
