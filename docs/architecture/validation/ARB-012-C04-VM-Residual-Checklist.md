# ARB-012-C04 — VM Residual Validation Checklist

| Field | Value |
|---|---|
| Checklist ID | ARB-012-C04-VM-RES-001 |
| Work item | C04-W06 |
| Host | `dsg-arb012-c04-val` |
| Hyper-V VM | `DSG-ARB012-C04-VALIDATION` |
| Target model | Two-Person Limited Operations Model |
| Date | 2026-08-22 |
| Status | In Progress — VM-R01 PASS; VM-R02 PASS; VM-R03 next |
| Runtime effect | Validation VM controls only; no observatory runtime effect |

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
| VM-R01 | PRV-004 / ENV-001 | Verify the validation environment has no route to observatory operational subnet `192.168.1.0/24` while retaining required non-operational connectivity | Hyper-V VM `DSG-ARB012-C04-VALIDATION`, guest `dsg-arb012-c04-val`, IP `172.30.54.130/20`; Netplan persistent `blackhole 192.168.1.0/24`; route checks to `.1` and `.254` denied; Internet route retained | **PASS** |
| VM-R02 | ENV-002 | Scan/attest that no production credentials, VPN profiles, plaintext secrets or production endpoint secrets exist in the validation environment | no OpenVPN/WireGuard files; no global/system Git credential helper; no `.git-credentials`, `.netrc`, `gh/hosts.yml` or Docker config; no suspicious environment variable names; no credential/secret/token/key/pem files in `$HOME`; `/etc` findings limited to standard `fwupd` LVFS CA certificates | **PASS** |
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

### Remediation and result

Netplan `/etc/netplan/00-installer-config.yaml` was backed up and extended with a static blackhole route for `192.168.1.0/24`. `netplan generate` passed, `netplan try --timeout 60` was accepted without loss of SSH, and post-change routing denied `192.168.1.1` and `192.168.1.254` while retaining the Internet route through `172.30.48.1`.

**VM-R01 / PRV-004 / ENV-001: PASS.**

## 5. VM-R02 execution evidence — 2026-08-22

Executed read-only checks on `dsg-arb012-c04-val` as `dsgoperator`.

Observed results:

- `find /etc/openvpn /etc/wireguard ...` returned no files;
- no global Git credential helper;
- no system Git credential helper;
- `/home/dsgoperator/.git-credentials` absent;
- `/home/dsgoperator/.netrc` absent;
- `/home/dsgoperator/.config/gh/hosts.yml` absent;
- `/home/dsgoperator/.docker/config.json` absent;
- environment-variable-name scan found no names matching token/secret/password/API-key/private/credential/VPN patterns;
- `$HOME` file-name scan found no credential/secret/token/OVPN/P12/PFX/KEY/PEM files;
- `/etc` file-name scan returned only:
  - `/etc/pki/fwupd-metadata/LVFS-CA.pem`;
  - `/etc/pki/fwupd-metadata/LVFS-CA-2025PQ.pem`;
  - `/etc/pki/fwupd/LVFS-CA.pem`;
  - `/etc/pki/fwupd/LVFS-CA-2025PQ.pem`.

These are standard `fwupd` LVFS CA certificate files and are not treated as production credentials or private-key evidence.

**VM-R02 / ENV-002: PASS.**

Scope note: this PASS covers the inspected validation environment and naming/location checks above. It does not claim cryptographic inspection of every file byte and does not authorize storing secret material in the repository.

## 6. Suggested execution grouping

### Group A — host/environment evidence

VM-R01 and VM-R02 are complete.

### Group B — identity and authorization plumbing

Execute VM-R03 through VM-R05 next. Never commit passwords or MFA material.

### Group C — persistence and evidence services

Execute VM-R06 through VM-R08 after the non-production DB/audit-store design is selected.

### Group D — denial and revocation scenarios

Execute VM-R09 through VM-R12 last, once accounts, roles, logging and reset are available. These tests must remain simulator-only and must never send a command to a physical observatory device.

## 7. Safety stop conditions

Stop immediately if any residual test reveals an observatory route/VPN path, production credential/profile, physical-device endpoint, self-approval, ineffective revocation, positive C4/break-glass availability or inability to preserve evidence.

## 8. Completion criteria

This checklist is complete when VM-R01 through VM-R12 have attributable `Passed` evidence, except for controls explicitly reclassified N/A by approved governance decision.

## 9. Current disposition

**IN PROGRESS — VM-R01 PASS; VM-R02 PASS; VM-R03 NEXT.**