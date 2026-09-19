# ADR-017 — BKL-036 archived-evidence score boundary

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-09-19 |
| Release | Release 2.x |
| Capability | BKL-036 |
| Scope | Repository-archived evidence score published read-only in the public portal |

## Context

BKL-036-F1 mapped evidence compatibility and BKL-036-F2 defined the versioned envelope. The owner now authorizes an immediate, bounded `0–100` score over repository-archived evidence. The score must not be confused with current telemetry, readiness or safety.

## Decision drivers

- use only telemetry already acquired and archived in the repository;
- publish the projection in the public Digital StarGate portal;
- make the calculation deterministic and explainable;
- fail closed when any mandatory domain is not comparable or current under its source-specific freshness contract;
- preserve BKL-032 readiness ownership and local physical interlock authority.

## Considered options

1. Aggregate live telemetry — rejected; live source, transport and runtime acceptance remain separate gates.
2. Calculate a partial score — rejected; missing, stale, unavailable, partial and conflicting evidence must not be normalized into a score.
3. Assign `100` to every comparable mandatory domain and average equally — selected as the bounded archived-evidence policy.

## Decision

The F3 projection uses exactly seven mandatory domains: weather, dome, mount, camera, power, network and EAGLE health. Every domain that is `PRESENT`, `COMPARABLE` and `CURRENT` contributes `100`; the equal-weight mean is therefore `100` only when all seven domains qualify. If any domain fails that condition, the published result is `UNAVAILABLE` with no partial score.

The projection is repository evidence, not live or real-time telemetry. The portal must display the evaluation timestamp, source locators, the non-live label and reasons. The projection is read-only and has no command, remediation, scheduling, readiness or Safety Authority semantics.

## Consequences

### Positive

- deterministic and auditable publication;
- no optimistic partial score;
- immediate public visibility of evidence completeness without implying current observatory health.

### Negative

- the current archived repository evidence produces `UNAVAILABLE` because all seven domains are not simultaneously comparable and current;
- the policy is a binary completeness/comparability score, not a physical health assessment.

## Migration and rollback

The published JSON projection and static portal consumer are additive. Regeneration is deterministic from the archived input manifest. Rollback is a documentation/projection revert; no runtime, provider, device or database migration is introduced.

## Safety and authority

BKL-032 remains the owner of readiness/go-no-go. Local physical interlocks remain the only Safety Authority. The score cannot open, close, move, power, schedule or remediate any apparatus.

## Validation

Validate schema shape, exact seven-domain coverage, equal-weight `100` policy, fail-closed `UNAVAILABLE` behavior, stale/missing/conflicting evidence, non-live labeling, public static consumer syntax and inherited BKL-031/BKL-032 governance.

## Open issues

- source-specific freshness and retention remain authoritative per source;
- no live telemetry consumer is introduced by F3;
- future non-binary health semantics, thresholds or operational use require a new governed increment.

## Traceability

- ADR-015 — source mapping and evidence compatibility boundary;
- ADR-016 — evidence envelope and descriptive projection boundary;
- `docs/architecture/telemetry/BKL-036-F3-Archived-Evidence-Score.md`;
- `contracts/telemetry/bkl-036-f3-health-score-v1.schema.json`.
