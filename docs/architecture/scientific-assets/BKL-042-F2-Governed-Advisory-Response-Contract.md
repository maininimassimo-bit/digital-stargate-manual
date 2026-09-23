# BKL-042 F2 — Governed Advisory Response Contract

**Status:** Active / Contract and fixture verified  
**Authority:** `READ_ONLY` / advisory-only

F2 definisce l'envelope machine-readable per risposte dell'Observatory Assistant con
citazioni, provenance, facts, inference, recommendations e human disposition separati.
La fixture comprende un caso corrente citato e un caso `INSUFFICIENT_EVIDENCE` per
dimostrare il comportamento fail-closed su provenance unavailable.

## Contract rules

- ogni evidence reference deve risolvere a una source con `sourceRef`, authority, lifecycle,
  freshness, completeness, citation e limitations;
- `ANSWERED` richiede facts/evidence citabili e non autorizza l'esecuzione;
- `INSUFFICIENT_EVIDENCE` è obbligatorio per missingness, stale, unknown o provenance
  unavailable e non può contenere raccomandazioni subject-specific;
- human disposition è separata e non equivale a execution evidence;
- `executionState=NOT_OBSERVED`, `actionAuthority=NONE`, `commandAuthority=NONE` e
  `safetyAuthority=NONE` sono invarianti del contratto;
- la fixture è sintetica e non è output di modello, provider o runtime assistant.

## Evidence

- schema: `schemas/bkl042-f2-advisory-response.schema.json`;
- fixture: `docs/data/bkl042-f2-advisory-response-fixture.json`;
- validator: `.github/scripts/verify-bkl042-f2-advisory-response.mjs`;
- F1 boundary: `docs/architecture/scientific-assets/BKL-042-F1-Observatory-Assistant-Source-Discovery-and-Advisory-Contract.md`.

F2 non abilita model/provider selection, external transfer, RAG, vector database, upload,
tool execution, PixInsight apply, automatic acceptance, command, remediation, scheduler o
Safety Authority. Il consumer conversazionale resta un gate futuro.
