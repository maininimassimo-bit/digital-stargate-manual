# BKL-039 F4-B — Equipment Performance Portal Projection

| Field | Value |
|---|---|
| Identifier | `BKL-039-F4-B` |
| Capability | BKL-039 — Equipment Performance Registry |
| Status | In Progress |
| Version | 0.1 |
| Date | 2026-09-09 |
| Base | F4-A accepted merge `c9ccf2bdfd849a4ae7305a4a7d134572353aa45e` |
| Runtime impact | None — GitHub Pages / static browser projection only |
| Safety impact | None — local physical Safety Authority unchanged |

## 1. Objective

F4-B exposes the accepted F4-A machine-readable read model in the Digital StarGate portal without introducing a service, API, persistence layer, runtime collector or operational command path.

The browser reads `docs/data/equipment-performance-registry-f4-read-model.json` directly and renders only the semantics already accepted by F4-A.

## 2. Portal surface

The bounded portal projection provides:

- configuration, session, target, filter and declared population context;
- the four accepted descriptive FWHM statistics without recalculation;
- the 19 accepted source-backed FWHM measurements in deterministic source order;
- explicit source-native unit, unit semantics and unproven angular calibration state;
- Citation, Provenance and source-record drill-down;
- visible interpretation and authority limitations.

## 3. Fail-closed browser contract

The browser must render the projection only when all of the following remain true:

- `component=DSG.EquipmentPerformanceRegistry.F4.ReadModel`;
- `authority=projection`;
- `action_authority=NONE`;
- `unit=NINA_FILENAME_FWHM_SOURCE_UNIT`;
- `unit_semantics=SOURCE_NATIVE_UNCALIBRATED`;
- `angular_calibration_state=NOT_PROVEN`;
- measurement array length equals the declared measurement count;
- the accepted no-health/ranking/threshold/recommendation limitation remains present;
- the historical read-only / not-Safety-Authority limitation remains present.

If any guard fails, or the repository artifact cannot be loaded, the browser fails closed and displays no inferred performance state.

## 4. Semantic boundary

The portal must not display or derive:

- GOOD/BAD/HEALTHY/DEGRADED equipment states;
- RAG or severity states;
- thresholds, target ranges or pass/fail performance criteria;
- rankings, percentiles or scores;
- anomaly/failure diagnosis or root-cause inference;
- predictive maintenance or maintenance scheduling;
- recommendations or remediation;
- present-time observatory Safety state;
- controls or commands for EAGLE, camera, focuser, mount, filter wheel, USB, power or network.

FWHM values remain source-native and uncalibrated. They are not labelled as arcseconds, pixels, seeing, focus quality or equipment health.

## 5. Security, runtime and Safety

F4-B is static browser rendering. It adds no secrets, credentials, listeners, writable APIs, background process or EAGLE/PC dependency.

Historical equipment-performance evidence is not current Safety evidence. Local physical interlocks and the local Safety Authority remain independent and authoritative.

## 6. Validation and acceptance

Acceptance requires:

1. existing F4-A generator, validator and negative regression suite remain green;
2. browser authority/unit/population/limitation guards are repository-verified;
3. MkDocs strict build succeeds;
4. Developer Foundation succeeds on the exact head;
5. independent ARB approval;
6. Release Quality READY;
7. final exact-head CI succeeds;
8. merge and post-merge exact-SHA workflows, including Pages when triggered, succeed.

No PC/EAGLE action is required.
