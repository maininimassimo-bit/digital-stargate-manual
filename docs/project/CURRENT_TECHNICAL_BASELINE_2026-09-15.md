# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — F3-A2 ACCEPTED WITH CONDITIONS / NOT IMPLEMENTED** |
| Repository baseline | `main@64ecee230431de95fd892849757649da87314e7e` |
| Working branch | `docs/bkl-031-f3-a2-acceptance` |
| Current package | `BKL-031-F3-A2-ACCEPTANCE-001` |
| Runtime delta | None |
| Data/schema delta | None |
| Infrastructure delta | None |

## 1. Baseline integrata

F3-A2 handoff è accepted tramite PR #195. `DSG-AEM-001` è integrato tramite PR #196. Il detailed contract e validation plan sono integrati tramite PR #197 merge `64ecee230431de95fd892849757649da87314e7e`, verificato con 9/9 workflow post-merge inclusi Pages e Governed Projection Sync.

## 2. Stato tecnico corrente

Il contratto definisce aggregate, reference envelope, lifecycle, approval separation, UTC half-open validity, deterministic resolution, failure semantics e public/protected boundary con `publicReasonCode` allowlisted.

Non esistono baseline concrete approvate attestate, assignment, schema JSON, fixture, validator, persistence, API, cache, provider, deployment o integrazione EAGLE.

## 3. Finding disposition

| Finding | Stato |
|---|---|
| `ARB-195-MI01` | closed normatively |
| `ARB-197-MI01` | open / owner-architecture decision required before materialization |
| `ARB-193-MI01` | open before F3-B |
| `ARB-193-MI02` | open before F3-B |
| `ARB-191-MI01` | open before F3-B/F3-C |
| `ARB-191-MI02` | normative design satisfied / executable gate open |

## 4. Dependency readiness

| Elemento | Stato |
|---|---|
| F3 architecture | accepted with conditions |
| F3-A1 | accepted with conditions / not implemented |
| F3-A2 handoff | accepted with conditions / post-merge verified |
| F3-A2 detailed contract | accepted with conditions / post-merge verified |
| F3-A2 validation plan | accepted / tests not executed |
| Concrete authority decision | **not determined — stop condition** |
| F3-A3/B/C | not promoted |
| S08/S09/S10 | unavailable |

## 5. Decision target

L'owner deve determinare o autorizzare:

- authoritative system/registry della Configuration Baseline;
- baseline owner/custodian/Approval Authority;
- assignment owner/custodian/Approval Authority;
- approval evidence source;
- prima concrete approved baseline instance, oppure una decisione esplicita che rinvii ogni materializzazione.

## 6. Rollback

Revert documentale del merge #197 e della acceptance reconciliation. Nessuna migrazione, credenziale o azione operativa.
