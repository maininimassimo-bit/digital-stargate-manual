# ARB-012-C04 — W06 ENV-011 Host Provisioning and Evidence Procedure

| Field | Value |
|---|---|
| Campaign ID | `C04-W06-20260731-01` |
| Work item | `C04-W06` |
| Control | `ENV-011 — Tested commit and configuration are immutable and recorded` |
| Version | 1.0 |
| Status | `PROCEDURE DEFINED — NOT EXECUTED` |
| Runtime effect | None |

## 1. Purpose

This procedure defines the operator-ready steps and evidence format for provisioning or designating the isolated validation host required by ENV-011. It does not assert that a host, network boundary, account, database, audit store, configuration or simulator runtime has been provisioned.

## 2. Frozen baseline

| Item | Required value |
|---|---|
| Documentation baseline | `6e43a7597594b44094c2231a285705ae5e9d20e5` |
| Implementation repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Application commit | `37bbd581f37b62243f012cb7a72057207ab10ca6` |
| Operating mode | simulator-only |
| Fixture SHA-256 | `d4071db1a4b534d8cfb0e8dee9f931665d28307a26b000e7c3ec61811f091c94` |

## 3. Preconditions

Execution requires named values for:

- validation host owner;
- provisioning operator;
- independent reviewer;
- host or runner identifier;
- isolation technology;
- evidence storage location;
- non-production configuration identifier.

Execution must not begin if the reviewer is the same person as the operator or if the host can reach production observatory networks, brokers, VPN profiles or physical-device endpoints.

## 4. Evidence directory structure

Use the following logical structure outside the repository. Commit only sanitized manifests and checksums.

```text
C04-W06-20260731-01/
  01-host-identity/
  02-isolation/
  03-application-baseline/
  04-configuration/
  05-simulator-endpoints/
  06-fixture/
  07-review/
```

Secrets, credentials, certificates, private keys, recovery codes and unrestricted network exports must not be committed.

## 5. Execution sequence

### Step 1 — Identify the host

Record hostname or runner ID, operating system, exact version, virtualization or container boundary, owner, operator, reviewer, timezone and synchronized time source.

Evidence: `E-ENV011-01`.

### Step 2 — Prove isolation before deployment

Export active routes, VPN profiles, firewall or network-policy rules and configured DNS or proxy settings. Test known prohibited destinations and retain failed-connection results. Stop if any production destination is reachable.

Evidence: `E-ENV011-01A` and input to `ENV-001`.

### Step 3 — Deploy the immutable application baseline

Deploy only commit `37bbd581f37b62243f012cb7a72057207ab10ca6`. Record the command and output proving the deployed revision. Do not rebuild from an unrecorded working tree.

Evidence: `E-ENV011-02`.

### Step 4 — Establish the non-production configuration

Create a secret-free simulator-only configuration with a unique identifier. Normalize line endings and ordering where applicable, export the effective configuration and calculate SHA-256. Recalculate independently and compare.

Evidence: `E-ENV011-03`.

### Step 5 — Inventory simulator adapters and endpoints

Export the simulator manifest, adapter versions and complete endpoint inventory. Every endpoint must be local, loopback, isolated test infrastructure or an explicitly approved simulator. No production fallback is permitted.

Evidence: `E-ENV011-04`.

### Step 6 — Verify the canonical fixture

Load the canonical fixture and calculate SHA-256 from the deployed copy. The value must equal `d4071db1a4b534d8cfb0e8dee9f931665d28307a26b000e7c3ec61811f091c94`.

Evidence: `E-ENV011-05`.

### Step 7 — Independent review

The reviewer compares host identity, deployed application SHA, configuration checksum, simulator manifest, endpoint inventory and fixture checksum against the frozen baseline. Record one disposition: `Passed`, `Failed` or `Blocked`.

Evidence: `E-ENV011-06`.

## 6. Sanitized evidence manifest template

| Evidence ID | Artifact | SHA-256 | Produced by | Reviewed by | Timestamp | Result |
|---|---|---|---|---|---|---|
| `E-ENV011-01` | Host and OS identity | Pending | Pending | Pending | Pending | Not Executed |
| `E-ENV011-01A` | Isolation and failed-connectivity evidence | Pending | Pending | Pending | Pending | Not Executed |
| `E-ENV011-02` | Deployed application commit proof | Pending | Pending | Pending | Pending | Not Executed |
| `E-ENV011-03` | Effective configuration and checksum | Pending | Pending | Pending | Pending | Not Executed |
| `E-ENV011-04` | Simulator manifest and endpoint inventory | Pending | Pending | Pending | Pending | Not Executed |
| `E-ENV011-05` | Deployed fixture checksum | Pending | Pending | Pending | Pending | Not Executed |
| `E-ENV011-06` | Independent review disposition | Pending | Pending | Pending | Pending | Not Executed |

## 7. Acceptance criteria

ENV-011 may be marked `Passed` only when:

1. the isolated host is uniquely identified;
2. production routes, credentials and endpoints are absent or denied;
3. the deployed application SHA equals the frozen commit;
4. the configuration identifier and reproducible SHA-256 are recorded;
5. the simulator manifest and endpoint inventory contain no production fallback;
6. the fixture checksum matches the canonical checksum;
7. every evidence item is attributable, timestamped and independently reviewed.

## 8. Stop conditions

Stop immediately if production connectivity exists, the application SHA differs, the configuration checksum is not reproducible, a simulator has a physical-device fallback, the fixture checksum differs, evidence exposes secrets, or independent review cannot be performed.

## 9. Current disposition

**Procedure status: DEFINED — NOT EXECUTED.**

ENV-011 remains `READY FOR EXECUTION`. C04-W06 remains `IN PROGRESS`; C04-W07 remains blocked. Runtime activation, physical-device control, positive C4, break-glass, self-approval and local-interlock bypass remain prohibited.
