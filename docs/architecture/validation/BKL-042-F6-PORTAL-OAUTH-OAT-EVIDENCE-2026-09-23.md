# BKL-042 F6 — Portal Google OAuth live OAT evidence

| Campo | Valore |
|---|---|
| Stato | **PASS — OWNER-WITNESSED** |
| Owner / accountable | Massimo Mainini |
| Portal | `https://maininimassimo-bit.github.io/digital-stargate-manual/bkl042-chat/` |
| Ingress | Google OAuth gateway `dsg-bkl042-portal-gateway` |
| Scope | Authenticated bounded read-only live consultation |
| Provider traffic | One owner-authenticated live request, as reported by owner |

## Evidenza osservata

L'owner ha verificato dal portale pubblicato il seguente risultato:

> Accesso Google verificato; risposta live read-only ricevuta.

Questo completa il gate di ingresso autenticato del consumer Pages. L'evidenza è
registrata come owner-witnessed; non viene attribuito alcun correlation ID non
fornito dall'owner e non vengono introdotte nuove chiamate provider per ripetere il
test.

## Controlli di perimetro

- la richiesta è passata dal gateway Google OAuth al relay privato;
- la risposta è stata ricevuta in modalità live e read-only;
- `command_authority=NONE`;
- `safety_authority=NONE`;
- nessun tool, upload, PixInsight apply, comando, remediation o scheduler
  decisionale è stato eseguito;
- l'evidenza scientifica resta `NOT_EVALUABLE_CURRENT_EVIDENCE`;
- il client secret OAuth e la chiave OpenAI non sono esposti nel portale.

## Decisione

Il gate portal-ingress di BKL-042 F6 è **completato** per il perimetro
authenticated bounded read-only. Restano separati e non autorizzati retrieval
generico, storage/upload runtime, elaborazione, applicazione automatica, command
path e Safety Authority.
