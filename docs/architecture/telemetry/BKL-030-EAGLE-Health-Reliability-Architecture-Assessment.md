# BKL-030 — EAGLE Health & Reliability Architecture Assessment

| Campo | Valore |
|---|---|
| Identificativo | BKL-030 |
| Stato | **In Progress — D1/D2/D3 complete; D4 designed; G1 complete; G2 architecture-ready; G3 next** |
| Data | 2026-09-03 |
| Priorità | P1 |
| Target | EAGLE30154 / Digital StarGate Observatory Status |
| Dipendenza bloccante | Nessuna — BKL-029 closed as `Done` |

## 1. Scopo e boundary

BKL-030 governa un lightweight `DSG.EagleHostHealthCollector`, host-side, non-elevated e read-only, separato da N.I.N.A. e dalla Safety Authority. Produce evidence spiegabile del computer EAGLE; non autorizza comandi verso cupola, montatura, power, router, Windows Update o altri apparati.

Sequenza canonica:

```text
BKL-029 Done -> BKL-030 In Progress -> BKL-015 -> BKL-044
```

## 2. Evidence e gate discovery

- D1 Host Baseline Inventory: **COMPLETE**.
- D2 Privilege Assessment: **COMPLETE**; low-privilege boundary praticabile, detailed SMART unavailable non-elevated.
- D3 Overhead Pilot: **COMPLETE**; D3-A e D3-B eseguiti, incluso imaging reale con N.I.N.A./PHD2.
- D4 Failure Model: **DESIGNED**; runtime validation demandata a G3/G4/G5.

Evidence primaria:

- `evidence/BKL-030-EAGLE-Health-Source-Discovery-2026-09-03.md`
- `BKL-030-D1-D2-Progress-2026-09-03.md`
- `evidence/BKL-030-D3A-Overhead-Pilot-2026-09-03.md`
- `evidence/BKL-030-D3B-Overhead-Pilot-2026-09-03.md`
- `BKL-030-D4-Failure-Model.md`

## 3. G1 — source inventory COMPLETE

Canonical inventory: `BKL-030-G1-Source-Inventory.md`.

Verified source families include OS/uptime, CPU, RAM, logical disk capacity, physical disk aggregate health, time/service evidence, Task Scheduler, process table, Event Log, PnP/COM, pending reboot raw evidence, Windows Update service state and DSG/log filesystem metadata. Detailed SMART remains `UNAVAILABLE_NON_ELEVATED`; configuration drift remains an explicit source gap until a baseline manifest exists.

Storage is governed as two independent evidence families:

- **capacity:** `size_bytes`, `free_bytes`, `free_ratio/free_pct` per logical volume;
- **physical health:** disk identity, `HealthStatus`, `OperationalStatus`, optional detailed reliability.

The 03/09 evidence for C: (~0.67% free) remains a capacity risk input, not an invented severity threshold.

## 4. G2 — projection contract ARCHITECTURE READY

Canonical contract: `BKL-030-EAGLE-Health-Projection-Contract.md`.

Target:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json
```

Each signal carries evidence state, freshness quality, timestamps, source provenance, cadence class, optional reason and raw data. Governed cadence classes are `FAST`, `MEDIUM`, `SLOW_ON_CHANGE`; no numeric interval is accepted yet.

Freshness semantics:

```text
valid sample before fresh_until_utc -> CURRENT
valid sample after fresh_until_utc  -> STALE
no valid/readable sample            -> UNKNOWN
```

Summary severity remains `UNKNOWN/POLICY_NOT_ACTIVATED` until a separate threshold/severity policy is governed. Raw CURRENT telemetry does not require an overall HEALTHY classification.

## 5. D3 workload consequence

D3-A full discovery: 3/3 success, average elapsed 9502.1 ms, max 11308.9 ms, available CPU average 5.859 s, max working set 232718336 B.

D3-B during N.I.N.A./PHD2: 3/3 success, average elapsed 16769.9 ms, max 23204.4 ms, available CPU average 7.086 s, max working set 206995456 B.

Therefore G3 must not run monolithic discovery at fast cadence. It must isolate probes by cadence/cost, prevent overlap and preserve imaging workload priority.

## 6. D4 implementation obligations for G3

G3 must implement:

- per-probe exception/failure isolation;
- bounded probe execution/timeout handling;
- non-overlapping cycles (skip/coalesce rather than pile up);
- per-signal provenance/freshness/reason semantics;
- atomic temp/validate/replace publication of `eagle-health.json`;
- preservation of last valid projection on serialization/write failure;
- no automatic privilege elevation or remediation;
- no process priority increase over N.I.N.A./PHD2.

## 7. Acceptance plan

- **G1 Source inventory: COMPLETE.** Governed source precedence and gaps recorded.
- **G2 Contract: ARCHITECTURE READY.** Projection/provenance/cadence/failure contract consolidated.
- **G3 Collector: NEXT.** Implement lightweight collector against G1/G2/D4.
- **G4 CI: PENDING.** Must test malformed source, access denied, timeout, partial success, serialization/write failure and schema behavior.
- **G5 Runtime OAT: PENDING.** Must validate on EAGLE30154, including normal imaging non-interference.
- **G6 History: PENDING.**
- **G7 Portal: PENDING.**
- **G8 Safety review: PENDING.** Boundary defined but final independent acceptance not yet executed.

## 8. Open policy questions (do not block G3 raw collector skeleton)

1. Storage capacity severity/trend thresholds.
2. Event Log provider/event allowlist and severity mapping.
3. Scheduled Task result-code mapping per governed task.
4. Deterministic pending reboot policy.
5. Configuration-drift baseline manifest.
6. Numeric cadence/freshness intervals, to be tuned and validated by implementation/OAT evidence.
7. CPU/hardware temperature source, if any non-invasive verified source becomes available.

These gaps require fields to remain raw/null/UNKNOWN as specified; they must not be filled by assumptions.

## 9. Safety and security

BKL-030 cannot kill/restart N.I.N.A./PHD2/ASCOM, reset USB/COM, reboot Windows, install updates, modify tasks/registry/config, alter power/network, or claim physical safe state. Local physical interlocks and approved Safety Authority remain independent even if EAGLE telemetry is stale, absent or wrong.

## 10. Next package

**G3 — lightweight collector implementation** is the next dependency-ordered package. Initial implementation should produce the governed projection with raw evidence and `summary.state=UNKNOWN` until severity policy is activated, followed by G4 CI and G5 EAGLE OAT before operational acceptance.

**Disposition: BKL-030 remains `In Progress`; G1 COMPLETE; G2 ARCHITECTURE READY; G3 NEXT.**
