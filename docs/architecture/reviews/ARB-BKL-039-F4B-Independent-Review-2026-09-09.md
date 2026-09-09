# ARB — BKL-039 F4-B Independent Architecture Review

| Field | Value |
|---|---|
| Scope | BKL-039 F4-B — Equipment Performance Portal Projection |
| Review date | 2026-09-09 |
| Reviewed exact head | `87b960bcceb6c8a5d70ded74f943036af6f3a3a5` |
| PR | #131 |
| Review ID | `5157531319` |
| Decision | **APPROVED** |
| Score | **97/100** |

## Executive decision

The independent Architecture Review Board approves BKL-039 F4-B at exact head `87b960bcceb6c8a5d70ded74f943036af6f3a3a5`.

F4-B is a bounded static/read-only browser projection over the accepted F4-A repository read model. It introduces no service, persistence layer, alternate measurement pipeline, writable API, command path or Safety Authority. The portal preserves `authority=projection`, `action_authority=NONE`, the source-native uncalibrated FWHM semantics and the unproven angular calibration state.

Local physical interlocks and the local Safety Authority remain independent and authoritative.

## Verified exact-head evidence

The following GitHub Actions runs completed successfully on the reviewed exact head:

- BKL-039 F4 Governance #10 — SUCCESS;
- Developer Foundation #1169 — SUCCESS;
- Validate documentation (no deploy) #788 — SUCCESS;
- Genera manuale Word #1213 — SUCCESS.

The dedicated F4 governance workflow retains the accepted F4-A generator verification, validator and negative regression suite and adds source-level checks for the F4-B browser authority, unit, population and limitation guards.

## Architecture assessment

| Area | Score | Assessment |
|---|---:|---|
| Scope and dependency direction | 100 | Static browser projection consumes the accepted F4-A read model directly. |
| Source/statistic fidelity | 100 | Accepted measurements and descriptive statistics are rendered without recalculation. |
| Unit/calibration boundary | 100 | Source-native unit, uncalibrated semantics and `NOT_PROVEN` angular calibration are guarded. |
| Authority/Safety boundary | 100 | Projection-only authority and no action authority; no current Safety inference. |
| Fail-closed browser behavior | 96 | Load, authority, unit, calibration, population and limitation drift close the view. |
| Output safety | 98 | Dynamic values are HTML-escaped before browser insertion. |
| Citation/Provenance | 96 | Citation, Provenance and source-record references remain visible. |
| CI integration | 98 | Dedicated F4 governance and repository documentation gates are green on the reviewed head. |
| Migration/rollback | 100 | Additive static portal change; rollback is repository revert. |

## Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observation O01 — Behavioral browser regression

When the portal test harness is next extended, execute the browser logic against nominal and mutated fixtures, including authority drift, missing limitations, population mismatch and fetch failure. Current governance verifies these browser guards structurally; this is acceptable for this bounded static/read-only increment because the upstream F4-A artifact remains independently generated and fail-closed validated.

### Observation O02 — Compatibility navigation aliases

The three historical MkDocs locators added during documentation remediation are non-authoritative aliases to existing canonical ARB documents. They must remain non-authoritative or be removed by a separate documentation-cleanup change if navigation is migrated directly to canonical locators.

## Validation not claimed

This review does not claim browser automation, live GitHub Pages execution, EAGLE/PC runtime validation, hardware validation, physical Safety validation or operational commissioning.

## Final decision

**APPROVED — 97/100.**

F4-B may proceed to Release Quality after repository integration of this review evidence and a new exact-head CI cycle. Any evidence commit changes the exact head and therefore requires fresh exact-head validation before Release Quality.