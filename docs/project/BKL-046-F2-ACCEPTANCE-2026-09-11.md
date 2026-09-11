# BKL-046 F2 — Acceptance Record

| Campo | Valore |
|---|---|
| Increment | BKL-046 F2 — Machine-Readable Recommendation and Human Decision Contracts |
| Stato | CLOSED / ACCEPTED / POST-MERGE WORKFLOWS VERIFIED |
| Data | 11/09/2026 |
| Pull request | #167 |
| Accepted merge | `b8a9025fdfc9b5254b9c79a5c37a775b4f8fd083` |
| Exact reviewed head | `94d3179ede2799c271c8042645278dbafb16590d` |
| Successor | BKL-046 F3 — Deterministic Advisory Demonstrator |

## 1. Acceptance decision

BKL-046 F2 è accettato come baseline machine-readable dell'AI Post-Processing Assistant per PixInsight. L'incremento definisce Recommendation e Human Decision Receipt separati, source binding e subject correlation fail-closed, parameter advice bounded, confidence indisponibile, authority human-only/read-only e identity SHA-256 deterministica.

L'acceptance riguarda schema, fixture sintetica, validator, test e documentazione. Non dichiara implementati model/provider, inference runtime, RAG/vector store, image transfer, recommendation engine produttivo, consumer dinamico o PixInsight apply.

## 2. Verified evidence

- exact-head CI della PR: 5/5 workflow `SUCCESS`;
- contract verifier e 16/16 test positivi/negativi passed;
- Architecture Review Board: `APPROVED`, 98/100, nessun Blocker/Major/Minor;
- Release Quality: `READY FOR MERGE`, nessun waiver;
- protected merge PR #167: `b8a9025fdfc9b5254b9c79a5c37a775b4f8fd083`;
- 6/6 workflow post-merge `SUCCESS`;
- deploy MkDocs artifact to GitHub Pages `34634735881`: `SUCCESS`.

La verifica post-merge attesta build e pubblicazione del pacchetto integrato sul merge SHA. Non viene dichiarato un test runtime dell'assistente, perché F2 non introduce alcun runtime.

## 3. Accepted contracts

- root fixture envelope chiuso e versionato;
- Recommendation distinta da evidence, decisione umana ed esecuzione;
- Human Decision Receipt con `executionState=NOT_OBSERVED` e execution refs vuoti;
- source stale/partial/unavailable/invalid o `SUGGESTED` non può sostenere `validated`;
- subject correlation irrisolta, conflicts e unknowns falliscono chiuso;
- parameter advice limitato a categorical, bounded interval o `UNKNOWN_NOT_RECOMMENDED`;
- confidence `UNAVAILABLE_F2` senza numeric value;
- action/execution authority `NONE`, PixInsight apply e automatic acceptance `false`;
- tampering rilevato con digest deterministici.

## 4. Dynamic update boundary

F2 è un incremento statico di contratto e non crea una projection alimentata dalle sessioni. La pipeline automatica di import, il catalogo AP-014 e i consumer esistenti rimangono invariati.

Qualsiasi futuro consumer BKL-046 dovrà essere rigenerato e pubblicato automaticamente e atomicamente dopo ogni nuova sessione scientifica importata. Questo vincolo resta un gate obbligatorio di F4 e non è anticipato artificialmente in F2.

## 5. Retained limitations

- PixInsight complete process history resta `UNAVAILABLE` nella evidence reale BKL-045;
- recommendation quality e confidence calibration non sono definite;
- nessun dataset di evaluation, model/provider o runtime placement è accettato;
- il fixture envelope non è un runtime envelope e richiede versioning/riuso esplicito in F3;
- `ASSISTED APPLY` resta fuori scope e richiede nuova architecture/security review.

## 6. Transition

F3 è dependency-ready esclusivamente per:

1. demonstrator deterministico e read-only;
2. input limitato alle fixture bounded F2;
3. output Recommendation conforme allo schema F2;
4. known-answer behavior e test di determinismo/idempotenza;
5. reason code, correlation e audit senza dati reali.

F3 non seleziona un modello/provider, non ingerisce sessioni reali e non autorizza PixInsight apply, automatic acceptance, remediation, device command o Safety Authority.
