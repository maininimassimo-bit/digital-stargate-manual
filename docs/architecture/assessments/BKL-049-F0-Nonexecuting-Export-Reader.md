# BKL-049 F0 — Nonexecuting export subset reader

Date: 2026-09-30. Status: ISOLATED RESEARCH / F0 OPEN. No production ingestion, runtime observation, PXP emission or gallery write.

The [archive linkage experiment](BKL-049-F0-Archive-Linkage-Experiment.md) identified the need to read supplied JavaScript exports without running them. This experiment implements an original, bounded reader using Python standard libraries only. It contains no PCL/PJSR/vendor source and requires no SDK, dependency installation or PixInsight access. It is not a general JavaScript parser, an accepted F1 implementation or a security-audited import service.

## Behavior and boundaries

The reader tokenizes the full input, then recognizes declarations of process-shaped instances, literal property assignments, literal string concatenation, nested arrays, qualified enum-like values and ProcessContainer add/setMask/invertMask calls. It builds an in-memory structure while preserving container order, repeated process types, local mask indices, source spans and lexical numeric precision. Enum-like values and class names are represented as data; their validity against a particular installed module is not verified.

It never evaluates JavaScript or PixelMath, instantiates a PixInsight process, accesses a referenced image, resolves a view name, downloads anything or interprets comments as commands. PixelMath expression strings remain opaque data. Comments are retained as source spans; timestamps and total-time comments are not automatically assigned execution authority or summed. Source spans are Python character offsets in the decoded input, not raw byte offsets. The CLI reports a separate digest of original file bytes; the internal text digest covers UTF-8 re-encoding and can differ after BOM removal.

Unsupported constructs reject the whole parse without a partial success result: execution calls, loops, arbitrary expressions, unrecognized syntax/escapes, duplicate declarations/properties, reused instances, invalid mask indices, cycles, ambiguous roots and mutation after an instance has been added to a parent. This deliberate restriction avoids guessing snapshot-versus-reference semantics of later mutations. Individual copied snippets with repeated variable names must be treated as separate artifacts; do not concatenate them and silently overwrite earlier instances.

Resource bounds: 2 MiB input, 200,000 tokens, 512 declared instances, 32 levels of array/container nesting. Bounds are research limits, not changes to PXP. Unsupported encodings or oversized files require explicit reassessment; no truncation to a seemingly valid workflow occurs. The grammar supports double-quoted strings with JSON-compatible escapes; other legal JavaScript string forms may be rejected. Mask commands are retained in order rather than assumed to establish independently measured mask state.

## Running the experiment

From the repository root:

```text
python experiments/bkl049-f0/test_read_export_subset.py
python experiments/bkl049-f0/read_export_subset.py <local-export-file>
```

The CLI emits aggregate counts, original-byte digest and evidence status only. It omits names, paths, parameter values and source excerpts, including from error messages. The in-memory parse result **does contain original values** and must remain private unless separately reviewed. A digest can disclose equality with a known artifact; count-only output is not a general guarantee of anonymity. Do not add private exports to Git or pass source code as shell arguments.

The [reader](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/read_export_subset.py), [synthetic tests](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/test_read_export_subset.py) and [sanitized observations](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/codex/bkl-049-f0/experiments/bkl049-f0/export-reader-observations.json) are isolated from production and not wired into an application or upload endpoint.

## Verification and findings

Twenty-seven synthetic tests pass. They cover literal preservation, nested/repeated processes, mask operations, source spans, private-value omission from summaries, malformed/unsupported input, execution attempts, cycles/reuse, post-attachment mutation and resource bounds. Rejection tests demonstrate the implemented subset boundary, not exhaustive security certification.

Two private Owner-supplied attachments were inspected with the reader, without execution. Public results contain aggregate counts and evidence aliases only:

| Source alias | Containers | Non-container instances | Assigned properties | Mask commands |
|---|---:|---:|---:|---:|
| E01 single-image initial export | 1 | 1 | 28 | 0 |
| E04 completed-project history | 2 | 21 | 381 | 9 |

For E01, the parsed input table contains 30 rows. For E04, 19 root entries and the three ordered PixelMath children of the nested container agree with manual inspection; seven assignments and two inversions account for the nine mask commands. Original source data and private identifiers are not redistributed. These real-source observations cannot be independently reproduced from this public report alone; the synthetic tests are reproducible without private data.

Successful parsing returns `PARSED_SUBSET`, `executionEvidence=NOT_ESTABLISHED`, and `workflowCompleteness=UNAVAILABLE`. The latter describes what the reader alone can certify; it does not erase the separately recorded overall PARTIAL research assessment. No step is automatically classified OBSERVED. Owner declarations and inspected text remain distinct evidence sources.

## Implications for F0

The supplied export structures can be read without executing their contents, preserving distinctions the earlier regex-only inspection could not formally enforce. This advances the artifact route and resolves the narrow missing-reader experiment, not universal extraction or complete workflow capture.

Still unproven: additional real export syntax, module/schema version interpretation, automatic history acquisition, immutable image/mask identities, originating script identity, complete project graph, snapshot overlap/restart behavior and final gallery binding. The reader does not resolve PixelMath dependencies or infer script names from expressions. Any future adapter must also address PXP ordering/capacity/privacy gaps and scientific asset authority. No contract or authority is changed here; F1 is not promoted.
