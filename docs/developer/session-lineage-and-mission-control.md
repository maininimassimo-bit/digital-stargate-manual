# Catene informative, Mission Control e brand condiviso

| Campo | Valore |
|---|---|
| Identificativo | DSG-PORTAL-LINEAGE-REF-001 |
| Versione | 1.0 |
| Data | 14/10/2026 |
| Stato implementazione | Pubblicato e verificato: PR587, PR588, PR589 |
| Baseline tecnica | Merge `9ea5f2ca377eca2e48af1c081fc64c4e7bb5b582` |
| Perimetro | Consumer pubblici read-only e presentazione MkDocs; nessuna nuova authority |

## 1. Fonti e responsabilità

Questo riferimento descrive l'implementazione effettiva dopo le correzioni del 14 ottobre. Le [ricevute di rilascio](../releases/2026-10-14-session-lineage-and-brand.md) distinguono test, revisioni IA indipendenti, integrazione e verifica online. Non sostituisce AP-013/AP-014, i manifest canonici o l'accettazione scientifica.

| Fonte | Contratto e funzione | Pubblicazione |
|---|---|---|
| `docs/data/scientific-session-catalog.json` | Schema 1.5, `VERSIONED_ANALYTICS_PROJECTION`; sessioni, metriche, metadati, meteo e guida | Projection scientifica versionata aggiornata dalla pipeline esistente |
| `data/sessions/YYYY/MM/SESSION_ID/manifest.json` | Schema 1.0, ID esatto, `report_status=COMPLETE`; inventario documenti/telemetria con size/SHA-256 | Producer EAGLE e commit del pacchetto; fonte canonica |
| `docs/data/session-package-transfer.json` | Schema 1.0, `SESSION_PACKAGE_TRANSFER_PROJECTION`, authority `projection`, scope `SESSION_DOCUMENT_PACKAGE` | Artefatto ricostruito a ogni build Pages; ignorato da Git |
| Gallery pubblica configurata da `docs/data/photo-ingestion-config.json` | `DSG_SESSION_PHOTO_COLLECTION_V1`; immagini/versioni, workflow dichiarati e session IDs | GET anonimo del servizio pubblico esistente; distinto dal deploy Pages |
| `docs/data/scientific-platform-status.json` | Schema 1.0; baseline AP-013, discovery storica, scheduler documentato e boundary | Generatore esistente da fonti governate; non telemetria operativa |
| `docs/assets/images/dsg-brand-mark.png` | PNG trasparente Owner, byte invariati | Asset comune di header Material/custom e favicon |

Il percorso `raw/` nel manifest della sessione contiene log/telemetria del reporting: non implica un inventario dei RAW fotografici. Il manifest di reporting AP-014 è distinto dai manifest scientifici/storage/provenance descritti da [DSDM-003](../architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model.md).

## 2. Dal producer alla pagina

1. Il producer mattutino EAGLE pubblica il pacchetto e il manifest secondo il [runbook AP-014](../operations/AP14-EAGLE-Automatic-Session-Deployment-Runbook.md).
2. `.github/workflows/analyze-session-automatic.yml` reagisce ai manifest, controlla ID/COMPLETE e produce analytics/report/projection nel publish set governato.
3. `.github/workflows/deploy-pages.yml`, unico proprietario del deploy, genera anche la projection dei pacchetti prima del build. `generate-session-package-transfer.mjs` legge gli ID del catalogo e `projectSessionPackage` verifica i file canonici reali con size e SHA-256 streaming.
4. Pages pubblica l'artefatto. I consumer rileggono le projection pubblicate e la gallery corrente. Un rinnovo del browser non genera dati assenti e non sostituisce il completamento della pipeline server.

Il generatore accetta solo identità esatte e inventory non vuoti/bounded; rifiuta oggetti null/malformati, ID discordanti, duplicati, traversal e percorsi fuori repository/sessione. Preservare i byte dei log secondo `.gitattributes` (`data/sessions/**/raw/** -text`): una normalizzazione delle righe può invalidare un hash senza cambiare il significato del testo. Non rigenerare SHA nel manifest per mascherare una discrepanza. I record espongono solo `sessionId`, `scope`, `state`, `manifestRef`, `fileCount`, `verifiedFileCount`.

| Stato pacchetto | Significato |
|---|---|
| `VERIFIED` | Tutti i file di un manifest valido e completo coincidono per dimensione e SHA-256 |
| `INCOMPLETE` | Uno o più file non sono disponibili o non coincidono |
| `INVALID` | Forma, identità, COMPLETE, inventory o percorsi non validi |
| `UNAVAILABLE` | Manifest mancante/non leggibile o lettura non disponibile |

`VERIFIED` non attesta autenticazione del mittente, orario fisico del trasferimento, osservatorio attualmente operativo o copia dei RAW fotografici.

## 3. Dettaglio sessione

`scientific-session-detail.js` usa `DSGScientificDataEngine`, `DSGSessionPublication`, `DSGSessionTransfer` e il routing esistente. Il rinnovo rilegge in parallelo catalogo, gallery e pacchetti, mantenendo lo stesso session ID.

| Passaggio | Derivazione e limite |
|---|---|
| Observation session | Record corrente selezionato con ID esatto e unico |
| Acquisition metrics | `lightCompleted` ed evidence del catalogo corrente; non inventario di singoli binari |
| Scientific assets | Tutte le versioni pubblicate con associazione `OWNER_DECLARED` all'ID esatto; stato parziale perché RAW e contributo dei frame non sono attestati |
| Manifest | Stato del catalogo; distinto dalla verifica crittografica del pacchetto |
| Transfer · pacchetto sessione | Projection dei documenti/telemetria e link al manifest canonico pubblico |
| Processing | Workflow delle versioni associate; capture parziale/non disponibile, esecuzione `NOT_ESTABLISHED` |
| Publication | Versioni attualmente pubblicate associate alla sessione dichiarata dall'autore |

Il target non stabilisce correlazioni: nomi coincidenti, ID simili/sottostringhe e immagini storiche senza session IDs non creano associazioni. I collegamenti gallery fissano sessione e frammento della versione; Session metrics usa il blob GitHub canonico sotto `data/sessions/.../normalized/session-metrics.json`, evitando il precedente404.

## 4. Mission Control

`mission-control.js` e `DSGMissionLineage.describe` aggregano **l'intero catalogo corrente**, non la sola ultima sessione. KPI e sessioni recenti usano la stessa lettura aggiornata.

- Target ed Equipment contano metadati disponibili; Equipment richiede telescopio, camera e filtro.
- Metrics conta `SOURCE_METRICS_AVAILABLE`; Manifest conta `VERSIONED`, senza trasformarlo in prova SHA-256.
- Transfer conta solo i pacchetti `VERIFIED` corrispondenti agli ID correnti, con denominatore esplicito.
- Scientific assets e Publication contano le versioni della gallery con almeno un ID corrente esattamente associato e le sessioni distinte dichiarate. Una versione può essere associata a più sessioni; non contare versioni e sessioni come se fossero la stessa unità.
- Processing conta versioni con passi disponibili e conserva workflow parziale/esecuzione non verificata.

I pannelli AP-013 e Observatory overview rileggono la projection governata esistente. Discovery 203/203 è evidence del **4 agosto 2026**; l'accettazione AP-013B documenta `COPY_ONLY`, `MaxFilesPerRun <=30`, SHA-256, no-overwrite e no-source-cleanup. Il trigger 07:30 è documentato come storico: la [fonte scheduler](../architecture/validation/AP-013-Morning-Transfer-Scheduler-Evidence.md) distingue avvio 07:30–08:05 e completamento previsto entro 08:15. Questi orari non sono presentati come nuova osservazione del runtime EAGLE o del producer documentale AP-014. Safety Authority locale è un vincolo architetturale, non uno stato safety corrente.

## 5. Freshness, limiti e guasti

Entrambe le pagine rileggono all'inizializzazione, al ritorno di visibilità, ogni **60 secondi mentre visibili** e con il rispettivo pulsante manuale. Le letture concorrenti sullo stesso controller sono soppresse. Una root staccata non riceve risposte tardive; timer/listener vengono rimossi. Integrazione con component registry/Instant Navigation conservata.

| Lettura | Timeout | Limite byte e vincoli |
|---|---|---|
| Catalogo corrente | 15s | 16 MiB; same-origin, no-store, credentials omit, redirect error; schema 1.5, <=1000 record oggetto, identità uniche |
| Configurazione gallery | 10s per fetch/body | Abort deadline; la configurazione non è un inventario scientifico |
| Gallery | 10s dopo configurazione | 2 MiB; no-store, credentials omit, redirect error; validazione collection/record/preview/version/workflow |
| Pacchetti | 10s | 1 MiB; same-origin, no-store, credentials omit, redirect error; <=1000 record, scope/count/manifestRef coerenti |
| Baseline AP-013 | 10s | 128 KiB; same-origin, no-store, credentials omit, redirect error; authority non-runtime e vincoli validati |

Nel dettaglio, la risoluzione iniziale dell’ID passa prima dallo store esistente `getSessions/getSession`: `loadCatalog` mantiene cache con `maxAgeMs=Infinity` di default e non imposta una deadline propria. I limiti15s della tabella riguardano la successiva lettura corrente `getCurrentSession`, che aggira quella cache. Il timer si avvia dopo la risoluzione iniziale; un bootstrap catalogo bloccato non equivale a un rinnovo riuscito. Mission Control usa direttamente `getCurrentSessions`.

Configurazione e gallery sono due fasi consecutive: il rinnovo complessivo può attendere fino alle rispettive scadenze, non un unico timeout10s. Le altre fonti sono lette in parallelo.

Le attestazioni precedenti della catena, i link e i nodi di pubblicazione vengono rimossi prima della rilettura. Una lettura riuscita ma vuota è distinta da una fonte non verificabile. Il ritiro di un'immagine rimuove asset/pubblicazione al successivo rinnovo. Un errore gallery non annulla catalogo/pacchetto; un errore catalogo impedisce di dichiarare corrente la catena del catalogo. Nel dettaglio i metadati generali conservati sono qualificati come ultima lettura; Mission Control cancella KPI e associazioni non calcolabili. Una baseline operativa non disponibile cancella i valori precedenti, senza fallback positivo.

## 6. Logo e layout

L'asset condiviso è PNG RGBA 1254×1254, SHA-256 `15c42df78d0dad73350005c6a2022f4a50174cca5526c95eb9c71fe73a51e52a`, identico all'originale fornito dall'Owner. Non è stato modificato o rigenerato.

`mkdocs.yml` lo usa per logo/favicon; `page-enhancements.js` usa lo stesso percorso anche come fallback. `enterprise-navigation.css` applica `object-fit:contain`, dimensioni desktop 2.75 rem e logo Material mobile 1.8 rem sotto 62 rem; attributi immagine44×44 e shrink0 riducono shift/deformazioni. I px effettivi dipendono dal font-size del tema: nei controlli registrati55 px desktop/36 px mobile. Titolo e descrizione delle tile Mission Control sono blocchi separati con wrapping di ID/testo lungo. Tema chiaro/scuro e layout390 px verificati nei limiti delle ricevute.

## 7. Verifica e manutenzione

Eseguire dal root del repository:

```text
node --test .github/scripts/test-scientific-session-publication.mjs .github/scripts/test-session-package-transfer.mjs .github/scripts/test-scientific-session-detail-routing.mjs
node .github/scripts/generate-session-package-transfer.mjs --write
node .github/scripts/generate-session-package-transfer.mjs --check
node .github/scripts/generate-scientific-platform-status.mjs --check
node .github/scripts/generate-roadmap.mjs --check
node .github/scripts/verify-roadmap-consistency.mjs
node .github/scripts/verify-no-inline-portal-js.mjs
python -m mkdocs build --strict --config-file mkdocs.pages.yml
python .github/scripts/verify-published-site.py --site site --base-path /digital-stargate-manual/
```

Non committare `session-package-transfer.json`: è un artefatto di build. Le modifiche di dati canonici seguono la propria governance; l'integrità non si ottiene cambiando uno stato nella projection.

Controlli browser: ID esatto19–20 settembre, M27/versione/workflow, manifest6/6, rinnovo manuale e timestamp automatico senza interazione per almeno un minuto; Mission Control con denominatori e pannelli storici. Ritiro/errori/ripristino si provano con fixture isolate o test, non alterando record pubblici. localhost può non leggere la gallery per la policy di origine: registrare il limite e verificare infine Pages dalla sua origine autorizzata. Verificare anche layout e link alle fonti. Nessuna operazione PC/EAGLE è richiesta per questo consumer.

## 8. Rollback e residui

Revert normale del package interessato e nuovo deploy Pages; validare artefatto e fonti/URL dopo il ripristino. Conservare sessioni, gallery, originali e servizi privati; non eseguire cleanup, force push, task runtime o reingestion come parte del rollback UI. Una regressione del brand si ripristina nella configurazione/asset condivisi.

Restano non attestati l'inventario fotografico completo per sessione, il contributo dei frame e l'esecuzione completa del workflow pubblico. I conteggi nelle ricevute sono snapshot datati, non costanti da reinserire nelle pagine. Le correzioni non chiudono BKL-050, non promuovono accettazione scientifica M27/P6/BKL-051 e non concedono comandi/safety authority.

## 9. Promozione sessioni e calibrazioni — correzione 15 ottobre 2026

Il pacchetto EAGLE arriva nel ramo session/ID. La promozione usa ora main
corrente e un merge limitato a pacchetto/report della sessione, con manifest
COMPLETE, hash e dimensioni verificati. Un aggiornamento concorrente di main
si ritenta senza force push; conflitti o modifiche fuori scope bloccano.
L'analisi e la pubblicazione partono su main dopo la promozione. Il workflow
supporta recupero manuale con session_id e rilancio idempotente.

Le evidenze di calibrazione non identificano il target o telescopio LIGHT:
il parser usa i salvataggi scientifici e la camera attiva in quei momenti.
Più strumenti differenti restano indeterminati. Non aggiungere una nuova
configurazione per compensare un accoppiamento errato nel parser.
[Diagnosi, prove e rollback](../project/HANDOVER_2026-10-15-SESSION-IMPORT-RECOVERY.md).

## 10. Contatori LIGHT e stato analytics — 15 ottobre 2026

Gli avvii TakeExposure con ImageType BIAS/DARK/FLAT e varianti DarkFlat
esplicite non sono avvii LIGHT. Completamenti/errori della calibrazione non
modificano i contatori LIGHT. I tipi sconosciuti/privi di tipo mantengono la
precedente interpretazione conservativa; criteri severity invariati.
qualityState eredita analyticsState quando i metadati sono completi: i due
ATTENTION_REQUIRED non sono necessariamente due guasti distinti.
[Audit su tutte le sessioni, correzione e limiti](../project/HANDOVER_2026-10-15-LIGHT-CALIBRATION-AUDIT.md).
