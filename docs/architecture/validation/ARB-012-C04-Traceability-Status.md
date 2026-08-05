# ARB-012-C04 — Traceability Status

| Field | Value |
|---|---|
| Condition | `ARB-012-C04` |
| Scope | Role Assignment and Four-Eyes Enforcement |
| Status | `Blocked — ENV-011 technical evidence complete; formal acceptance and remaining environment controls pending` |
| Updated | 2026-08-04 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `validation/arb-012-c04-env011-technical-evidence-complete` |
| Pull request | Pending |

## Work-item traceability

| Work item | Artifact | Verified status |
|---|---|---|
| C04-W01 | `ARB-012-C04-Closure-Plan.md` | Recorded |
| C04-W02 | Sponsor decision and role assignment register | Recorded |
| C04-W03 | `ARB-012-C04-Identity-Training-Access-Review.md` | Defined; evidence incomplete |
| C04-W04 | `ARB-012-C04-Four-Eyes-Validation-Plan.md` | Defined; FE-01…FE-12 not executed |
| C04-W05 | `ARB-012-C04-Validation-Environment-Baseline.md` | Baseline defined |
| C04-W06 | Provisioning record, execution campaign, host procedure and execution result | ENV-011 technical evidence complete; formal acceptance pending; remaining PRV/ENV controls incomplete |
| C04-W07 | Four-eyes scenario execution and evidence | Blocked by W03 and W06 formal acceptance |
| C04-W08 | Validation report and independent ARB re-review | Not started |

## Immutable DSOC baseline

| Field | Verified value |
|---|---|
| Implementation repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Immutable application commit | `37bbd581f37b62243f012cb7a72057207ab10ca6` |
| Application source PR | `DigitalStarGate.Control#1` |
| Application CI | `DSOC Bootstrap CI #2` — `success` |
| Initial evidence PR | `DigitalStarGate.Control#2` |
| Initial evidence merge commit | `7363e1b9b1bfb84277c378dbed52348c9716c70e` |
| Host-identification PR | `DigitalStarGate.Control#3` |
| Host-identification merge commit | `c58fbd4bfac5435daa5e5f9cafab437b28283b9b` |
| Technical-evidence completion PR | `DigitalStarGate.Control#4` |
| Technical-evidence completion merge commit | `8883c596849907cd63a76c33347ff01386bdd34c` |
| Technical-evidence CI | `DSOC Bootstrap CI #8` — `success` |
| Runtime | `.NET 8` |
| Validation host | `dsg-arb012-c04-val` on Microsoft Hyper-V |
| Guest OS | Ubuntu 26.04 LTS |
| Configuration mode | simulator-only |
| Effective configuration ID | `DSOC-ENV011-SIM-CONFIG-001` |
| Fixture SHA-256 | `d4071db1a4b534d8cfb0e8dee9f931665d28307a26b000e7c3ec61811f091c94` |
| Checkpoint | `CP03-ENV011-EVIDENCE-COMPLETE` |

## Evidence status

| Evidence item | Status |
|---|---|
| `E-ENV011-01` | Recorded; host provisioning, identity and attribution completed |
| `E-ENV011-01B` | Recorded; Chrony provider and synchronized clock state verified |
| `E-ENV011-02` | Recorded; immutable commit, host, SDK and 4/4 online tests verified |
| `E-ENV011-03` | Recorded; fixture and manifest checksums verified; no persisted Git credential found |
| `E-ENV011-03A` | Recorded; effective deterministic simulator configuration and reproducible checksums verified |
| `E-ENV011-04` | Recorded as reconstructed historical narrative |
| `E-ENV011-04A` | Recorded as primary raw offline transcript; 4/4 tests passed with adapter disconnected |
| `E-ENV011-05` | Recorded; simulator-only and physical-device prohibition verified |
| `E-ENV011-06` | Review form prepared; attributable independent-review disposition pending |
| Independent AI technical re-review | Technical review completed; not a formal acceptance disposition |
| ENV-011 | Technical evidence complete; not formally accepted |

## Governance disposition

- Four domain tests passed against the immutable application baseline both online and offline.
- The raw offline transcript records `eth0` down, no global IPv4 address and no default route.
- Ping and GitHub HTTPS/DNS access failed while disconnected, as expected.
- The effective simulator configuration is uniquely identified and reproducibly checksummed.
- The simulator-only manifest prohibits ASCOM, Alpaca, NINA, CPWI, production MQTT brokers, physical relay controllers and production weather stations.
- The active time-synchronization provider is Chrony and the system clock was synchronized.
- No persistent Git credential helper or plaintext credential file was identified.
- `E-ENV011-06` remains mandatory before formal acceptance.
- Distinct validation accounts, database, audit store, reset verification and the remaining `ENV-001` through `ENV-012` controls remain incomplete.
- W03 evidence remains incomplete and FE-01 through FE-12 remain not executed.
- DSOC runtime command enablement, production credentials, observatory routes, physical-device control, positive C4, break-glass, self-approval and local-interlock bypass remain prohibited.

## Published-roadmap projection

`docs/data/roadmap.json` must record ENV-011 as having complete technical evidence while retaining formal acceptance, remaining PRV/ENV controls, W03, W07 and ARB re-review as pending.

## Exit criteria

ARB-012-C04 may move from `Blocked` only after:

1. W03 evidence is complete and accepted;
2. W06 completes all required provisioning records and distinct accounts;
3. `E-ENV011-06` is completed with an attributable `Passed` disposition;
4. the isolated environment passes the complete `ENV-001` through `ENV-012` set;
5. FE-01 through FE-12 are executed with complete evidence;
6. incompatible-role and self-approval denial tests pass;
7. independent audit and ARB re-review are completed.
