# PixInsight portal importer 1.2 — 2026-10-02

Owner-requested technical maintenance following the complete available-history export. BKL-049 remains accepted for available history; no scientific completeness or execution evidence is inferred.

## Compatibility and bounds

New imports use importer **1.2**, permitting decoded strings through **131,072 characters**, including concatenation. Packet schema remains 1.0. Only this bound changes: 2 MiB source, 200,000 tokens, 512 instances, depth 32, 2,048 parameters per instance, 4,096 array items and all identifier, mask and packet bounds remain enforced. Parsing never executes JavaScript. Oversized or unsupported source is preserved privately without silent truncation.

Historical packets are reverified under their recorded profile: 1.0 retains 4,096 and 1.1 retains 16,384 characters. Existing unsupported results are immutable. A deliberate new import or Owner-requested recheck produces a new review; upgrading does not silently rewrite old reviews.

The service's `/health` response adds `workflowImporterVersion` for deployment verification. Review still lists each process while omitting parameters over the existing 4,096-byte presentation bound, reporting `unlistedParameterCount`. The complete value remains in the private source/archive. Publication still requires explicit field selection and Owner rights confirmation; no long parameter is automatically made public.

## Evidence and release

A local read-only verification of the Owner-provided project export found 49 process instances across 13 image histories. The 70,514-character spectral parameter parsed intact; packet round-trip verification and original-byte preservation passed. No real source, paths, parameters, image or private receipt is committed or uploaded by this release.

Synthetic regression covers legacy immutable profiles, string and concatenation boundaries, surrogate rejection, unchanged array and execution restrictions, and the upload/review pipeline with a 72,000-character parameter. HTTP browser regression verifies importer 1.2 and the existing Owner/origin, private-save, explicit-publication, withdrawal and resume boundaries. CI path filters include workflow archive changes so future importer changes trigger the runtime regression.

Release requires exact-head CI, separate ARB then Release Quality review, expected-head merge and post-merge validation under W-DSG-AEM-RULESET-001. Build the existing Cloud Run service from an allowlisted committed merge SHA with synthetic tests only, deploy by immutable digest, preserve environment/IAM/resources, and verify readiness and `/health` version 1.2. Deployment evidence belongs in the PR and private operator receipt; this document alone does not assert deployment success.

Rollback updates only the service image to its prior pinned digest/revision and preserves private originals, reviews and publication state. A rolled-back 1.1 runtime cannot verify newly created 1.2 packets; preserve them and restore the compatible reader before reviewing them. Do not reinterpret them as 1.1 or delete them. The existing activation authorization and manual real-file acceptance boundary remain in [the runtime activation record](../../project/SCIENTIFIC-PHOTO-RUNTIME-ACTIVATION-2026-10-02.md).
