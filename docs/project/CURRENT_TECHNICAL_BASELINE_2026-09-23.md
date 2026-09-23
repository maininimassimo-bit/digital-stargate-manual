# Digital StarGate — Current Technical Baseline 23/09/2026

| Field | Value |
|---|---|
| Identifier | `DSG-BASELINE-2026-09-23` |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Current package | BKL-042 AI Observatory Assistant |
| Closed predecessor | BKL-034-F2 Governed Image Ingestion and Metadata Archive |
| Owner | Massimo Mainini |
| Current repository head | `7be9fd0bfbef9fb5f95a62f2250394d1ac73f1d3` |
| Latest portal publication | Pages workflow `35925512667` — `SUCCESS` |
| BKL-042 relay | `dsg-bkl042-ai-relay-00007-wrm` — 100% traffic; rollback `00006-ktv` |

RC2, AP-015 and BKL-033 are frozen and accepted. BKL-033 delivered the bounded descriptive/read-only asset and dependency projection with explicit current/stale/unknown/unavailable states. AP-008 and BKL-036-F5 remain closed bounded read-only capabilities; EAGLE Health remains live `HEALTHY/100` under fail-closed policy.

The current package is BKL-042. Its bounded F6 portal-ingress gate has passed owner-witnessed authenticated OAT and formal bounded acceptance. The first server-side retrieval/provenance increment, limited to public target identity and historical-session projections, is merged in PR #355 (`b4d45c12`). Owner OAT returned `INSUFFICIENT_EVIDENCE` for compact target spelling `m27` while all three source digests matched the published projections; local replay over those projections found five M 27 sessions. PR #357 (`7be9fd0b`) adds compact/spaced astronomical designation normalization as method v2 and is deployed to the existing relay as `dsg-bkl042-ai-relay-00007-wrm`, with `00006-ktv` rollback. New authenticated owner-witnessed post-deployment OAT and formal acceptance remain pending; full F1 source coverage is not claimed. BKL-034 is closed after delivery of the bounded read-only portal consumer for images, sessions, targets and processing provenance. BKL-034-F2 is closed / accepted / post-merge verified for governed image-ingestion contract and storage-boundary dry-run preflight, including checksum, quarantine, metadata completeness and PixInsight workflow relations; runtime storage and upload write authority remain separately gated. AP-015 and BKL-033 remain closed within their explicitly design/contract-only scopes. The portal theme compatibility remediation is complete and published on the governed head `ad74a35d`: the light scheme has been normalized across shared and legacy surfaces while the dark scheme and semantic status colors remain preserved. No image mutation, processing execution, operational control, readiness, provider action, automatic apply, command path, broker, remediation or Safety Authority is authorized by this baseline.
