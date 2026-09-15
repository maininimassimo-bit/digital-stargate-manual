# BKL-031 F3-A2 — Setup Authority Contract Acceptance

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-ACCEPTANCE-001 |
| Stato | **ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED — NOT IMPLEMENTED** |
| Data | 15/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento | F3-A2 — Governed Setup Authority Contract |
| Pull request | [#197](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/197) |
| Technical head valutato | `6de6ac21acc6f310b022df20954fd0389bd275d1` |
| Review-publication head | `7d917fada3e6048940984bcf21d54dddb84b69d3` |
| Merge commit | `64ecee230431de95fd892849757649da87314e7e` |
| Runtime / dati reali | None |
| PC Principale / EAGLE | Nessuna azione richiesta |
| Successore | **OWNER / ARCHITECTURE DECISION REQUIRED** — `ARB-197-MI01` |

## 1. Decisione

Il Governed Setup Authority Contract F3-A2 e il relativo validation plan sono accettati con condizioni come baseline documentale source-neutral. La decisione riconosce la completezza del contratto normativo, la chiusura di `ARB-195-MI01` al livello di specifica e la verifica post-merge della PR #197.

Non dichiara implementazione, baseline reale, current assignment, schema, fixture, validator, adapter, provider, runtime o production readiness. S09 resta `UNAVAILABLE_CURRENT`.

## 2. Evidenza di integrazione

| Evidenza | Esito |
|---|---|
| PR #197 | merged |
| ARB AI-assisted sul technical head | APPROVED WITH CONDITIONS — 97/100 |
| Release Quality AI-assisted sul technical head | CONDITIONALLY READY FOR MERGE |
| Technical-head CI | 7/7 SUCCESS |
| Review-publication head | `7d917fada3e6048940984bcf21d54dddb84b69d3` |
| Review-publication CI | 7/7 SUCCESS |
| Merge commit su `main` | `64ecee230431de95fd892849757649da87314e7e` |
| Workflow post-merge | 9/9 SUCCESS |
| Pages build/integrity e deployment | SUCCESS |
| Governed Projection Sync | SUCCESS |

Le review sono AI-assistite, process-separated e owner-authorized tramite `DSG-AEM-001`; non equivalgono ad approvazioni umane indipendenti.

## 3. Scope accettato

Sono accettati come specifica:

- separazione tra AP-006 architecture/governance authority, concrete approved baseline instance, `CurrentSetupAssignment` e observed/history evidence;
- reference envelope version-pinned con identity, version, digest, lifecycle, ownership e approval evidence;
- approvazione baseline separata dall'approvazione assignment;
- lifecycle append-only e intervalli UTC half-open coerenti con F3-A1;
- risoluzione deterministica fail-closed senza latest-wins, mtime, filename o host-state fallback;
- porte Application e outbound source-neutral;
- namespace protected/public deny-by-default;
- `publicReasonCode` generalizzato e allowlisted, distinto dai motivi interni;
- 12 casi positivi e 33 casi negativi/fail-closed, oltre a property/security/rollback tests futuri.

## 4. Condizioni carried-forward

| ID | Stato | Gate |
|---|---|---|
| `ARB-197-MI01` | **OPEN / DECISION REQUIRED** | identificare Configuration Baseline Authority, Assignment Authority, approval evidence source e prima approved baseline prima di schema, fixture, validator, adapter, assignment reale o F3-B |
| `ARB-193-MI01` | OPEN / CARRIED | definire vertical reference, unità e range di `elevationM` prima di F3-B |
| `ARB-193-MI02` | OPEN / CARRIED | definire identità canonica e scope del Site Authority resolver prima di F3-B |
| `ARB-191-MI01` | OPEN / CARRIED | enforcement pubblico/interno e leak tests prima di F3-B/F3-C |
| `ARB-191-MI02` | NORMATIVE DESIGN SATISFIED / EXECUTABLE GATE OPEN | test eseguibili temporali obbligatori prima della materializzazione |

`ARB-195-MI01` è **CLOSED NORMATIVELY** da ARB-197-O01. La sua istanziazione reale è deliberatamente trasferita a `ARB-197-MI01`.

## 5. Verifica post-merge

Sul merge commit `64ecee230431de95fd892849757649da87314e7e` hanno concluso SUCCESS:

1. Developer Foundation #1432 — 34961866306;
2. Validate documentation #1069 — 34961866190;
3. Genera manuale Word #1495 — 34961866166;
4. Scientific Platform Governance #132 — 34961866288;
5. BKL-041 F4 Governance #134 — 34961866360;
6. BKL-046 F4 governance #108 — 34961866336;
7. BKL-046 F5 governance #93 — 34961866160;
8. Governed Projection Sync #54 — 34961866159;
9. Deploy MkDocs artifact to GitHub Pages #805 — 34961866355.

Nel workflow Pages, build autorevole, published-site integrity, artifact upload e deploy hanno concluso SUCCESS. L'evidenza vale esclusivamente per l'exact SHA indicato.

## 6. Stati e boundary preservati

- S08 resta `UNAVAILABLE`: nessun record sito approvato è materializzato;
- S09 resta `UNAVAILABLE_CURRENT`: nessuna baseline e nessun assignment corrente sono attestati;
- S10 resta `UNAVAILABLE`: nessun provider ephemeris/lunar è selezionato;
- nessun dato protetto, locator interno, digest interno o reason code interno è pubblicato;
- nessun forecast, ranking, readiness/go-no-go, device command o automatic remediation è autorizzato;
- PC/EAGLE, interlock e Safety Authority fisica/locale sono invariati.

## 7. Waiver e ruleset

Per il merge #197 è stata applicata la deroga continuativa `W-DSG-AEM-RULESET-001`. I gate sostitutivi exact-head CI, zero-behind, mergeability, ARB/RQ, rollback, privacy, tracciabilità ed expected-head merge sono stati soddisfatti.

La deroga resta attiva secondo il mandato; non sostituisce controlli tecnici, sicurezza, privacy, safety o verifica post-merge.

## 8. Rollback

Il rollback è documentale: revert del merge #197 e, se necessario, di questa acceptance reconciliation. Non sono richieste migrazioni dati, rotazioni di credenziali, rollback runtime o azioni hardware.

## 9. Prossima decisione governata

Il repository non identifica univocamente:

1. il sistema o registro autorevole della Configuration Baseline;
2. l'owner/custodian e l'Approval Authority della baseline;
3. l'owner/custodian e l'Approval Authority del `CurrentSetupAssignment`;
4. la prima concrete approved baseline instance e la relativa approval evidence source.

Questi elementi comportano una scelta funzionale/architetturale e non possono essere inventati. In applicazione di `DSG-AEM-001`, il lavoro si arresta dopo l'integrazione di questa acceptance finché l'owner non assume o autorizza tale decisione.

F3-A3, F3-B, F3-C, provider/ADR, schema, fixture, validator, adapter, dati reali, runtime ed EAGLE non sono promossi automaticamente.
