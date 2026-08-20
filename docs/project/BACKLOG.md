# Project Backlog

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-BKL-001 |
| Versione | 1.7 |
| Stato | Active |
| Data baseline | 20/08/2026 |

## 1. Scopo

Raccogliere il lavoro pianificato del progetto senza sostituire `AMP-002`, i singoli Architecture Package o il sistema di issue tracking. Questo backlog ordina le attività per priorità, dipendenze e milestone.

## 2. Regole

Ogni voce deve includere:

- identificativo;
- titolo;
- priorità;
- stato;
- dipendenze;
- risultato atteso;
- riferimenti a roadmap, technical debt, decision log o Architecture Package.

Stati ammessi: `Planned`, `Ready`, `In Progress`, `Blocked`, `Done`, `Cancelled`.

## 3. Backlog prioritario

| ID | Priorità | Titolo | Stato | Dipendenze | Risultato atteso | Riferimenti |
|---|---|---|---|---|---|---|
| BKL-001 | P0 | RC1-HF01 Enterprise Theme Manager | Ready | Governance Framework baseline | `dsg-theme-manager.js`, persistenza, Instant Navigation, rimozione handler fragile | TD-001, DLG-005 |
| BKL-002 | P0 | Integrare Project Governance Center nella nav MkDocs | Ready | Documenti governance completi | Sezione `Project Governance` navigabile nel portale | TD-006 |
| BKL-003 | P0 | Creare `AI_BOOTSTRAP.md` in root | Ready | Context, Knowledge Map, Backlog e registri disponibili | Bootstrap universale per nuove sessioni | DLG-010 |
| BKL-004 | P1 | Aggiornare `docs/project/index.md` con Knowledge Map e stato package | Ready | BKL-002/BKL-003 | Indice completo e coerente | GP-001 |
| BKL-005 | P1 | Eseguire `mkdocs build --strict` sul Governance Package | Planned | BKL-002–BKL-004 | Build documentale verificata | RELEASE_PLAYBOOK |
| BKL-006 | P1 | Verificare GitHub Pages dopo pubblicazione governance | Planned | BKL-005 | Governance Center pubblicato e navigabile | RELEASE_PLAYBOOK |
| BKL-007 | P1 | Razionalizzare workflow documentali e Pages | Planned | Inventario workflow | Un solo owner per build/deploy; duplicati ritirati | TD-004 |
| BKL-008 | P1 | Riallineare README root alla piattaforma enterprise | Planned | Governance Foundation completata | Entry point repository aggiornato | TD-003 |
| BKL-009 | P1 | Aggiungere consistency checks tra AMP-002 e roadmap JSON | Planned | Definizione schema projection | Riduzione rischio proiezioni stale | TD-005, AP-002 |
| BKL-010 | P1 | Ridurre script inline nel portale | Planned | Inventario pagine con script inline | Moduli JS proprietari e Instant Navigation sicura | TD-002 |
| BKL-011 | P1 | Completare evidence residue ARB-012-C04 | In Progress | W03/W06/W07 e controlli PRV/ENV | Acceptance formalmente riesaminabile | AP-012 |
| BKL-012 | P1 | Validare primo unattended AP-013 COPY_ONLY run | In Progress | Scheduler, launcher protetto, evidence | Evidenza operativa prima di ampliare scope | AP-013 |
| BKL-013 | P1 | Completare AP-014 Observation Catalog and Search | In Progress | AP14-W01-W06 implementati; W07 OAT aperto | Catalogo/search governati con acceptance operativa reale | AP-014, AP14-W07 |
| BKL-018 | P0 | Eseguire EAGLE runtime inspection e M27 end-to-end OAT | In Progress | Accesso EAGLE; evidence NINA/PHD2/CloudWatcher M27; runtime contract | OAT M27 completata tecnicamente e remediation assessment chiuse prima dell'acceptance formale | AP-014, AP14-W07-EAGLE-OAT-001, AP14-INT-EAGLE-PUBLISH-001 |
| BKL-019 | P0 | Correggere logging profile N.I.N.A. C8 e validare telemetria informativa | Done | Evidence N.I.N.A. C8 versionata | Logging `INFO` e telemetria informativa attestati dalla sessione M 27 del 14/15 agosto: QHY695A, Advanced Sequence, target M 27, exposure lifecycle, 600 s, L-Pro, binning 1x1, save path e coordinate target | `data/sessions/2026/08/2026-08-14_2026-08-15/raw/nina/20260814-201744-3.2.0.9001.3996-202608.log`, `480c3fe2a8d36cd315cb814e7af97f8d6aa3260b` |
| BKL-020 | P0 | Correggere data lineage scientifica M27 e future session | Done | BKL-019; registry metadata governato | Lineage scientifica governata: la M 27 10/11 agosto resta esplicitamente `PARTIAL` per i campi non attestati; le sessioni 14/15 e 15/16 agosto sono `REGISTERED` con source reference N.I.N.A./configuration map e senza inferenze non tracciabili | `session-scientific-metadata.csv`, `session-configuration-map.csv`, `480c3fe2a8d36cd315cb814e7af97f8d6aa3260b`, `5fd4b0ebae58bf558e1d4818bdfc8840f8ed7137` |
| BKL-021 | P0 | Eliminare eredità target precedente da `latest-observation` | Done | BKL-020 | `latest-observation.json` usa solo metadata della sessione corrente; refresh strutturale idempotente ricostruisce la projection dai metadata governati durante il deploy Pages | AP-014, Mission Control, `46a528234b6c787fec592953b98c763b848baca8`, `cac81e264f8750cc9eea5455e9bed98c7fc85bda` |
| BKL-022 | P0 | Separare severity analytics da metadata completeness/catalog quality | Done | BKL-020 | `GREEN` non implica automaticamente `VALIDATED_ANALYTICS`; `METADATA_INCOMPLETE`/equivalente è propagato separatamente nel catalogo e nell'observation index | AP-014, scientific session catalog, `ffae9b81a43b82a142b37b587096ea97b1b05ec9` |
| BKL-023 | P1 | Rigenerare e riallineare tutte le proiezioni AP-014 e viste portale | Ready | BKL-020–BKL-022 Done | `sessions.csv`, target projection, scientific-session-catalog, observation index, Mission Control, Enterprise Search e Session Detail semanticamente coerenti | AP-014 |
| BKL-024 | P1 | Riallineare Observatory Status e Session Reports index alla sessione più recente | Planned | BKL-023 | Ultima sessione corretta, distinzione chiara tra stato operativo realtime e ultima sessione scientifica; indice report popolato e senza mojibake | AP-014, portal IA |
| BKL-025 | P1 | Correggere broken links, asset mancanti e sitemap dell'artifact Pages | Done | BKL-023 | Nessun riferimento interno rotto nei percorsi rilevati dall'assessment; asset Roadmap/intelligence risolti; sitemap popolata/coerente. Acceptance verificata su `5068843608880466ba62e7ba18b8982209083645`: `deploy-pages.yml` run 381 PASS, published-site integrity PASS, deploy GitHub Pages PASS; `docs.yml` run 285 PASS; `gh-pages` commit `f1fcd04f93afe8909a80d5d916d73f42186bae8c` pubblica `5068843`. | MkDocs, Pages, PR #46, PR #47 |
| BKL-026 | P0 | Rieseguire deep assessment ARB e chiudere OAT/AP-014 acceptance | Blocked | BKL-023 e BKL-024 non ancora chiusi; OAT M27 designata ancora `Pending` | Re-crawl completo del portale, proiezioni coerenti, documentazione OAT aggiornata allo stato reale e decisione ARB finale | AP14-W07-EAGLE-M27-OAT-Result, AP-014-Operational-Acceptance |
| BKL-014 | P2 | Preparare AP-015 Scientific Knowledge Platform | Planned | AP-014 e Knowledge Graph | Architecture Package CAP-40 | AMP-002 |
| BKL-015 | P2 | Implementare repository Knowledge Graph machine-readable | Planned | Governance Foundation e schema relazioni | Relazioni AP/ADR/component/evidence interrogabili | TD-008, GP-003 |
| BKL-016 | P2 | Contestualizzare release e guide storiche in root | Planned | Inventario e supersession map | Lineage chiaro e baseline corrente distinguibile | TD-007 |
| BKL-017 | P2 | Introdurre futura modalità tema `system` | Planned | RC1-HF01 stabilizzata | Preferenza OS gestita dal Theme Manager | RC1-HF01 |

### Reconciliation note — 20/08/2026

La repository governance è stata riconciliata con le evidence già presenti su `main` senza richiedere test fisici ridondanti e senza promuovere evidence di sessioni successive a sostituto dell'OAT designata 10/11 agosto.

- BKL-019 è chiuso perché la sessione M 27 del 14/15 agosto contiene un log N.I.N.A. versionato a livello `INFO` con connessione QHY695A, Advanced Sequence, exposure lifecycle, filtro L-Pro, binning, target M 27, save path e coordinate target.
- BKL-020 è chiuso perché la lineage usa registry/source reference governati e conserva esplicitamente `PARTIAL` per la sessione 10/11 agosto dove i campi non sono attestati; le sessioni successive sono `REGISTERED` solo dove l'evidence lo consente.
- La chiusura BKL-019/BKL-020 non rende retroattivamente completa la sessione OAT 10/11 agosto. Il package designato è già stato copiato/versionato su `main` da `4266f4249cda7b2a8c47c21fd5b69c890d3ff6ed`; il workflow di promotion con ricalcolo SHA-256 è stato introdotto successivamente e quindi un run storico di quel contratto sulla pubblicazione del 13 agosto è `N/A`, non `Pending`.
- Restano da riconciliare o validare i gate realmente applicabili: integrità indipendente del package/versioned evidence, percorso di promotion attuale su una sessione reale successiva, analytics/proiezioni, portale, PARTIAL-path production semantics e idempotenza real-session.
- BKL-021 e BKL-022 restano chiusi rispettivamente per refresh strutturale di `latest-observation` e separazione metadata completeness/analytics state.
- BKL-023 diventa `Ready` perché BKL-020–BKL-022 sono ora chiusi.
- BKL-026 resta bloccato da BKL-023/BKL-024 e dall'OAT designata ancora `Pending`.
- Power e Network in Observatory Status restano correttamente `UNKNOWN` finché non vengono identificate sorgenti read-only reali e verificabili.

## 4. Sequenza di esecuzione raccomandata

```text
Governance Foundation completion
  -> AI Bootstrap
  -> MkDocs navigation integration
  -> Build and Pages verification
  -> RC1-HF01 Theme Manager
  -> RC1 consolidation
  -> AP-012/AP-013 evidence closure
  -> AP-014 implementation
  -> EAGLE runtime inspection + M27 OAT
  -> BKL-019 N.I.N.A. C8 logging evidence reconciliation [DONE]
  -> BKL-020 scientific metadata lineage reconciliation [DONE]
  -> BKL-021 latest-observation stale-target fix [DONE]
  -> BKL-022 analytics severity vs metadata completeness separation [DONE]
  -> BKL-023 regenerate AP-014 projections and portal views [READY]
  -> BKL-024 status/report index alignment
  -> BKL-025 Pages link/sitemap remediation [DONE]
  -> BKL-026 deep ARB reassessment + OAT/AP-014 acceptance [BLOCKED]
  -> AP-015 / Knowledge Graph
```

## 5. Criteri di priorità

- **P0**: blocco release, regressione, safety/security o governance essenziale.
- **P1**: rischio elevato, dipendenza diretta della roadmap o debito con impatto attuale.
- **P2**: evoluzione pianificata o miglioramento strutturale non bloccante.
- **P3**: ottimizzazione o opportunità futura.

## 6. Definition of Ready

Una voce è `Ready` quando:

- scope e outcome sono chiari;
- dipendenze soddisfatte o esplicite;
- fonti autorevoli identificate;
- acceptance criteria definibili;
- rischi principali noti.

## 7. Definition of Done

Una voce è `Done` solo quando:

- implementazione o documentazione completata;
- test e validazioni applicabili registrati;
- commit/push effettivi;
- deployment verificato quando rilevante;
- registri e context aggiornati;
- nessun debito equivalente introdotto senza registrazione.

## 8. Aggiornamento

Il backlog va riesaminato dopo ogni commit di milestone, release, hotfix, review ARB o variazione di `AMP-002`.
