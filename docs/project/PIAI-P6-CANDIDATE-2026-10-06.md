# P6 candidate — private refinements and conservative native recovery

Status: candidate, not released. BKL-049 remains closed in its accepted archive scope;
BKL-049-EXT-PIAI and its operational acceptance remain open. No scientific image,
workflow parameters, local paths, credentials or production receipts are included here.

The Owner approved the final local M31 image in chat and requested completion of the
extension and tests. This records approval of that local image; it does not fabricate
a portal decision, publication, catalog/session association or acceptance of every
processing profile. The Owner will specify the master directory for each future
processing request. No fixed directory is inferred from that clarification.

## Private refinements

The first scientific delivery remains immutable. A refinement has a separate opaque
revision ID, original descriptor, preview, incremental native workflow, correlations
and immutable receipt bound to the first delivery's exact review digest. The image
identity and scientific context remain the parent's; version/workflow identities
change. The original stays on the Owner PC. The service imports workflow source as
data, never executes it, never queues a refinement and never publishes it.

Only the authenticated outbound worker can submit a refinement. Only authenticated
Owner routes can read the version and record an exact-digest decision. A refinement
cannot overwrite the parent's acceptance or result. The classifications remain
`WORKER_REPORTED_NOT_ATTESTED`, `INCREMENTAL_REFINEMENT_ONLY` and upstream History
`NOT_ESTABLISHED`. The workflow is not a complete replay of all original masters,
branches, masks or past processing. Local native journals retain that additional
evidence. The empirical Hα estimate from dual-band RGB is not pure or photometric Hα.

At most sixteen refinements per job are indexed in the existing authorized mutable
control object. Assets, receipts and decisions are immutable. An interrupted or
conflicting index commit cannot make an unindexed receipt reviewable; an identical
retry can complete the same delivery. No new IAM permission or cloud resource is
required. The old result and its downloads remain accessible beside refinements.

The explicit `revision_delivery` CLI requires a selected bundle, a nonlinear
declaration, full pixel inspection and locally supplied preview/workflow/correlations.
It performs no native launch, acceptance or publication. Preview encoding for M31
was performed natively, separately from the approved original.

## Native interruption

An explicit `native_stopped` confirmation plus runtime events without a terminal
receipt now reports `RECOVERY_REQUIRED`. It retains the native reservation and
transport binding, blocks other queued jobs and cannot relaunch processing.
Before any runtime event, the same confirmation retains `AWAITING_NATIVE`.
Offline status alone does not imply stopped processing and cannot trigger recovery
or reassignment. Collection still requires a valid native terminal receipt.

The native launcher uses explicit CRLF line endings. In the installed Windows
PixInsight 1.9.5, LF-only engine directives consumed following source and failed
before execution; CRLF launchers ran successfully. Both preparation launchers now
use the same explicit encoding.

The local operational exercise used native synthetic monochrome fixtures, an
isolated PixInsight instance and an actual authenticated loopback HTTP adapter. The
test terminated only its own instance after a process-start event, before a terminal
receipt. Result: `RECOVERY_REQUIRED`, same claim after reconstructing the coordinator
from its on-disk state in the same Python process, second job still
queued, reservations retained, fourteen job files unchanged on restart, original
fixtures/copies unchanged, no automatic native restart. Existing Owner instances
and the approved M31 were not terminated or modified. This is controlled native
process termination with synthetic data, not an OS worker-process restart,
power-loss/desktop crash or a cloud
end-to-end recovery test. See the [minimized candidate evidence](evidence/BKL-049-PIAI-P6-CANDIDATE-2026-10-06.json).

## Remaining gates

The candidate requires exact-head CI, separate sequential ARB and RQ reviews,
merge, API/Pages deployment and authenticated private refinement delivery/review.
No deployment or receipt for the approved M31 refinement is claimed yet.

P6 must reconcile the existing real cancellation, offline, CAS and service restart
evidence with concurrency, cloud recovery/rollback and explicit operational Owner
acceptance. Controlled native termination above is bounded evidence, not blanket P6
acceptance. Real SII/Hα/OIII and OSC CFA masters have not been selected for those
profile tests; RGB Extreme panels cannot replace them. Profile acceptance cannot be
inferred from synthetic tests or M31 approval.

Rollback of this candidate means reverting code through the governed release flow,
retaining immutable private receipts/assets and the current queue state. Do not
restore old state over current decisions, change M27 publication, clear an ambiguous
native reservation, expand IAM or revoke credentials merely to exercise a test.
Actual rollback OAT remains separate from this documented procedure.

The single C-to-F root compatibility junction remains pending the Owner's explicit
confirmation that PixInsight has been closed. Per-folder compatibility and the
verified approved delivery on F are retained in the meantime.
