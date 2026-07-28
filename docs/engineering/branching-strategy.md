# Branching Strategy

## Model

Digital StarGate uses a lightweight feature-branch model.

```text
main
  ├─ feature/<scope>-<description>
  ├─ fix/<scope>-<description>
  ├─ docs/<scope>-<description>
  └─ release/<version>
```

## Rules

- `main` represents the latest approved and releasable state.
- Feature branches must be short lived and rebased or merged frequently.
- Release branches are used only when stabilization must be separated from ongoing work.
- Hotfixes originate from the affected release baseline and are merged back into active development.
- Direct commits to protected branches are prohibited except for explicitly approved emergency procedures.

## Merge policy

A branch can be merged when required reviews are complete, automated checks pass, conflicts are resolved and release notes are updated when the change is user-visible or operationally relevant.
