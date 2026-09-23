# BKL-042 — Governed Retrieval and Provenance Increment

| Campo | Valore |
|---|---|
| Stato | **DEPLOYED — owner-witnessed retrieval OAT pending; package remains open** |
| Owner / accountable | Massimo Mainini |
| Authority | bounded read-only; `command_authority=NONE`; `safety_authority=NONE` |
| Provider | relay e selezione modello esistenti; nessuna nuova credenziale o provider |
| Sources | sole proiezioni pubbliche allowlistate indicate sotto |
| Budget | ledger persistente e cap pilota preesistenti, applicati a ogni richiesta |
| Runtime pre-deploy | `dsg-bkl042-ai-relay-00005-d97`, 100% traffic — read-only describe 23/09/2026 |
| First retrieval deployment | `dsg-bkl042-ai-relay-00006-ktv`, 100% traffic — 23/09/2026 |
| Current runtime | `dsg-bkl042-ai-relay-00007-wrm`, 100% traffic — 24/09/2026 |
| Immediate rollback | riportare il traffico a `dsg-bkl042-ai-relay-00006-ktv` |
| Portal ingress | `dsg-bkl042-portal-gateway-00002-m7c`, readiness `READY` |
| Retrieval method | `bkl042-static-projection-retrieval-v2` — compact/spaced astronomical designation normalization |

## Scope

Questo incremento sostituisce la fixture client-side per la consultazione live con
retrieval server-side deterministico. Il browser invia soltanto domanda, modalità e
correlation ID; evidenze e citazioni non possono essere dichiarate dal client. Il
relay non acquisisce file privati, non accede a EAGLE o ad altre API runtime e non
esegue immagini, workflow o azioni.

Durante la transizione della pagina, gateway e relay possono ricevere i vecchi campi
`evidence`/`citations` solo per compatibilità; entrambi li ignorano e il gateway inoltra
al relay esclusivamente i tre campi correnti. Non sono input fattuali in alcuna
versione del retrieval.

Fonti ammesse:

- `docs/data/scientific-observation-index.json`: titolo e keywords sono usati solo
  per discovery/ranking e non vengono passati al modello come evidenza fattuale;
- `docs/data/target-knowledge-read-model.json`: canonical name, aliases e identity
  state; sono esclusi target key/ID, provenance refs e qualsiasi coordinata;
- `docs/data/scientific-session-catalog.json`: solo data osservazione, target,
  analytics/metadata/evidence state, integration hours, completion percentage e
  severity. RA/Dec, local paths, dettagli hardware, rete e telemetry sono esclusi.

I tre URL sono fissati nel relay su GitHub Pages, con timeout e limite di dimensione;
redirect e contenuto non JSON sono rifiutati. Qualunque source non disponibile causa
risposta non disponibile fail-closed. Le citazioni sono costruite dal server su route
allowlistate e associate al SHA-256 del documento pubblico acquisito. Ogni risposta
AI usa schema JSON strict, deve riferirsi a citation refs restituite dal retrieval,
associa i facts alle proprie citation refs, separa facts, inference, recommendation e
limitation, e viene rifiutata se lo schema o il binding delle citazioni non è valido.
La risposta e la UI conservano correlation ID, provider/model, `method_version`, source
SHA-256, authority `NONE` e decisione umana obbligatoria.

Queste fonti sono projection versionate/storiche: non sono telemetria corrente e non
possono supportare affermazioni di salute live, readiness o efficacia scientifica.
Assenza di match produce `INSUFFICIENT_EVIDENCE`; non viene usato fallback generativo
senza evidenza citabile. Un target la cui projection dichiara conflitti restituisce
`CONFLICT_REQUIRES_REVIEW` senza chiamata al modello e senza conclusioni. I testi delle
fonti e la domanda sono trattati come dati non fidati, non come istruzioni.

## Gate e limiti

- non cambia provider, modelli, endpoint, autenticazione, cap pilota o ledger;
- non introduce tool calling, upload, storage, image processing, PixInsight apply,
  scheduler, target selection, remediation, broker o Safety Authority;
- `store=false` resta invariato; non equivale a garanzia di zero retention del provider;
- deployment sul servizio relay esistente solo dopo review e workflow exact-head;
- nessuna acceptance è attribuita prima della verifica OAT owner-witnessed post-deploy.

## Verification record

Test unitari Python 9/9, compilazione Python, JavaScript syntax, BKL-042 contract verifier,
runtime dry-run, roadmap consistency, MkDocs strict e tutti i workflow exact-head e
post-merge applicabili hanno esito PASS. Il riscontro GET read-only ha confermato le tre
risorse pubbliche disponibili, digest acquisiti e citazioni sul dominio Pages; nessun
record è stato stampato.

Il primo OAT live owner-witnessed ha restituito `INSUFFICIENT_EVIDENCE`, `model=NONE`,
fonti `AVAILABLE` e nessuna citazione per la domanda "riassumi le sessioni per m27 e
indica le fonti" (correlation `bkl042-pages-4728c49e-0210-41ce-bc16-a9565d39036e`). I
digest riportati coincidevano con le tre proiezioni governate pubblicate; la riproduzione
offline sulla stessa domanda e sugli stessi contenuti ha trovato cinque sessioni M 27.
La causa era la mancata normalizzazione fra designazione compatta `m27` e canonica `M 27`.
PR #357 (`7be9fd0b`) introduce tale normalizzazione, incrementa il method version a v2 e
aggiunge regression test per entrambe le grafie e la query esatta. Non è stata eseguita
una richiesta provider per il ramo senza evidenze; l'esito precedente non costituisce
acceptance positiva.

Il redeploy necessario sul servizio relay esistente ha creato la revisione `00007-wrm`
con 100% del traffico; la `00006-ktv` è disponibile per rollback immediato. Il gateway
conserva la revisione `00002-m7c`, punta al canonical service URL e
`/health` restituisce `READY`; il relay rifiuta richieste non autenticate con HTTP `403`.
La configurazione del secret resta vincolata a Secret Manager, senza leggere o stampare
valori. Nessuna richiesta autenticata post-redeploy è stata eseguita; la nuova OAT positiva
owner-witnessed è ancora richiesta.

Resta obbligatoria l'OAT autenticata post-deploy witnessed dall'owner. L'assistente non
simula né attribuisce tale testimonianza; BKL-042 resta `In Progress` fino alla sua
registrazione e alla valutazione esplicita della copertura residua delle fonti.
