# REL-000 — Release Registry

| ID | Artifact | Status | Release | Owner | Evidence |
|---|---|---|---|---|---|
| REL-001 | Release scope | Approved candidate | 1.0 | Product owner | `release-scope.md` |
| REL-002 | Architecture baseline | Approved candidate | 1.0 | Architecture owner | `architecture-baseline.md` |
| REL-003 | Documentation status | Verified candidate | 1.0 | Documentation owner | `documentation-status.md` |
| REL-004 | Release notes | Draft complete | 1.0 | Release manager | `release-notes.md` |
| REL-005 | Changelog | Draft complete | 1.0 | Release manager | `changelog.md` |
| REL-006 | Quality checklist | Ready for execution | 1.0 | QA owner | `checklists/release-quality-checklist.md` |
| REL-007 | Documentation checklist | Ready for execution | 1.0 | Documentation owner | `checklists/documentation-review-checklist.md` |
| REL-008 | Link validation checklist | Ready for execution | 1.0 | Maintainer | `checklists/link-validation-checklist.md` |
| REL-009 | Release procedure | Ready for execution | 1.0 | Release manager | `runbooks/release-procedure.md` |
| REL-010 | Rollback procedure | Ready for execution | 1.0 | Release manager | `runbooks/release-rollback.md` |

## Registry rules

- Every release artifact must have a unique identifier.
- Status changes require evidence from repository validation.
- Approved artifacts must not be modified without a new commit.
- The release registry is reviewed before tagging the release.
