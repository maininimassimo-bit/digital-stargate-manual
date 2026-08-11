# ARB-013 — Scientific Image Repository Architecture Review

| Field | Value |
|---|---|
| Review ID | ARB-013 |
| Package | AP-013 — Scientific Image Repository Architecture |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Review date | 11/08/2026 |
| Review authority | Digital StarGate Architecture Review Board |
| Review basis | Repository `main` through AP-013B QG-20 closure baseline |
| Decision | Approved with conditions |
| Runtime decision | AP-013B OneDrive COPY_ONLY limited production approved; broader preservation/provenance runtime not certified |

## 1. Executive decision

The Architecture Review Board independently reviewed AP-013, its scientific asset model, contract and importer design, the repository evidence for the COPY_ONLY ingestion path, the AP-013B OneDrive operational acceptance campaign, security/ACL review, recovery tests, scheduler behavior and QG-20 promotion decision.

The package is **Approved with conditions** as the governing architecture for the Digital StarGate Scientific Image Repository. The architecture is coherent, preserves the separation between scientific binary storage, authoritative metadata/provenance and downstream catalog projections, and has operational evidence for the bounded COPY_ONLY ingestion path.

This decision does not claim that every future preservation, provenance, PixInsight, backup/restore, migration or capacity capability is implemented. Those concerns remain governed conditions and downstream evolution items.

## 2. Repository evidence reviewed

The Board verified the presence and consistency of:

- `docs/architecture/packages/AP-013-Scientific-Image-Repository-Architecture.md`;
- `docs/architecture/scientific-assets/AP13-W02-Current-State-Scientific-Asset-Inventory-Specification.md`;
- `docs/architecture/scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model.md`;
- `docs/architecture/scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model.md`;
- `docs/architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model.md`;
- `docs/architecture/scientific-assets/DSDM-004-Session-Importer-Architecture-and-Safe-Transfer-Design.md`;
- AP-013 discovery, COPY_ONLY, scheduler and transfer-readiness evidence;
- `docs/architecture/validation/AP-013B-OneDrive-Transport-Operational-Acceptance.md`;
- `docs/architecture/validation/AP-013B-QG20-Promotion-Review.md`;
- `.github/roadmap/evidence/AP-013.evidence.json`;
- AP-014 dependency boundary for read-only catalog/search projection.

The Board also verified that the latest AP-013B closure baseline had successful `quality-gate`, `build-word` and `deploy` GitHub Actions checks before this review.

## 3. Review scores

| Dimension | Score | Assessment |
|---|---:|---|
| Architecture consistency | 96/100 | Binary storage, registry, provenance and catalog boundaries are explicit and mutually consistent. |
| Domain and layer integrity | 95/100 | AP-013 owns authoritative asset/provenance truth while AP-014 remains a read-only projection boundary. |
| Data model and contracts | 94/100 | DSDM-001/002/003 establish conceptual, logical and manifest baselines with stable identity and explicit unknown/provenance semantics. |
| Integrity and preservation | 91/100 | COPY_ONLY, SHA-256, no overwrite and no delete are validated; long-term backup/restore certification remains open. |
| Security | 94/100 | Least-privilege intent, no-secret rules, ACL review and scheduled-task principals are documented and verified for AP-013B. |
| Operability | 95/100 | Scheduler, evidence, idempotency, interruption recovery, restart recovery and rollback have been exercised for the active ingestion path. |
| Observability and auditability | 92/100 | Per-run CSV/JSON evidence, manifests and traceable hash outcomes are present; enterprise retention remains a future concern. |
| Migration and rollback | 90/100 | COPY_ONLY rollout is reversible and legacy transport retained for rollback; full archive migration strategy is not yet certified. |
| Test and quality evidence | 97/100 | Pester, regression, batch, fault-injection and GitHub CI evidence are strong for the bounded operational path. |
| Documentation and traceability | 90/100 | Core artifacts are present, but the original AP-013 initiation document and traceability/roadmap narrative require closure realignment. |

**Weighted overall score: 93.4/100**

## 4. Findings

### 4.1 Major — AP-013 initiation document is historically stale

The primary AP-013 package still describes several work items and validations as not started even though later DSDM and AP-013B artifacts supersede part of that state.

**Required treatment:** preserve the initiation history but add/maintain closure artifacts and roadmap/evidence status so readers do not interpret the initial table as current runtime truth.

### 4.2 Major — Long-term preservation certification remains open

AP-013 defines backup, restore, retention, media migration and integrity-scan responsibilities, but AP-013B evidence validates transport/integrity rather than a complete long-term preservation service.

**Condition ARB-013-C01:** no claim of certified long-term preservation, RPO/RTO or tested archive restore may be made until AP-009/AP-013 evidence exists.

### 4.3 Major — Processing provenance runtime remains partially architectural

DSDM-001/002/003 define ProcessingRun, WorkflowDefinition, ProcessingStep and environment/provenance contracts, but repository evidence does not certify end-to-end provenance capture for all PixInsight processing.

**Condition ARB-013-C02:** provenance runtime claims must remain bounded to evidence actually captured; AP-014/AP-015 integrations must not fabricate historical provenance.

### 4.4 Major — Full archive migration/capacity scale-out is not certified

COPY_ONLY import, batch progression and rollback are validated. A complete migration of the existing scientific archive and 1000-file capacity claim are not.

**Condition ARB-013-C03:** migration remains phased, non-destructive and separately authorized; batch scale-out above the validated AP-013B limit requires new evidence.

### 4.5 Minor — Contract implementation maturity differs from architecture maturity

DSDM-003 is a contract baseline and explicitly does not assert that all JSON schemas/validators are implemented.

**Condition ARB-013-C04:** consumers must distinguish architecture-contract status from implemented schema/runtime status.

### 4.6 Observation — Safety boundary is correctly preserved

AP-013 and its operational tooling do not own observatory command authority. Local physical interlocks and safety authority remain independent from the scientific repository path.

## 5. Condition disposition

| Condition | Disposition at closure | Closure effect |
|---|---|---|
| ARB-013-C01 Preservation certification | Open | Non-blocking for architecture closure; blocks preservation/RPO/RTO claims |
| ARB-013-C02 Provenance runtime completeness | Open | Non-blocking; blocks unsupported end-to-end provenance claims |
| ARB-013-C03 Migration/capacity scale-out | Open | Non-blocking; batch/large migration changes require new validation |
| ARB-013-C04 Contract implementation maturity | Open | Non-blocking; architecture contract must not be represented as fully implemented schema runtime |
| AP-013B operational gates | Passed | Supports bounded limited-production ingestion |

## 6. Approval conditions

Approval remains valid while:

1. RAW/source immutability is preserved;
2. overwrite remains prohibited unless a separately governed decision explicitly changes it;
3. checksum mismatch blocks acceptance rather than being corrected silently;
4. OneDrive remains transport/staging, not the authoritative scientific repository;
5. AP-014 remains a read-only catalog/search projection over AP-013 authority;
6. safety and physical-device command authority remain outside AP-013;
7. unexecuted preservation, provenance, migration or scale validations are not presented as executed evidence.

## 7. Stakeholder acknowledgement

The Project Owner reports that **Leonardo Di Egidio has read and approved the AP-013 closure package**. This acknowledgement is recorded as stakeholder approval and does not replace the independent ARB findings or conditions above.

## 8. Re-review criteria

A new ARB review is required before:

- certifying long-term preservation or restore objectives;
- materially changing RAW immutability or overwrite policy;
- increasing AP-013B operational batch/capacity beyond validated limits;
- enabling automatic destructive cleanup;
- changing the authority boundary between AP-013 and AP-014/AP-015;
- claiming complete PixInsight provenance capture without new evidence.

## 9. Final decision

**APPROVED WITH CONDITIONS**

AP-013 may close as an architecture package with the conditions above remaining visible. The bounded AP-013B ingestion path is operationally accepted for limited production; broader preservation/provenance/migration capabilities remain subject to their explicit evidence and future validation.