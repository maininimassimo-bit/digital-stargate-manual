# BKL-051 — Segnalazioni scientifiche e oggetti mobili

| Campo | Valore |
|---|---|
| Stato | Owner-approved scope — Planned, non implementato o attivato |
| Data | 2026-10-08 |
| Milestone | BKL-051; nessuna milestone separata |
| Decisione | «ok inseriamole nelle funzionalità da realizzare nella milestone» |

## Funzionalità approvate

L'Owner include in BKL-051 la preparazione dei dossier, la selezione del destinatario, l'invio assistito e la possibilità di invio autonomo per canali compatibili, con stato e ricevute. Include il percorso per possibili asteroidi: il controllo di oggetti mobili noti già previsto non equivale alla ricerca e segnalazione di nuovi oggetti. [Evento minimizzato](evidence/BKL-051-OWNER-REPORTING-SCOPE-2026-10-08.json).

L'approvazione estende lo scope da realizzare. Non attiva oggi invii, account, credenziali, nuove risorse, pubblicazione di fotografie, soglie scientifiche o scheduler osservativi. La modalità autonoma è una funzionalità da realizzare e collaudare; resta disattivata fino all'accettazione esplicita della policy quantitativa e delle condizioni di invio. Il percorso iniziale richiede conferma Owner del contenuto e del destinatario esatti. Le autorizzazioni precedenti sulle query e sul trasporto privato non autorizzano una trasmissione scientifica esterna.

## Canali e procedure verificate

Ricerca su fonti primarie l'8 ottobre 2026. Ricontrollare requisiti e formati alla progettazione dell'adapter e prima dell'attivazione; alcune pagine CBAT contengono sezioni storiche sulle supernovae, superate per quel canale dalle istruzioni TNS.

| Tipo | Destinatario | Procedura | Automazione prevista |
|---|---|---|---|
| Possibile nova galattica | CBAT | Email testuale a `cbatiau@eps.harvard.edu`, oggetto informativo; coordinate/equinozio, fotometria/banda, UTC, osservatore, sito e strumentazione, più immagini e controlli su variabili/oggetti mobili, riferimenti con limiti disponibili | Dossier ed email preparati dal modulo; invio assistito. Non è verificata un'API CBAT né un'autorizzazione del destinatario a un flusso autonomo. Non allegare immagini non richieste. |
| Supernova candidata o transiente extragalattico pertinente | TNS | Account registrato, report di scoperta con posizione e fotometria, non-detection misurata oppure informazioni archivistiche consentite; classificazione separata con spettro richiesto | Modulo e Bulk API con bot/API key; test esclusivamente nel sandbox. TNS esclude variabili/CV e nove galattiche: non instradare automaticamente ogni candidato al TNS. |
| Nuova stella variabile | AAVSO/VSX | Account, controllo duplicati, coordinate accurate, identificazioni e curva di luce; revisione dei moderatori | Dossier/esportazione e percorso assistito al modulo ufficiale. Nessuna API pubblica di nuova registrazione verificata: non promettere invio autonomo e non aggirare il modulo con automazione UI. |
| Possibile asteroide | Minor Planet Center | Astrometria finale, tempi corretti, sito/codice osservatorio e intestazione; ADES XML/PSV preferito. Normalmente almeno tre osservazioni per oggetto/notte; dimostrare qualità su oggetti noti prima delle scoperte | Validazione ed export ADES, invio HTTPS e ricevuta. Endpoint di test separati, mai prove sugli endpoint produttivi. ACK/CurlID non certifica qualità, nuova scoperta o assegnazione di designazione. |

NASA/ESA restano fonti scientifiche: non costituiscono un destinatario universale delle scoperte. «Nuova stella» non è una categoria automatica di invio: una sorgente senza corrispondenza resta da identificare; assenza di catalogo non prova nuova formazione stellare o nova.

## Incrementi dentro le fasi esistenti

| Incremento | Risultato richiesto |
|---|---|
| S1-R — contratto di segnalazione | Schema per ogni destinatario, authority per invio/pubblicazione, identità e credenziali, requisiti osservativi e condizioni di uso; policy autonoma definita e approvata soltanto dopo validazione. Decisioni architetturali necessarie registrate prima di implementare adapter esterni. |
| S3-M — oggetti mobili | Rilevamento/associazione temporale su esposizioni singole o dati adatti, tracce e tempi, confronto con oggetti noti, controlli reali di qualità, recupero e falsi positivi. Un master integrato o una foto estetica non prova moto/orbita. Nessuna acquisizione o comando agli apparati. |
| S4-R — dossier e invio | Dossier per canale con provenienza e hash; anteprima Owner di autore/destinatario/dati esatti, conferma associata all'hash; invio assistito, ricevute e stato riconciliato; modalità autonoma condizionata e inizialmente disabilitata per i canali ammessi. Nessuna promessa di API non verificata. |
| S5-R — accettazione | Prove dei formati, test provider quando disponibili, duplicati/timeout/risposta persa/rate limit, istruzioni operative e revoca; collaudo Owner delle modalità. Chiusura BKL-051 include questi nuovi requisiti; non basta consegnare il comparatore. |

Ordine: contratto e base scientifica validata → percorso assistito testato → policy autonoma e sua accettazione/attivazione per canale. Nessuna data aggiunta; BKL-050 resta conclusiva dopo BKL-051 e le altre dipendenze.

## Invarianti e criteri di collaudo

- Misure da dati scientifici appropriati con UTC, banda, qualità e provenienza; mancanze esplicite, mai valori inventati. Distinguere candidato, segnalazione e conferma esterna.
- Verifica di duplicati aggiornata prima dell'invio; dossier immutabile e ledger locale con destinatario, hash, identità dell'autore, evento di autorizzazione/policy, tentativo, risposta e identificativo esterno. Una modifica del contenuto invalida la precedente conferma.
- Stato minimo: bozza, da verificare, pronto, autorizzato, invio in corso, ricevuto, rifiutato, esito da riconciliare, confermato esternamente. Lo stato «ricevuto» non diventa «scoperto» o «confermato».
- Risposta persa o timeout dopo trasmissione: riconciliare l'esito; nessun reinvio cieco che possa creare duplicati. Rispettare limiti del provider e conservare i tentativi falliti.
- Separare credenziali esterne da Google Owner/worker PIAI/transient; nessun segreto nel frontend, dossier pubblico, repository o log. Account e policy di invio richiedono decisioni concrete prima dell'attivazione.
- Trasmettere soltanto i campi richiesti e approvati; nessun upload automatico dell'intero archivio. La segnalazione può rendere pubblici identità/coordinate/misure: la schermata deve indicarlo prima della conferma. Gallery e segnalazione restano indipendenti.
- Invio autonomo: canale ammesso, policy approvata/versionata, validazione positiva, dati completi, duplicati controllati e revoca disponibile; se manca un requisito, restare in revisione. Nessuna soglia inventata da questo piano.
- Rollback: disabilitare nuovi invii, conservare ledger e ricevute, riconciliare quelli in corso. Non promettere che un revert ritiri segnalazioni già consegnate o pubblicate dal destinatario.

## Fonti primarie

- [CBAT: invio](https://tamkin3.eps.harvard.edu/HowToReportDiscovery.html) e [contenuto dei report](https://tamkin3.eps.harvard.edu/iau/DiscoveryInfo.html).
- [TNS: ambito, report e Bulk API](https://www.wis-tns.org/content/tns-getting-started) e [API/sandbox](https://www.wis-tns.org/content/faq).
- [AAVSO/VSX: submission policy](https://vsx.aavso.org/index.php?view=about.notice).
- [MPC: requisiti osservativi](https://docs.minorplanetcenter.net/mpc-ops-docs/astrometry/reporting-observations/) e [invii HTTPS e test](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/command-line-submissions/).

Questa consegna modifica soltanto pianificazione e governance: nessun messaggio o report inviato, nessun account creato, nessun runtime o risorsa modificato.
