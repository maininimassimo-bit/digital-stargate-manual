# Pipeline Quality Gates

## Mandatory gates

| Gate | Minimum evidence | Failure result |
|---|---|---|
| Repository integrity | clean checkout and valid structure | block |
| Documentation | strict MkDocs build | block |
| Schemas | valid JSON or YAML schemas and examples | block |
| Tests | required test suites pass | block |
| Security | no critical exposed secret or accepted vulnerability breach | block |
| Packaging | reproducible artefact with metadata | block |
| Deployment readiness | approved release and rollback plan | block |

## Exceptions

A gate can be bypassed only through an explicit, time-bound approval recording the risk owner, reason, compensating controls and remediation date.
