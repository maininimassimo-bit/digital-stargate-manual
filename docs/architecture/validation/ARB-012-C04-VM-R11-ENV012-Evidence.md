# ARB-012-C04 — VM-R11 / ENV-012 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R11 |
| Work item | C04-W06 |
| Control | VM-R11 / ENV-012 |
| Host | `dsg-arb012-c04-val` |
| DSOC repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Validated commit | `fdb9114524314ec7ebacad243b7eb3d722c9e36d` |
| Date | 2026-08-22 |
| Result | **PASS** |

## 1. Purpose

Verify that positive C4 authorization and break-glass paths are unavailable in the ARB-012-C04 validation environment by design, with attributable correlated evidence and no downstream execution.

## 2. Execution result

```text
ENV012_RESULT=PASS
C4_DECISION=DENY
C4_REASON=capability-prohibited-in-validation
C4_CORRELATION_ID=d53ba1e9-b329-4bad-a562-a32141010e75
BREAK_GLASS_DECISION=DENY
BREAK_GLASS_REASON=capability-prohibited-in-validation
BREAK_GLASS_CORRELATION_ID=77c3a6f1-10d0-4c36-8d8c-a1bb10895c83
EXECUTION_ATTEMPTED=false
RUN_CORRELATION_ID=9d4711c3-b867-4b0c-aed5-78dc5eb42b54
OCCURRED_AT_UTC=2026-08-22T15:51:25.5912231+00:00
```

## 3. Correlation and audit proof

The JSONL log contains two records under the same run correlation ID:

- C4 / `AuthorizeC4` → `DENY` / `capability-prohibited-in-validation`;
- BREAK_GLASS / `BreakGlass` → `DENY` / `capability-prohibited-in-validation`.

Both records explicitly state `execution_attempted=false` and `result=PASS`.

The audit database independently returned:

```text
2026-08-22T15:51:25.5912231+00:00|77c3a6f1-10d0-4c36-8d8c-a1bb10895c83|dsgleonardo|BreakGlass|DENY|capability-prohibited-in-validation
2026-08-22T15:51:25.5912231+00:00|d53ba1e9-b329-4bad-a562-a32141010e75|dsgleonardo|AuthorizeC4|DENY|capability-prohibited-in-validation
```

The exported JSON evidence groups both cases under run correlation ID `9d4711c3-b867-4b0c-aed5-78dc5eb42b54` and records `execution_attempted=false` at both run and case level.

Evidence SHA-256:

```text
01ffae2ee01bd9db2551b145dca1d5ecb0371a2ec4c8f14fed01471a6896f5eb
```

## 4. Disposition

**VM-R11 / ENV-012: PASS.**

C4 authorization and break-glass are both prohibited by the real Application authorization policy in the validation environment, both denial outcomes are auditable, and no downstream execution is attempted.