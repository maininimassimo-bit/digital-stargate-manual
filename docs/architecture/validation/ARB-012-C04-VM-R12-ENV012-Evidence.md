# ARB-012-C04 — VM-R12 / ENV-012 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R12 |
| Work item | C04-W06 |
| Control | VM-R12 / ENV-012 |
| Host | `dsg-arb012-c04-val` |
| DSOC repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Validated commit | `3f855b5124d747f00efe5f727383fd46ad613980` |
| Date | 2026-08-22 |
| Result | **PASS** |

## 1. Purpose

Verify that the ARB-012-C04 validation runtime remains simulator-only, that physical-device access is disabled, that a production fallback is not selectable, and that no physical command is sent.

## 2. Repository baseline

The versioned simulator manifest defines:

- `mode = simulator-only`;
- `physicalDeviceAccess = false`;
- simulator adapters only (`SIM-*`);
- explicit prohibitions for ASCOM, Alpaca, NINA, CPWI, MQTT production brokers, physical relay controllers and production weather stations.

The VM-R12 guard validates this manifest and fails if simulator-only mode is not selected, physical device access is enabled, a non-simulator adapter is exposed, or a required prohibition is missing.

## 3. Execution result

```text
ENV012_VMR12_RESULT=PASS
SELECTED_MODE=simulator-only
PHYSICAL_DEVICE_ACCESS=false
PRODUCTION_FALLBACK_SELECTABLE=false
PHYSICAL_COMMAND_SENT=false
MANIFEST_SHA256=ff3e98f9740c8c9cad586230d6cb9918bea75e1bf6a7a9b9c5e5d76d62b3008b
RUN_CORRELATION_ID=b6796670-96db-43c6-9f30-a074c39ab26c
OCCURRED_AT_UTC=2026-08-22T16:18:58.3950873+00:00
EVIDENCE_PATH=/var/lib/digitalstargate-validation/evidence/ENV-012-VM-R12-b6796670-96db-43c6-9f30-a074c39ab26c.json
```

Exported evidence JSON SHA-256:

```text
c870659ffc3956315dd47de19bfc94931c6568937b4fb111f67be4641d7d78a9
```

The exported JSON recorded `result=PASS`, `failures=[]`, `selected_mode=simulator-only`, `physical_device_access=false`, `production_fallback_selectable=false`, and `physical_command_sent=false`.

## 4. Safety interpretation

The test is configuration/runtime selection evidence, not a physical-device probe. This is intentional: the validation environment must prove that the physical path cannot be selected without sending any command to production or observatory equipment.

The manifest SHA-256 matches the previously governed simulator baseline:

```text
ff3e98f9740c8c9cad586230d6cb9918bea75e1bf6a7a9b9c5e5d76d62b3008b
```

## 5. Disposition

**VM-R12 / ENV-012: PASS.**

The validation runtime is simulator-only; physical-device access is disabled; production fallback is not selectable; and no physical command was sent. This completes the VM-R01…VM-R12 residual validation sequence for C04-W06.