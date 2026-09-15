# Digital StarGate — Current Technical Baseline 14/09/2026

| Campo | Valore |
|---|---|
| Stato | Active |
| Repository baseline verificata | `3a79bb93c9a0925280eba5214d517107804cb13c` |
| Current governed package | BKL-031 F3 — Solution Architecture accepted with conditions; implementation decision pending |
| Accepted increments | BKL-031 F1/F2; F3 handoff and Solution Architecture integrated/post-merge verified |
| Runtime impact | None |
| PC Principale / EAGLE | Nessuna azione richiesta |

## 1. Accepted foundation

BKL-015, BKL-044, BKL-035, BKL-040, BKL-038, BKL-039, BKL-045, BKL-037, BKL-041 e BKL-046 restano accepted nei rispettivi boundary documentati.

BKL-031 F1 è ACCEPTED / POST-MERGE VERIFIED tramite PR #183 e merge `b14d9cdd991b5eef74dd9b972958e74c5903a32d`.

BKL-031 F2 è ACCEPTED / POST-MERGE VERIFIED tramite PR #188 e merge `7f861f7399079858c9744e69b6c773664b6b5b54`.

## 2. Accepted F2 boundary

La baseline F2 comprende JSON Schema, fixture bounded M 27, validator normativo fail-closed, 37 test e integrazione Developer Foundation. S07–S11 restano unavailable/unknown; S02 è la sola authority F2 per RA/Dec/epoch e S04 non può attestare coordinate.

Le review ARB/RQ sono AI-assisted, owner-authorized e non equivalenti ad approvazioni umane indipendenti. Tutti i finding M-01–M-04 e M-R1 sono chiusi.

## 3. Verified evidence

- technical head: `8e46ae3eccdaca5763aee7103063e020f97e2946`;
- review-publication head: `09b6e2272f40688c7ead0eba964b8eb6f64a0920`;
- merge: `7f861f7399079858c9744e69b6c773664b6b5b54`;
- exact-head CI: 7/7 SUCCESS;
- post-merge CI: 9/9 SUCCESS, incluso Pages;
- test suite: 37/37 PASS;
- malformed JSON probe: 250/250 fail-closed, 0 throws;
- waiver `W-BKL031-F2-MERGE-001`: consumed/expired.

## 4. Preserved invariants

- projection non diventa authority;
- Citation, Provenance, identity, freshness, missingness e conflict restano espliciti;
- BKL-031 advisory resta separato da BKL-032 readiness;
- interlock fisici/locali restano Safety Authority;
- workload pesante e chiamate esterne restano fuori da EAGLE.

## 5. Current F3 gate

L'handoff F3 è integrato/post-merge verified tramite PR #190 e merge `2ffc77917bcd3fc25a3c5657e8f12e62c9284303`, con 9/9 workflow post-merge; `W-BKL031-F3-HANDOFF-MERGE-001` è consumata/scaduta.

Il Solution Architecture Package F3 è integrato tramite PR #191: technical head `43a46ac28c30badc40e4cb180ed98924ebcf74a1`, review-publication head `d0f8098cfff9651b3ba1597fd77f09a11a7c634a`, merge `3a79bb93c9a0925280eba5214d517107804cb13c`. ARB AI-assisted: `APPROVED WITH CONDITIONS`, 98/100; Release Quality: `CONDITIONALLY READY`; post-merge: 9/9 workflow SUCCESS. `W-BKL031-F3-SA-MERGE-001` è consumata/scaduta. L'architettura è accettata con condizioni, non implementata. `ARB-191-MI01` e `ARB-191-MI02` restano gate obbligatori. BKL-031 resta attivo; nessuna slice F3-A1/A2/A3/B/C è promossa. Provider/ADR, record reali, schema/fixture/validator/adapter, runtime, F4/F5, BKL-032 e Safety restano non autorizzati.
