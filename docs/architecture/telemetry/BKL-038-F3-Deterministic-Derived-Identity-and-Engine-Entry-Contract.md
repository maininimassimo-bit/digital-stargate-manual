# BKL-038 F3 — Deterministic Derived Identity and Engine Entry Contract

| Field | Value |
|---|---|
| Identifier | `BKL-038-F3` |
| Status | In Progress — F3-A |
| Version | 0.1 |
| Date | 2026-09-08 |
| Parent | BKL-038 — Anomaly & Trend Center |
| Accepted upstream | F2-A merge `67aaaa0dccddeeb77c7654554fc7783a9dc63c16` |
| Authority | Projection only |
| Runtime impact | None |
| Safety Authority | No |

## 1. Purpose

F3-A establishes the normative deterministic identity algorithm required by accepted F1/F2 before any dynamic analytical-record production. It deliberately does not add anomaly thresholds, detector policy, causal inference or runtime execution.

## 2. Canonical identity method

Method: `BKL038-F3-DERIVED-ID-SHA256-1`  
Version: `1.0`

The identity input is exactly the accepted F1 tuple, serialized as a JSON object in this fixed property order:

1. `semantic_type`;
2. `method_id`;
3. `method_version`;
4. `source_record_refs` preserving declared order;
5. `analysis_window.start_utc`;
6. `analysis_window.end_utc`.

No other analytical field participates in identity. Measurement values, quality, explanation text, Citation/Provenance payloads and consumer presentation therefore cannot silently change identity.

The UTF-8 bytes of that exact compact JSON serialization are hashed with SHA-256 and emitted as:

`AT-SHA256-<64 lowercase hexadecimal characters>`

## 3. Failure semantics

Identity generation fails closed when the record is not an object, semantic/method identity is missing, source references are empty or malformed, or the analysis window is absent/malformed. Source-reference order is intentionally significant because F1 made the ordered source identifiers part of the identity tuple.

F3-A does not normalize, reorder or infer source references or timestamps. It does not rewrite BKL-040 evidence and does not retrofit TD-012.

## 4. Determinism guarantees

For the same canonical identity tuple and method version, every conforming implementation must produce the same identifier. Changes to semantic type, method id/version, ordered source references or analysis window must produce a different identifier except for the cryptographic collision risk inherent in SHA-256.

Non-identity fields must not perturb the identifier.

The repository test suite includes a fixed known-answer vector derived from the accepted F2-A CloudWatcher-to-N.I.N.A. trend tuple.

## 5. Engine entry boundary

This slice establishes identity infrastructure only. A later F3 slice may dynamically derive records from accepted repository-resolvable evidence only after it preserves:

- the F1 semantic distinctions;
- F2 source/Citation/Provenance resolution;
- observation-time quality;
- `authority=projection`;
- `action_authority=NONE`;
- correlation-not-causation semantics;
- fail-closed unsupported/unknown handling.

No dynamic engine may invent a severity threshold or anomaly rule. A positive anomaly candidate requires a separately governed rule origin already allowed by F1.

## 6. Safety and runtime

F3-A is repository-only Node.js validation logic. It creates no collector, service, scheduler, listener, API, EAGLE filesystem access, device command, remediation path or present-time Safety inference.

Local physical interlocks remain independent and authoritative.

## 7. EAGLE evidence observation

The F2 ARB observation remains open. BKL-030 EAGLE history must not be onboarded until a bounded accepted repository-resolvable sample/evidence projection exists preserving upstream identifiers, timestamps, quality, source and provenance. F3-A does not bypass that constraint.

## 8. Acceptance criteria

F3-A is review-ready when:

- the canonical algorithm is versioned and repository-integrated;
- a fixed known-answer vector passes;
- idempotence is tested;
- source order is proven identity-significant;
- semantic type, method version and temporal window are proven identity-significant;
- non-identity fields are proven identity-neutral;
- malformed identity input fails closed;
- Developer Foundation executes the F3 identity tests;
- exact-head CI is green before independent ARB review.

## 9. Next bounded slice

After F3-A acceptance, F3-B may implement the first deterministic read-only derivation engine over the already accepted BKL-040 repository fixture. It must generate only semantics justified by governed source evidence and must not fabricate a positive anomaly candidate merely to satisfy coverage. EAGLE onboarding remains separately gated by repository-resolvable accepted evidence.
