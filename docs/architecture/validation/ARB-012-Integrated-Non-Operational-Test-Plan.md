# ARB-012 — Integrated Non-Operational Validation Test Plan

| Campo | Valore |
|---|---|
| Evidence target | E-ARB012-INT-01 |
| Scope | Integrated simulated and non-operational validation |
| Conditions covered | C01, C02, C03, C05, C06, C07 and C08 evidence chain; C04 blocker enforcement |
| References | AP-012; ARB-012; ARB-012-VAL-001 |
| Runtime enablement | Prohibited |

## 1. Objective

Validate that the previously tested simulated controls remain coherent when exercised as one integrated non-operational scenario, without connecting to operational services, devices, adapters or physical safety systems.

## 2. Scenarios

1. unknown or stale safety state blocks authorization, dispatch and any normal-health claim;
2. dependency failure enters degraded mode and correlates alarm acknowledgement, incident creation, recovery and evidence;
3. return to service requires stability, independent safety verification and complete audit evidence;
4. the single bootstrap identity cannot self-approve a C3 or C4 operation;
5. runtime, physical adapters and local-interlock bypass remain disabled by construction.

## 3. Expected evidence

- integrated test source under `DigitalStarGate.UnitTests/OperationsCenter`;
- successful restore, build, test and formatting checks;
- successful MkDocs strict verification;
- immutable references to implementation head, merge commit, workflow run and quality-gate job;
- explicit confirmation that C04 remains blocked and that integrated validation does not establish operational readiness.

## 4. Safety and governance limits

- in-memory fixtures only;
- no hardware, ASCOM, Alpaca, N.I.N.A., dome or mount integration;
- no production identity, authorization, alarm, incident, audit, retention or time source;
- no operational endpoint, threshold, routing, notification or fault injection;
- no C2-C4 runtime command path;
- no self-approval, break-glass runtime or waiver of separation of duties;
- local physical interlocks and Safety Authority remain independent and authoritative.

## 5. Pass criteria

The integrated non-operational validation may be classified `Passed` only when all scenarios pass and the repository quality gate succeeds. This result must not change C04 from `Blocked`, must not classify any operational gate as passed and must not enable runtime operation.
