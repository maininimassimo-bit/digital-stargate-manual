# Local PixInsight pilot — P1 and P2

> Stato corrente al 6 ottobre 2026: [dossier P6 rilasciato](../../../docs/project/PIAI-P6-CANDIDATE-2026-10-06.md). Le sezioni precedenti conservano gli snapshot e i limiti delle prove; le note di candidato o consegna pendente sono superate soltanto nei perimetri del riepilogo corrente.

Trusted PJSR library for an explicit `PREFLIGHT_ONLY` manifest. It opens selected
XISF containers, checks SHA-256 before/after reading, selects an explicit image
index, checks expected monochrome dimensions and instantiates the fixed native
process list without executing any process. Four roles in R/G/B/L order are
required. Master windows remain open for inspection; no save or close occurs.

Manifest fields: `schemaVersion: "1.0"`, safe `jobId`, mode, and four inputs with
`role`, private absolute `path`, `sha256`, `imageIndex`, `width`, `height`.
The local wrapper includes `preflight.jsh`, calls `DSGPilotPreflight(manifest)`
and writes its private receipt to a previously selected local destination.
Never include an imported History export as a library or executable script.

Module constructors demonstrate availability, not plugin model/license readiness
or version compatibility; process-instance module versions are explicitly unknown.
Reading a multi-image container can leave its auxiliary masks open too.

Synthetic boundary verification: `node --test tools/pixinsight/local_pilot/preflight.test.mjs`.
These tests stub native objects; the real PixInsight test is reported separately.
Plan: `docs/architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md`.

## P2: controlled local execution

`worker.py` prepares and collects one job in one configured worker root;
`executor.jsh` executes the fixed `LRGB_LINEAR_PREP_V1` recipe in PixInsight.
The supported native platform is Windows with the exclusive PJSR File handle
verified before processing. Linux CI exercises synthetic boundaries only.
Python 3.12+ is required. Run the coordinator from the repository root.

The request has exactly `schemaVersion: "1.0"`, a new safe `jobId`, the recipe,
four R/G/B/L inputs as above, and `background` with bounded `polyDegree`,
`boxSize`, `boxSeparation`. Select parameters after inspecting the data; there
is no universal M27 or LRGB preset. Source and worker directories must be
separate. Keep requests, hashes, images, runtime parameters and receipts private.

1. Create an empty dedicated worker root and validate the selected masters with
   P1. Keep this PixInsight instance dedicated to the job while it runs.
2. Prepare: `python -m tools.pixinsight.local_pilot.worker prepare --root <private-root> --request <private-request.json>`.
   This reserves the root, copies and hashes inputs, and snapshots the trusted
   executor into the new job. It never starts PixInsight or executes uploaded JS.
3. In PixInsight use **Script → Execute Script File** to run that job's `run.js`.
   This owner-supervised launch is the P2 procedure; remote dispatch is future work.
4. To request cancellation use `python -m tools.pixinsight.local_pilot.worker cancel --root <private-root> --job <job-id>`.
   The coordinator reads the immutable job-scoped `reservation.json`, not the
   exclusively leased file. It validates manifest/scope/identity and publishes
   complete token-bound JSON atomically with a create-only hard link. The native
   executor checks that identity before accepting the marker. The local worker
   filesystem must support hard links; failure preserves evidence and sends no
   cancellation. The marker is checked before each process and save. It does not guarantee
   immediate interruption of a native process already running.
5. After the native run stops, collect:
   `python -m tools.pixinsight.local_pilot.worker collect --root <private-root> --job <job-id>`.
   Collection checks original/copy/runtime/output hashes, bounded XISF headers,
   terminal state and successful process journal; only then releases the root.

The recipe clones the four selected master images, applies native background
subtraction to each clone and creates an RGB from prepared R/G/B. It saves
four monochrome Float32 checkpoints and one RGB Float32 checkpoint, all linear.
The L checkpoint is prepared but not integrated into RGB yet. RGB astrometry,
colour calibration, detail recovery, denoising, stretch and visual validation
belong to P3. Header/integrity checks do not certify finite pixels, clipping,
colour accuracy, alignment or scientific quality. All opened scratch images and
auxiliary masks remain available for inspection; source files are never targets.

## Evidence and recovery

Each job retains `manifest.json`, executor snapshot, immutable numbered events,
`reservation.json`, `terminal.json`, checkpoints, `verification.json` and
`reservation-closed.json`.
The native exclusive lease lasts through processing and terminal writing. A
second preparation in the configured root and replay of a claimed job are
refused. This is a per-root guard, not a global multi-worker coordinator.

`workflow.js` contains only successful native process instances from this run,
as a ProcessContainer data export accepted by the bounded importer 1.2.
Identifier tokens are renamed to avoid duplicate native `P` variables; literal
values and the exact original sources in the private journal are preserved.
`runtime-correlations.json` retains runtime targets/dependencies separately.
Neither file is a complete upstream project History or guaranteed executable
replay. Import the export as data only, never through PixInsight's script runner.

`FAILED` and `CANCELLED` retain partial evidence and outputs. A crash or failed
preparation retains the reservation and blocks new jobs. There is no automatic
retry, resume, expiry or force-unlock command. After confirming PixInsight is
stopped and preserving the entire job, an operator can quarantine the failed
worker root and use a new dedicated root; never release a live lease or overwrite
an old job. Collection is idempotent for unchanged evidence. Local administrator
control is the trust boundary; receipts are not signed remote attestations.

No provider API, remote queue, portal command, automatic upload, publication or
observatory control is included. The existing published M27 remains unchanged.

Synthetic verification:

```text
node --test tools/pixinsight/local_pilot/preflight.test.mjs tools/pixinsight/local_pilot/executor.test.mjs
python -m unittest tools.pixinsight.local_pilot.test_worker tools.pixinsight.local_pilot.test_quality
```

Native receipts are reported separately; stub tests do not establish native
platform compatibility or scientific acceptance.
One coordinator test uses an actual Windows sharing-mode handle and is skipped
on Linux. It proves cancellation does not read the leased file; the separate
native PixInsight test proves the command during a real process.

## P3 — supervised M27 nonlinear recipe

Use the same strict request envelope with recipe `M27_LRGB_NONLINEAR_V1`.
The fixed empirical preset is for these aligned M27 masters, not a universal
LRGB recipe. Background fields retain P2 bounds; all subsequent native settings
are reviewed code defaults, not arbitrary request parameters. Inputs must have
at least 1000×800 pixels. No uploaded code, provider API or unattended dispatcher
is introduced. The user must not work on the same instance during a job.

All required constructors are checked before pixel processing. Successful actual
plugin execution demonstrates readiness on that PC for that run; it does not
attest a particular model/version/license or commercial rights. BlurXTerminator
is applied while data remain linear. The pipeline includes background correction,
stellar ColorCalibration (not SPCC), denoising, native star separation, separate
MaskedStretch, masked luminance contrast, LRGB transfer, selective saturation,
independent stars stretch and screen recombination. The background ROI is an
M27-specific relative rectangle; other fields require another reviewed recipe.

A complete run requires 29 recorded native actions and 15 Float32 XISF
checkpoints. `LRGB-nonlinear.xisf` is the final result. Metadata generated by
native ChannelCombination is retained, including its inherited astrometry;
conflicting per-filter acquisition metadata is not silently copied from Red.
Native sources alone omit masks and extra outputs. The separate runtime
correlations therefore record clone, stars-output and mask attachment/removal
relations plus the five masked actions. The derived workflow contains successful
native instances as data; it is not an executable replay or complete upstream
History. The current imported gallery workflow retains its original classification.

Collection checks all hashes, dimensions, channels, processing-domain labels,
recipe order, masks and native process types. It streams every final Float32
sample, rejecting NaN/infinity, values outside [0,1], constant channels, invalid
attachments, truncated pixels, compression and unsupported layout/byte order.
Compression must be disabled for this pilot's XISF output. Unsupported output
retains the reservation and requires documented recovery; it is not auto-converted.
Counts of zero/saturated samples and per-channel ranges/means are measurements,
not claims of no clipping or calibrated colour. A successful execution receipt
alone cannot bypass collection. Visual comparison and Owner evaluation remain
necessary, and scientific acceptance is `OWNER_REVIEW_REQUIRED`.

Intermediate views remain available; originals and the published M27 are protected.
This phase supplies a local nonlinear result for review. Remote job transport,
paid provider integration and portal linkage/acceptance belong to P4–P6.

## P4: authenticated outbound transport candidate

`broker.py`, `transport_http.py` and `transport.py` implement a bounded queue and one-shot supervised PC adapter. SESSION_ASSISTED, no paid AI API or automatic native launch. See [procedure and approved activation](../../../infrastructure/pixinsight-pilot/README.md). Owner-approved cloud/credential active; partial HTTP/IAM/restore OAT passed. Owner Google login/native end-to-end OAT remain gated. The P2/P3 executor is unchanged. The separate Owner diagnostic page cannot request a scientific run.

`python -m unittest tools.pixinsight.local_pilot.test_transport`


## P5b: private folder/prompt intake and Owner-reviewed plan

`intake.py` separates private planning requests from native jobs. `intake_assistant.py` performs an explicit session-assisted local inspection/proposal using the existing outbound worker identity. Paths and prompt are private Owner data; no folder upload, arbitrary script execution, background assistant or provider call. Ambiguous roles/multi-image containers require an explicit local filename/imageIndex map. Owner confirms the immutable proposal hash before creating the context-bound queue job. See the [P5/P5b procedure](../../../docs/project/PIAI-P5-PORTAL-2026-10-05.md).

The candidate accepts other known imported targets. Single-field trusted recipes cover LRGB, OSC RGB, SHO and HOO, requiring explicit reviewed field/background/mask/stretch parameters. Their action/checkpoint counts are respectively 29/15, 26/12, 27/15 and 26/14. OSC uses derived RGB luminance; SHO/HOO use Ha-derived luminance and assigned palettes, without claiming photometric calibration. These new profiles still require native validation. Legacy M27 manifests preserve their exact defaults and input digest. New processing and field settings are included in the registered input digest and immutable native manifest, checked by Python and the executor before pixel operations. Actual native sources journal applied parameters; the prompt alone is not proof of execution.

`source_profile.py` provides bounded header inventory and explicit source selection for LRGB, OSC, CFA, SHO/HOO and 2–16 mosaic panels, including multiple panels/filter groups in one folder. Normalization references, drizzle candidates, calibration files and auxiliary container images are distinguished rather than silently chosen. CFA requires a declared Bayer pattern. Mosaic/CFA execution requires a separate immutable preparation proposal and exact Owner approval before local supervised preparation; a verified prepared result is required before the nonlinear processing proposal. Planning/inventory alone cannot authorize native execution. This preparation/source-selection increment was released with P5b; profile-specific operational acceptance remains open. See the [current scope and remaining validation](../../../docs/project/PIAI-P5B-SOURCE-PROFILES-2026-10-05.md).

Assistant actions are explicit one-shot `list`, `inventory`, `inspect`, `propose-sources`, `propose-preparation`, `prepare-sources`, `collect-sources`, `propose` commands. `propose-sources` validates exact mosaic filenames/image indices against the immutable intake folder/session scope, inspects local headers/hashes, and saves an immutable private source-selection proposal. Owner confirmation of its exact digest authorizes inspection of that selection; it does not create a job or native execution authority. `propose-preparation` binds the reviewed canvas/merge settings or Bayer pattern to a path-free digest of exact selected sources. Owner confirmation of the preparation proposal permits `prepare-sources` to create verified copies and a supervised native launcher, without queueing final processing. `collect-sources` checks originals, copies, all output pixels and native instances before closing the local lease and recording an immutable Worker-reported linear result. `propose` registers these exact prepared outputs with a provenance trace; a separate Owner confirmation creates the final processing queue job. The original intake remains unchanged. Credentials use the existing private worker identity and are never stored in output artifacts. The processing proposal command reserves the private configuration, writes a recoverable backup and atomically registers the exact new input manifest. No CLI command launches PixInsight. Configuration remains bounded at 64 KiB and eight registered groups.

`source_preparation.jsh` is a candidate kernel requiring a caller-held native lease, scoped checkpoint saves, explicit astrometric canvas and previously verified selected copies. It reprojects solved panels with the installed official PJSR ImageReprojection and merges them with GradientMergeMosaic; native Float64 results are converted explicitly to Float32 with a journal relation. Its Debayer helper requires an explicit pattern. `preparation_bridge.py` admits only closed, verified, Owner-approved prepared masters inside the local worker root; ordinary internal sources remain rejected. Preparation instances precede recipe instances in the combined workflow; correlations include original role/panel references, astrometric reprojections, metadata transfer, conversion and prepared-master edges. Exported mosaic frame paths become explicit logical resource names; exact native source remains in the local journal. Header inventory, synthetic tests and a local administrative OAT cannot establish portal end-to-end or scientific acceptance.

`python -m unittest tools.pixinsight.local_pilot.test_intake` exercises synthetic states and actual loopback HTTP with synthetic identities, not a native/Owner OAT.
# Local common preparation candidate

The [P6 refinement/recovery candidate](../../../docs/project/PIAI-P6-CANDIDATE-2026-10-06.md)
adds immutable private versions beside completed deliveries, with separate exact-digest
Owner review and no native dispatch/publication. `revision_delivery` reads a selected
local bundle and verifies RGB Float32 pixels before an explicit outbound submission.
It requires a confirmed nonlinear declaration; pixel range alone is not proof of
processing domain. The refinement/recovery increment was deployed in PR #491; operational P6 acceptance remains open.

Explicit native-stop confirmation after runtime events without a terminal receipt
retains reservations and reports `RECOVERY_REQUIRED`; it cannot restart execution or
release another job. An offline diagnostic alone never establishes native stop.

`preparation.prepare(root, request)` creates an immutable private request, verified input copies, runtime snapshots and a supervised launcher. It does not start PixInsight or create an Owner portal job. `DSGExecuteMasterPreparation` preflights every selected image before Debayer/reprojection/merge and saves linear checkpoints. `preparation.collect(root, job_id)` independently verifies source/copy/output hashes, headers, every mono/RGB pixel, process sequence and source dependencies before closing the matching native reservation.

This contract currently accepts only completed local preparation jobs. Failed/cancelled jobs retain their reservation for separate integrity recovery. Native instance source is parsed as data and parameters are bound to the approved preparation envelope. The candidate bridge separately checks exact Owner intake/approval, runtime, original/copy/checkpoint hashes and journal before nonlinear preparation. The source-selection approval in the portal is separate and cannot authorize local execution by itself. Headers containing master History are bounded at 4 MiB. Release validation is recorded in the current baseline. Private M31 refinement delivery/review is verified; it does not attest the complete new preparation chain for every profile. Local tests alone do not imply a service change.
