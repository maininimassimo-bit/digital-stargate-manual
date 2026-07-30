# ARB-012-C06 — Degraded Mode and Dependency Failure Test Plan

| Campo | Valore |
|---|---|
| Evidence target | E-ARB012-C06-01 |
| Condition | ARB-012-C06 |
| Scope | Simulated technical validation only |
| References | AP-012, OPSC-REF-001, OPSC-RUN-001, ARB-012 |
| Runtime enablement | Prohibited |

## 1. Objective

Validate, using in-memory fixtures only, that dependency failures do not produce false healthy states, unsafe command availability or ungoverned return to service.

## 2. Scenarios

1. a required dependency failure enters degraded mode;
2. a safety-critical dependency failure enters safe-restricted mode and blocks command dispatch;
3. an optional dependency failure prevents a full-health claim;
4. an unknown or stale dependency outcome is not treated as available;
5. restored dependencies enter recovery rather than immediately returning to normal;
6. return to normal requires both a satisfied stability window and independent safety verification;
7. degraded, recovery and return-to-service transitions produce explicit evidence.

## 3. Expected evidence

- test source under `DigitalStarGate.UnitTests/OperationsCenter`;
- successful restore, build, test and formatting checks;
- successful MkDocs strict verification;
- immutable references to implementation commit, merge commit, workflow run and quality-gate job;
- explicit separation between simulated technical validation and operational validation.

## 4. Safety limits

- no hardware or device adapters;
- no ASCOM, Alpaca, N.I.N.A., dome or mount integration;
- no operational dependency endpoints or thresholds;
- no C2-C4 runtime command path;
- no assertion that an actual service, network, weather source, identity provider or safety system has been tested;
- local physical interlocks and Safety Authority remain independent and authoritative.

## 5. Pass criteria

C06 may be classified `Passed` only for simulated technical scope when all scenarios pass and the repository quality gate is successful. Operational C06 remains `Blocked` until authorized fault injection, dependency monitoring, degraded-mode operations, recovery and return-to-service validation are performed with distinct authorities.
