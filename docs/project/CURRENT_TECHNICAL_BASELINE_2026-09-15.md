# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — PR #195 POST-MERGE VERIFIED / DSG-AEM-001 ACTIVE / F3-A2 CONTRACT NEXT** |
| Repository baseline | `main@8520f4272d31f5578769e8d12ac34101e1c044e8` |
| Working branch | `docs/dsg-aem-001-governance` |
| Current package | Governance mandate persistence and F3-A2 contract transition |
| Runtime delta | None |
| Data/schema delta | None |
| Infrastructure delta | None |

## 1. Baseline integrata

PR #195 è merged come `8520f4272d31f5578769e8d12ac34101e1c044e8` e verificata con 9/9 workflow post-merge. Pages build/deployment, published-site integrity e Governed Projection Sync sono SUCCESS.

## 2. Governance corrente

`DSG-AEM-001` autorizza l'esecuzione continuativa fino a completamento o revoca. `W-DSG-AEM-RULESET-001` accetta l'assenza del ruleset soltanto quando tutti i gate sostitutivi sono verificati per l'exact head.

Le review AI-assistite restano dichiarate come non equivalenti ad approvazioni umane indipendenti. Safety, privacy, rollback e tracciabilità non sono derogati.

## 3. Stato tecnico

F3-A2 handoff è accepted with conditions/post-merge verified. Il detailed contract non è ancora prodotto.

Non esistono setup assignment reali, baseline concrete attestate, classi, schema JSON, fixture, validator, persistence, API, cache, provider, deployment o integrazione EAGLE.

## 4. Dependency readiness

| Elemento | Stato |
|---|---|
| F3 architecture | accepted with conditions |
| F3-A1 contract | accepted with conditions / not implemented |
| F3-A2 handoff | accepted with conditions / post-merge verified |
| AP-006 governance concepts | disponibili; nessuna concrete approved baseline attestata |
| F3-A2 detailed contract | dependency-ready / next |
| F3-A3/B/C | not promoted |
| S09 | UNAVAILABLE_CURRENT |

## 5. Gate del prossimo package

Il detailed F3-A2 contract deve:

- risolvere `ARB-195-MI01`;
- distinguere authority architetturale e baseline instance evidence;
- identificare owner/custodian e source reference;
- definire lifecycle, approval/revision e validità UTC half-open;
- definire resolution e failure semantics fail-closed;
- preservare public/protected boundary;
- includere validation plan, migration e rollback;
- restare documentale e non materializzato.

## 6. Rollback

Il package corrente è repository-only. Nessuna migrazione, rotazione credenziali o azione operativa è richiesta.
