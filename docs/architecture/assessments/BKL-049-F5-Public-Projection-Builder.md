# BKL-049 F5 — Explicit public-field projection builder

| Field | Value |
|---|---|
| Date | 2026-10-01 |
| Scope | Bounded producer API and additive schema; synthetic verification |
| Status | IMPLEMENTED / REVIEW PENDING; full F5 OPEN |
| Authority | Processing evidence only; action/catalog/publication authority NONE |

## Result and boundary

`tools/pixinsight/workflow_archive/public_projection.py` constructs a minimized workflow object from an independently anchored, reverified [private delivery bundle](BKL-049-F4-Exact-Binding-Guard.md) and a separately approved field selection. It never copies the private archive and then removes fields. Only explicitly selected process labels and parameter names/values enter the output. No real selection, public artifact, gallery change, upload or cloud access change is delivered by this increment.

This implements the producer portion of [F1 section 8](BKL-049-F1-Workflow-Archive-Architecture.md). The additive `schemas/bkl049-public-workflow.schema.json` is separate from closed PXP, manifest, AP-013/AP-014 and BKL-034 contracts. The existing bounded schema-profile checker validates every keyword used by the producer schema; it is not a general JSON Schema implementation or a browser validation boundary.

## Trusted input and approval

`build_public_projection` requires delivery bytes plus an independently retained digest, the authority's current snapshot digest, canonical selection bytes plus their independently retained digest, and the current approved-selection digest. The caller must obtain current anchors from governed sources. Computing a digest from an arbitrary candidate does not grant permission or acceptance. A stale authority snapshot, changed delivery or withdrawn/replaced selection rejects generation.

The private selection has a closed set of fields: kind `BKL049_PRIVATE_PUBLIC_SELECTION_V1`, scope `EXACT_WORKFLOW_FIELDS_ONLY`, delivery digest, accountable approver/time, three explicitly approved public aliases (`IMG-`, `VER-`, `WF-`) and selected steps. Every step identifies the source step and exact process label. Every selected parameter identifies its exact name and digest of the canonical tagged lexical value. The delivery digest also binds the original export, final/preview identities, declaration and source order. Approval predating delivery is rejected. No automatic approval generator is provided.

Public aliases are newly approved references, not private image IDs or digests. Their mapping remains in the private selection bound to the verified delivery. Alias assignment must be reviewed for privacy; syntactically safe text is not automatically public. This function handles one association. Cross-record alias uniqueness, immutable version registration and withdrawal in the published collection remain mandatory duties of the future publisher/consumer, not guarantees made by this API.

## Output semantics and limits

- Evidence stays DECLARED; execution stays NOT_ESTABLISHED. Source ordinal is exported configuration order, not observed chronology. Selection order cannot reorder source steps.
- Selected available steps produce PARTIAL; an empty selection produces UNAVAILABLE. Omitted step/parameter counts are explicit. Fixed gaps disclose incomplete history, unobserved execution, unresolved upstream relations, unavailable process versions and omitted private fields.
- Parameters retain canonical tagged lexical JSON as display text. No evaluation, coercion, replay or silently truncated value is permitted. An explicitly approved expression is inert data; the future UI must render it with text APIs, never HTML or executable interpolation.
- No private actor, account, path, receipt/source digest, mask/view reference, notes, source bytes or full archive is copied by default. A selected parameter can itself contain sensitive text: exact-value review is the privacy authority; this API is not a secret detector or a substitute for review.
- Public aliases reject URLs, slashes, query strings, fragments, encoded traversal and markup. The sole route is a fixed relative **method citation**, not a claim that public readers can access the private source evidence. Preview hosting URLs are not accepted here.
- Limits: 512 selected steps, 128 selected parameters per step, 4096 characters per lexical display value and 256 KiB total output. Private source limits remain unchanged. Oversized selections fail; a new explicit selection can omit such fields. Original private values remain intact.

Unknown fields, duplicate steps/parameters, mismatched process labels or values, unknown source references, missing anchors and invalid aliases reject atomically with fixed diagnostics. The API returns a detached object; it performs no file/network write and grants no publication permission.

## Verification and remaining gates

Synthetic tests cover allowlist leakage checks, exact lexical preservation, omission counts, empty selection, source order, independent/current anchors, changed delivery, parameter mismatch, unknown/duplicate fields, unsafe identifiers/routes, inert expressions, canonical input and resource limits. Existing archive, declaration, binding and delivery tests plus PXP/AP14-W06 bridges remain applicable. CI runs the new suite on Windows and Linux and triggers on the additive schema.

Before full F5 acceptance: implement Scientific Data Engine loading and gallery text rendering; reject duplicate/version-conflicting public records; verify collection freshness/withdrawal, safe routes and no fixture fallback; test browser/keyboard/mobile/refresh/Instant Navigation. A real accepted [external-origin registration](BKL-049-External-Origin-Registration-Plan.md), retained binding and exact approved field selection are still required. Synthetic fixtures cannot replace those decisions. Exact preview publication/access remains separately authorized.

Rollback removes the additive producer/schema through a reviewed revert. Existing private archives, gallery fixture behavior, scientific contracts, BKL-043 and Safety Authority remain unchanged. This increment does not close F4 real binding, F5 or BKL-049.
