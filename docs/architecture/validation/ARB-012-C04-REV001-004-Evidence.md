# ARB-012-C04 — REV-001..REV-004 Technical Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-REV-TECH-001 |
| Work item | C04-W03 |
| Controls | REV-001, REV-002, REV-003, REV-004 |
| Host | `dsg-arb012-c04-val` |
| DSOC repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Validated commit | `9c69fe1d1d5cea5c777293a1ddac2eeb31aa2fe3` |
| Date | 2026-08-24 |
| Result | **PASS** |

## 1. Execution

The validation harness was built successfully with 0 warnings and 0 errors:

```text
Build succeeded.
0 Warning(s)
0 Error(s)
```

The harness then produced:

```text
REV_RESULT=PASS
REV001_RESULT=PASS
REV002_RESULT=PASS
REV003_RESULT=PASS
REV004_RESULT=PASS
REV001_DECISION=DENY
REV002_STALE_APPROVAL_VALID=false
REV003_INVALIDATED=true
REV004_DETERMINISTIC=true
PHYSICAL_COMMAND_SENT=false
PRODUCTION_ACCESS_USED=false
RUN_CORRELATION_ID=c3e9b339-f341-4723-b96b-8e0f507297f6
OCCURRED_AT_UTC=2026-08-24T12:06:41.2709906+00:00
AUDIT_DB_PATH=/var/lib/digitalstargate-validation/dsoc-audit.db
EVIDENCE_PATH=/var/lib/digitalstargate-validation/evidence/REV-001-004-c3e9b339-f341-4723-b96b-8e0f507297f6.json
```

## 2. Control interpretation

- **REV-001 PASS** — Massimo eligibility is denied after suspension; Leonardo governance attribution is separately recorded.
- **REV-002 PASS** — Leonardo's approval eligibility is denied after suspension and a previously valid approval cannot be reused (`stale_approval_valid=false`); Massimo Sponsor governance attribution is separately recorded.
- **REV-003 PASS** — a pending approval is invalidated after suspension (`invalidated=true`).
- **REV-004 PASS** — denial after revocation/suspension is deterministic across repeated evaluation.

## 3. Safety outcome

```text
PHYSICAL_COMMAND_SENT=false
PRODUCTION_ACCESS_USED=false
```

No physical-device command or production access was used by this validation.

## 4. Correlation

Run correlation ID:

```text
c3e9b339-f341-4723-b96b-8e0f507297f6
```

Evidence JSON path on the validation host:

```text
/var/lib/digitalstargate-validation/evidence/REV-001-004-c3e9b339-f341-4723-b96b-8e0f507297f6.json
```

## 5. Disposition

**REV-001 THROUGH REV-004: PASS.**

Together with the attributable governance attestations already recorded for REV-001 and REV-002, this completes the revocation/suspension evidence required by C04-W03.