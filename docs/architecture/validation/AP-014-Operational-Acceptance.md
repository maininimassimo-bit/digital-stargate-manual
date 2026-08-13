# AP-014 Scientific Observation Catalog and Search — Operational Acceptance

| Campo | Valore |
|---|---|
| Documento | AP-014 Operational Acceptance |
| Package | AP-014 |
| Workstream | AP14-W07 Validation & Operational Acceptance |
| Versione | 1.0 |
| Data | 2026-08-13 |
| Stato | Pending |
| Owner | Digital StarGate Architecture Office |

## 1. Scopo

Registrare l'accettazione operativa end-to-end di AP-014 sulla base di evidence reali e versionate. La presenza di implementazione, documentazione o CI verde non equivale ad accettazione operativa.

## 2. Boundary di accettazione

Il percorso da provare è:

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

AP-013B XISF transport verso `F:\Astrofotografia` resta un percorso separato e non costituisce fonte diretta delle metriche AP-014.

## 3. Sessione OAT designata

La sessione operativa designata è M 27, notte 10/11 agosto 2026.

La finestra temporale effettiva deve essere determinata dai log NINA/PHD2 reali. Non è accettabile assumere una finestra nominale se non confermata dalle evidence.

## 4. Prerequisiti

- [ ] Scheduled Task EAGLE `Digital StarGate - Daily Session Upload` ispezionata.
- [ ] `Invoke-DSGAutomaticSession.ps1` acquisito con path, sorgente e SHA-256.
- [ ] Runtime conforme a `AP14-EAGLE-Session-Publisher-Runtime-Contract.md` oppure riconciliato con change governato.
- [ ] Versione e path `DigitalStarGate.Reporting` verificati.
- [ ] Configurazione Reporting verificata.
- [ ] NINA evidence M 27 disponibile.
- [ ] PHD2 evidence M 27 disponibile.
- [ ] CloudWatcher evidence M 27 disponibile.
- [ ] EAGLE repository clean e sincronizzato a `main` con fast-forward only.

## 5. Criteri OAT

- [ ] `Import-DSGSession` produce `Status = COMPLETE`.
- [ ] Il manifest contiene `session_id` corretto e SHA-256 verificabili.
- [ ] NINA, PHD2 e weather sono presenti nel package.
- [ ] Nessun XISF viene cancellato, spostato o modificato.
- [ ] `Publish-DSGSession` pubblica il branch `session/<session-id>`.
- [ ] Il GitHub promotion gate valida e promuove il package su `main` esclusivamente fast-forward.
- [ ] `analyze-session-automatic.yml` completa con successo.
- [ ] `data/analytics/history/sessions.csv` contiene M 27.
- [ ] `data/analytics/history/target-exposures.csv` contiene dati derivati dalle evidence versionate, senza metriche inventate.
- [ ] `data/analytics/history/targets.csv` riflette M 27.
- [ ] `docs/data/scientific-session-catalog.json` contiene M 27.
- [ ] `docs/data/scientific-observation-index.json` contiene M 27.
- [ ] Developer Foundation e quality gate applicabili sono PASS.
- [ ] GitHub Pages deployment è PASS.
- [ ] M 27 è visibile nel portale AP-014 senza modifica manuale del catalogo.

## 6. Fail-safe checks

- `PARTIAL` o `NO_SESSION` non devono essere promossi.
- Un branch sessione non discendente dall'attuale `main` deve essere rifiutato.
- File manifest con size/hash divergenti devono bloccare la promotion.
- Modifiche estranee al package devono bloccare la promotion.
- Nessuna metrica scientifica/quality può essere sintetizzata da filename XISF o transfer plan.

## 7. Evidence richieste per la chiusura

- `AP14-W07-EAGLE-Runtime-Inspection-Checklist.md` compilata tramite evidence runtime;
- `AP14-EAGLE-Session-Publisher-Runtime-Contract.md` con conformance verificata;
- `AP14-W07-EAGLE-M27-OAT-Result.md` con risultati e riferimenti commit/workflow;
- package M 27 versionato in `data/sessions/...`;
- analytics/catalog projection versionate;
- CI e Pages workflow run verificati.

## 8. Decisione

**Stato: Pending**

AP-014 non può essere promosso a `completed` finché l'OAT M 27 reale non soddisfa tutti i criteri obbligatori e questo campo non viene modificato a `Accepted` sulla base delle evidence registrate.
