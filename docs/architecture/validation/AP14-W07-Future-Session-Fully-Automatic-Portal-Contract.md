# AP-014 Future Session Fully Automatic Portal Contract

| Campo | Valore |
|---|---|
| Documento | AP14-W07 Future Session Fully Automatic Portal Contract |
| Identificativo | AP14-W07-AUTO-002 |
| Versione | 1.0 |
| Data | 2026-08-13 |
| Stato | Implemented; EAGLE deployment/OAT pending |
| Owner | Digital StarGate Architecture Office |

## Requirement

Every new observing session produced now or in the future must enter the AP-014 portal without manual catalog edits or manual GitHub promotion when complete scientific evidence is available.

## Permanent flow

```text
EAGLE scheduled task
  -> Invoke-DSGAutomaticSession.ps1
  -> sync clean main by fast-forward only
  -> Import-DSGSession staging
  -> NO_SESSION: no-op
  -> PARTIAL: deferred, no repository publication
  -> COMPLETE: CopyToRepository
  -> Publish-DSGSession -CreateBranch -Push
  -> session/<session-id>
  -> promote-session-package.yml
  -> manifest/hash/scope/fast-forward validation
  -> main
  -> analyze-session-automatic.yml
  -> normalized session analytics
  -> sessions.csv
  -> target-exposures.csv
  -> targets.csv
  -> scientific-session-catalog.json
  -> scientific-observation-index.json
  -> deploy-pages.yml
  -> GitHub Pages
```

## EAGLE producer

The authoritative launcher is versioned in `maininimassimo-bit/DigitalStarGate.Reporting` as `Invoke-DSGAutomaticSession.ps1`. The scheduled-task installer is `Install-DSGAutomaticSessionTask.ps1`.

The launcher intentionally performs discovery in staging before repository publication. `PARTIAL` and `NO_SESSION` therefore do not dirty the authoritative repository. Only `COMPLETE` sessions are eligible for publication.

The historic Scheduled Task name remains:

`Digital StarGate - Daily Session Upload`

Deployment on the physical EAGLE remains an operational action and must be evidenced before AP14-W07 acceptance.

## Portal projection consumers

The web pages do not require per-session source edits. They consume versioned projections dynamically:

- `docs/scientific-session-catalog/index.md` -> `docs/data/scientific-session-catalog.json`;
- `docs/scientific-session-detail/index.md` -> `docs/data/scientific-session-catalog.json`;
- `docs/mission-control/index.md` -> `docs/data/scientific-session-catalog.json`;
- AP-014 enterprise search -> `docs/data/scientific-observation-index.json` through the governed search service.

Therefore a new valid session updates all correlated portal views by regenerating the shared projections and redeploying Pages; individual Markdown pages are not rewritten for each observing night.

## No manual catalog rule

The following are prohibited as normal operations:

- manually inserting a session into `scientific-session-catalog.json`;
- manually inserting an observation into `scientific-observation-index.json`;
- editing web pages to add a newly observed target/session;
- deriving AP-014 quality metrics directly from XISF filenames or AP-013B transfer plans;
- pushing a session directly from EAGLE to `main`;
- promoting `PARTIAL` evidence.

Manual workflow dispatch is reserved for governed replay/recovery, not normal session ingestion.

## Idempotency and recovery

- an already-published session branch is treated as already published rather than overwritten;
- GitHub promotion accepts only a session branch based on current `main` and only by fast-forward;
- analytics/history and catalog generators remain deterministic/idempotent;
- if `main` advances before promotion, the branch is rejected and requires controlled replay from a synchronized EAGLE baseline;
- if analytics fails, the package remains versioned and can be replayed by explicit workflow dispatch after remediation;
- Pages is explicitly dispatched after analytics/catalog processing so publication does not depend on secondary push-trigger behavior from `github-actions[bot]`.

## Acceptance

M 27 is the first designated end-to-end OAT for this permanent automation. Acceptance requires proof that the real EAGLE Scheduled Task/launcher produces the session branch and that the complete GitHub chain updates the shared projections and all correlated portal views without manual catalog/page edits.

After M 27 acceptance, the same path is the production path for all future sessions. Subsequent sessions are operational evidence of continuity, not new architecture changes unless the contract changes.
