# BKL-036-F4 — Governed Telemetry Acquisition and Archival Validation Plan

| Campo | Valore |
|---|---|
| ID | BKL-036-F4-VAL-001 |
| Stato | Accepted / Post-Merge Verified |
| Scope | Contract, validator, archive projection and boundary enforcement |

## Matrix

| Check | Expected |
|---|---|
| Valid offline snapshot | PASS |
| Exactly seven mandatory domains | PASS |
| Duplicate or missing domain | FAIL |
| Incomplete evidence marked comparable | FAIL |
| Present evidence without timestamps | FAIL |
| Live transport flag | FAIL |
| Commands, scheduling or remediation flag | FAIL |
| Local physical interlocks preserved | PASS |
| F3 score promotion | Not applicable / prohibited |
| Live source access | Not executed / out of scope |

## Evidence

The bounded fixture is `docs/data/bkl-036-f4-telemetry-ingest-fixture.json`; the deterministic archive is `docs/data/bkl-036-f4-telemetry-archive.json`. Exact-head CI and post-merge verification passed on PR #320 / merge `c58f0cb241e1b8432ec81c17d9d6b967d023e102`. The current fixture intentionally contains unavailable domains and therefore cannot produce an F3 numeric score. The current fixture intentionally contains unavailable domains and therefore cannot produce an F3 numeric score.
