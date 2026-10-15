# Private campaign input archive

This local adapter retains the exact bytes supporting a three-frame campaign
input witness. It does not send a request, start PixInsight, create a job or
authenticate an Owner. It preserves the existing campaign input contract.

The private source JSON has exactly `protocol`, `witness` and `files`.
`protocol` is `DSG_CAMPAIGN_INPUT_SOURCE_V1`; `witness` contains `witnessRef`,
`purpose`, `correlationRef` and the three existing campaign frame records.
Each file record contains `role`, `frameRef`, `path`, `sha256`, `bytes`.
Paths are relative to an existing private source directory. Every frame needs
IMAGE, METADATA and BANDPASS records whose hashes match its witness fields.
Reported complete calibration, uncertainty or time states additionally require
CALIBRATION_PROOF, UNCERTAINTY_PROOF or TIME_PROOF files respectively.

Proof presence and byte integrity do **not** attest the contents. This adapter
does not parse image formats, validate calibration, establish UTC, determine
null truth or prove independence. Arbitrary synthetic bytes used in its tests
are not valid astronomical images. Unknown scientific states remain unknown.
Owner review and all scientific acceptance gates remain separate.

Run from the repository root with private paths and a previously recorded
SHA-256 of the exact source JSON:

```text
python -m tools.scientific_transients.campaign_input_archive prepare --source-root SOURCE --manifest MANIFEST --sha256 SOURCE_SHA256 --archive-root ARCHIVE
python -m tools.scientific_transients.campaign_input_archive export --directory ARCHIVE/WITNESS_REF --sha256 ARCHIVE_SHA256 --output NEW_PRIVATE_OUTPUT
```

Both roots must already exist and must not overlap. Preparation creates a new
witness directory exclusively, retains the original manifest and copies all
referenced files without conversion. The printed hash pins `archive.json`;
retain that hash outside the archive. Export rechecks the pinned index,
manifest and every retained file before writing a new minimized witness JSON.
Its `reportSha256` identifies the actual private source manifest. Original
paths and proof bytes stay private; export alone never transmits anything.

Failures preserve partial files and an opaque failure receipt. Existing
witness directories and output files cannot be overwritten. There is no
implicit resume, retry, deletion or cleanup. Operators must keep source and
archive directories quiescent while preparing or verifying. These checks do
not protect against a privileged actor rewriting both artifacts and their
externally retained hash. Shared metadata or bandpass bytes do not establish
independent exposures or independent scientific controls.

Every inspection reports `NOT_VALIDATED`, zero qualified controls and no
execution authorization. This increment addresses byte provenance only;
it does not complete R02, R09, the full uncertainty model or the milestone.
