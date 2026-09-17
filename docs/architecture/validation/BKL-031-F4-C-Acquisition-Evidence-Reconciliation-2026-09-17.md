# BKL-031 F4-C — Acquisition Evidence Reconciliation

| Field | Value |
|---|---|
| Evidence ID | `BKL-031-F4-C-EVIDENCE-RECONCILIATION-001` |
| Status | **RECONCILED EVIDENCE CANDIDATE / NO FURTHER REQUEST** |
| Workflow run | [35214129960](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/35214129960) |
| Authorized main | `053fc766bfc7908a984828cc335eef07a558909c` |
| Artifact | `10494298154` / `bkl-031-f4c-evidence-35214129960` |
| Provider result | HTTP 200; 4,723 bytes |
| Raw SHA-256 | `e51c6935f8e04bcce38983bc03147f4f897a833f90feb6271b2f510ee6eec102` |
| Normalized evidence digest | `350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5` |
| Request accounting | 2 cumulative; budget exhausted |

The replacement request returned one explicit ItaliaMeteo/ARPAE ICON-2I run through Open-Meteo Single Runs for the fixed generalized point. The response contained 72 hourly positions, correct GMT/zero-offset metadata and the ten governed variables. The initial position had `precipitation=null`; every other required value was finite.

The online gate rejected the response rather than imputing or silently accepting missing data. The uploaded artifact retained the request plan, raw bytes and structured failure summary. Offline reconciliation then applied `DROP_INCOMPLETE_INSTANT_NO_IMPUTATION`:

- excluded exactly source index 0 at `2026-09-17T00:00:00Z` for `INCOMPLETE_REQUIRED_VARIABLE` / `precipitation`;
- accepted exactly indices 1–71, a contiguous 71-hour suffix;
- preserved the exact raw digest and all returned values;
- imputed zero values;
- retained `visibility` as unavailable;
- kept authority `NONE`, public projection false and protected-site use false.

The private repository evidence package is:

- `governance/forecast-evidence/BKL031-F4C-RUN-35214129960/raw-response.json`;
- `governance/forecast-evidence/BKL031-F4C-RUN-35214129960/request-plan.json`;
- `governance/forecast-evidence/BKL031-F4C-RUN-35214129960/failure-summary.json`;
- `governance/forecast-evidence/BKL031-F4C-RUN-35214129960/normalized-evidence.json`.

The deterministic reconciliation verifier recomputes the raw SHA-256, checks request accounting, proves the single exclusion and zero imputation, validates time ordering, lengths, finite values and physical bounds, rebuilds the normalized evidence and verifies its canonical digest.

The two-request ceiling is exhausted. No further provider request is authorized. F4-D public projection, F5 ranking/consumer, BKL-032 readiness and Safety remain separate gates.
