# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — F3-A2 DETAILED CONTRACT REVIEW CANDIDATE / DOCUMENTATION ONLY** |
| Repository baseline | `main@357a5edfbd39346b10a1a2d751018ff6d1dd208f` |
| Working branch | `docs/bkl-031-f3-a2-setup-authority-contract` |
| Current package | `BKL-031-F3-A2-CONTRACT-001` + `BKL-031-F3-A2-VAL-001` |
| Runtime delta | None |
| Data/schema delta | None |
| Infrastructure delta | None |

## 1. Baseline integrata

`DSG-AEM-001` è integrato tramite PR #196 e merge `357a5edfbd39346b10a1a2d751018ff6d1dd208f`, verificato con 9/9 workflow post-merge inclusi Pages e Governed Projection Sync.

F3-A2 handoff è accepted with conditions/post-merge verified tramite PR #195.

## 2. Stato tecnico corrente

Il detailed contract definisce aggregate, reference envelope, ports, eligibility, lifecycle, UTC half-open validity, failure semantics e public/protected boundary.

Non esistono baseline concrete approvate attestate, assignment, classi, schema JSON, fixture, validator, persistence, API, cache, provider, deployment o integrazione EAGLE.

## 3. Risoluzione ARB-195-MI01

| Requisito | Stato |
|---|---|
| separazione AP-006 architecture / baseline instance | defined |
| canonical baseline identity/version/digest | required by reference contract |
| owner/custodian/approval authority | required as resolvable references |
| approval evidence and effective validity | required |
| missing/unapproved/ambiguous/mismatch failure | fail-closed reason codes defined |
| S09 without materialization | UNAVAILABLE_CURRENT |

La closure formale della Minor spetta alla review ARB.

## 4. Dependency readiness

| Elemento | Stato |
|---|---|
| F3 architecture | accepted with conditions |
| F3-A1 | accepted with conditions / not implemented |
| F3-A2 handoff | accepted with conditions / post-merge verified |
| F3-A2 detailed contract | review candidate |
| F3-A2 validation cases | documented / not executed |
| F3-A3/B/C | not promoted |
| S09 | UNAVAILABLE_CURRENT |

## 5. Verification target

- documentation-only scope;
- no existence claim for concrete baseline/assignment;
- deterministic no-latest-wins resolution;
- public allowlist deny-by-default;
- validation matrix marked NOT EXECUTED;
- exact-head CI, nav and projection consistency;
- AI-assisted ARB/RQ disclosure;
- repository-only rollback.

## 6. Rollback

Revert documentale del package. Nessuna migrazione, credenziale o azione operativa.
