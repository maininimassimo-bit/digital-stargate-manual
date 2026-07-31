# ARB-012-C04 — W06 Provisioning Execution Runbook

| Field | Value |
|---|---|
| Work item | C04-W06 — Validation Environment Provisioning and Account Setup |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condition | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Version | 1.0 |
| Date | 2026-07-31 |
| Status | Execution runbook defined; no provisioning evidence recorded |
| Runtime effect | None |

## 1. Purpose

This runbook converts the W06 provisioning record into an executable, evidence-driven sequence. It defines what must be performed, what evidence must be retained, who may perform and review each action, and which stop conditions block progression.

This document does not assert that any host, account, network rule, database, audit store, simulator or validation control has been provisioned or passed.

## 2. Mandatory prerequisites

Before execution begins, record:

- implementation repository and component;
- immutable application commit SHA;
- validation host owner;
- provisioning operator;
- reviewer for network isolation and access controls;
- non-production configuration identifier;
- planned evidence-bundle identifier.

Execution must not begin while the implementation repository or tested commit is unknown.

## 3. Execution phases

### Phase A — Baseline identification

1. Record the documentation baseline commit from `main`.
2. Record the implementation repository, component and immutable commit SHA.
3. Assign a campaign identifier in the form `C04-W06-YYYYMMDD-NN`.
4. Create an evidence directory or store using that identifier.
5. Record operator and reviewer identities.

Exit condition: PRV-005 and the campaign identifier are populated.

### Phase B — Isolated host preparation

1. Provision or designate a non-production host, VM or container runner.
2. Record hostname, operating system and exact version.
3. Disable automatic connection to production VPN profiles.
4. Confirm that no production credentials, certificates or secrets are installed.
5. Create a clean snapshot or rebuild point.

Required evidence:

- host inventory export;
- operating-system version output;
- installed credential and VPN-profile review result;
- initial snapshot identifier.

Exit condition: PRV-001, PRV-002, PRV-003 and PRV-011 have evidence references.

### Phase C — Network isolation

1. Apply deny rules before deploying the application.
2. Deny operational subnets, VPN routes, device endpoints and production brokers.
3. Test all known prohibited destinations.
4. Record commands, timestamps and results.
5. Have a reviewer inspect the deny rules and test results.

Required evidence:

- firewall or network-policy export;
- route table export;
- failed connection-test results;
- reviewer disposition.

Stop immediately if any prohibited destination is reachable.

Exit condition: PRV-004 and ENV-001 are supported by accepted evidence.

### Phase D — Non-production data and audit services

1. Provision a separate test database.
2. Provision a separate audit evidence store.
3. Configure append-only or tamper-evident controls where supported.
4. Define retention and export procedures.
5. Verify that neither service references production data sources.

Required evidence:

- engine and version identifiers;
- instance identifiers;
- configuration exports with secrets removed;
- append-only or integrity-control evidence;
- retention setting.

Exit condition: PRV-007, PRV-008 and ENV-008 have evidence references.

### Phase E — Application and simulator deployment

1. Deploy only the recorded immutable application commit.
2. Deploy the recorded non-production configuration.
3. Record configuration checksum.
4. Deploy deterministic simulation adapters.
5. Inventory all configured endpoints.
6. Verify that no simulator has a production fallback.
7. Load the canonical fixture bundle and record its checksum.

Required evidence:

- application commit output;
- configuration checksum;
- endpoint inventory;
- simulator version;
- fixture checksum.

Exit condition: PRV-005, PRV-006, PRV-009, PRV-010, ENV-003 and ENV-011 have evidence references.

### Phase F — Account creation and least privilege

1. Create ACC-001 for Massimo Mainini.
2. Create ACC-002 for Leonardo Di Egidio.
3. Enforce distinct credentials and sessions.
4. Apply deny-by-default grants.
5. Export the effective role-to-permission mapping.
6. Verify that Massimo cannot self-approve.
7. Verify that Leonardo cannot request and approve the same operation.
8. Verify that both accounts lack production, C4 and break-glass authority.

Required evidence:

- non-sensitive account identifiers;
- role and permission exports;
- login and failed-access audit events;
- denial-test outputs;
- reviewer disposition.

Exit condition: ACC-001, ACC-002, ENV-004, ENV-005, ENV-006 and ENV-012 have evidence references.

### Phase G — Revocation, reset and observability

1. Revoke one validation role before execution and confirm immediate denial.
2. Invalidate any pending approval made by the revoked role.
3. Restore the initial snapshot or deterministic seed.
4. Repeat the reset and compare resulting state.
5. Confirm correlation IDs, audit event IDs and evidence export.
6. Confirm synchronized time and explicit timezone.

Required evidence:

- revocation event and denial result;
- invalidated approval record;
- before and after reset checksums or state exports;
- log and correlation-ID sample;
- time-source output.

Exit condition: PRV-011, PRV-012, ENV-007, ENV-009 and ENV-010 have evidence references.

### Phase H — Environment acceptance

1. Review ENV-001 through ENV-012.
2. Mark each result `Passed`, `Failed`, `Blocked` or `Not Executed`.
3. Record evidence references and reviewer identity.
4. Record all deviations and remediation actions.
5. Freeze the accepted application commit, configuration checksum and fixture version.

The environment is accepted only when every ENV check is `Passed`.

## 4. Evidence index template

| Evidence ID | Related control | Description | Produced by | Reviewed by | Date | Result |
|---|---|---|---|---|---|---|
| Pending | PRV/ACC/ENV ID | Pending | Pending | Pending | Pending | Not Executed |

Secrets, passwords, tokens, private keys, certificates, recovery codes and identity-document images must never be committed.

## 5. Acceptance decision template

| Field | Value |
|---|---|
| Campaign ID | Pending |
| Documentation baseline | Pending |
| Implementation repository | Pending |
| Tested commit SHA | Pending |
| Configuration checksum | Pending |
| Fixture checksum | Pending |
| ENV-001…ENV-012 disposition | Not Executed |
| Accepted by | Pending |
| Acceptance date | Pending |
| W07 authorization | Denied until all criteria pass |

## 6. Stop conditions

Stop execution immediately when:

- any production route, credential, endpoint or device is reachable;
- the implementation commit cannot be proven;
- self-approval succeeds;
- role revocation is not immediately enforced;
- evidence is missing, mutable without detection or unattributable;
- a simulator can fall back to production;
- positive C4, break-glass or physical control becomes available;
- deterministic reset cannot be demonstrated.

A failed denial or isolation test blocks all later positive scenarios.

## 7. Completion criteria

This runbook is complete as a document when its execution sequence, evidence requirements, stop conditions and acceptance decision are reviewable.

C04-W06 itself is complete only when:

- PRV-001 through PRV-012 are evidenced and accepted;
- ACC-001 and ACC-002 exist with approved least privilege;
- ENV-001 through ENV-012 are executed and passed;
- the accepted baseline is frozen;
- an identified reviewer authorizes progression to W07.

## 8. Current disposition

**Runbook status: DEFINED — execution not performed.**

**C04-W06 remains IN PROGRESS.** C04-W07 remains blocked. Runtime activation, physical-device control, positive C4, break-glass, self-approval and local-interlock bypass remain prohibited.
