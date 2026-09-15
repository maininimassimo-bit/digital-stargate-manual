# Digital StarGate Site Authority Registry

This directory is the GitHub-governed protected authority location for exact observatory-site records.

## Classification and publication boundary

- The registry is outside `docs/` and is not a GitHub Pages input.
- Exact coordinates, elevation, source locator, internal identifiers and internal digests are `PROTECTED_EXACT_SITE`.
- Protected values may exist only in governed records/evidence under this directory and must not be printed by validators, workflows, reviews or public documentation.
- Public material may expose only an independently assigned opaque public reference, the generalized label `Manciano (GR), Italia`, the governed timezone display, availability metadata and public-only provenance.
- A public identifier or digest must not be derived from an internal identifier, protected value or internal digest.

## Authority

- Authority system: protected registry in `maininimassimo-bit/digital-stargate-manual`.
- Site owner and human Approval Authority: `github:user:maininimassimo-bit`.
- Technical custodian: `role:digital-stargate-architecture-office`.
- The custodian may prepare, validate and remediate candidates but cannot approve them.
- N.I.N.A. is the owner-attested consulted application source; observed application state is not independently promoted to authority.

## Lifecycle

`DRAFT -> APPROVED -> RETIRED`

Only an `APPROVED` envelope with a matching, separately committed, exact-digest human approval receipt is resolver-eligible. A source authorization or generic repository-write authorization is not lifecycle approval.

The immutable DRAFT candidate is retained as proposal evidence. The Repository Owner has separately approved its exact canonical payload digest and validity; this promotion package adds an `APPROVED` envelope with the identical payload plus a bound receipt. After integration, the protected repository resolver may return the site only to an authorized caller within validity. No runtime adapter or `CurrentSetupAssignment` is created, so the Observation Planner's runtime S08/S09 sources remain unavailable.

## Layout

- `site-records/`: protected immutable site payloads and lifecycle envelopes;
- `decision-evidence/`: owner decisions authorizing protected source facts and draft materialization;
- `approval-evidence/`: immutable exact-digest lifecycle approvals;
- `schemas/`: versioned JSON Schema contracts.
- `tools/`: validator and synthetic contract tests confined to this protected governance boundary.

## Canonicalization and validation

Payload identity uses `DSG-F3A1-CANONICAL-JSON-SHA256-1`: recursively sort object keys, preserve array order, serialize compact JSON, encode UTF-8 and compute SHA-256.

Validation is fail-closed and executed by:

- `governance/site-authority/tools/site-authority-validator.mjs`;
- `governance/site-authority/tools/test-site-authority.mjs`;
- `.github/workflows/bkl-031-f3-a1-site-authority-governance.yml`.

The validator checks lifecycle, authority, WGS84 ranges, orthometric elevation semantics, IANA timezone, half-open validity, digest integrity, DRAFT-to-APPROVED payload immutability, approval-receipt binding, authorized/unauthorized resolution and absence of protected literals from `docs/`. Its output intentionally omits protected values and internal digests.

## Rollback

Revert or retire records through reviewed Git history. Never delete history, infer a replacement from N.I.N.A./EAGLE state or fall back to public/generalized data. No runtime, device or observatory rollback is involved.
