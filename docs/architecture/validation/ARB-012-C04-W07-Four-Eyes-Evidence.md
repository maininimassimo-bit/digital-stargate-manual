# ARB-012-C04 — W07 Four-Eyes Validation Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-W07-001 |
| Work item | C04-W07 — Four-Eyes Validation Execution |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Host | `dsg-arb012-c04-val` |
| DSOC repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Validated commit | `7881408279921f83556ebc48f27c29477f27d9cd` |
| Date | 2026-08-24 |
| Result | **PASS — FE-01..FE-12 complete** |
| Runtime effect | None |

## 1. Build result

The four-eyes validation harness built successfully:

```text
Build succeeded.
0 Warning(s)
0 Error(s)
```

## 2. Execution result

```text
FE_RESULT=PASS
FE_01_RESULT=PASS
FE_02_RESULT=PASS
FE_03_RESULT=PASS
FE_04_RESULT=PASS
FE_05_RESULT=PASS
FE_06_RESULT=PASS
FE_07_RESULT=PASS
FE_08_RESULT=PASS
FE_09_RESULT=PASS
FE_10_RESULT=PASS
FE_11_RESULT=PASS
FE_12_RESULT=PASS
FE04_STALE_APPROVAL_VALID=false
FE07_SAFETY_DECISION=DENY
LOCAL_INTERLOCK_TOUCHED=false
FE12_TAMPER_DETECTED=true
PHYSICAL_COMMAND_SENT=false
PRODUCTION_ACCESS_USED=false
RUN_CORRELATION_ID=9141ad57-6c11-48ab-a272-192c9a3d7890
OCCURRED_AT_UTC=2026-08-24T17:48:19.6710716+00:00
AUDIT_DB_PATH=/var/lib/digitalstargate-validation/dsoc-audit.db
EVIDENCE_PATH=/var/lib/digitalstargate-validation/evidence/FE-01-12-9141ad57-6c11-48ab-a272-192c9a3d7890.json
```

## 3. Scenario disposition

| Scenario | Expected outcome | Result |
|---|---|---|
| FE-01 | Massimo C3 request -> Leonardo approval | **PASS** |
| FE-02 | Massimo self-approval attempt denied | **PASS** |
| FE-03 | Leonardo requester+approver conflict denied | **PASS** |
| FE-04 | Leonardo approval suspension invalidates stale approval | **PASS** — `FE04_STALE_APPROVAL_VALID=false` |
| FE-05 | Massimo eligibility revocation denies execution | **PASS** |
| FE-06 | Massimo maintenance -> distinct Leonardo return-to-service approval | **PASS** |
| FE-07 | Safety Authority simulated bounded decision with local interlocks untouched | **PASS** — `FE07_SAFETY_DECISION=DENY`, `LOCAL_INTERLOCK_TOUCHED=false` |
| FE-08 | Leonardo own-access approval attempt denied | **PASS** |
| FE-09 | Audit/traceability completeness | **PASS** |
| FE-10 | Positive C4 denied by governance design | **PASS** |
| FE-11 | Break-glass denied by governance design | **PASS** |
| FE-12 | Evidence tamper resistance / detection | **PASS** — `FE12_TAMPER_DETECTED=true` |

## 4. Safety outcome

```text
LOCAL_INTERLOCK_TOUCHED=false
PHYSICAL_COMMAND_SENT=false
PRODUCTION_ACCESS_USED=false
```

The run remained isolated and simulator-only. No observatory interlock, physical device or production system was used.

## 5. Correlation

Run correlation ID:

```text
9141ad57-6c11-48ab-a272-192c9a3d7890
```

Evidence JSON path on the validation host:

```text
/var/lib/digitalstargate-validation/evidence/FE-01-12-9141ad57-6c11-48ab-a272-192c9a3d7890.json
```

## 6. Current disposition

**C04-W07: PASS / COMPLETE — FE-01 THROUGH FE-12 = 12/12 PASS.**

This is validation evidence only. It does not authorize production runtime, physical-device control, positive C4 or break-glass.