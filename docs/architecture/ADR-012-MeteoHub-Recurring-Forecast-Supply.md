# ADR-012 — MeteoHub recurring forecast supply

| Field | Value |
|---|---|
| Status | **ACCEPTED — SUPERSEDED LIMIT / POST-MERGE VERIFIED** |
| Date | 2026-09-19 |
| Capability | BKL-031 F9 |
| Monetary budget | **EUR 0** |
| Cadence ceiling | **No workflow-imposed daily acquisition limit** |

## Context

F8 proved the planner for one governed night, while Open-Meteo Single Runs remained a one-shot evaluation interface. The Repository Owner has authorized a no-fee recurring operating model using the official ItaliaMeteo MeteoHub open-data publication.

## Decision

F9 consumes ItaliaMeteo/ARPAE ICON-2I directly from MeteoHub under CC BY 4.0. The model authority remains ItaliaMeteo/ARPAE; only the delivery interface changes from the bounded Open-Meteo evidence path to the official GRIB publication.

The operating contract is:

- monetary budget EUR 0;
- the repository is public and the refresh job additionally requires repository variable `F9_ZERO_EUR_GUARD=CONFIRMED` as an explicit activation switch;
- no workflow-imposed daily acquisition limit; the two cron entries remain aligned with the 00/12 UTC ICON-2I runs, while authorized manual dispatches are not blocked by a daily counter;
- a governed `workflow_dispatch` diagnostic path requires explicit `ALLOW_ONE_TEST_ACQUISITION` confirmation and a purpose string; scheduled and manual attempts do not share a daily acquisition counter; no automatic retry;
- exact run identity, per-variable SHA-256 and retrieval time in the sanitised projection;
- all GRIB inputs held only in an ephemeral temporary directory and deleted before the job ends;
- no GRIB artifact, cache, repository commit or durable raw payload;
- exact site/grid coordinates excluded from logs and public projection;
- missing, late, incomplete, inconsistent or stale data fail closed;
- no automatic fallback, provider/model stitching or silent substitution.

The GitHub workflow may publish only the small read-only JSON projection. This decision supersedes the prior daily acquisition cap; it does not authorize automatic retries, additional cron entries, paid runners, raw GRIB retention, or any operational authority. The repository is public, so standard GitHub-hosted runner execution is free; the explicit repository variable remains a defense-in-depth activation switch. EAGLE is not involved.

## Authority boundaries

The output is `EVALUATION / NONE / READ_ONLY`. It has no readiness, go/no-go, scheduling, automatic-target-selection, action, command or Safety Authority. BKL-032 retains Session Readiness / Go-No-Go; local physical interlocks remain Safety Authority.

## Consequences

The provider subscription cost is eliminated, and the public-repository standard runner boundary avoids runner charges. F9 still assumes operational parsing of official GRIB data and availability of MeteoHub. Provider failure never revives stale F7/F8 data as current. Attribution to ItaliaMeteo/ARPAE and the CC BY 4.0 source must remain visible.

ADR-011 remains the historical authority for the accepted Open-Meteo single-run evidence. ADR-012 governs only the F9 recurring supply and does not rewrite that evidence.


## Closure evidence

The prior daily acquisition cap is retired by owner decision recorded in DLG-065; the remaining EUR 0, ephemeral-retention, privacy and authority boundaries are unchanged.

BKL-031 closure is recorded in `docs/project/BKL-031-CLOSURE-2026-09-18.md`. PR #301 merged at `4a509d574a004fe7fb72bc6c678c9e7f71fe821f`; governed workflows, documentation validation, Word generation, GitHub Pages deployment and direct public planner verification succeeded. The capability remains `EVALUATION / NONE / READ_ONLY`; S10 remains `UNAVAILABLE`.

## Rollback

Disable the scheduled workflow and revert the F9 consumer. The portal then fails closed; no provider fallback is enabled and the accepted F8 bounded evidence remains historical only.
