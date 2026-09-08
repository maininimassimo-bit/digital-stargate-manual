# BKL-038 F1 — Anomaly & Trend Center Source Discovery and Semantic Contract

| Field | Value |
|---|---|
| Identifier | `BKL-038-F1` |
| Status | In Progress |
| Version | 0.1 |
| Date | 2026-09-08 |
| Parent backlog item | BKL-038 — Anomaly & Trend Center |
| Baseline | `d030e3031dabb737e76a32220a132b49b6e58c74` |
| Dependencies | BKL-030; BKL-040; BKL-044 |
| Authority | Repository governance contract |
| Runtime impact | None |
| Safety Authority | No |

## 1. Purpose

Define the bounded source inventory, semantic model, authority rules and fail-closed behavior for the Digital StarGate Anomaly & Trend Center before any detector, score, dashboard or automated analysis is implemented.

BKL-038 is an advisory/read-only analytical capability over accepted historical evidence. It must detect and describe evidence-supported changes, patterns and candidate anomalies without inventing operational thresholds, without converting incomplete evidence into certainty and without introducing command, remediation or Safety Authority.

## 2. Governing constraints

BKL-038 inherits these non-negotiable constraints:

- GitHub repository artifacts and accepted runtime evidence remain the source of truth for governed contracts;
- source records are immutable evidence inputs to the analytical projection;
- derived anomaly/trend records are projections and cannot override source authority;
- Citation, Provenance, lifecycle and semantic type from BKL-044 must be preserved where applicable;
- historical `CURRENT`/quality values are interpreted at their original observation time and are not rewritten because time has passed;
- unknown, missing, stale-at-observation, conflicted or unsupported evidence remains explicit;
- no severity threshold, warning limit, statistical cutoff or maintenance interval may be invented merely to classify a condition;
- no anomaly/trend result may open/close the roof, move the mount, power-cycle equipment, restart software, change network configuration or alter Safety state;
- local physical interlocks remain the sole physical Safety Authority.

## 3. Approved bounded source inventory

F1 authorizes only sources already accepted by the BKL-030 and BKL-040 foundations. Later increments may add sources only through explicit versioned governance.

| Order | Canonical source | Role in BKL-038 | Authority classification | F1 disposition |
|---:|---|---|---|---|
| 1 | BKL-030 historical EAGLE health records under the accepted `BKL-030-G6` contract | Host-health signal history with signal state, quality, timestamps, source, cadence, reason and raw data | governed historical projection | **primary source for EAGLE host trend evidence** |
| 2 | `docs/architecture/telemetry/BKL-030-G6-EAGLE-Health-History-Persistence-Design.md` | Meaning, identity, freshness and persistence semantics for source 1 | repository architecture authority | semantic authority for EAGLE historical records |
| 3 | `docs/data/night-timeline-replay-f3.json` | Accepted synchronized historical multi-source replay artifact | governed historical projection | **primary synchronized event source for BKL-040 event evidence** |
| 4 | `docs/data/night-timeline-read-model.json` | Consumer-oriented read model over source 3 | projection/read optimization | consumer support only; cannot override source 3 |
| 5 | `docs/architecture/telemetry/BKL-040-F3-Multi-Source-Synchronization-and-Skew-Classification.md` | Temporal ordering, source preservation and synchronization semantics | repository architecture authority | semantic authority for synchronized event relationships |
| 6 | `docs/architecture/telemetry/BKL-040-F4-Night-Timeline-Consumer-Read-Model-and-Closure-Contract.md` | Read-only/visual-only consumer boundary | repository architecture authority | consumer authority boundary |
| 7 | `docs/data/knowledge-ai-evidence-contract.json` and accepted BKL-044 documentation | Citation, Provenance, lifecycle, observation/inference/recommendation distinction | repository governance authority/projection | mandatory cross-cutting semantic rules |

### 3.1 Source precedence

Precedence is fact-class specific:

- EAGLE host signal observations: source 1, interpreted through source 2;
- synchronized historical event ordering: source 3, interpreted through source 5;
- consumer presentation: source 4, bounded by source 6;
- Citation/Provenance/lifecycle semantics: source 7.

A downstream read model may improve discoverability but cannot resolve or overwrite a conflict in its upstream evidence.

## 4. Initial source coverage boundary

The functional roadmap names guiding, autofocus, USB errors, network, EAGLE, camera, weather, SQM and failure patterns as candidate analytical domains. F1 does **not** claim all of those domains are already materialized as accepted historical BKL-038 inputs.

The accepted starting baseline is deliberately narrower:

- BKL-030 EAGLE host-health historical signal records;
- BKL-040 historical replay events actually present in the accepted F3 artifact;
- only source channels and fields proven by those accepted artifacts.

BKL-040 closure established that N.I.N.A., PHD2 and CloudWatcher are the principal executable synchronized sources, with session projection where defined. SQM/EAGLE may be supplied through their separately accepted foundations. Power, Network and Safety must not be fabricated as historical BKL-038 channels merely because they appeared in an earlier functional roadmap.

## 5. Semantic model

BKL-038 distinguishes five record types.

### 5.1 Observation

A source-backed historical fact copied or referenced without analytical reinterpretation.

Required semantics:

- source identity;
- source record locator;
- observed timestamp or explicit absence thereof;
- quality/lifecycle as emitted by the source;
- semantic type `observation`;
- no generated severity.

### 5.2 Trend measurement

A deterministic derived measurement comparing two or more compatible observations over a declared time window.

Examples permitted in later increments include:

- first/last numeric difference;
- minimum/maximum/mean/median where input type and method permit it;
- event count over an explicit interval;
- time between compatible events;
- monotonic direction where mathematically demonstrable;
- source coverage ratio.

Every trend measurement must declare:

- `method_id` and version;
- ordered input record identifiers;
- window start/end;
- measurement unit when applicable;
- result value;
- Citation/Provenance;
- evidence coverage and quality summary;
- whether the result is descriptive only.

A trend measurement is not automatically an anomaly.

### 5.3 Anomaly candidate

An evidence-supported condition that violates an **explicit governed rule** or exhibits an explicitly declared analytical pattern. An anomaly candidate is not a Safety event and not a command authorization.

F1 authorizes anomaly candidates only when one of these rule origins exists:

1. an already-governed source state transition or reason code;
2. a later approved versioned rule/method with explicit evidence and rationale;
3. an explicit source contract violation such as malformed/missing required evidence handled by a validator.

F1 does **not** authorize arbitrary statistical cutoffs, z-score limits, percentage-change limits, severity thresholds or predictive limits.

Required semantic state:

- `candidate_state`: `OBSERVED_RULE_MATCH`, `DATA_QUALITY_EXCEPTION`, `NOT_ASSESSED`, or `UNSUPPORTED`;
- `rule_id` when a governed rule exists;
- source/citation/provenance references;
- explanatory reasons;
- confidence only when inherited from an approved confidence method;
- no automatic operational action.

### 5.4 Correlation candidate

A derived relationship between two or more temporally comparable observations/trends.

F1 permits only explicit temporal/co-occurrence relationships such as:

- event A occurred before/after event B;
- records overlap the same declared time window;
- two trend measurements move in the same/opposite direction when the mathematical method is declared.

Correlation does not imply causation. A correlation candidate must never be labeled root cause without a separately governed inference method and evidence.

### 5.5 Recommendation

A human-readable advisory response to an accepted anomaly/trend/correlation result. Recommendation support is deferred beyond F1 and must inherit BKL-044 recommendation semantics. It remains advisory and cannot execute remediation.

## 6. Time semantics

BKL-038 preserves BKL-040 temporal rules:

- `event_time_utc` is canonical where present in the accepted replay contract;
- `PLACED` and `UNPLACED` states are preserved;
- source timestamps are never rewritten to force alignment;
- records without sufficient temporal evidence cannot be inserted into a trend window by inference;
- synchronization/skew metadata may describe relationships but does not mutate source observations;
- temporal comparison must declare the exact method and ordering input.

BKL-030 signal history preserves the observation-time quality emitted by the collector. BKL-038 must not retroactively convert historical quality because the record is old today.

## 7. Numeric analysis rules

F1 permits future numeric trend methods only when all of the following hold:

- the source field is explicitly numeric in its governed contract or accepted evidence;
- compatible units are known and preserved;
- missing/non-numeric values are excluded explicitly, not coerced to zero;
- the exact input set is recorded;
- the method is deterministic and versioned;
- no result is automatically mapped to `good`, `bad`, `critical`, `degraded` or `anomalous` without an approved rule.

A change from 10 to 20 may be represented as a numeric delta where semantically valid. F1 does not authorize declaring that change abnormal without a governed comparison rule.

## 8. Categorical/event analysis rules

For categorical source states and events, later increments may deterministically produce:

- state-transition sequences;
- transition counts;
- reason-code counts;
- repeated identical event signatures;
- durations between explicitly timestamped compatible events;
- source coverage/missingness summaries.

A repeated failure/event pattern may become an anomaly candidate only if the method and the rule for calling it anomalous are separately governed. Frequency alone does not create severity.

## 9. Identity and deduplication

BKL-038 must preserve upstream identifiers.

Derived record identity must be deterministic over:

```text
record_type
+ method_id/version
+ ordered source record identifiers
+ declared analysis window
```

Replay or duplicate execution of the same method over the same evidence must produce the same logical derived identity.

No derived identity replaces BKL-030 `record_id`, BKL-040 `replay_event_id` or any upstream source identifier.

TD-012 remains applicable to BKL-040 F1/F2 compatibility. BKL-038 must consume the accepted BKL-040 contract as it exists and must not silently retrofit `source_event_id`/`replay_event_id` semantics.

## 10. Data quality and fail-closed semantics

The analytical pipeline must use explicit data-quality outcomes.

Minimum states:

- `CURRENT_AT_OBSERVATION` — source evidence was current according to its accepted source contract;
- `STALE_AT_OBSERVATION` — source evidence was stale according to the source contract;
- `UNKNOWN` — source quality/value unknown;
- `INCOMPLETE` — required inputs for the requested method are missing;
- `CONFLICTED` — governed inputs materially disagree and the method has no approved reconciliation rule;
- `UNSUPPORTED` — source type/unit/method combination is outside the approved contract.

`INCOMPLETE`, `CONFLICTED`, `UNKNOWN` and `UNSUPPORTED` must not be converted to normal/healthy states.

## 11. Explainability contract

Every non-observation record must be explainable from repository data without relying on hidden model reasoning.

Required fields for later machine-readable implementation:

- derived record id;
- semantic type;
- method/rule id and version;
- source record references;
- Citation references;
- Provenance references;
- analysis window;
- exact derived value/state;
- quality/coverage result;
- explanatory reason codes;
- authority classification = `projection`;
- action authority = `NONE`.

If AI is later used to summarize or recommend, the deterministic analytical evidence remains separately visible and the AI output must retain BKL-044 inference/recommendation semantics.

## 12. Prohibited behavior

BKL-038 validation must reject or prevent:

1. source observations without resolvable source reference;
2. derived results without method/version;
3. anomaly labels without an explicit governed rule origin;
4. invented numeric thresholds or severity cutoffs;
5. conversion of missing data to zero/normal/healthy;
6. causal/root-cause claims from correlation alone;
7. mutation or overwrite of accepted BKL-030/BKL-040 evidence;
8. use of UI text/browser state as source authority;
9. fabricated source channels not present in accepted inputs;
10. hidden loss of Citation/Provenance/lifecycle semantics;
11. command, restart, power-cycle, network-change or device-control actions;
12. Safety Authority promotion;
13. present-time Safety inference from historical replay;
14. silent retrofit of TD-012 compatibility semantics.

## 13. Security, runtime and Safety boundary

F1 is repository-only and introduces no runtime executable on EAGLE or PC principale.

No new collector, service, Scheduled Task, network listener, API endpoint, device command path or filesystem cleanup is authorized.

Future BKL-038 computation should preferentially run downstream/off-observatory where practical. If a later increment requires runtime execution on EAGLE, that workload must be separately assessed for bounded CPU, memory, I/O and scheduling impact before activation.

Local physical Safety Authority and interlocks remain independent from BKL-038.

## 14. Proposed delivery increments

- **F1 — Source Discovery & Semantic Contract:** current increment.
- **F2 — Machine-readable analytical record schema + bounded deterministic fixture:** observations, trend measurements, anomaly candidates and explicit quality states over accepted source fixtures.
- **F3 — Deterministic trend/candidate engine:** versioned methods, idempotent derived identities, fail-closed validation and bounded multi-source temporal correlation.
- **F4 — Anomaly & Trend Center consumer read model / portal projection and closure:** read-only/advisory presentation, source drill-down and package acceptance.

A later package may add predictive maintenance or advanced statistical methods only after method governance, validation evidence and independent ARB review. Automatic remediation remains out of scope.

## 15. F1 acceptance criteria

F1 is ready for independent review when:

1. accepted BKL-030 and BKL-040 source families are identified precisely;
2. source authority and downstream projection authority are separated;
3. observation, trend, anomaly candidate, correlation candidate and recommendation semantics are distinct;
4. no threshold is invented;
5. time, identity, quality and unknown/stale behavior are explicit;
6. Citation/Provenance and explainability requirements are explicit;
7. TD-012 compatibility is acknowledged without retrofit;
8. fail-closed rules are explicit;
9. runtime/Safety boundary is explicit;
10. documentation and repository CI gates pass;
11. independent ARB approves F1 before F2 implementation.

## 16. Open decisions deferred beyond F1

- exact JSON schema field names and enum encoding for F2;
- which bounded real/fixture records form the first deterministic proof set;
- approved descriptive trend methods beyond elementary deterministic aggregates;
- whether any statistical anomaly method is justified and, if so, its training/reference baseline and governance;
- portal visualization details;
- retention policy for derived analytical projections;
- predictive-maintenance semantics;
- AI-assisted summarization/recommendation presentation.

None of these open decisions authorizes implementation by implication.

## 17. Disposition

**BKL-038 F1 initiated.**

The next safe step is repository CI followed by independent ARB review of this semantic contract. F2 must not begin until F1 is accepted.