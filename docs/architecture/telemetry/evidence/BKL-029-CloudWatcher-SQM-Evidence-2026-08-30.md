# BKL-029 — CloudWatcher SQM Evidence — 2026-08-30

## Scope

Runtime evidence collected from `EAGLE30154` to determine whether the installed Lunatico CloudWatcher can provide a real SQM measurement for BKL-029.

This evidence is read-only and does not authorize any change to CloudWatcher, ASCOM, SafetyMonitor, firmware, serial configuration or observatory safety logic.

## Observed ASCOM data file

ASCOM driver configuration points to:

```text
C:\Users\PrimaLuceLab\Documents\aag_json.dat
```

Observed file metadata:

```text
Length: 581 bytes
LastWriteTime: 2026-07-19 12:00:03 local
```

Observed content includes:

```json
{
  "dateLocalTime": "2026/07/19 12:00:03",
  "cwinfo": "Serial: 2264, FW: 5.86",
  "clouds": 9.1,
  "cloudsSafe": "Unsafe",
  "temp": 35.0,
  "wind": 10.0,
  "windSafe": "Safe",
  "gust": 16.4,
  "rain": 3200,
  "rainSafe": "Safe",
  "light": 2,
  "lightSafe": "Unsafe",
  "switch": 1,
  "safe": 0,
  "hum": 55.804,
  "humSafe": "Safe",
  "dewp": 24.878,
  "abspress": 996.688,
  "relpress": 1007.789,
  "pressureSafe": "Safe",
  "rawir": 24.363
}
```

No field named or semantically equivalent to `sqm`, `skyQuality`, `sky_quality` or `mpsas` is present in the observed file.

## Device identity evidence

The observed CloudWatcher data reports:

```text
Serial: 2264
Firmware: 5.86
```

This is stronger device evidence than the Windows application version. `AAG_CloudWatcher.exe` version 9.05 identifies the client software, not the physical device firmware.

## Vendor protocol evidence

Lunatico's published RS232 protocol v1.4 states that, from firmware 5.89 onwards, command `C!` can include the additional `!8` block **if and only if** the new sky-quality light sensor is installed. `!8` contains the raw period from the new light sensor. The legacy `!4` block remains the LDR voltage and must not be interpreted as SQM.

Lunatico's current download page also states that CloudWatcher firmware 5.8.9 is required for user-upgraded units with the sky-quality grade light sensor and that this firmware includes sky-quality readings.

References:

- <https://lunaticoastro.com/aagcw/TechInfo/Rs232_Comms_v140.pdf>
- <https://lunaticoastro.com/cloudwatcher-software-downloads.html>

## ASCOM correlation

The verified ASCOM source is:

```text
ProgID: ASCOM.CloudWatcher.ObservingConditions
Driver: Lunatico CloudWatcher Observing Conditions
DriverVersion: 1.1
DataFile: C:\Users\PrimaLuceLab\Documents\aag_json.dat
MaxSecsDiff: 60
```

The controlled runtime probe returned:

```text
SkyQuality read: True
SkyQuality: 0
SensorDescription(SkyQuality): unavailable/empty
TimeSinceLastUpdate(SkyQuality): unavailable/empty
```

The value `0` is rejected as an SQM measurement. The configured `DataFile` is stale relative to the 2026-08-30 observation date, with last update on 2026-07-19.

## Active-output discovery

A passive filesystem inventory executed on `EAGLE30154` on 2026-08-30 identified the following relevant outputs:

```text
C:\Users\PrimaLuceLab\Documents\CloudWatcher\AAG_CWNetData.dat
  LastWriteTime observed: 2026-08-30 21:51:15 local
  Format: binary/proprietary; not suitable for semantic inspection using Get-Content text parsing

C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv
  Length observed: 241092326 bytes
  LastWriteTime observed: 2026-08-30 21:53:15 local

C:\Users\PrimaLuceLab\Documents\aag_json.dat
  LastWriteTime: 2026-07-19 12:00:03 local
```

This is direct evidence that `aag_json.dat` is not the currently active CloudWatcher output path. No ASCOM `DataFile` setting has been changed.

## Live CSV schema evidence

The active `CloudWatcher.csv` header observed on 2026-08-30 is:

```text
Date
Time
Cloud Condition
Rain Condition
Brightness Condition
Cloud Value
Cloud Sensor Temperature
Rain Value
Brightness Value
Ambient Temperature
Rain Heating Percentage
Rain Sensor Temperature
Heating Status
Switch Status
Read Cycle
Timeout Errors
Safe Status
Wind Condition
Wind Value
Relative Humidity
Dew Point
Raw IR Temperature
Absolute Pressure
Relative Pressure
```

No column named or semantically equivalent to `SQM`, `Sky Quality`, `mpsas`, `mag/arcsec2` or another explicit instrumental sky-quality measurement is present.

Observed complete live samples around 2026-08-30 21:52-21:53 include:

```text
Cloud Condition: Clear
Rain Condition: Dry
Brightness Condition: Dark
Cloud Value: 0.6-0.7
Brightness Value: 57232
Ambient Temperature: 25.7 C
Safe Status: Safe
Wind Condition: Calm
Wind Value: approximately 6.2-6.9
Relative Humidity: 60
Dew Point: approximately 17.2-17.3 C
Raw IR Temperature: approximately 11.0-11.1 C
Absolute Pressure: approximately 997.1-997.4 hPa
Relative Pressure: approximately 1008.6-1008.8 hPa
```

The final `Get-Content -Tail 5` row was observed partially written while the live CSV was being appended. Only complete rows are evidence.

`Brightness Condition` and `Brightness Value` are explicitly **not** accepted as SQM. They remain legacy brightness/light measurements and are prohibited as proxies by the BKL-029 architecture contract.

## Architecture disposition

Current disposition:

```text
ASCOM PROPERTY: reachable
ASCOM DATA SOURCE: configured but stale
DEVICE SERIAL: 2264
DEVICE FIRMWARE: 5.86
SQM FIELD IN STALE ASCOM DATA FILE: absent
SQM FIELD IN LIVE CSV: absent
LIVE BINARY OUTPUT: present but proprietary/not semantically decoded
VALID SQM SAMPLE: not verified
BKL-029 G1: BLOCKED — CURRENT CLOUDWATCHER PIPELINE DOES NOT EXPOSE VALID SQM
weather.sqm_mag_arcsec2: must remain null
```

Firmware 5.86 is earlier than the vendor-documented 5.89 protocol support for the new sky-quality sensor. This evidence does **not** by itself prove the physical unit lacks the upgrade sensor, but it proves that the currently observed firmware/data pipeline does not expose a valid SQM measurement.

No firmware update is authorized by BKL-029 source discovery. A firmware change would be a separate controlled maintenance decision with compatibility, rollback and safety review.

## Governed decision point

Passive discovery is complete for the current runtime pipeline. The repository now has sufficient evidence to state that BKL-029 cannot proceed to realtime integration G2 using the current CloudWatcher outputs.

The next architecture decision must choose between:

1. **CloudWatcher upgrade path** — establish whether physical unit serial 2264 supports the Lunatico sky-quality sensor upgrade and firmware 5.89/5.8.9 path; requires maintenance assessment, compatibility check, rollback plan and post-upgrade OAT before any firmware change;
2. **Dedicated SQM path** — introduce a dedicated read-only SQM instrument with a stable interface and explicit provenance, independent from Safety Authority.

Until one path is approved and produces a real instrumental sample:

- `weather.sqm_mag_arcsec2` remains `null`;
- SQM quality remains `UNKNOWN`;
- no historical SQM statistics are generated;
- no brightness/LDR proxy is permitted;
- BKL-030 does not start as a workaround for this blocked dependency.
