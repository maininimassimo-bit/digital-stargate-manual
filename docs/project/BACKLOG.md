# Project Backlog

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-BKL-001 |
| Versione | 2.7 |
| Stato | Active |
| Data baseline | 28/08/2026 |

## 1. Scopo

Raccogliere il lavoro pianificato del progetto senza sostituire `AMP-002`, i singoli Architecture Package o il sistema di issue tracking. Questo backlog ordina le attività per priorità, dipendenze e milestone.

## 2. Regole

Ogni voce deve includere identificativo, titolo, priorità, stato, dipendenze, risultato atteso e riferimenti. Stati ammessi: `Planned`, `Ready`, `In Progress`, `Blocked`, `Done`, `Cancelled`.

## 3. Backlog prioritario

| ID | Priorità | Titolo | Stato | Dipendenze | Risultato atteso | Riferimenti |
|---|---|---|---|---|---|---|
| BKL-001 | P0 | RC1-HF01 Enterprise Theme Manager | Done | Governance Framework baseline | Theme Service centralizzato, persistenza, Instant Navigation e separazione da `page-enhancements.js` | TD-001, WP-03 Completion Report, `5cb6cd3454b2b1d95fcf8ede3b42352e41514d88` |
| BKL-002 | P0 | Integrare Project Governance Center nella nav MkDocs | Done | Documenti governance completi | Sezione `Project Governance` navigabile nel portale | TD-006, `mkdocs.yml` |
| BKL-003 | P0 | Creare `AI_BOOTSTRAP.md` in root | Done | Context, Knowledge Map, Backlog e registri disponibili | Bootstrap universale per nuove sessioni | `AI_BOOTSTRAP.md` |
| BKL-004 | P1 | Aggiornare `docs/project/index.md` con Knowledge Map e stato package | Done | BKL-002/BKL-003 | Governance Center con documenti canonici, stato package e sequenza di lettura | `docs/project/index.md` |
| BKL-005 | P1 | Eseguire `mkdocs build --strict` sul Governance Package | Done | BKL-002–BKL-004 | Build documentale verificata | Developer Foundation #730 |
| BKL-006 | P1 | Verificare GitHub Pages dopo pubblicazione governance | Done | BKL-005 | Governance Center pubblicato e navigabile | BKL-025 Pages integrity baseline |
| BKL-007 | P1 | Razionalizzare workflow documentali e Pages | **Done** | Inventario workflow | Un solo owner per build/deploy; duplicati ritirati | TD-004; `deploy-pages.yml` authoritative owner; `docs.yml` validation-only; legacy `docs.yml.disabled` retired |
| BKL-008 | P1 | Riallineare README root alla piattaforma enterprise | Planned | Governance Foundation completata | Entry point repository aggiornato | TD-003 |
| BKL-009 | P1 | Aggiungere consistency checks tra AMP-002 e roadmap JSON | **Done** | Definizione schema projection | Riduzione rischio proiezioni stale | TD-005, AP-002, `.github/scripts/verify-roadmap-consistency.mjs`, Developer Foundation #778 |
| BKL-010 | P1 | Ridurre script inline nel portale | Planned | Inventario pagine con script inline | Moduli JS proprietari e Instant Navigation sicura | TD-002 |
| BKL-011 | P1 | Completare evidence residue ARB-012-C04 | **Done** | C04-W01–W08 e final repository CI completati | **ARB-012-C04 Closed — Approved; quality gate finale PASS** | AP-012, ARB-012-C04, W07 evidence, W08 re-review, Actions run `32871808946` |
| BKL-012 | P1 | Validare primo unattended AP-013 COPY_ONLY run | Done | Scheduler, launcher protetto, evidence | Scheduler COPY_ONLY validato con runtime evidence, `LastTaskResult = 0`, batch operativi e retry idempotenti | AP-013B OneDrive Transport OAT, AP-013 Operational Acceptance |
| BKL-013 | P1 | Completare AP-014 Observation Catalog and Search | Done | AP14-W01-W07 | Catalogo/search governati con acceptance operativa reale | AP-014, AP14-W07, BKL-026 |
| BKL-018 | P0 | Eseguire EAGLE runtime inspection e M27 end-to-end OAT | Done | Accesso EAGLE; evidence NINA/PHD2/CloudWatcher M27; runtime contract | OAT M27 completata, riconciliata e formalmente Accepted | AP-014, AP14-W07-EAGLE-M27-OAT-Result |
| BKL-019 | P0 | Correggere logging profile N.I.N.A. C8 e validare telemetria informativa | Done | Evidence N.I.N.A. C8 versionata | Logging `INFO` e telemetria informativa attestati dalla sessione M 27 del 14/15 agosto | `data/sessions/2026/08/2026-08-14_2026-08-15/raw/nina/20260814-201744-3.2.0.9001.3996-202608.log` |
| BKL-020 | P0 | Correggere data lineage scientifica M27 e future session | Done | BKL-019; registry metadata governato | Lineage governata; 10/11 resta `PARTIAL`, sessioni successive `REGISTERED` solo con evidence | `session-scientific-metadata.csv`, `session-configuration-map.csv` |
| BKL-021 | P0 | Eliminare eredità target precedente da `latest-observation` | Done | BKL-020 | Projection ricostruita dai metadata governati | AP-014, Mission Control |
| BKL-022 | P0 | Separare severity analytics da metadata completeness/catalog quality | Done | BKL-020 | Analytics severity e metadata completeness separati | AP-014, scientific session catalog |
| BKL-023 | P1 | Rigenerare e riallineare tutte le proiezioni AP-014 e viste portale | Done | BKL-020–BKL-022 Done | Proiezioni e viste semanticamente coerenti | Developer Foundation #702, Genera manuale Word #583 |
| BKL-024 | P1 | Riallineare Observatory Status e Session Reports index alla sessione più recente | Done | BKL-023 Done | Realtime separato dallo storico; Power/Network restano `UNKNOWN` senza sorgenti verificate | Developer Foundation #705, Genera manuale Word #586 |
| BKL-025 | P1 | Correggere broken links, asset mancanti e sitemap dell'artifact Pages | Done | BKL-023 | Pages integrity verificata | deploy-pages run 381, docs.yml run 285 |
| BKL-026 | P0 | Rieseguire deep assessment ARB e chiudere OAT/AP-014 acceptance | Done | BKL-019–BKL-025 Done | ARB re-review completata; promotion fail-safe e real-session semantic idempotency PASS; historical workflow criteria N/A; OAT/AP-014 Accepted; final governance CI PASS | AP14-W07-EAGLE-M27-OAT-Result v2.1, AP-014-Operational-Acceptance v1.4, Developer Foundation #730, Genera manuale Word #611 |
| BKL-027 | P1 | Observatory Status — runtime source discovery Power/Network | **Done** | DSG-OBS-RT-001 pilot; accesso EAGLE/RUT955 | Sorgenti read-only reali e verificabili per Power e Network, freshness/quality e adapter boundary definiti | N.I.N.A. NetworkTelemetryAdapter; TS Shelter SafetyMonitor J6 `safeties` mask `0x00000001`; AP-004, AP-009, AP-012 |
| BKL-028 | P1 | Observatory Status — integrare Power/Network telemetry | **Done** | BKL-027 Done | `systems.power` e `systems.network` alimentati da source verificate, fail-safe `UNKNOWN/STALE`, portale e relay aggiornati | N.I.N.A. telemetry exporter; canonical adapter; relay; Observatory Status; commits `91d78a2`, `06e6484` |
| BKL-014 | P2 | Preparare AP-015 Scientific Knowledge Platform | Planned | AP-014 e Knowledge Graph | Architecture Package CAP-40 | AMP-002 |
| BKL-015 | P2 | Implementare repository Knowledge Graph machine-readable | Planned | Governance Foundation e schema relazioni | Relazioni AP/ADR/component/evidence interrogabili | TD-008, GP-003 |
| BKL-016 | P2 | Contestualizzare release e guide storiche in root | Planned | Inventario e supersession map | Lineage chiaro e baseline corrente distinguibile | TD-007 |
| BKL-017 | P2 | Introdurre futura modalità tema `system` | Planned | RC1-HF01 stabilizzata | Preferenza OS gestita dal Theme Manager | RC1-HF01 |

### Reconciliation note — 28/08/2026

La repository governance è riconciliata con le evidence reali senza ripetere attività già accettate.

- BKL-001–BKL-006 restano `Done` sulla governance foundation e quality baseline già accettata.
- BKL-007 è **Done**: `deploy-pages.yml` è l'unico owner della pubblicazione GitHub Pages; `docs.yml` è validation-only senza Pages write permission; il legacy `docs.yml.disabled` è stato rimosso. TD-004 è `Resolved`.
- BKL-011 è **Done**: ARB-012-C04 è `Closed — Approved`; la closure non costituisce runtime authorization.
- BKL-012, BKL-013 e BKL-018–BKL-026 restano `Done` sulle acceptance già registrate.
- BKL-027 è **Done**: Network è osservato dal boundary N.I.N.A.; Power è osservato direttamente dal TS Shelter SafetyMonitor tramite `CommandString("safeties", false)` con J6 power-fault mask `0x00000001`. `IsSafe` resta solo diagnostico e non è la source dello stato Power.
- BKL-028 è **Done**: Power/Network sono proiettati nel canonical Observatory Status e resi dal portale; la perdita della source decade fail-safe a `UNKNOWN/STALE`. La Safety Authority fisica resta indipendente e autorevole.
- BKL-009 è **Done**: il consistency gate AMP-002/roadmap/backlog è attivo nel Developer Foundation; la baseline riconciliata ha superato `Verify generated roadmap` e `Verify AMP-002 / roadmap / backlog consistency` nel run #778.
- BKL-008 e BKL-010 restano lavori reali e non vengono chiusi per inferenza.

## 4. Sequenza di esecuzione raccomandata

```text
Governance Foundation [DONE]
  -> AI Bootstrap [DONE]
  -> MkDocs governance navigation [DONE]
  -> Governance build and Pages verification [DONE]
  -> Enterprise Theme Manager [DONE]
  -> AP-013 unattended COPY_ONLY evidence [DONE]
  -> AP-014 acceptance [DONE]
  -> BKL-011 / ARB-012-C04 [DONE]
  -> BKL-027 Power/Network source discovery [DONE]
  -> BKL-028 Power/Network integration [DONE]
  -> BKL-009 consistency gate [DONE]
  -> BKL-007 workflow rationalization [DONE]
  -> BKL-008/010 governance hardening
  -> AP-015 / Knowledge Graph
```

## 5. Criteri di priorità

- **P0**: blocco release, regressione, safety/security o governance essenziale.
- **P1**: rischio elevato, dipendenza diretta della roadmap o debito con impatto attuale.
- **P2**: evoluzione pianificata o miglioramento strutturale non bloccante.
- **P3**: ottimizzazione o opportunità futura.

## 6. Definition of Ready

Una voce è `Ready` quando scope e outcome sono chiari, dipendenze soddisfatte o esplicite, fonti autorevoli identificabili, acceptance criteria definibili e rischi principali noti. Per attività di source discovery, l'output può essere proprio l'identificazione della fonte autorevole.

## 7. Definition of Done

Una voce è `Done` solo quando implementazione/documentazione, test applicabili, commit/push, deployment rilevante e registri sono coerenti e non viene introdotto debito equivalente senza registrazione.

## 8. Aggiornamento

Il backlog va riesaminato dopo ogni commit di milestone, release, hotfix, review ARB o variazione di `AMP-002`.
