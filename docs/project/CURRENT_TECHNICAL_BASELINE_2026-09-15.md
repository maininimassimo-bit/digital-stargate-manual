# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — DOCUMENTATION-ONLY CHANGE IN REVIEW PREPARATION** |
| Repository baseline | `main@21524c687a1fa6a9d840a3951c7ef4fe298f9c3c` |
| Working branch | `docs/bkl-031-f3-a1-site-authority-contract` |
| Current package | BKL-031 F3-A1 — Site Authority Contract |
| Runtime delta | None |
| Data/schema delta | None |
| Infrastructure delta | None |

## 1. Baseline integrata

PR #192 è merged. Il commit `21524c687a1fa6a9d840a3951c7ef4fe298f9c3c` è la baseline di partenza verificata con 9/9 workflow post-merge. Il ruleset assente su `main` è stato trattato con decisione owner limitata al merge già consumato; non costituisce precedente automatico.

## 2. Stato tecnico corrente

F3-A1 introduce solo specifiche documentali:

- aggregate logico `GovernedSiteRecord`;
- value object `HalfOpenValidityInterval`;
- porta `SiteAuthorityPort`;
- failure semantics e public sanitization boundary;
- validation plan non eseguito.

Non esistono classi, schema JSON, fixture, validator, persistence, API, cache, deployment o record reali.

## 3. Condizioni

| ID | Stato corrente |
|---|---|
| `ARB-191-MI02` | risoluzione normativa proposta; pending ARB |
| `ARB-191-MI01` | boundary dettagliata; enforcement F3-B/F3-C ancora open |
| AI review independence | ogni futura review resta dichiarata AI-assisted |
| S08 | UNAVAILABLE |
| S09 | UNAVAILABLE_CURRENT |
| S10 | UNAVAILABLE |

## 4. Dependency order

`F3-A1 contract -> review/acceptance -> separate materialization decision -> F3-A2 -> F3-A3 -> F3-B -> F3-C`.

L'ordine descrive dipendenze, non autorizza automaticamente le slice.

## 5. Safety e operations

La baseline non modifica EAGLE, N.I.N.A., PHD2, CPWI, VPN, rete, interlock, storage operativo o procedure di emergenza. L'autorità di sicurezza resta fisica/locale.

## 6. Verification target

La draft PR deve dimostrare:

- build/documentation governance green;
- roadmap source/projection allineate;
- link e nav validi;
- nessun file runtime o dato sensibile;
- exact-head identificato.

## 7. Rollback

Revert documentale del singolo commit F3-A1. Nessuna migrazione o azione operativa.

