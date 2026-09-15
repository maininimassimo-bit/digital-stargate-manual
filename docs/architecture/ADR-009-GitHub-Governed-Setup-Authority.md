# ADR-009 — GitHub-Governed Setup Authority

| Campo | Valore |
|---|---|
| Identificativo | ADR-009 |
| Stato | **Accepted — owner-authorized authority model; first baseline remains DRAFT** |
| Data | 15/09/2026 |
| Decision owner | Repository Owner / human Approval Authority |
| Custodian | Digital StarGate Architecture Office |
| Repository baseline | `maininimassimo-bit/digital-stargate-manual@687f966fa544f7c4b31eaa29433cfa8ab48e52fe` |
| Parent contract | `BKL-031-F3-A2-CONTRACT-001` |
| Finding | `ARB-197-MI01` |
| Runtime / EAGLE / Safety impact | None |

## Context

F3-A2 requires a concrete Configuration Baseline Authority and Setup Assignment Authority before S09 can resolve current setup. AP-006 defines governance semantics but does not attest a concrete record. The current equipment registry is explicitly a projection and cannot be promoted by inference.

On 15/09/2026 the Repository Owner authorized the recommended GitHub-governed authority model and instructed the custodian to proceed. Approval of the first exact baseline payload remains a separate mandatory human decision.

## Decision

1. The authoritative registry root is `governance/setup-authority/` in `maininimassimo-bit/digital-stargate-manual`.
2. The registry stays outside `docs/`; MkDocs and GitHub Pages do not publish its protected records.
3. The Repository Owner, referenced as `github:user:maininimassimo-bit`, is:
   - Configuration Baseline Owner;
   - Setup Assignment Owner;
   - human Baseline Approval Authority;
   - human Assignment Approval Authority.
4. `role:digital-stargate-architecture-office` is custodian for both lifecycles. The assistant may prepare, validate, review and remediate records under `DSG-AEM-001`, but cannot approve a baseline or assignment.
5. Baseline approval and assignment approval are separate acts with separate immutable receipts under `approval-evidence/`.
6. Only records in `APPROVED` state, with an exact payload digest and matching approval receipt, are resolver-eligible.
7. A `DRAFT` can be derived from explicit repository evidence. Projection and observed fields retain their authority labels and unresolved values remain `DA_VALIDARE` or null.
8. The canonical payload identity method is `DSG-F3A2-CANONICAL-JSON-SHA256-1`: recursively sort object keys, preserve array order, serialize as compact JSON, encode UTF-8, compute SHA-256.
9. Approval changes the lifecycle envelope and adds an approval receipt; it must not mutate the approved payload or its digest.
10. No baseline approval creates a setup assignment. S09 remains `UNAVAILABLE_CURRENT` until an independently approved assignment and the required F3-A1 site authority record exist.

## Approval evidence contract

A future receipt must include at least:

- record type and receipt identifier;
- baseline or assignment identifier and version;
- exact payload digest;
- approving authority reference;
- explicit decision `APPROVED` or `REJECTED`;
- approval timestamp UTC;
- validity acknowledged by the approver;
- source statement that the approval was conveyed through the owner-controlled channel and recorded in GitHub;
- commit/PR locator once integrated.

The custodian must present the exact digest and material content before requesting approval. Silence, generic authorization, prior workflow success or assistant review never counts as approval.

## Initial DRAFT

`DSG-SETUP-BASELINE-001.draft.json` is derived only from:

- `data/analytics/configurations/equipment-registry.csv` at blob `734bceeaa517022aa2c78977ff0d13f685f20265`, explicitly `PROJECTION_ONLY`;
- AP-006 architecture rules;
- the accepted F3-A2 contract.

Its exact payload digest is `sha256:3f73d6a541faa88271e7c5fbef4f23791630713f0e3ca03bcb33dd79e8021cb8`. It proposes two configuration profiles and a half-open validity start of `2026-09-16T00:00:00Z`. It remains `DRAFT`, protected, ineligible and unpublished until the Repository Owner explicitly approves or corrects that exact payload.

## Consequences

Positive:

- concrete authority roles and repository source are deterministic;
- approval is auditable and process-separated;
- Pages cannot accidentally publish protected baseline data;
- rollback uses Git history and retirement without runtime fallback.

Constraints:

- `ARB-197-MI01` remains open for the first approved baseline and assignment;
- schema, validator, adapter, persistence, public projection and OAT remain future work;
- unresolved C8 guiding, serials and runtime versions cannot be inferred;
- no command, safety, readiness, ranking or go/no-go semantics are introduced.

## Alternatives rejected

- Using `data/analytics/configurations/equipment-registry.csv` directly: rejected because it is a projection.
- Reading EAGLE/N.I.N.A. state as current authority: rejected because observed state is not desired authority and no operational access is authorized.
- Storing records under `docs/`: rejected because protected configuration would enter the Pages publication input.
- Custodian self-approval: rejected because it would violate the required human Approval Authority boundary.

## Rollback

Revert ADR-009 and the DRAFT registry files. No migration, deployment, device operation or data deletion is involved. If a future record is approved, retire its approval/activation evidence and return S09 to `UNAVAILABLE_CURRENT`; never fall back to projection or observed state.
