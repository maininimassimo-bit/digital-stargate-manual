# Digital StarGate Current Technical Baseline — 12/09/2026

| Campo | Valore |
|---|---|
| Stato | Current technical continuity baseline |
| Data | 12/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Accepted main baseline | `af48cc2441cf956d88c13c81845fc2a2f7c599f2` |
| Current governed package | BKL-046 — AI Post-Processing Assistant for PixInsight |
| Current increment | BKL-046 F5 — Real-Evidence Evaluation and Capability Closure design |
| Accepted predecessor | BKL-046 F4; BKL-046 F3; BKL-046 F2; BKL-046 F1; BKL-041 closure; BKL-045; BKL-044; BKL-015 |

## 1. Accepted F4 implementation

- canonical population: `docs/data/scientific-session-catalog.json`, 15 sessioni;
- provenance source: sidecar BKL-045 allowlisted, validati al build e sanitizzati nella projection pubblica;
- deterministic rules: `BKL046-F3-CLOSED-RULES-1`;
- persisted projection: `docs/data/ai-post-processing-advisory-projection.json`;
- portal consumer: `docs/ai-post-processing-assistant/index.md`;
- automatic update: first/retry path di `.github/workflows/analyze-session-automatic.yml`;
- authority: `READ_ONLY`, `HUMAN_ONLY`, action/execution `NONE`, Safety Authority locale.

## 2. Accepted identities and evidence

| Elemento | Valore |
|---|---|
| Technical implementation head | `b2f8543d0a7fd3e354c40d9acb0206ef7e6edea4` |
| Review-publication head | `ae1b8f2ae04fc9c4891e794bc930ec0e09fcf640` |
| Accepted merge | `af48cc2441cf956d88c13c81845fc2a2f7c599f2` |
| PR | #175 |
| Projection tests | 24/24 PASS |
| Consumer tests | 11/11 PASS |
| F2/F3 regressions | 16/16 e 21/21 PASS |
| Post-merge | 6/6 workflow SUCCESS |

## 3. Current observed dataset state

La projection accettata contiene 15 record: 0 `PROVENANCE_MATCHED`, 15 `PROVENANCE_UNAVAILABLE`, 0 ambiguous, 0 invalid e 15 `PROCESSING_HISTORY_AVAILABILITY=FAIL_CLOSED`. Due source BKL-045 validate restano non correlate al catalogo. Questo stato è evidence reale preservata, non un errore da mascherare.

## 4. Freshness and publication boundary

Catalogo, source-set snapshot, singoli record e projection hanno digest SHA-256. Il consumer scarica catalogo/projection con `cache: no-store` e fallisce chiuso su stale data, session-set mismatch, tampering, schema/authority drift o Web Crypto non disponibile. Il workflow rigenera, controlla e pubblica la projection nello stesso commit governato del catalogo, anche nel retry dopo riallineamento a `main`.

## 5. Review and waiver record

ARB F4-C R2 è `APPROVED WITH CONDITIONS` 99/100 senza Blocker/Major/Minor attivi. Release Quality F4-C R2 è `READY FOR MERGE` con la deroga owner-approved `W-BKL046-F4-001`. Entrambe sono review AI-assistite e non equivalenti ad approvazioni umane indipendenti. La deroga era valida solo per PR #175 ed è consumata/scaduta.

## 6. Retained limitations

- processing history PixInsight reale incompleta o non correlabile resta unavailable;
- nessuna confidence scientifica, ground truth, calibrazione o production readiness;
- Recommendation, Human Decision Receipt ed execution evidence restano separati;
- nessun image upload/transfer, modello, provider, RAG/vector store o apply path;
- nessun comando apparato, remediation o modifica della Safety Authority.

## 7. F5 entry condition

F5 è promosso soltanto per progettare una valutazione bounded su evidence reale e i criteri di possibile closure della capability read-only. Prima di implementare o dichiarare closure servono cohort, eligibility rules, evidence sufficiency, metriche descrittive, failure/stop conditions e retained limitations esplicite.
