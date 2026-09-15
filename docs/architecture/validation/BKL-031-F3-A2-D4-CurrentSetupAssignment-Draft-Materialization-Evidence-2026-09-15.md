# BKL-031 F3-A2-D4 — CurrentSetupAssignment DRAFT Materialization Evidence

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D4-VAL-001 |
| Stato | **ACCEPTED / POST-MERGE VERIFIED** |
| Data | 15/09/2026 |
| PR | #207 |
| Implementation head | `96386395ff0d81d0d93e14666215296ade643a83` |
| Implementation workflow | `35011741820` — SUCCESS |
| Exact publication head | `d845042c1e2094cd82de762e7e2de60e9c54b2c5` — 5/5 SUCCESS |
| Merge | `e99e6b5ff5ea7247ee447a1c6c62dcaa479dee1b` |
| Post-merge | 7/7 SUCCESS; dedicated D4 run `35015436160` |
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

This evidence does not approve the assignment, create a receipt, activate a resolver, validate runtime behavior or authorize EAGLE/observatory activity. Exact-head repository workflows, AI-assisted process-separated reviews, expected-head merge and post-merge verification are complete. Explicit human approval of the exact protected digest remains mandatory.
