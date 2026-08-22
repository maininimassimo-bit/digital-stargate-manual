# ARB-012-C04 — VM Residual Validation Checklist

| Field | Value |
|---|---|
| Checklist ID | ARB-012-C04-VM-RES-001 |
| Work item | C04-W06 |
| Host | `dsg-arb012-c04-val` |
| Hyper-V VM | `DSG-ARB012-C04-VALIDATION` |
| Target model | Two-Person Limited Operations Model |
| Date | 2026-08-22 |
| Status | In Progress — VM-R01 PASS; VM-R02 next |
| Runtime effect | Validation VM network isolation only; no observatory runtime effect |

## 1. Purpose

Provide the minimal execution list for VM work that is genuinely still missing after reconciliation of the completed ENV-011 campaign. Completed baseline controls are deliberately excluded from rerun.

## 2. Do not repeat

Unless the VM/application baseline changes, do **not** repeat:

- host/OS/.NET identification;
- immutable application commit verification;
- simulator-only configuration checksum;
- canonical fixture checksum;
- four domain tests online;
- four domain tests with Hyper-V adapter disconnected;
- ENV-011 offline no-route transcript;
- simulator/physical-device prohibition source check;
- Chrony/time-sync verification;
- ENV-003 simulator-only baseline;
- ENV-011 immutable technical baseline.

## 3. Residual checklist

| Step | Controls | Action | PASS evidence | Status |
|---|---|---|---|---|
| VM-R01 | PRV-004 / ENV-001 | Verify the validation environment has no route to observatory operational subnet `192.168.1.0/24` while retaining required non-operational connectivity | Hyper-V VM `DSG-ARB012-C04-VALIDATION`, guest `dsg-arb012-c04-val`, IP `172.30.54.130/20`; before control, kernel routed `192.168.1.1` and `.254` via `172.30.48.1`; `ufw` inactive and nft ruleset empty. Added Netplan static `blackhole 192.168.1.0/24`, validated by `netplan generate`, accepted with `netplan try --timeout 60`; post-control `ip route` shows `blackhole 192.168.1.0/24 proto static`; `ip route get 192.168.1.1` and `.254` return `RTNETLINK answers: Invalid argument`; Internet route to `1.1.1.1` remains via `172.30.48.1`. | **PASS — persistent enforcement configured and accepted** |
| VM-R02 | ENV-002 | Scan/attest that no production credentials, VPN profiles, plaintext secrets or production endpoint secrets exist in the validation environment | command/output summary with sensitive values redacted; reciprocal review where applicable | Pending |
| VM-R03 | ACC-001 / ENV-004 | Create or identify Massimo's unique non-production validation account | username/account ID, ownership attestation, successful distinct session; no secret | Pending |
| VM-R04 | ACC-002 / ENV-004 | Create or identify Leonardo's unique non-production validation account | username/account ID, ownership attestation, successful distinct session; no secret | Pending |
| VM-R05 | ENV-005 | Apply/verify two-person least-privilege role mapping | role export/mapping showing Massimo cannot approve C3/own RTS and Leonardo cannot request+approve same action or approve own access | Pending |
| VM-R06 | PRV-007 / PRV-008 / ENV-008 | Define non-production test database and audit evidence store | engine/store identifiers, non-production designation, location, access/retention characteristics | Pending |
| VM-R07 | PRV-011 / ENV-009 | Prove deterministic reset/rebuild | before-state identifier, reset/rebuild procedure, after-state checksum/test result | Pending |
| VM-R08 | ENV-010 | Verify logs, correlation IDs and evidence export | one validation request correlated across log/audit/evidence export with timestamps | Pending |
| VM-R09 | ENV-006 | Attempt Massimo self-approval / same-identity C3 approval | deterministic denial plus audit record; no execution | Pending |
| VM-R10 | ENV-007 | Revoke/suspend an applicable validation role before execution | subsequent execution denied and audited | Pending |
| VM-R11 | ENV-012 | Attempt positive C4 and break-glass paths | both unavailable/denied by design and audited where applicable | Pending |
| VM-R12 | ENV-012 | Verify physical-device/production fallback cannot be selected from the effective validation configuration | configuration/runtime denial evidence; no physical command is sent | Pending |

## 4. VM-R01 execution evidence — 2026-08-22

### Baseline observed before enforcement

```text
hostname: dsg-arb012-c04-val
user: dsgoperator
IPv4: 172.30.54.130/20 on eth0
default route: via 172.30.48.1
route to 192.168.1.1: via 172.30.48.1 dev eth0
route to 192.168.1.254: via 172.30.48.1 dev eth0
ufw: inactive
nft ruleset: empty
VPN interfaces/services: none observed
```

This state was classified `FAIL` for persistent ENV-001 isolation because a kernel route existed from the validation VM toward the observatory LAN.

### Remediation

Netplan file `/etc/netplan/00-installer-config.yaml` was backed up as `/etc/netplan/00-installer-config.yaml.bak-20260822` and extended with:

```yaml
routes:
  - to: 192.168.1.0/24
    type: blackhole
```

Validation and activation evidence:

- `sudo netplan generate` completed without error;
- `sudo netplan get` returned the expected blackhole route;
- `sudo netplan try --timeout 60` kept SSH connectivity and was explicitly accepted;
- `ip route` returned `blackhole 192.168.1.0/24 proto static`;
- `ip route get 192.168.1.1` -> `RTNETLINK answers: Invalid argument`;
- `ip route get 192.168.1.254` -> `RTNETLINK answers: Invalid argument`;
- `ip route get 1.1.1.1` continued to use `172.30.48.1`.

### Result

**VM-R01 / PRV-004 / ENV-001: PASS.**

The validation VM retains the connectivity required for administration/updates through the Hyper-V Default Switch while the known Digital StarGate operational LAN `192.168.1.0/24` is explicitly unroutable from the guest. This evidence does not claim isolation from any additional operational subnet that has not been identified in the governed architecture.

## 5. Suggested execution grouping

### Group A — host/environment evidence

VM-R01 is complete. Execute VM-R02 next. VM-R02 is read-only/inspection-oriented and should not require application role plumbing.

### Group B — identity and authorization plumbing

Execute VM-R03 through VM-R05 after W03 identity/access decisions are attributable. Never commit passwords or MFA material.

### Group C — persistence and evidence services

Execute VM-R06 through VM-R08 after the non-production DB/audit-store design is selected.

### Group D — denial and revocation scenarios

Execute VM-R09 through VM-R12 last, once accounts, roles, logging and reset are available. These tests must remain simulator-only and must never send a command to a physical observatory device.

## 6. Evidence record format

For each completed step record:

```text
Step: VM-Rxx
Controls: <IDs>
Host: dsg-arb012-c04-val
Executed-by: <Massimo Mainini | Leonardo Di Egidio>
Reviewed-by: <other person where reciprocal review is applicable>
Date-UTC: <timestamp>
Baseline-commit: 37bbd581f37b62243f012cb7a72057207ab10ca6
Result: Passed | Failed
Evidence-reference: <repository path / issue / commit / redacted transcript>
Notes: <non-sensitive notes>
```

Failed results must be retained; do not overwrite them with a later successful run.

## 7. Safety stop conditions

Stop immediately if any residual test reveals:

- an observatory operational route or VPN path;
- a production credential/profile;
- a physical-device endpoint selected by the validation runtime;
- self-approval or same-identity C3 execution;
- ineffective revocation;
- positive C4 or break-glass availability;
- inability to correlate or preserve validation evidence.

No residual test authorizes production access, EAGLE access, dome/mount/camera commands or local-interlock bypass.

## 8. Completion criteria

This checklist is complete when VM-R01 through VM-R12 have attributable `Passed` evidence, except for any control explicitly reclassified N/A by an approved governance decision.

Completion of this checklist closes only the residual VM portion of C04-W06; W03 attributable evidence and W07 FE scenario execution remain separately governed.

## 9. Current disposition

**IN PROGRESS — VM-R01 PASS; VM-R02 NEXT.**

ENV-003 and ENV-011 remain covered by the existing immutable technical baseline and are not rerun items.