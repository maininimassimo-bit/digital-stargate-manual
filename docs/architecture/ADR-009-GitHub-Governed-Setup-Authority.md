# ADR-009 — GitHub-Governed Setup Authority

| Campo | Valore |
|---|---|
| Identificativo | ADR-009 |
| Stato | **Accepted — baseline and site APPROVED; assignment approval/promotion review candidate** |
| Data | 15/09/2026 |
| Decision owner | Repository Owner / human Approval Authority |
| Custodian | Digital StarGate Architecture Office |
| Repository baseline | `maininimassimo-bit/digital-stargate-manual@1ce08f4cc5458cc7ac68732a02df0d27a359f8d5` |
| Parent contract | `BKL-031-F3-A2-CONTRACT-001` |
| Finding | `ARB-197-MI01` |
| Runtime / EAGLE / Safety impact | None |

## Context

F3-A2 requires a concrete Configuration Baseline Authority and Setup Assignment Authority before S09 can resolve current setup. AP-006 defines governance semantics but does not attest a concrete record. The current equipment registry is explicitly a projection and cannot be promoted by inference.

On 15/09/2026 the Repository Owner authorized the GitHub-governed authority model and subsequently approved the first exact baseline payload, digest `[protected digest recorded outside docs]`, with validity from `2026-09-16T00:00:00Z`. The approval is recorded by a separate immutable receipt. It does not approve a site record or setup assignment.

## Decision

1. The authoritative registry root is `protected GitHub registry` in `maininimassimo-bit/digital-stargate-manual`.
2. The registry stays outside `docs/`; MkDocs and GitHub Pages do not publish its protected records.
3. The Repository Owner, referenced as `Repository Owner`, is:
   - Configuration Baseline Owner;
   - Setup Assignment Owner;
   - human Baseline Approval Authority;
   - human Assignment Approval Authority.
4. `Architecture Office` is custodian for both lifecycles. The assistant may prepare, validate, review and remediate records under `DSG-AEM-001`, but cannot approve a baseline or assignment.
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

## First approved baseline

`first protected setup baseline record` is derived only from:

- `data/analytics/configurations/equipment-registry.csv` at blob `734bceeaa517022aa2c78977ff0d13f685f20265`, explicitly `PROJECTION_ONLY`;
- AP-006 architecture rules;
- the accepted F3-A2 contract.

Its exact payload digest is `[protected digest recorded outside docs]`. It contains two configuration profiles and a half-open validity start of `2026-09-16T00:00:00Z`. The Repository Owner approved that exact payload through the owner-controlled channel on 15/09/2026. The lifecycle envelope is `APPROVED`, the matching receipt is stored under `protected GitHub registry`, and the protected record remains excluded from Pages. Proposal-time labels inside the immutable payload remain unchanged because they are covered by the approved digest; current lifecycle truth is the envelope plus receipt.

## Consequences

Positive:

- concrete authority roles and repository source are deterministic;
- approval is auditable and process-separated;
- Pages cannot accidentally publish protected baseline data;
- rollback uses Git history and retirement without runtime fallback.

Constraints:

- `ARB-197-MI01-B` and `ARB-199-MI01` are closed for the first approved baseline; the F3-A1 site record is approved and D5 supplies the separately approved assignment candidate;
- runtime adapter, persistence integration, public projection and OAT remain future work;
- unresolved C8 guiding, serials and runtime versions cannot be inferred;
- no command, safety, readiness, ranking or go/no-go semantics are introduced.

## Alternatives rejected

- Using `data/analytics/configurations/equipment-registry.csv` directly: rejected because it is a projection.
- Reading EAGLE/N.I.N.A. state as current authority: rejected because observed state is not desired authority and no operational access is authorized.
- Storing records under `docs/`: rejected because protected configuration would enter the Pages publication input.
- Custodian self-approval: rejected because it would violate the required human Approval Authority boundary.

## Rollback

Retire the applicable approved envelope and receipt through reviewed Git history, then return its repository eligibility to unavailable. No migration, deployment, device operation or data deletion is involved. Runtime S09 remains `UNAVAILABLE_CURRENT` because no adapter exists; never fall back to projection or observed state.


## D4 implementation note — 15/09/2026

The GitHub authority now contains a protected, immutable assignment DRAFT with closed schemas and executable validation. It has no receipt, is not resolver-eligible and does not make S09 available. A later explicit human decision tied to the exact protected assignment digest is mandatory before lifecycle promotion.


## D5 assignment approval note — 15/09/2026

The Repository Owner explicitly approved the exact protected `CurrentSetupAssignment` digest and its unbounded validity from the approved setup-baseline effective start. D5 records the approval in a separate protected receipt and creates an `APPROVED` lifecycle envelope without changing the assignment payload or digest. The protected repository resolver becomes eligible for authorized validated callers only; runtime S09 remains `UNAVAILABLE_CURRENT` because no adapter is included.
