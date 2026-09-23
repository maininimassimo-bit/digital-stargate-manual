# Digital StarGate — Current Technical Baseline 23/09/2026

| Field | Value |
|---|---|
| Identifier | `DSG-BASELINE-2026-09-23` |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Current package | BKL-034-F2 Governed Image Ingestion and Metadata Archive |
| Closed predecessor | BKL-034 Scientific Image Gallery evoluta |
| Owner | Massimo Mainini |

RC2, AP-015 and BKL-033 are frozen and accepted. BKL-033 delivered the bounded descriptive/read-only asset and dependency projection with explicit current/stale/unknown/unavailable states. AP-008 and BKL-036-F5 remain closed bounded read-only capabilities; EAGLE Health remains live `HEALTHY/100` under fail-closed policy.

The current package is BKL-034-F2. BKL-034 is closed after delivery of the bounded read-only portal consumer for images, sessions, targets and processing provenance. F2 defines governed image ingestion and metadata archive semantics, including checksum, quarantine, metadata completeness and PixInsight workflow relations; runtime storage and upload write authority remain separately gated. AP-015 and BKL-033 remain closed within their explicitly design/contract-only scopes. No image mutation, processing execution, operational control, readiness, provider action, automatic apply, command path, broker, remediation or Safety Authority is authorized by this baseline.
