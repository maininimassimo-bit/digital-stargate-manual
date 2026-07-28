# Environments

## Environment classes

| Environment | Purpose | Data and device policy |
|---|---|---|
| Local | authoring and isolated development | simulators and non-sensitive samples |
| Validation | integration and acceptance checks | controlled test devices or replay data |
| Production | live observatory operation | approved configurations and protected credentials |

## Promotion rules

The same versioned artefact is promoted between environments. Environment differences are supplied through governed configuration, not by rebuilding source code.

## Production safeguards

Production changes require an identified maintenance window when appropriate, current backup or rollback capability, operator awareness and post-change health verification.
