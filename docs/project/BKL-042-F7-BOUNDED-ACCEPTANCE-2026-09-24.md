# BKL-042 F7 — Bounded Read-Only Acceptance

| Campo | Valore |
|---|---|
| Identificativo | BKL-042-F7 |
| Stato | ACCEPTED / BOUNDED GATE / OWNER-WITNESSED |
| Data | 2026-09-24 |
| Owner / accountable | Massimo Mainini |
| Metodo accettato | `bkl042-static-projection-retrieval-v3` |
| Autorità | Advisory/read-only; `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |
| Runtime | Relay esistente `dsg-bkl042-ai-relay-00008-qat`; massimo 1 istanza; rollback `00007-wrm` |

## Decisione owner

Massimo Mainini ha eseguito e fornito i risultati dell'OAT autenticato dal portale
per entrambe le fonti aggiunte da F7. Dopo aver ricevuto la sintesi dei risultati e
dei limiti, ha confermato: «Accetto i limiti riportati» e ha confermato che tale
decisione costituisce formal acceptance di BKL-042/F7 entro il perimetro bounded
read-only.

L'accettazione è limitata alle evidenze, alle fonti e alle qualificazioni riportate
qui sotto. Non equivale ad accettazione scientifica delle proiezioni sperimentali.

## OAT owner-witnessed

| Percorso | Correlation ID / fonte | Esito |
|---|---|---|
| Confronto SQM BKL-037 | `bkl042-pages-7597330b-5970-4696-b7a6-767defa6e8ff`; fonte `BKL037-SQM-CATALOG-V1`; digest `b1d1e516eb872e686ce18178858f42eb85c690de2ce011d845a7f2436c0717d4` | `INSUFFICIENT_EVIDENCE` per confronti sessione-per-sessione, dichiarato correttamente. Il catalogo fornisce statistiche aggregate descrittive su 15 sessioni: min 18,66, max 20,96, mediana 20,57 mag/arcsec². La risposta chiarisce che non è un punteggio di qualità e cita la proiezione e due schede storiche prive di SQM individuale. |
| Contesto qualità M 27 BKL-041 | `bkl042-pages-4971ae55-44cf-47e0-afc5-ecca6e774442`; digest `7c4ffc905f2a57b18f221ffabf4e58820ad03549968db2e2aec78d2b88846838` | Risposta `ANSWERED`, con entrambe le proiezioni marcate `EXPERIMENTAL_NOT_ACCEPTED`; profilo sintetico e non calibrato; nessun giudizio definitivo sulla qualità reale. |

Entrambe le risposte identificano il metodo `bkl042-static-projection-retrieval-v3`.
Nessuna autorità command/execution/safety è stata concessa.

## Limiti accettati

- Non sono disponibili valori SQM individuali per le sessioni indicate; sono
  utilizzabili soltanto le statistiche aggregate storiche e descrittive citate.
- Le due proiezioni BKL-041 sono sperimentali, sintetiche e non calibrate; non sono
  ground truth, valutazioni accettate, ranking o raccomandazioni.
- Le proiezioni sono versionate e storiche, non dati in tempo reale.
- Digital Twin, archivio immagini, provenance PixInsight incompleta, planner
  scaduto, readiness non disponibile e snapshot EAGLE `UNAVAILABLE` / `UNKNOWN`
  restano esclusi come evidenza fattuale corrente.
- Questa acceptance non autorizza nuove fonti, servizi, deploy, provider, credenziali,
  tool, storage/upload, elaborazione, broker, scheduler, remediation o Safety
  Authority.

## Evidenze correlate

- Implementazione e copertura fonti: `docs/architecture/validation/BKL-042-F7-F1-SOURCE-COVERAGE-EVIDENCE-2026-09-24.md`.
- Deploy relay v3 e cap massimo 1 istanza: `docs/architecture/validation/BKL-042-F7-V3-DEPLOYMENT-EVIDENCE-2026-09-24.md`.
- PR di riconciliazione deploy: [#362](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/362), merge `bdb15037f4a2505992c284a1dff4930af90801f8`.

## Stato successivo

F7 è accettata entro questo perimetro bounded read-only. Ogni ulteriore copertura
delle classi escluse richiede una projection eleggibile e una decisione separata;
non viene inferita da questa acceptance. Preservare `acceptance_authority=HUMAN_ONLY`
e le tre autorità runtime `NONE`.
