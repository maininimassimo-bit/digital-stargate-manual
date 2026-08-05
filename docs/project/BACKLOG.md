# Project Backlog

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-BKL-001 |
| Versione | 1.0 |
| Stato | Active |
| Data baseline | 04/08/2026 |

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
| BKL-013 | P1 | Avviare AP-014 Observation Catalog and Search | Planned | Stabilizzazione AP-013 | Package architetturale e catalogo governato | AMP-002 |
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
  -> AP-014
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
