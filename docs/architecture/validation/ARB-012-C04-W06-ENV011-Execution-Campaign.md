# ARB-012-C04 — W06 ENV-011 Execution Campaign

| Field | Value |
|---|---|
| Campaign ID | `C04-W06-20260731-01` |
| Work item | `C04-W06` |
| Control | `ENV-011 — Tested commit and configuration are immutable and recorded` |
| Status | `READY FOR EXECUTION` |
| Date established | 2026-07-31 |
| Runtime effect | None |

## 1. Purpose

This campaign provides the controlled evidence record for executing ENV-011 against an isolated, non-production validation environment. Establishing this document does not assert that a validation host, deployed configuration, account, database, audit store, network isolation control or simulator runtime has been provisioned.

## 2. Frozen source baseline

| Baseline field | Verified value |
|---|---|
| Implementation repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Default branch | `main` |
| Immutable application commit | `37bbd581f37b62243f012cb7a72057207ab10ca6` |
| Source pull request | `DigitalStarGate.Control#1` |
| Source CI | `DSOC Bootstrap CI #2` — `success` |
| Runtime baseline | `.NET 8` |
| Operating mode | simulator-only |
| Canonical fixture SHA-256 | `d4071db1a4b534d8cfb0e8dee9f931665d28307a26b000e7c3ec61811f091c94` |
| Documentation baseline | `33cef4ada398232159d7593aac387e1a917d6b1b` |

## 3. Required execution inputs

The following values must be recorded from the real isolated environment before ENV-011 can pass:

| Input | Required value | Status |
|---|---|---|
| Validation host | Unique hostname or runner identifier | Pending |
| Host operating system | Product and exact version | Pending |
| Isolation mechanism | VM, container or dedicated runner boundary | Pending |
| Deployed application SHA | Must equal the frozen application commit | Pending |
| Configuration identifier | Unique non-production configuration ID | Pending |
| Configuration SHA-256 | Checksum calculated from the deployed, secret-free configuration | Pending |
| Simulator manifest | Deployed adapter manifest and version | Pending |
| Fixture checksum | Must equal the canonical fixture checksum | Pending |
| Endpoint inventory | Simulator endpoints only; no production fallback | Pending |
| Operator | Natural person executing the campaign | Pending |
| Reviewer | Independent reviewer of evidence | Pending |

## 4. Execution procedure

1. Provision or designate an isolated non-production host.
2. Confirm that no production VPN profile, credential, certificate, route or device endpoint is present.
3. Check out or deploy exactly commit `37bbd581f37b62243f012cb7a72057207ab10ca6`.
4. Record the deployed commit using a command whose output is retained as evidence.
5. Create the simulator-only configuration without secrets.
6. Produce a deterministic, normalized configuration export and calculate its SHA-256 checksum.
7. Deploy only the simulator manifest associated with the frozen source baseline.
8. Load the canonical fixture and calculate its SHA-256 checksum.
9. Export the complete endpoint inventory and verify that every endpoint is non-production and simulator-only.
10. Have the reviewer compare the deployed values against the frozen source baseline.
11. Record ENV-011 as `Passed`, `Failed` or `Blocked` with evidence references.

## 5. Evidence register

| Evidence ID | Description | Produced by | Reviewed by | Result |
|---|---|---|---|---|
| `E-ENV011-01` | Host and OS identity | Pending | Pending | Not Executed |
| `E-ENV011-02` | Deployed application commit output | Pending | Pending | Not Executed |
| `E-ENV011-03` | Secret-free configuration export and checksum | Pending | Pending | Not Executed |
| `E-ENV011-04` | Simulator manifest and endpoint inventory | Pending | Pending | Not Executed |
| `E-ENV011-05` | Canonical fixture checksum verification | Pending | Pending | Not Executed |
| `E-ENV011-06` | Independent comparison and disposition | Pending | Pending | Not Executed |

No password, token, private key, certificate, recovery code, production endpoint secret or personal identity document may be committed.

## 6. Pass criteria

ENV-011 passes only when all of the following are true:

- the deployed application SHA exactly matches the frozen application commit;
- the deployed non-production configuration has a recorded identifier and checksum;
- the simulator manifest is immutable and recorded;
- the loaded fixture checksum matches the canonical checksum;
- the endpoint inventory contains no production endpoint or fallback;
- all evidence is attributable, timestamped and independently reviewed.

## 7. Stop conditions

Stop immediately if:

- the deployed commit differs from the frozen commit;
- the configuration contains a production route, credential or endpoint;
- a simulator can fall back to a physical device or production service;
- the configuration checksum cannot be reproduced;
- evidence contains secrets;
- the reviewer cannot independently verify the baseline.

## 8. Current disposition

**ENV-011: READY FOR EXECUTION — not executed and not passed.**

C04-W06 remains `IN PROGRESS`. C04-W07 remains blocked. Runtime activation, physical-device control, positive C4, break-glass, self-approval and local-interlock bypass remain prohibited.
