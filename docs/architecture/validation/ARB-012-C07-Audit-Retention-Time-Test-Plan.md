# ARB-012-C07 — Audit, Retention and Time Integrity Test Plan

| Campo | Valore |
|---|---|
| Evidence target | E-ARB012-C07-01 |
| Condition | ARB-012-C07 |
| Scope | Simulated technical validation only |
| References | AP-004, AP-012, OPSC-ALM-001, ARB-012 |
| Runtime enablement | Prohibited |

## 1. Objective

Validate, using in-memory fixtures only, that audit records are complete, correlated, tamper-evident, time-ordered and governed by retention decisions that prevent premature or legally prohibited deletion.

## 2. Scenarios

1. audit records require actor, source, target, outcome, correlation ID and UTC timestamp;
2. incomplete records are rejected;
3. a chained audit ledger detects post-write tampering;
4. duplicate or non-monotonic timestamps are rejected;
5. untrusted clock evidence is rejected;
6. excessive simulated clock skew is rejected against an explicitly candidate, non-operational policy;
7. retention prevents deletion before expiry;
8. legal hold prevents deletion even after retention expiry;
9. retention decisions produce explicit evidence and reason codes.

## 3. Expected evidence

- test source under `DigitalStarGate.UnitTests/OperationsCenter`;
- successful restore, build, test and formatting checks;
- successful MkDocs strict verification;
- immutable references to implementation commit, merge commit, workflow run and quality-gate job;
- explicit separation between simulated technical validation and operational validation.

## 4. Safety and governance limits

- no operational audit store, SIEM, database or immutable storage service;
- no real retention schedule or legal requirement is asserted;
- no production NTP, PTP, GPS or other trusted-time source is validated;
- no operational clock-skew threshold is established;
- no hardware, ASCOM, Alpaca, N.I.N.A., dome or mount integration;
- no C2-C4 runtime command path;
- local physical interlocks and Safety Authority remain independent and authoritative.

## 5. Pass criteria

C07 may be classified `Passed` only for simulated technical scope when all scenarios pass and the repository quality gate is successful. Operational C07 remains `Blocked` until the authorized audit platform, retention schedule, legal-hold controls, trusted-time source, clock monitoring, delivery-failure handling, access controls and restoration evidence are validated with distinct authorities.
