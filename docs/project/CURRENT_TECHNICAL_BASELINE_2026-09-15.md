# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — F3-A1 ACCEPTANCE RECONCILIATION / DOCUMENTATION ONLY** |
| Repository baseline | `main@b9d08a7cf6b6287825907cab6a846b1ec70f0378` |
| Working branch | `docs/bkl-031-f3-a1-acceptance` |
| Current package | BKL-031 F3-A1 — Site Authority Contract Acceptance |
| Runtime delta | None |
| Data/schema delta | None |
| Infrastructure delta | None |

## 1. Baseline integrata

PR #193 è merged. Il commit `b9d08a7cf6b6287825907cab6a846b1ec70f0378` è la baseline di partenza verificata con 9/9 workflow post-merge. Il waiver una tantum `W-BKL031-F3A1-MERGE-001` relativo all'assenza del ruleset di `main` è consumato/scaduto e non costituisce precedente automatico.

## 2. Stato tecnico corrente

F3-A1 è accettato con condizioni come specifica documentale:

- aggregate logico `GovernedSiteRecord`;
- value object `HalfOpenValidityInterval`;
- porta `SiteAuthorityPort`;
- failure semantics e public sanitization boundary;
- validation plan accettato ma non eseguito.

Non esistono classi, schema JSON, fixture, validator, persistence, API, cache, deployment o record reali.

## 3. Condizioni

| ID | Stato corrente |
|---|---|
| `ARB-193-MI01` | vertical reference, unità e range di `elevationM` open prima di F3-B |
| `ARB-193-MI02` | resolver canonico e authority scope open prima di F3-B |
| `ARB-191-MI01` | boundary definita; enforcement/leak tests F3-B/F3-C open |
| `ARB-191-MI02` | normativa accettata; test eseguibili obbligatori prima della materializzazione |
| AI review independence | review PR #193 dichiarate AI-assisted |
| S08 | UNAVAILABLE |
| S09 | UNAVAILABLE_CURRENT |
| S10 | UNAVAILABLE |

## 4. Dependency order

`F3-A1 contract accepted -> owner successor decision -> authorized materialization/setup/provider slices -> F3-B -> F3-C`.

L'ordine descrive dipendenze, non autorizza automaticamente alcuna slice.

## 5. Safety e operations

La baseline non modifica EAGLE, N.I.N.A., PHD2, CPWI, VPN, rete, interlock, storage operativo o procedure di emergenza. L'autorità di sicurezza resta fisica/locale.

## 6. Verification target

La draft PR di riconciliazione deve dimostrare:

- build/documentation governance green;
- roadmap source/projection allineate;
- link e nav validi;
- nessun file runtime o dato sensibile;
- exact head finale identificato dopo ogni projection sync.

## 7. Rollback

Revert documentale del singolo commit di riconciliazione. Nessuna migrazione o azione operativa.
