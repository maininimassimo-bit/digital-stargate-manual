# Dependency Management

## Policy

Dependencies must be declared explicitly and pinned to reproducible versions where the ecosystem supports it.

## Controls

- maintain lock files or equivalent manifests;
- review licences and operational suitability;
- track end-of-life announcements;
- evaluate security advisories;
- test upgrades in validation before production;
- avoid unnecessary dependencies;
- document critical runtime and hardware-driver constraints.

## Update classes

Patch updates may follow the standard change process. Minor and major updates require compatibility assessment, regression testing and a documented rollback path.
