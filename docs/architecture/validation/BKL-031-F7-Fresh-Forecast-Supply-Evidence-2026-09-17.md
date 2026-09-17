# BKL-031 F7 — Fresh Forecast Supply Validation Evidence

| Field | Value |
|---|---|
| Status | **EVIDENCE ACQUIRED — REVIEW CANDIDATE** |
| Date | 2026-09-17 |
| Workflow run | `35243920092` |
| Workflow head | `7b4559111e5a84a00ecbd13611e1ead25276b8b9` |
| Run attempt | `1` |
| Artifact | `10506402579` / `bkl-031-f7-evidence-35243920092` |
| Artifact digest | `sha256:02cae087b85f6427a66891c85f8e823b200afb1e0590bf0f88be4d05eb909370` |
| F7 request budget | **`1/1_EXHAUSTED`** |

## Result

The single owner-authorized F7 request completed successfully against Open-Meteo Single Runs for upstream ItaliaMeteo/ARPAE ICON-2I run `2026-09-17T12:00Z` at the synthetic/generalized point `42.0,12.0`. Retrieval completed at `2026-09-17T16:01:16.208Z`; observed run age was `4.021169` hours, within the ADR-011 18-hour ceiling, so freshness is `FRESH`.

The raw response contains 72 hourly positions. Normalization accepts 71 complete positions, excludes the initialization instant `2026-09-17T12:00Z` because `precipitation` is null/non-finite, leaves 67 accepted instants in the future at retrieval time, and performs zero imputations. Availability is therefore `DEGRADED`, not silently upgraded to `AVAILABLE`.

Raw response SHA-256: `7c6805d77c66389aa3e280784f0219912d40089b3a55c5a8bc651ae073f86dbc`.

Normalized supply SHA-256: `7d8205a4d1379927e8648534a3463b19a1a0c99cab48bae01b612348f7d35680`.

The repository stores gzip/base64 copies of both exact evidence payloads. The F7 verifier decodes and hashes them offline. No provider request is performed during verification.

## Boundary verification

- protected-site use: `false`;
- recurring traffic: `false`;
- production runtime activated: `false`;
- readiness authority: `false`;
- scheduling authority: `false`;
- automatic target selection: `false`;
- command authority: `NONE`;
- Safety Authority: `LOCAL_PHYSICAL_INTERLOCKS`.

The one-shot acquisition script/workflow is removed after evidence capture. Any additional provider request now requires a new explicit owner authorization and a separately governed package.
