# BKL-036-F5 — Live Read-Only Score Handoff

| Field | Result |
|---|---|
| Identifier | `BKL-036-F5-HANDOFF-001` |
| Status | Owner-authorized / implementation candidate |
| Predecessor | BKL-036-F1/F2/F3/F4 accepted and post-merge verified |
| Runtime prerequisite | AP-008 bounded read-only integration accepted |
| Next decision | ARB and Release Quality review of live evidence compatibility |

AP-008 now supplies a continuous read-only transport for Observatory Status and EAGLE Health.
That evidence is sufficient to open F5, not to promote the existing archived-evidence score to
a live score. F5 must establish the seven-domain mapping, comparability rules, freshness policy,
machine-readable envelope and portal semantics before any live score is published.

The current public BKL-036 score remains `UNAVAILABLE` by design. No score, readiness state or
safety conclusion may be inferred from the AP-008 transport alone.

The F5 owner gate is explicitly separate from AP-008 closure. AP-008 is complete for its bounded
read-only integration scope; F5 is the successor package for live descriptive scoring.
