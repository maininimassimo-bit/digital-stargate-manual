# Release Rollback

## Use cases

Rollback is required when:

- the release tag points to the wrong commit;
- critical documentation is missing;
- navigation is broken;
- the generated site cannot be built;
- approval was not completed.

## Local tag rollback

```powershell
git tag -d v1.0.0
```

## Remote tag rollback

Use only after coordination:

```powershell
git push origin :refs/tags/v1.0.0
```

## Repository rollback

Prefer a corrective commit instead of rewriting shared history:

```powershell
git revert <commit-id>
```

## Recovery

1. Correct the documentation.
2. Re-run `mkdocs build --strict`.
3. Review the working tree.
4. Commit the correction.
5. Recreate the release tag after approval.
