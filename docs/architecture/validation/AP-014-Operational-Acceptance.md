# AP-014 Scientific Observation Catalog and Search — Operational Acceptance

| Campo | Valore |
|---|---|
| Documento | AP-014 Operational Acceptance |
| Package | AP-014 |
| Workstream | AP14-W07 Validation & Operational Acceptance |
| Versione | 1.4 |
| Data | 2026-08-21 |
| Stato | Accepted |
| Owner | Digital StarGate Architecture Office |

## 1. Scopo

Registrare l'accettazione operativa end-to-end di AP-014 sulla base di evidence reali e versionate. La presenza di implementazione, documentazione o CI verde non equivale da sola ad accettazione operativa.

Gli stati usati in questa pagina sono:

- **PASS**: evidence tracciabile disponibile;
- **N/A**: requisito non applicabile alla baseline storica, con rationale esplicito;
- **PENDING**: evidence ancora insufficiente.

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

La sessione designata M 27 del 10/11 agosto 2026 fu pubblicata il 13 agosto 2026 prima dell'introduzione del contratto corrente `session/<session-id>` + `promote-session-package.yml` e prima della baseline corrente di `analyze-session-automatic.yml`. Per la baseline storica, l'assenza di quei workflow è quindi **N/A**, non un run mancante.

AP-013B XISF transport verso `F:\Astrofotografia` resta un percorso separato e non costituisce fonte diretta delle metriche AP-014.

## 3. Sessione OAT designata

La sessione operativa designata è M 27, notte 10/11 agosto 2026.

La finestra è stata determinata dalle evidence N.I.N.A./PHD2 e il controlled package replay ha usato `2026-08-10 20:00:00` -> `2026-08-11 06:00:00` locale.

## 4. Prerequisiti

| Prerequisito | Stato | Evidence / rationale |
|---|---|---|
| Scheduled Task EAGLE `Digital StarGate - Daily Session Upload` ispezionata | PASS | Runtime inspection e unattended run 18/08/2026 registrati in `AP14-W07-EAGLE-M27-OAT-Result.md` |
| `Invoke-DSGAutomaticSession.ps1` acquisito con path, sorgente e SHA-256 | PASS | Path e hash storici/versionati registrati nell'OAT |
| Runtime conforme o riconciliato con change governato | PASS | Reporting 1.0.6, preflight fail-safe e `NO_SESSION` production PASS |
| Versione e path `DigitalStarGate.Reporting` verificati | PASS | 1.0.6 e ModuleBase registrati nell'OAT |
| Configurazione Reporting verificata | PASS | `C:\DigitalStarGate\Automation\reporting.config.psd1` e RepositoryRoot registrati |
| NINA evidence M 27 disponibile | PASS | package versionato 10/11 agosto |
| PHD2 evidence M 27 disponibile | PASS | DebugLog + GuideLog versionati |
| CloudWatcher evidence M 27 disponibile | PASS | weather CSV versionato |
| EAGLE repository clean e sincronizzato a `main` con fast-forward only | PASS | preflight 17/18 agosto; non attribuito retroattivamente alla pubblicazione storica |

## 5. Criteri OAT

| Criterio | Stato | Evidence / rationale |
|---|---|---|
| `Import-DSGSession` produce `Status = COMPLETE` | PASS | controlled preview M27 `COMPLETE` |
| Manifest con `session_id` corretto e SHA-256 dichiarati | PASS | `manifest.json` del package versionato contiene session_id, size e SHA-256 |
| NINA, PHD2 e weather presenti nel package | PASS | package `data/sessions/2026/08/2026-08-10_2026-08-11/` |
| Nessun XISF cancellato, spostato o modificato | PASS | OAT runtime/safety evidence |
| `Publish-DSGSession` pubblica `session/<session-id>` per la sessione designata | N/A baseline storica | la M27 designata fu pubblicata prima dell'introduzione del contratto corrente |
| GitHub promotion gate promuove la sessione designata esclusivamente fast-forward | N/A baseline storica | `promote-session-package.yml` è successivo al commit storico `4266f4249cda7b2a8c47c21fd5b69c890d3ff6ed` |
| Contratto corrente di promotion: validation/fail-safe | PASS contract-level | Developer Foundation #714: nominal COMPLETE, PARTIAL rejection, size mismatch, SHA-256 mismatch, extraneous scope e non-descendant ancestry PASS usando lo stesso validator del workflow |
| `analyze-session-automatic.yml` completa per la pubblicazione storica designata | N/A baseline storica | la baseline corrente del workflow analytics è successiva alla pubblicazione del 13/08; le proiezioni storiche risultano materializzate e riconciliate senza inventare un run retroattivo |
| Pipeline analytics/projection corrente su sessione reale | PASS | Developer Foundation #723 esegue due volte la pipeline reale sulla sessione `2026-08-15_2026-08-16` |
| `data/analytics/history/sessions.csv` contiene M 27 | PASS | sessioni M27 presenti; 10/11 preservata con incompletezza storica |
| `target-exposures.csv` usa evidence versionate senza metriche inventate | PASS | BKL-020/BKL-023 reconciliation e source/provenance governati |
| `targets.csv` riflette M 27 | PASS | BKL-023 projection reconciliation |
| `scientific-session-catalog.json` contiene M 27 | PASS | BKL-023 |
| `scientific-observation-index.json` contiene M 27 | PASS | BKL-023; metadata completeness separata da analytics quality |
| Quality gate tecnico applicabile | PASS | Developer Foundation #723 e Genera manuale Word #604 entrambi SUCCESS sull'exact head `88ea7b1f915177906e5d514ee8254ef91ff5e45d` |
| Final exact-head governance CI | PASS | Developer Foundation #725 e Genera manuale Word #606 entrambi SUCCESS sull'exact head `a52c678ba6f3b498bc711ec7b8d5fad7359c7709` |
| GitHub Pages deployment PASS | PASS baseline portal | BKL-025: deploy-pages run 381 PASS e published-site integrity PASS |
| M 27 visibile nel portale AP-014 senza modifica manuale del catalogo | PASS | catalog/index/Search/Session Detail/Mission Control riconciliati in BKL-023 |

## 6. Fail-safe e idempotenza

| Controllo | Stato | Evidence / rationale |
|---|---|---|
| `NO_SESSION` non promosso | PASS production | unattended run 18/08/2026: `NO_SESSION`, task result 0, nessuno staging |
| `PARTIAL` non promosso | PASS contract-level | Developer Foundation #714 |
| Branch non discendente da `main` rifiutato | PASS contract-level | Developer Foundation #714 |
| Manifest size/hash divergenti bloccano la promotion | PASS contract-level | Developer Foundation #714 |
| Modifiche estranee al package bloccano la promotion | PASS contract-level | Developer Foundation #714 |
| Nessuna metrica scientifica/quality sintetizzata da filename XISF o transfer plan | PASS | BKL-020/BKL-022 |
| Re-run real-session semanticamente idempotente | PASS | Developer Foundation #723 sulla sessione reale `2026-08-15_2026-08-16`; doppia esecuzione con fingerprint canonico scientifico/projection invariato |

L'idempotenza accettata è **scientifica/semantica**: timestamp di generazione, line ending o metadata binari PDF non sono trattati come variazioni scientifiche. Un eventuale obiettivo futuro di byte-for-byte no-op è hardening separato e non altera l'accettazione AP-014.

## 7. Evidence di chiusura

| Evidence | Stato |
|---|---|
| Runtime inspection checklist / evidence | PASS |
| Runtime contract reconciliation | PASS |
| `AP14-W07-EAGLE-M27-OAT-Result.md` | PASS |
| Package M 27 versionato | PASS — `4266f4249cda7b2a8c47c21fd5b69c890d3ff6ed` |
| Analytics/catalog projection versionate | PASS |
| Promotion fail-safe validation set | PASS — Developer Foundation #714 |
| Real-session semantic idempotency | PASS — Developer Foundation #723 |
| Pages workflow verificato | PASS baseline BKL-025 |
| Final exact-head documentation/governance CI | PASS — Developer Foundation #725; Genera manuale Word #606 |

## 8. Decisione

**Stato: Accepted**

Tutti i gate tecnici e operativi applicabili risultano **PASS** oppure **N/A historical baseline** con rationale esplicito. Non restano criteri `PENDING`.

AP-014 Scientific Observation Catalog and Search è quindi **operativamente accettato** sulla baseline riconciliata. La chiusura non altera retroattivamente la sessione M27 10/11 agosto, che resta `PARTIAL` dove le sue evidence originarie sono incomplete, e non attribuisce a quella pubblicazione workflow introdotti successivamente.

L'eventuale eliminazione futura del byte-level churn dovuto a timestamp, line ending o metadata PDF è hardening separato e non riapre l'acceptance AP-014.