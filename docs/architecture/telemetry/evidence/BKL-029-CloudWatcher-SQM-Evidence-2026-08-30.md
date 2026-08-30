# BKL-029 — CloudWatcher SQM Evidence — 2026-08-30

## Scope

Runtime evidence collected from `EAGLE30154` to determine whether the installed Lunatico CloudWatcher can provide a real SQM measurement for BKL-029.

This evidence is read-only and does not authorize any change to CloudWatcher, ASCOM, SafetyMonitor, firmware, serial configuration or observatory safety logic.

## Observed data file

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
  "temp": 35.0,
  "wind": 10.0,
  "gust": 16.4,
  "rain": 3200,
  "light": 2,
  "safe": 0,
  "hum": 55.804,
  "dewp": 24.878,
  "abspress": 996.688,
  "relpress": 1007.789,
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

The value `0` is rejected as an SQM measurement. The configured `DataFile` is also stale relative to the 2026-08-30 observation date, with last update on 2026-07-19.

## Architecture disposition

Current disposition:

```text
ASCOM PROPERTY: reachable
ASCOM DATA SOURCE: configured but stale
DEVICE FIRMWARE: 5.86
SQM FIELD IN CONFIGURED DATA FILE: absent
VALID SQM SAMPLE: not verified
BKL-029 G1: blocked on valid instrumental source/value
weather.sqm_mag_arcsec2: must remain null
```

Firmware 5.86 is earlier than the vendor-documented 5.89 protocol support for the new sky-quality sensor. This evidence does **not** by itself prove the physical unit lacks the upgrade sensor, but it proves that the currently observed firmware/data path does not expose a valid SQM measurement.

No firmware update is authorized by BKL-029 source discovery. A firmware change would be a separate controlled maintenance decision with compatibility, rollback and safety review.

## Next governed step

Locate the CloudWatcher output that is being updated **currently** on EAGLE30154 and determine whether the ASCOM `DataFile` setting points to an obsolete file.

The next inspection must remain passive and must:

1. enumerate likely AAG/CloudWatcher JSON/DAT/CSV output files under the current user's Documents/AppData and configured CloudWatcher locations;
2. report path, size and UTC/local last-write timestamps;
3. identify files updated recently without modifying them;
4. inspect only small text files for `cwinfo`, `sqm`, `sky quality`, `mpsas` and related field names;
5. never infer SQM from `light`, LDR, cloud or sky-temperature fields;
6. never change the ASCOM `DataFile` setting automatically.
