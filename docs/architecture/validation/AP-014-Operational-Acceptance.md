# AP-014 Scientific Observation Catalog and Search — Operational Acceptance

| Campo | Valore |
|---|---|
| Documento | AP-014 Operational Acceptance |
| Package | AP-014 |
| Workstream | AP14-W07 Validation & Operational Acceptance |
| Versione | 1.2 |
| Data | 2026-08-21 |
| Stato | Pending |
| Owner | Digital StarGate Architecture Office |

## 1. Scopo

Registrare l'accettazione operativa end-to-end di AP-014 sulla base di evidence reali e versionate. La presenza di implementazione, documentazione o CI verde non equivale ad accettazione operativa.

Questa revisione riconcilia ogni criterio con lo stato realmente supportato dalle evidence. Gli stati ammessi in questa pagina sono:

- **PASS**: evidence tracciabile disponibile;
- **N/A**: requisito non applicabile alla baseline storica, con rationale esplicito;
- **PENDING**: controllo implementato o atteso, ma evidence di esecuzione insufficiente.

## 2. Boundary di accettazione

Il percorso target corrente è:

```text
EAGLE NINA/PHD2/CloudWatcher
  -> DigitalStarGate.Reporting
  -> COMPLETE session package
  -> session/<session-id>
  -> GitHub promotion gate
  -> main
  -> automatic analytics/history/target projections
  -> scientific-session-catalog.json
  -> scientific-observation-index.json
  -> GitHub Pages / AP-014 portal
```

La sessione designata M 27 del 10/11 agosto 2026 fu pubblicata il 13 agosto 2026 prima dell'introduzione del contratto corrente `session/<session-id>` + `promote-session-package.yml`. Per la baseline storica, l'assenza di quel workflow è quindi **N/A**, non un run mancante. Il contratto corrente resta soggetto a validazione separata su sessioni compatibili.

AP-013B XISF transport verso `F:\Astrofotografia` resta un percorso separato e non costituisce fonte diretta delle metriche AP-014.

## 3. Sessione OAT designata

La sessione operativa designata è M 27, notte 10/11 agosto 2026.

La finestra è stata determinata dalle evidence N.I.N.A./PHD2 e il controlled package replay ha usato `2026-08-10 20:00:00` -> `2026-08-11 06:00:00` locale.

## 4. Prerequisiti

| Prerequisito | Stato | Evidence / rationale |
|---|---|---|
| Scheduled Task EAGLE `Digital StarGate - Daily Session Upload` ispezionata | PASS | Runtime inspection e unattended run 18/08/2026 registrati in `AP14-W07-EAGLE-M27-OAT-Result.md` |
| `Invoke-DSGAutomaticSession.ps1` acquisito con path, sorgente e SHA-256 | PASS | Path e hash storici/versionati registrati nell'OAT |
| Runtime conforme o riconciliato con change governato | PASS per percorso validato | Reporting 1.0.6, preflight fail-safe e `NO_SESSION` production PASS |
| Versione e path `DigitalStarGate.Reporting` verificati | PASS | 1.0.6 e ModuleBase registrati nell'OAT |
| Configurazione Reporting verificata | PASS | `C:\DigitalStarGate\Automation\reporting.config.psd1` e RepositoryRoot registrati |
| NINA evidence M 27 disponibile | PASS | package versionato 10/11 agosto |
| PHD2 evidence M 27 disponibile | PASS | DebugLog + GuideLog versionati |
| CloudWatcher evidence M 27 disponibile | PASS | weather CSV versionato |
| EAGLE repository clean e sincronizzato a `main` con fast-forward only | PASS per runtime riconciliato | preflight 17/18 agosto; non attribuito retroattivamente alla pubblicazione storica |

## 5. Criteri OAT

| Criterio | Stato | Evidence / rationale |
|---|---|---|
| `Import-DSGSession` produce `Status = COMPLETE` | PASS | controlled preview M27 `COMPLETE` |
| Manifest con `session_id` corretto e SHA-256 dichiarati | PASS | `manifest.json` del package versionato contiene session_id, size e SHA-256 |
| NINA, PHD2 e weather presenti nel package | PASS | package `data/sessions/2026/08/2026-08-10_2026-08-11/` |
| Nessun XISF cancellato, spostato o modificato | PASS | OAT runtime/safety evidence |
| `Publish-DSGSession` pubblica `session/<session-id>` per la sessione designata | N/A baseline storica | la M27 designata fu pubblicata prima dell'introduzione del contratto corrente; non va simulato retroattivamente |
| GitHub promotion gate promuove la sessione designata esclusivamente fast-forward | N/A baseline storica | `promote-session-package.yml` fu introdotto dopo il commit storico `4266f4249cda7b2a8c47c21fd5b69c890d3ff6ed` |
| Contratto corrente di promotion: validation/fail-safe | PASS contract-level | Developer Foundation #714 su `ba3247aa891df3f11d43a0a808611956c0bb4ff5`: nominal COMPLETE, PARTIAL rejection, size mismatch, SHA-256 mismatch, extraneous scope e non-descendant ancestry tutti PASS usando lo stesso validator del workflow |
| `analyze-session-automatic.yml` completa con successo per la sessione designata | PENDING | proiezioni risultano materializzate, ma non è stato identificato un run ID tracciabile attribuibile alla pubblicazione storica |
| `data/analytics/history/sessions.csv` contiene M 27 | PASS | sessioni M27 presenti; 10/11 preservata con incompletezza storica |
| `target-exposures.csv` usa evidence versionate senza metriche inventate | PASS | BKL-020/BKL-023 reconciliation e source/provenance governati |
| `targets.csv` riflette M 27 | PASS | BKL-023 projection reconciliation |
| `scientific-session-catalog.json` contiene M 27 | PASS | BKL-023 |
| `scientific-observation-index.json` contiene M 27 | PASS | BKL-023; metadata completeness separata da analytics quality |
| Developer Foundation e quality gate applicabili PASS | PASS | Developer Foundation #714 e Genera manuale Word #595 entrambi SUCCESS sull'exact head `ba3247aa891df3f11d43a0a808611956c0bb4ff5` |
| GitHub Pages deployment PASS | PASS per baseline portal verificata | BKL-025: deploy-pages run 381 PASS e published-site integrity PASS |
| M 27 visibile nel portale AP-014 senza modifica manuale del catalogo | PASS | catalog/index/Search/Session Detail/Mission Control riconciliati in BKL-023 |

## 6. Fail-safe checks

| Controllo | Stato | Evidence / rationale |
|---|---|---|
| `NO_SESSION` non promosso | PASS production | unattended run 18/08/2026: `NO_SESSION`, exit/task result 0, nessuno staging |
| `PARTIAL` non promosso nel percorso automatico corrente | PASS contract-level | Developer Foundation #714, `test-session-promotion.ps1` usa `validate-session-promotion.ps1` condiviso con il workflow |
| Branch non discendente da `main` rifiutato | PASS contract-level | Developer Foundation #714: non-descendant ancestry rejection PASS |
| Manifest size/hash divergenti bloccano la promotion | PASS contract-level | Developer Foundation #714: size mismatch e SHA-256 mismatch rejection PASS |
| Modifiche estranee al package bloccano la promotion | PASS contract-level | Developer Foundation #714: extraneous scope rejection PASS |
| Nessuna metrica scientifica/quality sintetizzata da filename XISF o transfer plan | PASS | BKL-020/BKL-022 e registry provenance |
| Re-run real-session idempotente | PENDING | nessuna evidence tracciabile trovata di doppia esecuzione su package reale con risultato invariato |

## 7. Evidence richieste per la chiusura

| Evidence | Stato |
|---|---|
| Runtime inspection checklist / evidence | PASS |
| Runtime contract reconciliation | PASS per percorso `NO_SESSION` e preflight |
| `AP14-W07-EAGLE-M27-OAT-Result.md` | PASS come record, stato complessivo ancora Pending |
| Package M 27 versionato | PASS — `4266f4249cda7b2a8c47c21fd5b69c890d3ff6ed` |
| Analytics/catalog projection versionate | PASS |
| CI applicabile | PASS — Developer Foundation #714; Genera manuale Word #595 |
| Pages workflow verificato | PASS per baseline BKL-025 |
| Current-contract negative/fail-safe validation set | PASS contract-level — Developer Foundation #714 |
| Real-session idempotency evidence | PENDING |

## 8. Decisione

**Stato: Pending**

La maggior parte della OAT storica M27, delle proiezioni AP-014 e dei fail-safe del contratto corrente è ora supportata da evidence. I requisiti `session/<session-id>` e promotion workflow sono **N/A per la pubblicazione storica** perché introdotti successivamente.

I fail-safe del promotion contract sono ora validati in CI contro lo stesso validator usato dal workflow: PARTIAL, ancestry, size/hash mismatch e scope estraneo risultano PASS su Developer Foundation #714.

AP-014 non è ancora `Accepted` perché resta da chiudere l'idempotenza su una sessione reale. Il criterio storico `analyze-session-automatic.yml` resta inoltre `PENDING` finché non viene identificato un run tracciabile o riclassificato formalmente come N/A sulla base della timeline del workflow. La decisione finale richiede ARB re-review dopo la chiusura o disposizione formale di questi ultimi due punti.