# BKL-049 F0 — Feasibility acceptance

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-F0-ACCEPTANCE-001 |
| Version / date | 1.0 / 2026-09-30 |
| Status | F0 ACCEPTED / POST-MERGE VERIFIED for revised scope |
| Milestone | BKL-049 remains In Progress; F1 detailed design is next |
| Authority | Documentation and processing evidence only; action authority NONE |

## Decision and scope

F0 is accepted for the Owner-approved archive of available PixInsight workflow evidence, including explicit PARTIAL/UNAVAILABLE gaps, with **mandatory linkage to the correct gallery image and version**. This reconciles the pre-review OPEN labels in the PR #445 snapshot; it does not close BKL-049 or claim the image/workflow feature exists. BKL-043 remains the current open programme package.

The former universal native recorder requirement was explicitly superseded by the Owner. Native SDK licensing, ABI, toolchain and signing questions remain retained research for a future native route; they are not declared resolved. No SDK is used or redistributed by the selected artifact feasibility route. No vendor contact, installation, scientific processing, EAGLE operation or new public scientific payload is authorized here.

## Immutable evidence

| Gate | Verified result |
|---|---|
| Publication/review head | `dc3ab31a92d7d69c58fdb6b90510a709e6c578a9` |
| Baseline before merge | `a0d1ab8102ab19505536d301b7444edfa42ee4bd`; zero behind verified before merge |
| ARB | [APPROVED](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/445#issuecomment-5916551935); 0 Blocker, 0 Major, M01 editorial |
| Release Quality | [Conditional readiness](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/445#issuecomment-5916568089); sole remaining CI condition subsequently satisfied |
| Exact-head CI | 17/17 SUCCESS; [merge gate](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/445#issuecomment-5916665074) |
| Delivery | [PR #445](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/445), merge `fc281eb80342c746303c58c2d2a8f61d134a5f5b` |
| Post-merge | 17/17 workflows SUCCESS on that merge SHA; [record](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/445#issuecomment-5916764574) |
| Pages | [Authoritative deployment SUCCESS](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/36754290648); plan, dossier and gallery HTTP 200 with expected content |
| Merge authority | `W-DSG-AEM-RULESET-001`; rollback and public-data classification recorded in PR |

Reviews were separate AI-assisted ARB and RQ exercises, not independent human approvals. M01 concerned the obsolete native-successor status label in ADR-008; this reconciliation corrects it without changing the ADR authority boundary. This document reports the accepted PR #445 evidence; its own publication requires its own exact-head and post-merge checks.

## Feasibility result and limits

The [dossier](../architecture/assessments/BKL-049-F0-SDK-Licensing-Feasibility-Dossier.md) records official source references, source/license boundaries, supported artifact candidates, preliminary support matrix, alternatives and risks. Owner-supplied exports and isolated nonexecuting readers establish a bounded artifact route. SYN-01 retained three ordered synthetic configurations; SYN-02 correctly exposed missing history as UNAVAILABLE. Historical RC representations and model identities remain incomplete. No production importer or universal observation capability is claimed.

Validation retained with PR #445 includes 27 export-reader tests, 4 XISF-reader tests, 37 existing contract tests, 12 contract probes, 6 binding probes, 9 synthetic pipeline cases and 10 identity cases. Probes expose existing contract/identity limitations; they are not proof those limitations are repaired. Documentation, roadmap consistency and projection checks passed. No scientific pixels were decoded or modified by these verification tools.

## Obligations transferred to F1 and later gates

| Gate | Mandatory outcome |
|---|---|
| F1 architecture | Retention/access rules, supported source boundary, truthful PXP mapping, public sanitization, resource limits and explicit compatibility design |
| F2 import | Nonexecuting bounded parsing; reject or quarantine unsupported, corrupt and ambiguous inputs; no embedded path traversal |
| F3 evidence | Preserve originals separately from normalized values and lossy manifest projection; retain unsupported parameters and unknown lineage explicitly |
| F4 binding | Authoritative unique asset/version identity and integrity; verify original-to-preview relation; reject mismatches, duplicate identities and unresolved associations |
| F5 gallery | Real authorized image/version opens its own available workflow, sources and gaps; no inferred association or placeholder represented as real acceptance |
| F6/F7 acceptance | Compatibility/OAT evidence, privacy and meaningful negative tests, required reviews, exact-head delivery and post-merge verification |

Detailed design may now proceed under the existing mandate and revised plan. F1 is dependency-ready, not completed or architecturally accepted. No contract delta or structural dependency is pre-approved. If context required by PXP is absent, retain unresolved evidence rather than invent session, target, host or historical version facts. SUGGESTED activity is not executed provenance; supplied configuration is not automatically OBSERVED execution.

No further Owner input is required for this F0 acceptance. Later real-image publication, authoritative asset/version registration or unavailable context may require a specific decision after the architecture identifies exactly what is missing. Existing scientific material remains private; general permission to publish sanitized findings does not classify raw scientific payloads as public.

## Rollback and continuity

This reconciliation changes documentation and generated planning projections only. Revert its eventual merge through a reviewed PR if necessary, regenerate projections, validate documentation and verify Pages; retain the PR #445 evidence and Owner scope decision. No runtime migration or image rollback is involved.

Next: F1 detailed architecture under ADR-008 and the [revised plan](../architecture/assessments/BKL-049-PixInsight-Native-Workflow-Capture-Module-Plan.md). BKL-043 continuity documents remain authoritative for BKL-043; this phase acceptance does not replace them.

## Revision history

- 1.0 — Reconcile completed F0 reviews and post-merge evidence; retain all later implementation obligations.
