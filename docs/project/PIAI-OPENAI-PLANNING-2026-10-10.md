# PixInsight — pianificazione OpenAI dalla pagina

| Campo | Valore |
|---|---|
| Identificativo | BKL-049-EXT-PIAI-OPENAI-P1 |
| Versione | 1.0 |
| Data | 2026-10-10 |
| Stato | Candidato implementato; attivazione provider e OAT reale pendenti |
| Autorizzazione | Owner approva integrazione OpenAI e aggiornamento dei documenti, 10 ottobre 2026 |
| Baseline | P6 Accepted con limiti; main di partenza `2edf1131` |
| Perimetro | Pianificazione API, conferma Owner, esecutore nativo supervisionato |

## Stato corrente e risultato previsto

Il pilota accettato usa SESSION_ASSISTED: la chat interpreta il prompt, verifica i master e propone la ricetta. La nuova modalità OPENAI_API_PLANNING trasferisce la pianificazione al servizio già esistente e a un collegamento locale di pianificazione. Non cambia l'accettazione P6, l'archivio BKL-049 o l'assistente deterministico BKL-046. BKL-051 e i suoi residui restano separati.

Il nuovo flusso funziona per i campi configurati e verificati localmente. La preparazione dei mosaici/CFA resta il percorso esistente con le sue conferme. Il collegamento nuovo può pianificare i master preparati solo dopo la loro consegna e verifica; non seleziona pannelli, inventa astrometria o prepara automaticamente un mosaico. Nuovi campi, file ambigui e regioni di fondo non verificate richiedono verifica locale. Non viene dichiarato un servizio universale o un'esecuzione nativa automatica.

## Flusso e responsabilità

1. Owner sceglie OpenAI nella pagina e conferma il trasferimento dei dati. Le richieste precedenti conservano schema e hash originali; la modalità chat rimane disponibile.
2. Il PC legge solo le cartelle esplicitamente richieste e comprese nelle radici locali autorizzate. Un preset privato lega oggetto, ricetta, eventuale ROI verificata e mapping file/indice.
3. Il PC controlla header XISF, ruoli, geometria e integrità. Il fingerprint aggregato degli input resta nel servizio privato e non viene inviato al provider; i percorsi e gli hash individuali restano locali.
4. Il backend riserva durevolmente un solo invio per richiesta prima di contattare OpenAI. La Responses API restituisce esclusivamente numeri di tuning ammessi, motivazione e limiti mediante Structured Outputs.
5. Il backend valida nuovamente il risultato. La ricetta, la ROI e i ruoli restano quelli verificati sul PC. Il PC rilegge gli input e rifiuta qualsiasi cambiamento prima della registrazione del piano.
6. Owner conferma l'hash dell'esatto piano dalla pagina. Solo questo passaggio crea il job con contesto immutabile e `OPENAI_API_PLANNING` nella coda.
7. Preparazione delle copie, avvio supervisionato di PixInsight, raccolta e valutazione privata seguono il percorso accettato. La pianificazione non avvia PixInsight, non applica pixel e non pubblica immagini.

L'IA non verifica disponibilità/licenza dei plugin, linearità, calibrazione, ROI o qualità scientifica a partire dai soli header. I controlli nativi e il giudizio Owner restano distinti. `WORKER_REPORTED_NOT_ATTESTED`, `OWNER_DECLARED` e History a monte `NOT_ESTABLISHED` non vengono promossi dalla risposta del modello.

## Contratti additivi

| Contratto | Comportamento |
|---|---|
| Selection `openaiPlanning` | `{dataTransferConfirmed: true}`; assente conserva SESSION_ASSISTED; valori diversi rifiutati |
| GET `/v1/science/options` | `openaiPlanningEnabled` deriva dalla configurazione backend; nessuna chiave o modello segreto nel browser |
| POST `/v1/worker/science/intakes/{id}/openai-plan` | Credenziale worker, Origin browser vietato; `workerId` ed `evidence` verificati |
| Evidence | Ricetta, ruoli/dimensioni/indici, campo verificato o null, fingerprint aggregato locale; niente binari, percorsi o nomi file |
| Draft | Numeri bounded, rationale/limitations, ricetta e campo fissati, provenienza provider separata |
| Piano registrato | Draft esatto e metadati identici; provenienza inclusa nell'hash confermato dall'Owner |
| Provenienza | Provider, modello richiesto/effettivo, metodo, response ID, usage token, hash di binding/piano/evidence |

I processi e le sequenze derivano dal codice revisionato. Nessun tool OpenAI, codice generato, shell, PJSR arbitrario, endpoint configurabile dal prompt o file remoto viene eseguito. I contratti BKL-046 rimangono advisory; questa estensione usa esclusivamente la pianificazione e l'esecutore PIAI separati.

## Dati, credenziali e retention

Il provider riceve il prompt esplicitamente autorizzato, l'oggetto e metadati minimi/parametri di campo. Nessun upload XISF/FITS/preview in questo incremento. Percorsi, URL e indicatori comuni di credenziali nel prompt sono rifiutati prima dell'invio; questo controllo non è una garanzia universale di riconoscimento dei dati personali. L'Owner deve inserire soltanto il testo destinato al provider.

`store=false` disabilita la memorizzazione applicativa della risposta presso l'API; non equivale a Zero Data Retention né annulla eventuali log di abuso/obblighi del provider. Per la policy applicabile consultare la [documentazione sui dati API](https://developers.openai.com/api/docs/guides/your-data).

Le ricevute nel servizio privato seguono la conservazione già configurata dei bucket con versioning e backup: nessuna nuova cancellazione o promessa di scadenza. Repository e portale pubblicano soltanto codice, contratti, documenti e prove sintetiche. Non pubblicare prompt reali, ricevute ricche, token, chiavi o file scientifici.

`OPENAI_API_KEY` è fornita al processo backend mediante Secret Manager con versione fissata e accesso limitato alla sola identità del servizio. Non usarla nel browser, nel worker PC, nei comandi in chiaro o nel repository. L'attivazione richiede `DSG_PIAI_OPENAI_ACTIVATION=OWNER_AUTHORIZED`, `DSG_PIAI_OPENAI_MODEL` esplicito e `DSG_PIAI_OPENAI_DAILY_LIMIT` da 1 a 16; se manca l'attivazione il runtime precedente resta disponibile. Configurazione incompleta con attivazione presente fallisce all'avvio.

## Costi, duplicati e recupero

Una sola chiamata per intake, massimo 2400 token di output, timeout HTTP 20 secondi, nessun retry automatico del provider e nessuna catena di tool. Il limite giornaliero conta le prenotazioni nella data UTC del servizio, comprese quelle fallite; configurazione prudenziale iniziale: una prenotazione al giorno. La capacità cumulativa resta 16 tentativi sullo stato conservato: nessuna pulizia automatica o aggiramento della capacità. Questo non è un tetto monetario: tariffe del modello, input e costi cloud vanno verificati prima dell'attivazione.

La prenotazione CAS precede l'invio e viene conservata anche dopo timeout, crash o perdita della risposta. Con esito ambiguo compare `AI_REQUEST_RESERVED_NO_RETRY`: richiede riconciliazione amministrativa, mai eliminazione della prenotazione o un nuovo invio della stessa richiesta. Rifiuto/schema/processi/limiti non validi producono `AI_FAILED_NO_RETRY`; non si crea un job. La ripetizione del trasporto restituisce il risultato conservato, senza nuova chiamata. Un draft non può cambiare evidence, modello configurato o tuning dopo il binding.

## Installazione PC e attivazione

Avviare il modulo `planning_agent` con la configurazione worker privata esistente e un nuovo file privato di preset, protetto da ACL. Esempio sintetico:

```json
{
  "allowedMasterRoots": ["F:\\Astrofotografia"],
  "targets": {
    "M27": {"recipe": "M27_LRGB_NONLINEAR_V1", "field": null, "mapping": null}
  }
}
```

Il preset M27 è specifico di quel campo e non prova idoneità di altri master. Per altri oggetti usare ricetta compatibile e `field` verificato con tutti i campi di `worker.field_settings`; il modello non inventa la ROI. Un mapping esplicito è necessario quando nomi/indici non sono univoci.

```text
python -m tools.pixinsight.local_pilot.planning_agent --config <private-worker-config.json> --settings <private-planning-settings.json> --watch
```

Il token worker viene fornito dal wrapper DPAPI esistente per la durata del processo; nessun nuovo recupero o stampa della credenziale. Nessun servizio Windows/scheduled task viene installato da questo codice. Il loop continua finché il processo è attivo, con polling ogni 30 s; il costo cloud del polling deve essere incluso nella configurazione operativa. Ctrl+C ferma la pianificazione senza annullare i job. Il lancio PixInsight resta separato e supervisionato.

Prima del live: fissare modello/costi, inserire il secret protetto, build del codice revisionato, verificare digest e deploy sul servizio previsto; aggiornare prima il worker PC compatibile con la nuova modalità coda. Non riattivare il servizio isolato P6 o il lab BKL-051. Configurazione cloud reale, chiave e OAT provider non sono verificati dal presente candidato.

## Validazione e gate residui

La suite dedicata verifica payload minimizzato, consenso/provider disabilitato, schema/refusal/tool/incomplete, parametri fuori limite, duplicati e concorrenza, cap giornaliero, withdrawal, autenticazione HTTP reale loopback, conferma esatta e fingerprint locale. Provider, Google e storage sono sintetici nelle prove nuove; nessuna fatturazione o elaborazione nativa è attestata dai test.

Le regressioni Python/Node e MkDocs devono essere registrate sul codice finale. CI exact-head, ARB poi Release Quality separate, merge/post-merge e Pages restano gate di consegna. Nessuna review AI-assistita viene presentata come approvazione umana indipendente. Il candidato non è dichiarato produzione accettata.

OAT richiesto: un campo già revisionato, verifica worker → provider reale → piano visualizzato → conferma Owner → copie/nativo supervisionato → risultato privato; verificare assenza di duplicati, usage effettivo, originali invariati e rollback. Non ripetere automaticamente una chiamata ambigua per ottenere un test PASS.

## Rollback e riferimenti

Fermare il nuovo planning agent e rimuovere la sola attivazione OpenAI dal runtime revisionato; conservare tentativi, draft, hash, decisioni e stato. Le richieste API già conservate non diventano richieste chat e non devono essere modificate. Ripristinare un'immagine vecchia soltanto se non esistono job attivi con nuova modalità: il vecchio worker non li comprende. Non ripristinare una vecchia coda, cancellare prenotazioni o sovrascrivere master/output. Rimuovere l'accesso al secret secondo la gestione credenziali quando l'integrazione viene ritirata.

Riferimenti: [pilota](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md), [P6 accettata](BKL-049-EXT-PIAI-P6-CLOSURE-2026-10-07.md), [P5](PIAI-P5-PORTAL-2026-10-05.md), [profili](PIAI-P5B-SOURCE-PROFILES-2026-10-05.md), [ADR-008](../architecture/ADR-008-PixInsight-Provenance-Capture-Strategy.md), [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [autenticazione](https://developers.openai.com/api/reference/overview).
