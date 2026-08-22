# ARB-012-C04 — VM Residual Validation Checklist

| Field | Value |
|---|---|
| Checklist ID | ARB-012-C04-VM-RES-001 |
| Work item | C04-W06 |
| Host | `dsg-arb012-c04-val` |
| Hyper-V VM | `DSG-ARB012-C04-VALIDATION` |
| Target model | Two-Person Limited Operations Model |
| Date | 2026-08-22 |
| Status | In Progress — VM-R01…VM-R08 PASS; VM-R09 next |
| Runtime effect | Validation VM controls only; no observatory runtime effect |

## 1. Purpose

Provide the minimal execution list for VM work genuinely still missing after reconciliation of the completed ENV-011 campaign. Completed baseline controls are deliberately excluded from rerun.

## 2. Do not repeat

Unless the VM/application baseline changes, do **not** repeat the completed ENV-011 host/OS/.NET, simulator-only, canonical fixture, domain test, offline no-route, physical-device prohibition, Chrony/time-sync and immutable technical baseline controls.

## 3. Residual checklist

| Step | Controls | Action | PASS evidence | Status |
|---|---|---|---|---|
| VM-R01 | PRV-004 / ENV-001 | Isolate observatory operational subnet `192.168.1.0/24` while retaining required non-operational connectivity | persistent Netplan blackhole; `.1`/`.254` denied; Internet route retained | **PASS** |
| VM-R02 | ENV-002 | Verify no production credentials, VPN profiles or plaintext production secrets | read-only credential/profile scan; only standard fwupd CA certificates found | **PASS** |
| VM-R03 | ACC-001 / ENV-004 | Massimo unique non-production validation account | `dsgmassimo`, UID 1001, distinct authenticated session, no sudo | **PASS** |
| VM-R04 | ACC-002 / ENV-004 | Leonardo unique non-production validation account | `dsgleonardo`, UID 1002, distinct authenticated session, no sudo | **PASS** |
| VM-R05 | ENV-005 | Apply/verify two-person least-privilege application policy | DSOC Application authorization slice; 10/10 tests PASS at `c8c09f1962222f064e653864de8eee4196ffbbfe`; self-approval/own RTS/self-access denied; C4/break-glass prohibited; deny-by-default | **PASS — technical policy** |
| VM-R06 | PRV-007 / PRV-008 / ENV-008 | Define non-production test database and audit evidence store | local SQLite `dsoc-validation.db` and `dsoc-audit.db`; explicit NONPROD marker; `0640`; no DB listener; evidence `E-ARB012-C04-VM-R06` | **PASS** |
| VM-R07 | PRV-011 / ENV-009 | Prove deterministic reset/rebuild | versioned SQL + rebuild script; same logical schema/seed; audit reset to 0; evidence `E-ARB012-C04-VM-R07` | **PASS** |
| VM-R08 | ENV-010 | Verify logs, correlation IDs and evidence export | request `1ea67173-c596-423e-b49d-d470abe88cb3` correlated across JSONL log, SQLite audit and JSON evidence; evidence SHA-256 `a394357f8d8ba960d6a5cdb78abea255f3934af1033e572d9f8edb210cba990f` | **PASS** |
| VM-R09 | ENV-006 | Attempt same-identity C3 approval | deterministic denial plus audit record; no execution | **NEXT** |
| VM-R10 | ENV-007 | Revoke/suspend an applicable validation role before execution | subsequent execution denied and audited | Pending |
| VM-R11 | ENV-012 | Attempt positive C4 and break-glass paths | both unavailable/denied by design and audited where applicable | Pending |
| VM-R12 | ENV-012 | Verify physical-device/production fallback cannot be selected | configuration/runtime denial evidence; no physical command sent | Pending |

## 4. Completed evidence summary

- VM-R01 / ENV-001: persistent operational-LAN blackhole PASS.
- VM-R02 / ENV-002: credential/VPN scan PASS.
- VM-R03 / ACC-001: `dsgmassimo` PASS.
- VM-R04 / ACC-002: `dsgleonardo` PASS; ENV-004 two distinct validation identities PASS.
- VM-R05 / ENV-005: Application authorization policy compiled and executed on validation VM. Domain regression suite 4/4 PASS and Application authorization suite 10/10 PASS. The initial missing-xUnit-import compile failure is retained in evidence history; corrected baseline is commit `c8c09f1962222f064e653864de8eee4196ffbbfe`.
- VM-R06 / PRV-007 / PRV-008 / ENV-008: local non-production validation and audit SQLite stores PASS; no database listener exposed.
- VM-R07 / PRV-011 / ENV-009: deterministic logical reset/rebuild from versioned repository assets PASS.
- VM-R08 / ENV-010: correlation substrate PASS; one stable correlation ID and UTC timestamp traceable across application log, audit persistence and exported evidence at DSOC commit `8147c7a7a1263801f98baea4ffdefd43acee5891`.

## 5. Next execution group

VM-R09 uses the now-proven correlation/audit substrate to demonstrate deterministic denial of same-identity C3 approval with attributable audit evidence and no execution.

No additional Linux sudo/group privileges are required for the two validation identities.

## 6. Safety stop conditions

Stop immediately if any residual test reveals an observatory route/VPN path, production credential/profile, physical-device endpoint, self-approval, ineffective revocation, positive C4/break-glass availability or inability to preserve evidence.

## 7. Completion criteria

This checklist is complete when VM-R01 through VM-R12 have attributable `Passed` evidence, except for controls explicitly reclassified N/A by an approved governance decision.

## 8. Current disposition

**IN PROGRESS — VM-R01 THROUGH VM-R08 PASS; VM-R09 NEXT.**