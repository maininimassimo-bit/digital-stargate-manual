# BKL-031 F3-A2-D3 — CurrentSetupAssignment Owner Decision Assessment

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D3-PROGRAM-001 |
| Stato | **OWNER DECISION REQUIRED — NO ASSIGNMENT MATERIALIZATION** |
| Data | 15/09/2026 |
| Verified baseline | `main@e73b1aa631c41dff97b9e5ededb6d6be02a667d4` |
| Predecessor | F3-A1-M4 accepted with conditions / post-merge verified |
| Governing contract | `BKL-031-F3-A2-CONTRACT-001` |
| Runtime / data delta | None |
| PC Principale / EAGLE | Nessuna attività richiesta |

## 1. Program decision

F3-A2-D3 is selected as the next dependency-ready owner gate. The approved Site Authority and approved setup baseline now satisfy the two independent reference prerequisites, but they do not create a current relationship between site and setup.

This assessment authorizes only collection and recording of owner decisions. It does not create an assignment, schema, fixture, validator, adapter, persistence, API or runtime availability.

## 2. Maturity assessment

| Area | Maturità | Evidence |
|---|---:|---|
| Setup Authority logical contract | 90/100 | accepted with conditions and post-merge verified |
| Approved setup baseline authority | 100/100 | protected envelope and receipt integrated |
| Approved Site Authority | 100/100 | PR #204 accepted and post-merge verified |
| Assignment authority decision | 20/100 | logical roles defined; concrete choices absent |
| CurrentSetupAssignment materialization | 0/100 | no record, receipt, schema or tests |
| Runtime resolution | 0/100 | no adapter or operational evidence |

Scores describe architecture/delivery maturity, not scientific accuracy or operational readiness.

## 3. Required owner decisions

| Decision | Recommended default | Effect |
|---|---|---|
| Source authority | protected GitHub registry outside `docs/` | preserves review, audit and Pages separation |
| Assignment owner | Repository Owner | accountable for the site–baseline relationship |
| Assignment custodian | Architecture Office | may prepare/remediate but cannot approve |
| Approval Authority | human Repository Owner | preserves the established human approval boundary |
| Separation policy | custodian cannot approve; owner may be owner and Approval Authority | prevents Architecture Office self-approval |
| Validity | half-open, unbounded, with an explicit UTC start chosen by the owner | deterministic current resolution without sentinel dates |
| Publication | no internal assignment/site/baseline IDs, digests, locators or exact site facts | deny-by-default public boundary |

The exact approved site and baseline references are already present in their protected registries and need not be repeated in public documents.

## 4. Decision sequence

1. owner confirms the source/registry and concrete role assignments;
2. owner supplies the exact `validFromUtc` and chooses `UNBOUNDED` or an exclusive end;
3. Architecture Office records the protected source decision only;
4. a later, separately reviewed package defines schema/canonicalization and creates an ineligible DRAFT;
5. the owner receives and explicitly approves the exact assignment digest;
6. a separate receipt/lifecycle package may promote the assignment to APPROVED;
7. only a later runtime architecture package may implement S09 resolution.

## 5. Invariants and stop conditions

- baseline approval never implies assignment approval;
- Site Authority approval never implies assignment approval;
- DRAFT and RETIRED assignments are never current;
- gap yields `UNAVAILABLE_CURRENT`; overlap yields `CONFLICTED`;
- no latest-file, highest-revision, historical-session or EAGLE/N.I.N.A. fallback;
- no protected value in public docs, PR narratives, logs or generated projections;
- no runtime work until `ARB-204-MI02` is resolved;
- no second site revision/receipt until `ARB-204-MI01` is resolved;
- physical/local interlocks remain the only Safety Authority.

## 6. Acceptance criteria for this owner gate

F3-A2-D3 is complete only when the owner has explicitly decided all rows in section 3, including an exact validity start. Completion authorizes creation of protected decision evidence, not assignment approval or runtime work.

## 7. Handoff

After the owner decisions are complete, hand off a bounded DRAFT materialization package to the Solution Architect. The package must reuse the accepted F3-A2 contract and validation plan, preserve protected/public separation, and implement executable identity, interval, approval, conflict and privacy gates before any lifecycle promotion.
