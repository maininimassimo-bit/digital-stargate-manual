# ARB — BKL-049 PixInsight Native Workflow Capture Module Planning

| Field | Value |
|---|---|
| Review ID | ARB-PR187-BKL049-PLAN-AI-001 |
| Review mode | AI-assisted, owner-authorized, role-separated; not an independent human approval |
| Date | 2026-09-14 |
| Pull request | [#187](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/187) |
| Technical head reviewed | `f549297d2692eb8f5549b1728ab2d380dd93b793` |
| Base | `95b148c6bb26633417dc95c797ec5dca7624d554` |
| Decision | **APPROVED WITH CONDITIONS** |
| Score | **98 / 100** |

## 1. Independence and authorization disclosure

This review was produced by an AI acting in the Architecture Review Board role after explicit repository-owner authorization limited to PR #187 at technical head `f549297d2692eb8f5549b1728ab2d380dd93b793`.

The review is role-separated from proposal authoring and did not silently modify the reviewed package. It is **not equivalent to an independent human approval**. It does not authorize merge, branch-protection waiver, BKL-049 promotion, implementation, native code, installation or runtime activity.

## 2. Reviewed scope

The review covers:

- the BKL-049 planning document and its F0–F7 delivery sequence;
- the ADR-008 native-successor planning amendment;
- backlog and canonical-roadmap registration as `Planned`;
- generated roadmap synchronization;
- MkDocs discoverability;
- preservation of BKL-045, BKL-044, AP-013, AP-014/AP14-W06 and BKL-046 boundaries;
- exact-head documentation and regression evidence.

The technical head changes six documentation, navigation and governed source/projection files (+283/-7) across two commits. It introduces no native source code, schema change, installer, executable workflow, runtime component, PC Principale/EAGLE change or portal deployment.

## 3. Architecture assessment

The package correctly converts the retained BKL-045 limitation into a planned successor without misrepresenting the current hybrid exporter as complete. The F3-B runtime result remains truthful: `completeness=UNAVAILABLE`, zero automatically observed steps.

The phrase “complete workflow” is bounded correctly to 100% of an accepted, evidence-backed support matrix. Opaque or unsupported behavior remains `PARTIAL` or `UNAVAILABLE`; it cannot be inferred as `OBSERVED`.

The proposed topology maintains appropriate responsibility boundaries:

- the native PCL module observes and journals processing evidence locally;
- the local outbox provides atomic, retryable delivery;
- AP14-W06 remains the only synchronization and exact-reconciliation boundary;
- AP-013 and AP-014 remain authoritative for scientific asset and session identity;
- the portal remains a sanitized, derived, read-only projection;
- `actionAuthority=NONE` prevents capture from becoming execution or acceptance authority.

The plan uses incremental gates appropriately. F0 proves SDK, licensing, hooks and compatibility before F1 settles the detailed architecture, and before F2 introduces a module skeleton. This prevents an unverified native dependency from becoming an accepted implementation assumption.

Operational failure semantics are coherent: capture failure must not block or mutate PixInsight processing, while evidence publication fails closed and cannot claim completeness after journal gaps, unsupported activity or reconciliation failure.

BKL-049 remains `Planned`; BKL-031 remains the current governed package. The reserved BKL-048 identifier in PR #186 is documented and no identifier collision exists.

## 4. Scoring matrix

| Dimension | Score | Evidence-based assessment |
|---|---:|---|
| Program and enterprise alignment | 98 | new capability is planned without displacing BKL-031 or changing the governed sequence |
| Authority and source-of-truth integrity | 100 | AP-013/AP-014 authority and AP14-W06 ingestion remain explicit |
| Domain and semantic integrity | 100 | OBSERVED/DECLARED/SUGGESTED and completeness semantics are preserved |
| Scope control | 100 | planning only; implementation, runtime and execution authority are excluded |
| Dependency and layer integrity | 98 | clear native/local/repository/portal boundaries; SDK/API feasibility remains open by design |
| Safety | 100 | no device command, go/no-go, remediation or Safety Authority |
| Security and privacy | 97 | redaction and credential constraints are defined; delivery mechanism awaits F0/F1 proof |
| Operability and observability | 97 | journal, diagnostics, recovery and rollback are planned; quantitative budgets remain open |
| Persistence and messaging | 99 | append-only journal and local outbox are justified; AP14-W06 stays authoritative |
| Migration and rollback | 99 | disable/uninstall fallback to BKL-045 hybrid path is explicit |
| Traceability and documentation | 99 | ADR, backlog, roadmap, projection, plan and navigation are aligned |
| Validation evidence | 96 | all planning-package checks passed; native/runtime evidence is correctly not claimed |

Rounded ARB score: **98 / 100**.

## 5. Findings

| Severity | ID | Finding | Disposition |
|---|---|---|---|
| Blocker | — | None | — |
| Major | — | None | — |
| Minor | — | None | — |
| Observation | ARB-187-O01 | PCL process-event, project-history and workspace API coverage is not yet proven. | Treat F0 evidence as a mandatory entry gate before detailed native design or code. |
| Observation | ARB-187-O02 | SDK access, redistribution terms, ABI/version support and signing are open. | Resolve and record each item in F0; do not infer distributability. |
| Observation | ARB-187-O03 | “Complete” is support-matrix completeness, not universal observation of opaque processes. | Preserve this qualification in contracts, UI and release claims. |
| Observation | ARB-187-O04 | BKL-048 exists only on the still-open PR #186 while BKL-049 is proposed independently. | Preserve the reservation and reconcile ordering after both PRs reach main; no collision exists. |
| Observation | ARB-187-O05 | `main` is currently unprotected. | Require separate exact-head merge authorization; no implicit waiver is granted. |
| Observation | ARB-187-O06 | This review is AI-assisted and lacks independent human assurance. | Retain the disclosure in every downstream acceptance claim. |

## 6. Conditions

1. BKL-049 must remain `Planned` after this PR; implementation requires separate promotion and owner authorization.
2. F0 must verify PCL SDK access, licensing/redistribution, signing, supported hooks, ABI/version compatibility and technical observation limits before production code.
3. F1 must publish the detailed architecture, support matrix, threat model, data-contract delta, resource budget, migration and rollback decision before F2.
4. Completeness may be claimed only against a versioned, evidence-backed support matrix; unsupported or opaque actions remain explicit.
5. PixInsight processing remains fail-operational: capture failure cannot block or mutate processing. Provenance remains fail-closed: incomplete evidence cannot claim `COMPLETE`.
6. The native module may not write directly to AP-013/AP-014 or the portal. AP14-W06 remains the only governed ingestion/reconciliation path.
7. No credential may be embedded in the module; sensitive host, user and path data must be redacted before public projection.
8. Review-publication changes must pass all applicable workflows on their resulting exact head.
9. Merge requires separate repository-owner authorization on the final exact head. This review grants no branch-protection waiver.
10. No PC Principale, EAGLE or PixInsight installation/runtime action is authorized by this review.

## 7. Validation evidence

Verified on technical head `f549297d2692eb8f5549b1728ab2d380dd93b793`:

| Workflow | Run | Result |
|---|---:|---|
| Scientific Platform Governance | 34857935836 | SUCCESS |
| Developer Foundation | 34857935847 | SUCCESS |
| BKL-041 F4 Governance | 34857935956 | SUCCESS |
| BKL-046 F4 governance | 34857935880 | SUCCESS |
| Genera manuale Word | 34857935791 | SUCCESS |
| BKL-046 F5 governance | 34857935903 | SUCCESS |
| Validate documentation (no deploy) | 34857936197 | SUCCESS |

Additional verified facts:

- PR open, draft and mergeable;
- branch relation: two commits ahead and zero behind `main`;
- changed-file scope: six documentation/navigation/governed JSON files;
- generated roadmap source/projection are synchronized;
- no prior PR comments, review threads or reviews were present;
- `main` reports `protected=false`.

Not executed or claimed:

- PCL SDK/API/licensing feasibility;
- native module compilation, packaging, signing or installation;
- PixInsight automatic process-history capture;
- journal/outbox failure injection;
- AP14-W06 end-to-end ingestion using native evidence;
- portal workflow archive implementation or deployment;
- PC Principale/EAGLE/PixInsight runtime OAT;
- independent human approval;
- merge or post-merge verification.

## 8. ARB decision

**APPROVED WITH CONDITIONS** for integrating the BKL-049 planning package. The proposal is architecturally coherent, incrementally gated, evidence-safe and compatible with the accepted Digital StarGate authority model.

This decision approves planning documentation only. It does not authorize implementation, merge, waiver, installation or runtime activity.
