# BKL-042 F3 — Deterministic Advisory Demonstrator

**Status:** Active / Demonstrator verified
**Mode:** Bounded synthetic, deterministic, read-only

F3 applica il metodo `BKL042-F3-CLOSED-RULES-1` alla fixture F2 senza modello, provider,
retrieval runtime o trasferimento di dati. Produce due esiti riproducibili: un caso con
citazione corrente e un caso `INSUFFICIENT_EVIDENCE` per provenance unavailable.

## Evidence

- schema: `schemas/bkl042-f3-deterministic-advisory.schema.json`;
- input: `docs/data/bkl042-f2-advisory-response-fixture.json`;
- generator: `.github/scripts/generate-bkl042-f3-advisory.mjs`;
- output: `docs/data/bkl042-f3-deterministic-advisory-output.json`;
- validator: `.github/scripts/verify-bkl042-f3-advisory.mjs`;
- regression: `.github/scripts/test-bkl042-f3-advisory.mjs`.

## Governed behavior

- `CITATION_AND_AUTHORITY` passa solo con source references risolte;
- `SOURCE_AVAILABILITY` fallisce chiudendo il caso se la fonte è unavailable, unknown,
  stale, conflict o incompleta;
- il caso fail-closed non produce raccomandazioni subject-specific;
- method ID, producer version, input fixture e output digest sono espliciti;
- authority resta `READ_ONLY`, advisory-only, action/command/execution/safety `NONE`;
- l'output non è qualità scientifica, approvazione umana, execution evidence o model output.

F3 non abilita un consumer conversazionale, provider esterni, upload, tool execution,
PixInsight apply, automatic acceptance, scheduler, remediation o Safety Authority.
