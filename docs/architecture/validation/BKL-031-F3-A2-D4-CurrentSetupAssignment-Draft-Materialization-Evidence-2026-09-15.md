# BKL-031 F3-A2-D4 — CurrentSetupAssignment DRAFT Materialization Evidence

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D4-VAL-001 |
| Stato | **IMPLEMENTED / REVIEW CANDIDATE** |
| Data | 15/09/2026 |
| PR | #207 |
| Implementation head | `96386395ff0d81d0d93e14666215296ade643a83` |
| Workflow run | `35011741820` — SUCCESS |
| Runtime / EAGLE | Not applicable / none |

## Evidence summary

- the protected DRAFT parses and matches the closed envelope;
- owner-decision evidence matches its closed schema;
- exact Site Authority and setup-baseline bindings validate internally;
- canonical payload identity recomputes without being printed;
- DRAFT resolution returns `UNAVAILABLE_CURRENT`;
- public-tree scan rejects protected assignment literals and exact site facts;
- workflow output is redacted;
- 57/57 executable cases passed.

## Test coverage

| Group | Result |
|---|---|
| A2-P01–P12 | 12/12 PASS |
| A2-N01–N33 | 33/33 PASS |
| D4-P01–P06 | 6/6 PASS |
| PROP-01–PROP-06 | 6/6 PASS |
| Total | 57/57 PASS |

## Remediation trace

The first workflow attempt failed before tests at the protected binding gate. A diagnostic-only change exposed generic error codes and kept protected values redacted. The second diagnostic attempt passed 56/57 and isolated a semantic validity comparison defect. The comparison was remediated without changing the approved decisions or DRAFT payload. The implementation head then passed the gate and all 57 cases.

## Boundaries

This evidence does not approve the assignment, create a receipt, activate a resolver, validate runtime behavior or authorize EAGLE/observatory activity. The full publication head remains subject to exact-head repository workflows and AI-assisted process-separated ARB and Release Quality review.
