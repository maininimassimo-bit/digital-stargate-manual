# BKL-038 F4-A — Anomaly & Trend Consumer Read Model and Portal Projection

| Field | Value |
|---|---|
| Identifier | `BKL-038-F4-A` |
| Capability | BKL-038 — Anomaly & Trend Center |
| Status | In Progress |
| Version | 0.1 |
| Baseline | `615d46726c3998421bf04f9d6cc8cd8234023b62` |
| Upstream | F1, F2-A, F3-A, F3-B |
| Runtime impact | None — repository/Pages only |
| Safety impact | None |

## 1. Objective

F4-A materializes the bounded consumer projection and a read-only portal view over accepted F3-B output. It is not package closure by itself; closure remains a subsequent governed step after F4-A acceptance.

## 2. Data flow

`accepted BKL-040 F3 replay -> accepted BKL-038 F3-B deterministic engine -> F4 read model -> browser visual consumer`.

There is no reverse path to source evidence, EAGLE, observatory devices or Safety systems.

## 3. Machine-readable read model

`docs/data/anomaly-trend-read-model.json` is generated deterministically by `.github/scripts/generate-anomaly-trend-read-model.mjs` and binds accepted F3-B merge `615d46726c3998421bf04f9d6cc8cd8234023b62`.

The model preserves every F3-B analytical record including derived identity, semantic type, method/version, ordered source refs, Citation, Provenance, analysis window, measurement/state, quality, explanation codes and projection/action authority.

Consumer metadata is explicit: `authority=projection`, `action_authority=NONE`, `interaction_mode=READ_ONLY`, `advisory_mode=DESCRIPTIVE_ONLY`, `command_actions=[]`, `safety_authority=UNCHANGED_LOCAL_AUTHORITY`.

The bounded accepted fixture contains 5 records: 3 observations, 2 descriptive trend measurements, 0 anomaly candidates, 0 correlation candidates and 0 recommendations. Zero anomaly candidates means no governed anomaly rule is materialized in this slice; it does not mean the historical session was healthy or safe.

## 4. Portal semantics

`docs/anomaly-trend-center/index.md` and `docs/javascripts/anomaly-trend-center.js` render only the repository projection. The browser exposes source/Citation/Provenance drill-down and descriptive measurement values.

If the projection is unavailable or its authority contract is incompatible, the browser fails closed and displays no inferred analytical state.

The portal must not label a descriptive delta as anomaly, severity or root cause. It must not infer current Safety from historical records.

## 5. Source scope

F4-A does not onboard BKL-030 EAGLE history because repository-resolvable governed history evidence remains unavailable for analytical onboarding. It consumes only the source coverage already accepted through BKL-040/F3-B. This does not revoke EAGLE eligibility under F1; it keeps onboarding deferred until its evidence gate is satisfied.

## 6. Failure and validation rules

F4-A validation requires:

- deterministic read-model regeneration with semantic equality;
- preservation of accepted F3-B records and known bounded counts;
- projection/read-only/descriptive authority;
- empty command actions;
- fail-closed propagation of F3-B source-quality and evidence-reference violations;
- exact accepted temporal deltas without threshold reinterpretation;
- explicit `CAUSATION_NOT_INFERRED` on descriptive trends;
- browser fail-closed behavior when projection authority is unavailable or incompatible.

Developer Foundation executes the F4 generator check and F4 regression suite. Documentation/Word and Pages gates remain applicable.

## 7. Security, operations and Safety

No endpoint, listener, credential, collector, service, Scheduled Task or EAGLE workload is introduced. Static Pages reads a versioned repository JSON projection.

No command, remediation, restart, USB reset, network action, device control or Safety integration exists. Local physical interlocks remain independent and authoritative.

## 8. Acceptance criteria

F4-A is ready for independent ARB when:

1. the read model deterministically reproduces accepted F3-B output;
2. source/Citation/Provenance drill-down is preserved;
3. the portal is read-only and fails closed;
4. no anomaly threshold, severity, causal inference or recommendation is invented;
5. EAGLE history remains deferred without fabricated records;
6. exact-head Developer Foundation, Docs and Word gates are green.

After ARB approval and Release Quality, F4-A may merge. BKL-038 closure must then reconcile package status, closure evidence and canonical roadmap under the existing fail-closed closure governance.
