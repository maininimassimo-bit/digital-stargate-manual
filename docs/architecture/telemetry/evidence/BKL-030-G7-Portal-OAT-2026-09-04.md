# BKL-030 G7 — Portal OAT — 2026-09-04

| Campo | Valore |
|---|---|
| Identificativo | `BKL-030-G7-OAT-2026-09-04` |
| Capability | BKL-030 — EAGLE Health & Reliability Telemetry |
| Scope | G7 — Portal |
| PR | #89 |
| Pre-merge validated HEAD | `16ee056b336f1808ff73e1f7016017eef9625ae1` |
| Production deploy trigger | push to `main` |
| Safety Authority | **No** |
| Remediation | **None** |

## 1. OAT model

G7-E is split into two explicit stages because the authoritative GitHub Pages deployment workflow deploys only from `main` (or explicit workflow dispatch):

1. **Pre-merge static/contract OAT** — executable in PR and CI.
2. **Post-deploy hosted verification** — executable only after the G7 merge reaches the authoritative Pages deployment path.

This separation prevents claiming hosted evidence before the new portal code is actually published.

## 2. Pre-merge OAT evidence

On commit `16ee056b336f1808ff73e1f7016017eef9625ae1`:

```text
Genera manuale Word                 success
Validate documentation (no deploy)  success
Developer Foundation                success
```

G7-specific CI coverage includes:

- current public projection contract;
- removal of non-public process evidence;
- storage capacity / physical-health separation;
- bounded history projection;
- `MaxRecords` enforcement;
- exclusion of disallowed history signals;
- no destructive retention;
- current/stale browser rendering;
- malformed projection fail-closed;
- missing projection fail-closed;
- `POLICY_NOT_ACTIVATED` preservation;
- browser source check for ingest credential material.

## 3. Static fallback disposition

The repository contains a static fail-closed projection at:

```text
docs/data/realtime/eagle-health.json
```

Initial state is deliberately:

```text
quality = UNKNOWN
summary.state = UNKNOWN
summary.reason = POLICY_NOT_ACTIVATED
signals = {}
automatic_remediation = false
safety_authority = OUTSIDE_SCOPE
```

Therefore publication without a runtime export cannot accidentally display a healthy/current EAGLE state.

## 4. Hosted transport disposition

The existing Observatory Status hosted telemetry path remains separate from the new EAGLE Health static projection path. G7 does not add browser ingest credentials or command semantics.

Authoritative Pages workflow:

```text
.github/workflows/deploy-pages.yml
trigger: push -> main
```

The workflow builds MkDocs strictly, verifies published-site integrity, uploads the Pages artifact and deploys it through the `github-pages` environment.

## 5. Post-deploy hosted verification — REQUIRED

After merge and successful authoritative Pages deployment, verify the published Observatory Status page for all of the following:

1. `EAGLE Health` section is present.
2. Initial/public fallback renders `UNKNOWN / POLICY_NOT_ACTIVATED` when no current public export exists.
3. stale evidence never renders as current.
4. malformed/missing EAGLE projection does not break Observatory Status/weather/system panels.
5. storage capacity and physical-health evidence are displayed separately.
6. browser source contains no ingest token/credential.
7. no button, endpoint or text implies EAGLE remediation/control.
8. Safety wording remains observational and local interlocks retain authority.
9. history exposure, when enabled by later publication, is bounded and not a raw NDJSON download.

## 6. Acceptance matrix

| Criterion | Evidence | Status |
|---|---|---|
| Public current projection contract | G7-A/G7-B + CI | PASS |
| Public signal filtering | G7-B CI | PASS |
| `UNKNOWN/STALE` fail-closed | G7-D CI | PASS |
| `POLICY_NOT_ACTIVATED` preserved | G7-D CI | PASS |
| Capacity / physical health separated | projection + UI + CI | PASS |
| Bounded history | G7-C + CI | PASS |
| No browser credentials | G7-D source test | PASS |
| No remediation / Safety Authority | contracts + projection diagnostics | PASS |
| MkDocs/documentation | workflows green | PASS |
| Hosted published-page verification | requires merge/deploy | **PENDING** |
| Independent architecture/release review | required before merge/closure | **PENDING** |

## 7. Pre-merge disposition

**G7-E pre-merge OAT: PASS WITH POST-DEPLOY GATE.**

The package is eligible for independent architecture and release-quality review. It must not be declared fully accepted/closed until the authoritative Pages deployment succeeds and the hosted verification checklist is completed.
