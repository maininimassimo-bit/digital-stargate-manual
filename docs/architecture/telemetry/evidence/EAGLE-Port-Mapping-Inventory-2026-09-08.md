# EAGLE Port Mapping Inventory Evidence — 2026-09-08

| Field | Value |
|---|---|
| Evidence ID | `EVD-EAGLE-PORT-MAP-20260908` |
| System | `EAGLE30154` |
| Application | PrimaLuceLab EAGLE Manager X |
| Application version shown | `3.1` |
| Evidence type | Operator-provided EAGLE Manager screenshot, manually transcribed |
| Evidence date | 2026-09-08 |
| Scope | Logical USB/control-port labels and power-output labels visible in EAGLE Manager |
| Authority | Configuration inventory evidence only |
| Safety Authority | None |

## 1. Purpose

This evidence records the physical/logical mapping visible in the EAGLE Manager X screenshot supplied by the observatory owner on 2026-09-08. It closes the previous documentation gap for the EAGLE USB/control-port and power-output mapping without changing any Safety, command or telemetry authority.

The screenshot is treated as a point-in-time configuration view. Current and voltage values shown by the UI are observations from that screenshot, **not** nominal ratings, maximum ratings, thresholds or guaranteed steady-state values.

## 2. Controlled USB / top-port mapping

The four lettered top ports shown by EAGLE Manager are mapped as follows:

| EAGLE port | Configured label | UI state shown |
|---|---|---|
| `D` | `Mount` | `ON` |
| `C` | `Shelter` | `ON` |
| `B` | `USBST4` | `ON` |
| `A` | `Free` | `ON` |

Two additional USB indicators are visible at the upper-left of the EAGLE graphic, but the supplied screenshot does not show associated device labels. They remain **unresolved** and must not be assigned by inference.

## 3. Additional USB connections visible

Two lower-left USB connections are explicitly labelled in the supplied screenshot:

| UI position | Configured label | UI indication |
|---|---|---|
| Lower-left USB 1 | `USB Control Hub` | `USB` |
| Lower-left USB 2 | `Pegasus PPBAdvance` | `USB` |

The documentary labels above reproduce the EAGLE Manager configuration text. No additional device identity is inferred beyond the configured labels.

## 4. Power-output mapping

The EAGLE Manager screenshot shows the following numbered outputs and labels:

| Output | Configured label | Observed current in screenshot | Observed voltage in screenshot | Disposition |
|---:|---|---:|---:|---|
| `1` | `Free` | `--` | not shown per-output | Unused / no current shown |
| `2` | `PPBX` | `0.3 A` | not shown per-output | Mapped |
| `3` | `PPBA` | `0.3 A` | not shown per-output | Mapped |
| `4` | `UCH` | `0.1 A` | not shown per-output | Mapped |
| `5` | `Evoguide` | `0.6 A` | `11.5 V` | Mapped |
| `6` | `F4 Primario` | `0.1 A` | `11.5 V` | Mapped |
| `7` | `F4 Secondario` | `1.1 A` | `11.5 V` | Mapped |

The screenshot also shows `12.9 V` near the upper power rail and a **total instantaneous consumption of `40.1 W`**. These values are recorded only as screenshot observations; this evidence does not assign `12.9 V` as the nominal voltage of outputs 1–4 and does not derive any threshold from `40.1 W`.

## 5. Network context visible in the screenshot

For completeness, the screenshot displays:

- AP: `192.168.137.1`;
- HOST: `192.168.1.144`.

These addresses are already represented elsewhere in repository evidence and are not redefined by this record.

## 6. Authority and safety boundary

This evidence is an **inventory/configuration record** only.

It does not:

- create a passive telemetry source;
- authorize software control of power or USB ports;
- change BKL-027 source-discovery conclusions;
- create anomaly thresholds;
- authorize automatic remediation;
- change local physical Safety Authority or interlocks.

The EAGLE Manager UI may expose command-capable controls. This document records labels/states only; it does not authorize command execution.

## 7. Open items

The following remain unresolved after this evidence:

1. exact device labels for the two upper-left USB indicators;
2. nominal and maximum current ratings per connected device;
3. nominal per-output voltage policy for outputs 1–4;
4. explicit expansion/asset reconciliation of the configured abbreviations `UCH`, `PPBA` and `PPBX` where needed by the hardware inventory;
5. physical cable/connector photographs if required for a complete as-built dossier.

## 8. Documentation impact

This evidence supports updating:

- `docs/chapters/06-eagle.md` — USB/power inventory;
- `docs/chapters/44-allegati-piano-completamento.md` — `DSG-ATT-004` status.

No architecture decision or runtime implementation change is introduced.