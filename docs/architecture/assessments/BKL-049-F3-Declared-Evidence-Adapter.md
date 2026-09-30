# BKL-049 F3 — Declared evidence and PXP adapter

| Field | Value |
|---|---|
| Identifier | DSG-BKL049-F3-ADAPTER-001 |
| Version / date | 1.0 / 2026-09-30 |
| Status | ACCEPTED / POST-MERGE VERIFIED via PR #451; synthetic compatibility evidence only |
| Entry gate | F2 accepted via PR #450, merge `b57adb0e8ee8d43b5bf7d5e05a718341520128ab`, 19/19 post-merge SUCCESS and Pages verified |
| Authority | Processing evidence only; action NONE |

Delivery: [PR #451 post-merge evidence](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/451#issuecomment-5918603605), merge `f689bea2d0b0aba11774c589d47669486bf61978`, 19/19 post-merge runs SUCCESS and Pages verified.

## Scope and API

`tools/pixinsight/workflow_archive/provenance.py` provides `build_sidecar(packet_bytes, expected_packet_digest, declaration, exported_at=...)`. It verifies the F2 private packet using an independently retained expected digest and reconstructs source integrity before adapting it. The returned PXP sidecar is private: no CLI, filesystem write, public projection, catalog mutation or gallery association is wired by F3.

The supplied declaration must contain exactly `declaredBy`, `declaredAt`, `sourceSha256`, `scope=EXPORTED_CONFIGURATIONS_ONLY`, with optional `sessionId`, `target`, `productVersion`. It is bound to the original source-byte digest. Absence, wrong scope/source, excessive fields or invalid dates fail closed. The adapter does not discover the actor from OS identity or assign the import clock to a declaration. Declaration time must be supplied with evidence; a date-only historical declaration is insufficient to fabricate a date-time.

`exported_at` is separately supplied UTC representation-export time, no earlier than the import or attestation. Import, attestation, new sidecar export and historical execution clocks remain distinct. Historical run times and process versions are null; archive/import IDs are explicitly new receipt-based identities, not original PixInsight run IDs. Missing session/target/product context remains the truthful string `unknown`; that is not an eligible real-image binding.

## Preserved representation and semantics

The adapter flattens supported ProcessContainer children in their exported order, preserving separate ordinals for repeated process types. Each step is DECLARED, never OBSERVED, and cites its source packet/unique instance. The declaration concerns exported configurations, not proof of complete chronology or universal capture. Suggested activity cannot enter this profile. Unsupported source packets are rejected; a supported empty container yields UNAVAILABLE with zero steps. Nonempty supported export yields PARTIAL with fixed explicit limitations; COMPLETE is never produced.

PXP parameters use an adapter-specific envelope:

```json
{
  "bkl049LexicalV1": {
    "exportParameters": {"example": {"kind": "number", "literal": "+0.1200E-03"}},
    "sourceInstance": "SyntheticInstance",
    "containerPath": ["SyntheticContainer"]
  }
}
```

This preserves F2's numeric sign/precision/exponent, enum owner/member, arrays and literal expressions without interpreting or converting them to native numeric semantics. `bkl049LexicalV1` is internal adapter encoding inside the existing extensible parameters object, not a claim that arbitrary consumers understand native RC versions or masks. Unknown historical RC fields remain lexical data; processVersion is not inferred from today's installation.

Ordered mask commands, comments and all original bytes remain in the mandatory retained private F2 packet. `containerPath` and source locators connect the sidecar back to that record. Empty PXP mask/input/output references mean unresolved associations, not proof that no mask/input/output existed. F4 must supply governed binding; no expression parsing or name similarity creates asset identity.

## Contract compatibility and validation boundary

No PXP, manifest, catalog or gallery schema is changed. The emitted sidecar is checked against the existing PXP schema through a bounded evaluator of every keyword used by that profile: local definitions, types, required/extra fields, constant/enumerated values, bounds, patterns and UTC date-time representation. Unsupported new keywords fail closed. This is not a general JSON Schema implementation: time format is deliberately restricted to whole-second UTC, and unconstrained parameter values come only from the already reconstructed bounded F2 source. Input strings also honor the legacy JavaScript UTF-16 length bounds; no silent truncation occurs.

The producer guarantees ordered contiguous ordinals, truthful counts and DECLARED provenance by construction. The separate Node integration test then exercises existing semantic PXP validation, mapper, manifest validation, ledger, reconciliation, projection and read model. Generic reconciliation can be less strict than the future image-binding gate; passing it never substitutes for F4 identity/integrity checks.

The coarse manifest omits detailed lexical values and lists only observed process evidence. Consequently its process list stays empty for this all-DECLARED adapter. Preserve the rich sidecar **and** source packet; the manifest alone is not the workflow archive. The current read model contains private values and is not publishable without F5's explicit minimized selection.

## Verification

Nine synthetic Python tests cover source-bound attestation, no OBSERVED/binding inference, lexical/order preservation, original packet immutability, separate clocks, invalid/missing declaration, schema field constraints, limits including Unicode, unsupported sources, missing history and deterministic repeat. The synthetic Node bridge passes through existing AP14-W06 components and proves that absent catalog/output identities stay unresolved while detailed values survive the private read model. Sixteen existing provenance/mapper/read-model regressions pass locally.

Windows/Linux CI runs these alongside F2's packet tests and retained F0 grammar/header tests. No real source was imported, no scientific image was read/modified and no public scientific payload was generated by F3 tests. Exact-head review, CI and post-merge evidence are separate gates recorded in the delivery PR.

## Remaining acceptance and rollback

F4 requires an authoritative exact asset/version/source association and integrity guard, with external acquisition provenance retained honestly. The Owner has separately declared the selected demonstration image to originate outside Digital StarGate; no observatory session may be invented. F5 requires approved public fields/image and real gallery linkage. F6/OAT and final release remain open. These are not satisfied by the synthetic bridge.

Rollback removes this additive adapter/test wiring through a reviewed PR while preserving F2 packets and existing BKL-045 behavior. Any retained sidecar must keep its packet and encoding version. No runtime migration, catalog or image rollback is involved; no new dependency or native installation is introduced. BKL-043 stays current.

## Revision history

- 1.0 — Private declared-evidence adapter and bounded schema/existing-pipeline verification; real association and publication remain unimplemented.
