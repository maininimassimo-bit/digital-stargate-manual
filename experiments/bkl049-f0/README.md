# BKL-049 F0 isolated contract probes

Run from the repository root with `node experiments/bkl049-f0/contract-probes.mjs`.
Node built-ins only; no installation, network, PixInsight, images, external writes or production imports of this experiment. Output goes to standard output. The committed result is reproduced by the same command; callers may redirect it to a research file.

These assertions reproduce existing contract boundaries and counterexamples. `REPRODUCED` means a stated behavior was confirmed, including gaps; it does **not** mean native capture, privacy, full JSON Schema validity, gallery integration or F0 acceptance passed. Synthetic OBSERVED labels exercise validation and do not constitute evidence of actual processing. No SDK code is copied or used here.

C04 checks the schema step ceiling and JavaScript validators, not a complete JSON Schema engine. C07 checks one explicit schema constraint. C06 and C09 exercise direct consumer calls: they do not demonstrate that an existing production route allows untrusted data to reach those calls. Future design must establish upstream invariants or reject these cases explicitly. No production fix is included in F0.

See the [research addendum](../../docs/architecture/assessments/BKL-049-F0-Evidence-Addendum.md) for implications and outstanding proof gates.

Probed DSG baseline: `dddb95748f2741b1bcbf8a550cd4ba0d7e9b0880`. Re-run assertions against later revisions; a failing assertion can indicate a corrected boundary and requires reassessment, not automatic restoration of old behavior.

## Asset binding follow-up

Run `node experiments/bkl049-f0/asset-binding-probes.mjs` for six direct reconciliation observations with synthetic identifiers. These use minimal internal inputs, not a fully validated manifest. A reproduced gap is not product acceptance. See the [archive linkage experiment](../../docs/architecture/assessments/BKL-049-F0-Archive-Linkage-Experiment.md). No scientific image, private exported source or SDK code is included.

## Nonexecuting JavaScript export subset reader

Run `python experiments/bkl049-f0/test_read_export_subset.py` for 27 synthetic tests. `python experiments/bkl049-f0/read_export_subset.py <local-export-file>` reads the bounded subset and emits an aggregate summary only. No JS/PixInsight execution, SDK or dependency installation. The in-memory result contains private values; do not publish it by default. See [reader boundaries and observations](../../docs/architecture/assessments/BKL-049-F0-Nonexecuting-Export-Reader.md).

## Fixed synthetic export-to-consumer path

Run `node experiments/bkl049-f0/synthetic-pipeline-probes.mjs` (requires existing Python on PATH). Nine assertions exercise reader -> candidate DECLARED sidecar -> existing validators/mapper/ledger/reconciliation/projection/read model. The Python builder accepts no arbitrary file input and reads only the fixed synthetic fixture. No real export ingestion, full JSON Schema validation, production adapter or native observation is claimed. See the [pipeline report](../../docs/architecture/assessments/BKL-049-F0-Synthetic-Pipeline-Experiment.md).
