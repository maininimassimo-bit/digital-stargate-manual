# Release 1.0 Scope

## In scope

Release 1.0 includes the documentation foundation required to operate and evolve Digital StarGate:

- enterprise architecture and governance;
- solution and platform architecture;
- observatory assets, dependencies and recovery references;
- automation orchestration, state models and emergency workflows;
- infrastructure, networking, security, monitoring and continuity;
- engineering standards, CI/CD, testing and release management;
- scientific data ingestion, processing, catalog, lineage and retention;
- release governance, validation checklists and operating procedures.

## Out of scope

The following are intentionally deferred:

- production software implementation;
- live CI/CD pipelines;
- automated observatory control code;
- executable data processing pipelines;
- infrastructure-as-code deployment;
- integration tests against physical equipment;
- formal regulatory certification.

## Acceptance conditions

Release 1.0 is accepted when:

1. `mkdocs build --strict` completes successfully.
2. All new navigation entries resolve to existing documents.
3. Release artifacts are committed to the repository.
4. Known legacy link issues are documented.
5. The working tree is clean.
6. A signed or annotated release tag is created.
