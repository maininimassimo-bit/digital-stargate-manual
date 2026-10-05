# Local PixInsight pilot — P1 and P2

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
python -m unittest tools.pixinsight.local_pilot.test_worker
```

Native receipts are reported separately; stub tests do not establish native
platform compatibility or scientific acceptance.
One coordinator test uses an actual Windows sharing-mode handle and is skipped
on Linux. It proves cancellation does not read the leased file; the separate
native PixInsight test proves the command during a real process.
