# Project Backlog

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-BKL-001 |
| Versione | 1.3 |
| Stato | Active |
| Data baseline | 15/08/2026 |

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
| BKL-019 | P0 | Correggere logging profile N.I.N.A. C8 e validare telemetria informativa | Ready | Accesso profilo N.I.N.A. C8 | Logging almeno `Information`; test controllato con target, sequence, exposure lifecycle e metadata utili all'analytics presenti nel log | AP-014, AP14-W07-EAGLE-OAT-001 |
| BKL-020 | P0 | Correggere data lineage scientifica M27 e future session | In Progress | BKL-019; registry metadata governato | Metadata sessione risolti da evidence/registry governato; nessuna inferenza non tracciabile; M27 identificata come M 27 con campi non attestati esplicitamente incompleti | AP-014, `session-scientific-metadata.csv` |
| BKL-021 | P0 | Eliminare eredità target precedente da `latest-observation` | Ready | BKL-020 | `latest-observation.json` usa solo metadata della sessione corrente; assenza dati => `null`/unavailable, mai valori della sessione precedente | AP-014, Mission Control |
| BKL-022 | P0 | Separare severity analytics da metadata completeness/catalog quality | Ready | BKL-020 | `GREEN` non implica automaticamente `VALIDATED_ANALYTICS`; introdotto stato tipo `METADATA_INCOMPLETE`/equivalente per record parziali | AP-014, scientific session catalog |
| BKL-023 | P1 | Rigenerare e riallineare tutte le proiezioni AP-014 e viste portale | Planned | BKL-020–BKL-022 | `sessions.csv`, target projection, scientific-session-catalog, observation index, Mission Control, Enterprise Search e Session Detail semanticamente coerenti | AP-014 |
| BKL-024 | P1 | Riallineare Observatory Status e Session Reports index alla sessione più recente | Planned | BKL-023 | Ultima sessione corretta, distinzione chiara tra stato operativo realtime e ultima sessione scientifica; indice report popolato e senza mojibake | AP-014, portal IA |
| BKL-025 | P1 | Correggere broken links, asset mancanti e sitemap dell'artifact Pages | Done | BKL-023 | Nessun riferimento interno rotto nei percorsi rilevati dall'assessment; asset Roadmap/intelligence risolti; sitemap popolata/coerente. Acceptance verificata su `5068843608880466ba62e7ba18b8982209083645`: `deploy-pages.yml` run 381 PASS, published-site integrity PASS, deploy GitHub Pages PASS; `docs.yml` run 285 PASS; `gh-pages` commit `f1fcd04f93afe8909a80d5d916d73f42186bae8c` pubblica `5068843`. | MkDocs, Pages, PR #46, PR #47 |
| BKL-026 | P0 | Rieseguire deep assessment ARB e chiudere OAT/AP-014 acceptance | Planned | BKL-019–BKL-025 completati; workflow verdi; Pages pubblicate | Re-crawl completo del portale, data lineage coerente, documentazione OAT aggiornata allo stato reale e decisione ARB finale | AP14-W07-EAGLE-M27-OAT-Result, AP-014-Operational-Acceptance |
| BKL-014 | P2 | Preparare AP-015 Scientific Knowledge Platform | Planned | AP-014 e Knowledge Graph | Architecture Package CAP-40 | AMP-002 |
| BKL-015 | P2 | Implementare repository Knowledge Graph machine-readable | Planned | Governance Foundation e schema relazioni | Relazioni AP/ADR/component/evidence interrogabili | TD-008, GP-003 |
| BKL-016 | P2 | Contestualizzare release e guide storiche in root | Planned | Inventario e supersession map | Lineage chiaro e baseline corrente distinguibile | TD-007 |
| BKL-017 | P2 | Introdurre futura modalità tema `system` | Planned | RC1-HF01 stabilizzata | Preferenza OS gestita dal Theme Manager | RC1-HF01 |

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
  -> BKL-019 N.I.N.A. C8 logging correction + controlled test
  -> BKL-020 scientific metadata lineage correction
  -> BKL-021 latest-observation stale-target fix
  -> BKL-022 analytics severity vs metadata completeness separation
  -> BKL-023 regenerate AP-014 projections and portal views
  -> BKL-024 status/report index alignment
  -> BKL-025 Pages link/sitemap remediation [DONE]
  -> BKL-026 deep ARB reassessment + OAT/AP-014 acceptance
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
