# Release Procedure

## Preconditions

- Release scope approved.
- All release files committed.
- MkDocs strict build successful.
- Working tree clean.
- Known issues reviewed.

## Procedure

```powershell
cd C:\DigitalStarGate\digital-stargate-manual

git branch --show-current
git status
mkdocs build --strict
git log --oneline -12
```

Create the release commit if required:

```powershell
git add mkdocs.yml
git add docs\release-1.0
git commit -m "docs(release): consolidate Digital StarGate 1.0 baseline"
```

Create the annotated tag:

```powershell
git tag -a v1.0.0 -m "Digital StarGate documentation release 1.0.0"
```

Verify:

```powershell
git show v1.0.0 --stat
git status
```

Push only after final approval:

```powershell
git push origin feature/sol-osm-001-foundation
git push origin v1.0.0
```

## Evidence

Capture:

- final build output;
- commit identifier;
- tag identifier;
- approval record;
- known issue acceptance.
