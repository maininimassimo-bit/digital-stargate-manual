# Repository Governance

## Repository responsibilities

The repository is the system of record for architecture, documentation, schemas, configuration templates, automation logic and release history.

## Mandatory controls

- protected primary branches;
- reviewed pull requests for non-trivial changes;
- descriptive commits with a stable scope;
- no credentials, tokens or private keys in version control;
- generated output excluded unless explicitly required as a release artefact;
- traceable links between issues, decisions, changes and releases.

## Commit convention

Recommended format:

```text
<type>(<scope>): <imperative description>
```

Examples:

```text
docs(automation): clarify unsafe weather recovery
fix(network): correct failover health check
feat(platform): add session cancellation event
chore(deps): update documentation toolchain
```

## Pull request expectations

Each pull request should state:

- purpose and scope;
- affected architecture or services;
- validation performed;
- security and operational impact;
- rollback approach;
- related issue, decision or roadmap item.
