# ARB-012-C04 — Traceability Status

| Field | Value |
|---|---|
| Condition | `ARB-012-C04` |
| Scope | Role Assignment and Four-Eyes Enforcement |
| Status | `Blocked — ENV-011 technically executed; formal acceptance and remaining environment controls pending` |
| Updated | 2026-08-03 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `validation/arb-012-c04-env011-executed` |
| Pull request | Pending |

## Work-item traceability

| Work item | Artifact | Verified status |
|---|---|---|
| C04-W01 | `ARB-012-C04-Closure-Plan.md` | Recorded |
| C04-W02 | Sponsor decision and role assignment register | Recorded |
| C04-W03 | `ARB-012-C04-Identity-Training-Access-Review.md` | Defined; evidence incomplete |
| C04-W04 | `ARB-012-C04-Four-Eyes-Validation-Plan.md` | Defined; FE-01…FE-12 not executed |
| C04-W05 | `ARB-012-C04-Validation-Environment-Baseline.md` | Baseline defined |
| C04-W06 | Provisioning record, execution campaign, host procedure and execution result | ENV-011 technical execution positive; formal acceptance pending; remaining PRV/ENV controls incomplete |
| C04-W07 | Four-eyes scenario execution and evidence | Blocked by W03 and W06 acceptance |
| C04-W08 | Validation report and independent ARB re-review | Not started |

## Immutable DSOC baseline

| Field | Verified value |
|---|---|
| Implementation repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Immutable application commit | `37bbd581f37b62243f012cb7a72057207ab10ca6` |
| Application source PR | `DigitalStarGate.Control#1` |
| Application CI | `DSOC Bootstrap CI #2` — `success` |
| Evidence PR | `DigitalStarGate.Control#2` |
| Evidence merge commit | `7363e1b9b1bfb84277c378dbed52348c9716c70e` |
| Evidence CI | `DSOC Bootstrap CI #4` — `success` |
| Runtime | `.NET 8` |
| Validation host | `dsg-arb012-c04-val` on Microsoft Hyper-V |
| Guest OS | Ubuntu 26.04 LTS |
| Configuration mode | simulator-only |
| Fixture SHA-256 | `d4071db1a4b534d8cfb0e8dee9f931665d28307a26b000e7c3ec61811f091c94` |
| Checkpoint | `CP03-ENV011-EVIDENCE-COMPLETE` |

## Evidence status

| Evidence item | Status |
|---|---|
| `E-ENV011-01` | Pending formal host provisioning and identification record |
| `E-ENV011-02` | Recorded; immutable commit, host, SDK and 4/4 tests verified |
| `E-ENV011-03` | Recorded; fixture and manifest checksums verified; no persisted Git credential found |
| `E-ENV011-04` | Recorded; offline test positive, supported by retained screenshot; narrative reconstructed |
| `E-ENV011-05` | Recorded; simulator-only and physical-device prohibition verified |
| `E-ENV011-06` | Pending independent review and formal acceptance |
| ENV-011 | Executed with positive technical result; not formally accepted |

## Governance disposition

- Four domain tests passed against the immutable application baseline.
- The same tests passed with the VM network adapter disconnected.
- No IPv4 address or default route existed during the offline execution.
- The simulator-only manifest prohibits ASCOM, Alpaca, NINA, CPWI, production MQTT brokers, physical relay controllers and production weather stations.
- No persistent Git credential helper or plaintext credential file was identified.
- `E-ENV011-01` and `E-ENV011-06` remain mandatory before formal acceptance.
- Distinct validation accounts, database, audit store, reset verification and the remaining `ENV-001` through `ENV-012` controls remain incomplete.
- W03 evidence remains incomplete and FE-01 through FE-12 remain not executed.
- DSOC runtime command enablement, production credentials, physical-device control, positive C4, break-glass and local-interlock bypass remain prohibited.

## Published-roadmap projection

`docs/data/roadmap.json` must record ENV-011 as technically executed with positive result, while retaining formal acceptance, remaining PRV/ENV controls, W03, W07 and ARB re-review as pending.

## Exit criteria

ARB-012-C04 may move from `Blocked` only after:

1. W03 evidence is complete and accepted;
2. W06 completes all required provisioning records and distinct accounts;
3. `E-ENV011-01` and `E-ENV011-06` are accepted;
4. the isolated environment passes the complete `ENV-001` through `ENV-012` set;
5. FE-01 through FE-12 are executed with complete evidence;
6. incompatible-role and self-approval denial tests pass;
7. independent audit and ARB re-review are completed.
