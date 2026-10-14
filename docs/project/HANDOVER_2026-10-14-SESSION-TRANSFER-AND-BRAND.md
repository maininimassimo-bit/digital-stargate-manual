# Session transfer evidence and shared logo — 14 October 2026

Owner clarifies that the session-detail Transfer node refers to EAGLE's morning document/telemetry package committed with `manifest.json`, triggering the GitHub session-analysis bot. It does not represent the separate photographic RAW storage transfer.

## Dynamic transfer projection

`generate-session-package-transfer.mjs` derives a public read model at every authoritative Pages build from catalog session IDs and canonical session manifests. Each complete matching manifest is checked against actual repository file sizes and streaming SHA-256. Exact session identity, bounded inventory, duplicate/traversal rejection and repository containment apply. Missing/invalid/incomplete input cannot yield VERIFIED. Projection contains only scope, session ID, state, public manifest reference and counts; no local paths, credentials or new scientific authority.

The generated JSON is a build artifact, deliberately ignored by Git; source manifests remain canonical. Existing manifest-triggered bot publication automatically runs the Pages generator. The detail independently reads this same-origin projection and the public gallery with no-store/bounded time and size. It refreshes both at initialization, visibility return, every visible minute and manually. Clearing before reads prevents stale positive claims; failures of either source remain distinct. A matching public manifest link is supplied. No EAGLE task or private runtime was modified.

Session `2026-09-19_2026-09-20`: six of six manifest files independently matched size and SHA locally. This establishes repository package integrity, not continuous telemetry, sender authentication, physical transfer timing or photographic RAW movement. Of23 catalog sessions,16 packages currently verify; the remaining states are preserved without invented success.

## Logo

Owner's transparent PNG copied byte-for-byte to the shared theme brand asset, SHA256 `15c42df78d0dad73350005c6a2022f4a50174cca5526c95eb9c71fe73a51e52a`. Header/fallback/favicon reference that asset. CSS contain sizing and intrinsic width/height preserve proportions and reduce layout shift. No generative modification or pixel alteration was made.

## Validation and release

Nine transfer/reader regressions plus14 publication/routing regressions passed locally; strict Pages build and no-inline-script gate passed. Local browser: verified6/6 -> synthetic incomplete3/6 -> restored6/6; gallery unavailability remains independent. Mobile390px shows the unchanged logo at36px with no horizontal overflow; desktop logo uses contain sizing, light/dark checked. Final exact-head CI, separate ARB then RQ and merge/deployment/live checks remain required and will be recorded in the delivery PR. Rollback: revert UI/build-generator/brand configuration and redeploy; canonical packages, scheduler, private gallery and device/safety authority remain untouched. BKL statuses and M27 scientific acceptance remain unchanged.
