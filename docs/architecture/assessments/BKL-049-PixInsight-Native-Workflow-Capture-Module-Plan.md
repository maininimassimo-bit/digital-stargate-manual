# BKL-049 — PixInsight Workflow Archive and Gallery Linkage Plan

| Field | Value |
|---|---|
| Identifier | DSG-BKL-049-PLAN-001 |
| Status | CLOSED / ACCEPTED — bounded revised scope; real gallery OAT verified; limitations retained |
| Version / date | 1.7 / 2026-10-02 |
| Predecessor | BKL-045 — CLOSED / ACCEPTED |
| Related decision | ADR-008, Owner scope revision recorded in Decision Log |
| Action authority | NONE |

## Current acceptance — 2026-10-02

The [closure record](../../project/BKL-049-CLOSURE-2026-10-02.md) supersedes the historical open-gate observations retained below. F0–F7 are accepted for the Owner-revised bounded archive and exact gallery-linkage scope after the real publication and browser OAT. Metadata and scientific quality are not promoted. The Owner subsequently removed automatic gallery expiry; publication now lasts until explicit withdrawal. Local recovery remains same-volume and native capture remains excluded.

## 1. Current objective and supersession

The Owner explicitly changed the earlier decision on 2026-09-30: archive the PixInsight history/evidence that is available, **including partial workflows**, and **link the workflow to the corresponding image and version in the Scientific Image Gallery**. Automatic integral capture is no longer an acceptance requirement. This supersedes the earlier native-module/integral-capture plan and reconfirmation recorded in Git history and the F0 research dossier. The filename and BKL identifier are retained for link continuity.

The image-to-workflow link is mandatory. Accepted gaps concern workflow detail, unsupported operations, historical parameters/models and upstream relationships; they do not authorize guessing which gallery image the workflow belongs to. Unresolved image identity remains visibly unlinked until governed reconciliation succeeds. Missing history is UNAVAILABLE, never proof of no processing. Partial history remains PARTIAL and the portal must expose its limitations.

## 2. Scope

- Accept explicitly selected supported history exports and bounded saved-history evidence, preserving original sources separately from derived representations.
- Retain available process order, parameters, source locators, available input/output/mask references and explicit unknowns.
- Preserve distinctions among OBSERVED, DECLARED and SUGGESTED; human-supplied/exported configuration is not automatically observed execution.
- Bind retained evidence to the governed scientific asset and exact image version; preserve any original-to-gallery-derivative relationship.
- Deliver through existing PXP/AP14-W06 validation and exact reconciliation, with AP-013/AP-014 retaining authority.
- Show the linked workflow, evidence sources and gaps from the gallery image; retain read-only behavior and public-data sanitization.

No native PCL module, universal observer, installation, automatic scientific processing or complete historical reconstruction is required by this revised scope. Native SDK research is retained as historical evidence and a future option only. No vendor contact is authorized. No production contract, catalog authority or Safety Authority is changed by this plan.

## 3. Evidence already available

The [F0 dossier](BKL-049-F0-SDK-Licensing-Feasibility-Dossier.md) and [real-evidence report](BKL-049-F0-Real-Identity-Evidence-Index.md) retain official sources, compatibility findings, isolated contract probes and private-source comparisons. SYN-01 demonstrates retained configurations for three synthetic PixelMath steps; SYN-02 demonstrates missing history reported as UNAVAILABLE. These are bounded results, not released import capability. RC Astro representation gaps and unknown historical models remain accepted visible limitations, not silently repaired data.

The published gallery currently uses bounded fixture data. No real image/workflow association has yet been accepted. Partial workflows are acceptable; a disconnected evidence archive alone does not fulfill BKL-049.

## 4. Revised increments and gates

| Increment | Outcome | Exit evidence |
|---|---|---|
| F0 — Feasibility and scope | Supported artifact candidates, source/privacy constraints, contract gaps and Owner scope decision | Revised feasibility review; distinguish completed probes from remaining ingestion/binding questions |
| F1 — Architecture | Source retention, bounded importer boundary, evidence semantics, privacy, exact identity and gallery route | Reviewed ADR-008 alignment and any explicitly versioned contract changes |
| F2 — Artifact import | Nonexecuting supported-subset ingestion; unsupported/corrupt/ambiguous inputs fail closed | Positive/negative fixtures, bounded resources, no expression execution |
| F3 — Workflow evidence | Available steps and relationships with source provenance and explicit omissions | Parameter/order/source preservation; no guessed migration or completeness promotion |
| F4 — Governed binding and delivery | Exact image/version binding, PXP/AP14-W06 handoff and idempotent retained evidence | Accepted source/asset association; mismatch/duplicate/unresolved cases |
| F5 — Gallery workflow access | Image opens its linked available workflow with limitations and citations | Real authorized end-to-end association; privacy and desktop/mobile/accessibility checks |
| F6 — Compatibility and OAT | Supported artifact/version matrix and partial/unavailable cases | Real authorized read-only import evidence and negative cases |
| F7 — Release and closure | Runbook, upgrade/rollback and governed delivery | Required reviews, exact-head CI, merge and post-merge verification |

F0 is ACCEPTED for this revised scope; see the [phase decision and exact delivery evidence](../../project/BKL-049-F0-ACCEPTANCE-2026-09-30.md). F1 architecture is accepted via PR #449; F2 bounded importer is accepted via PR #450; F3 private evidence adapter is accepted via PR #451; the F4 guard increment is accepted via PR #452, with operational retention and real association still open. Native SDK licensing/ABI/signing gates are not applicable to an implementation that neither uses nor redistributes the SDK; they are not declared resolved or waived for any future native work. F1 and production work are not automatically promoted by the scope decision. BKL-043 remains the current open package.

## 5. Acceptance criteria

1. An accepted gallery image/version is explicitly associated with its retained workflow evidence through governed identifiers and integrity checks, not filename similarity.
2. The gallery exposes the linked workflow, available steps/parameters, source citations and completeness/limitations; PARTIAL is an acceptable disclosed result.
3. Original evidence is retained separately from normalized/export-time representations, including RC schema differences; no original is silently overwritten.
4. Unsupported/missing history, model versions and lineage remain explicit, with no inferred executed steps.
5. Invalid, ambiguous, duplicate or mismatched binding fails closed; unlinked evidence is not shown as a verified image association.
6. PXP/AP14-W06 and catalog authority are preserved; any necessary contract delta receives separate review.
7. Public views exclude private paths, host/user identity, secrets and raw scientific content; expressions are never executed by ingestion.
8. Import and publication do not alter scientific images or execute processing; no EAGLE or device authority is introduced.
9. Meaningful compatibility, privacy, integrity and end-to-end tests plus required release reviews pass before closure.

## 6. Retention, risk and rollback

Scientific images/projects stay in external scientific storage. Governed evidence retention preserves sources, versioned references and fingerprints; public projections contain only sanitized permitted data. Source license/permission checks remain necessary for what is actually stored or redistributed, even without SDK dependency. Unsupported project internals are not converted into a production importer by the earlier structural inspections.

Risks include lossy exports, missing history, changed module schemas, unknown historical models, ambiguous masks/branches and incorrect derivative association. Treat these with separate source retention, explicit gaps and exact governed binding. Accepting partial evidence does not permit an incorrect link. Rollback must preserve accepted source evidence while disabling the new import/projection path, retaining BKL-045 behavior.

## 7. Current review boundary

F0 is accepted. The [F1 detailed architecture](BKL-049-F1-Workflow-Archive-Architecture.md) is accepted. The [F2 bounded importer](BKL-049-F2-Bounded-Importer-Implementation.md) is accepted. Review the [F3 declared-evidence adapter](BKL-049-F3-Declared-Evidence-Adapter.md) before promotion. The design preserves the partial archive scope and mandatory exact image/version association; production import and real gallery acceptance remain later gates. No new scientific processing is needed for design.
