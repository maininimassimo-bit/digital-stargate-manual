# Digital StarGate — Current Technical Baseline 25/09/2026

| Field | Value |
|---|---|
| Identifier | `DSG-BASELINE-2026-09-25` |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch baseline | `main` |
| Current `main` head before this continuity reconciliation | `df4d575a10d1517cdaa3bd2777c4db577034a5c3` |
| Current package | BKL-043 Observatory Reliability Engineering — F3 review / F4 exact pilot authorization preparation |
| Owner / accountable | Massimo Mainini |
| Authority | bounded advisory and read-only; local physical interlocks remain independent Safety Authority |

## 1. Canonical programme state

The canonical roadmap source records 47 items: 44 completed, 1 active and 2 planned
(94%). `RC2-BASELINE` is closed / accepted / post-merge verified and is recorded as
completed. `BKL-043` is the sole active roadmap item; `BKL-049` and `BKL-050` remain
planned. The generated roadmap is a projection of
`.github/roadmap/roadmap-source.json` and must be regenerated with the governance
scripts after any source change.

BKL-042 is CLOSED / ACCEPTED within its bounded read-only scope. Its accepted
retrieval/OAT limitations remain binding: aggregate SQM context has no per-session
values, M 27 quality context is experimental and uncalibrated, and excluded source
classes are not promoted. Evidence:
`docs/project/BKL-042-CLOSURE-2026-09-24.md` and
`docs/project/BKL-042-F7-BOUNDED-ACCEPTANCE-2026-09-24.md`.

## 2. BKL-043 verified state

- F1 source/population discovery is complete. There is no eligible operational
  population for availability, incident rate, MTBF, MTTR, failure budget or numeric
  SLI/SLO claims.
- F2 two-plane logical architecture is owner-approved and design-only. It defines a
  local read-only observer plus an independent witness; it does not authorize a
  collector, polling, persistence, alerting or deployment.
- F3 is repository-only. The closed synthetic observation envelope and ten offline
  tests passed locally and in Developer Foundation post-merge run `36021635340` on
  `b2aa86d790644cf6791ffa413d23b80701c72170`; review findings remain pending.
- F4 is a preparation-only decision draft. The two-plane scope and target
  `EAGLE30154` are selected. GitHub is a witness-provider candidate, and Leonardo
  Di Egidio is nominated as independent reviewer. These selections do not constitute
  runtime authorization.

The following F4 fields remain stop conditions: current host/OS attestation,
service identity, immutable artifact/configuration, source boundaries, exact private
GitHub resource, durable receipt store and independence proof, transport/authentication,
cadence/freshness, persistence, retention, start mode, resource limits, rollback and
OAT criteria. The public manual repository must not receive operational telemetry.

## 3. Implemented and operationally validated boundaries

The Observation Planner remains a published read-only/advisory capability. The
hourly weather-window GO/NO-GO presentation is advisory only and does not replace
BKL-032 readiness, local interlocks or Safety Authority. The governed refresh commit
`df4d575a10d1517cdaa3bd2777c4db577034a5c3` is the current source baseline.

AP-008 and BKL-036-F5 remain closed within their accepted bounded read-only scopes.
Their presence does not authorize BKL-043 live collection or a reliability metric.
S10 production runtime remains `UNAVAILABLE`.

## 4. Non-negotiable safety and authority boundary

`command_authority=NONE`; `execution_authority=NONE`; `safety_authority=NONE` for
the BKL-043 work. No command path, device control, scheduler, automatic remediation,
broker, live writer, startup service or change to physical local interlocks is
included or authorized.

## 5. Continuity and next gate

Read `AI_BOOTSTRAP.md`, this baseline, and
`docs/project/HANDOVER_2026-09-25-BKL043-F4.md` before modifying BKL-043. The next
dependency-ordered work is to close F3 findings, complete every F4 exact decision
field, obtain independent security/privacy/ARB/Release Quality findings, and only
then seek a separately versioned pilot authorization.
