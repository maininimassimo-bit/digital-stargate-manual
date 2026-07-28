# Configuration Standards

## Principles

Configuration is treated as a governed artefact with the same traceability requirements as source code.

## Rules

- Separate defaults, environment overrides and secrets.
- Validate configuration against schemas where possible.
- Use explicit units for durations, sizes, angles and thresholds.
- Record the effective version of configuration used by a release.
- Avoid ambiguous boolean flags; prefer named modes or enumerations.
- Changes affecting safety thresholds require independent review.

## Secrets

Secrets must be stored outside the repository and injected through an approved secret-management mechanism. Example files must contain placeholders only.
