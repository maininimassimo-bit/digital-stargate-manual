# Digital StarGate — Current Technical Baseline 23/09/2026

| Field | Value |
|---|---|
| Identifier | `DSG-BASELINE-2026-09-23` |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Current package | BKL-042 AI Observatory Assistant |
| Closed predecessor | BKL-034-F2 Governed Image Ingestion and Metadata Archive |
| Owner | Massimo Mainini |
| Current repository head | `b4d45c12c99e653e8563ca137e4d9022fd94e58b` |
| Latest portal publication | Pages workflow `35920330566` — `SUCCESS` |
| BKL-042 relay | `dsg-bkl042-ai-relay-00006-ktv` — 100% traffic; rollback `00005-d97` |

RC2, AP-015 and BKL-033 are frozen and accepted. BKL-033 delivered the bounded descriptive/read-only asset and dependency projection with explicit current/stale/unknown/unavailable states. AP-008 and BKL-036-F5 remain closed bounded read-only capabilities; EAGLE Health remains live `HEALTHY/100` under fail-closed policy.

The current package is BKL-042. Its bounded F6 portal-ingress gate has passed owner-witnessed authenticated OAT and formal bounded acceptance. The first server-side retrieval/provenance increment, limited to public target identity and historical-session projections, is merged in PR #355 (`b4d45c12`) and deployed to the existing relay as `dsg-bkl042-ai-relay-00006-ktv`; its authenticated post-deployment OAT and formal acceptance remain pending owner witness. This increment does not establish full F1 source coverage. BKL-034 is closed after delivery of the bounded read-only portal consumer for images, sessions, targets and processing provenance. BKL-034-F2 is closed / accepted / post-merge verified for governed image-ingestion contract and storage-boundary dry-run preflight, including checksum, quarantine, metadata completeness and PixInsight workflow relations; runtime storage and upload write authority remain separately gated. AP-015 and BKL-033 remain closed within their explicitly design/contract-only scopes. The portal theme compatibility remediation is complete and published on the governed head `ad74a35d`: the light scheme has been normalized across shared and legacy surfaces while the dark scheme and semantic status colors remain preserved. No image mutation, processing execution, operational control, readiness, provider action, automatic apply, command path, broker, remediation or Safety Authority is authorized by this baseline.
