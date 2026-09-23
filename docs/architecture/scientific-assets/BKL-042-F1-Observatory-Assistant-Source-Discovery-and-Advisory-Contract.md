# BKL-042 F1 — Observatory Assistant Source Discovery and Advisory Contract

**Identifier:** BKL-042-F1
**Status:** Active / Owner-Authorized
**Owner / accountable:** Massimo Mainini
**Mode:** Advisory-only, repository-bound, read-only

## Purpose

Definire la base governata per l'AI Observatory Assistant: fonti eleggibili,
citazioni, provenance, freshness, missingness e limiti dell'assistenza advisory prima
di qualsiasi scelta di modello, provider, retrieval runtime, UI conversazionale o tool
execution.

## Scope

F1 comprende source discovery e authority, semantica di observation/evidence/explanation/
recommendation/human decision, citazione obbligatoria, provenance e freshness, missingness
fail-closed, separazione fra consiglio, decisione ed esecuzione e criteri per BKL-042-F2.

F1 non seleziona o esegue modelli/provider, non trasferisce dati a servizi esterni, non
introduce RAG/vector database, non interpreta immagini, non invia comandi e non modifica
asset, workflow PixInsight, apparati o Safety Authority.

## Source eligibility

| Classe | Uso ammesso | Authority preservata |
|---|---|---|
| BKL-033 digital twin projection | contesto asset/dependency/status | `projection`, mai operational truth |
| BKL-034 image/session/target projection | identità, lineage e provenance | `projection`, read-only |
| BKL-034-F2 archive contract | checksum, metadata completeness e workflow refs | `archive_projection`, write `NONE` |
| BKL-045 PixInsight provenance | evidenza observed/declared/suggested | processing evidence |
| BKL-031 planner projection | contesto astronomico e ranking spiegabile | advisory projection, non GO |
| BKL-032 readiness | contesto decision-support | mai Safety Authority o command |
| BKL-036-F5 EAGLE Health | contesto osservatorio live | descriptive health, non readiness |
| BKL-041 quality projection | contesto sperimentale | `EXPERIMENTAL_NOT_ACCEPTED`, mai ground truth |

Una fonte è eleggibile solo se il riferimento è stabile, la freshness è verificabile, la
provenance è risolta e le limitazioni sono esposte. Claim conversazionali, memoria del
modello, dati non citati e inferenze da assenza di evidenza non sono fonti.

## Advisory semantic boundary

Ogni risposta futura dovrà distinguere:

1. **facts** — valori direttamente citati da una projection governata;
2. **evidence** — record con authority, lifecycle, freshness e completeness;
3. **inference** — spiegazione derivata, non fonte e non verità osservata;
4. **recommendation** — suggerimento non vincolante, sempre advisory;
5. **human decision** — scelta dell'utente, separata dall'esecuzione;
6. **execution evidence** — evidenza successiva e indipendente.

Una risposta priva di citazioni o con correlazione soggetto non risolta deve essere
`INSUFFICIENT_EVIDENCE`, non una risposta apparentemente completa.

## Fail-closed rules

| Condizione | Esito obbligatorio |
|---|---|
| fonte assente o non citabile | `INSUFFICIENT_EVIDENCE` |
| fonte stale o non disponibile | esporre stato e non usare il dato come corrente |
| conflitto fra fonti | `CONFLICT_REQUIRES_REVIEW` |
| correlazione asset/session/workflow non risolta | nessun consiglio subject-specific |
| provenance PixInsight incompleta | non ricostruire passaggi mancanti |
| qualità sperimentale non accettata | contesto limitato, mai ground truth |
| richiesta di comando/apply/remediation | rifiuto bounded e auditabile |
| modello/provider/versione non dichiarati | nessuna raccomandazione validata |

`VALIDATED` significa solo validità strutturale e di evidenza; non significa correttezza
scientifica, approvazione umana, readiness o esecuzione.

## Authority boundary

```text
Governed projections -> citation/evidence gate -> advisory explanation
                                      -> human review (separata)
                                      -.-> independent execution evidence
```

```text
consumer_mode=READ_ONLY
advisory_only=true
acceptance_authority=HUMAN_ONLY
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
automatic_acceptance=false
```

## Acceptance criteria for F1

- ogni fonte ha authority, lifecycle, freshness e limite espliciti;
- facts, evidence, inference, recommendation, human decision ed execution sono separati;
- le projection upstream sono consumate solo downstream/read-only;
- dati stale, unknown, unavailable o conflittuali falliscono chiudendo il consiglio;
- nessun modello, provider, RAG, tool execution o threshold scientifico è inventato;
- command, apply, remediation, scheduler e Safety Authority restano esclusi;
- roadmap, backlog, handover, MkDocs e review sono coerenti.

## Next governed increment

Il successivo gate BKL-042-F2 potrà definire un envelope machine-readable per citation,
provenance, explanation e human disposition su fixture sintetiche bounded. Non potrà
abilitare provider esterni, upload immagini, tool execution, PixInsight apply o decisioni
automatiche.
