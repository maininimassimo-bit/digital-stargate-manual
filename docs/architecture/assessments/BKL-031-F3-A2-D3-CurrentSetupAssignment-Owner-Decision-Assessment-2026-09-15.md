# BKL-031 F3-A2-D3 — CurrentSetupAssignment Owner Decision Assessment

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-D3-PROGRAM-001 |
| Stato | **OWNER DECISIONS COMPLETE / PROTECTED EVIDENCE INTEGRATION CANDIDATE** |
| Data | 15/09/2026 |
| Verified baseline | `main@d5f403bbe6a39731213c372cb22296324d10b03d` |
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
| Assignment authority decision | 100/100 | source, roles, separation and validity explicitly selected by owner |
| CurrentSetupAssignment materialization | 0/100 | no record, receipt, schema or tests |
| Runtime resolution | 0/100 | no adapter or operational evidence |

Scores describe architecture/delivery maturity, not scientific accuracy or operational readiness.

## 3. Completed owner decisions

| Decision | Owner choice | Effect |
|---|---|---|
| Source authority | protected GitHub registry outside `docs/` | preserves review, audit and Pages separation |
| Assignment owner | Repository Owner | accountable for the site–baseline relationship |
| Assignment custodian | Architecture Office | may prepare/remediate but cannot approve |
| Approval Authority | human Repository Owner | preserves the established human approval boundary |
| Separation policy | custodian cannot approve; owner may be owner and Approval Authority | prevents Architecture Office self-approval |
| Validity | half-open and unbounded from the approved setup-baseline effective start | deterministic current resolution without sentinel dates |
| Publication | no internal assignment/site/baseline IDs, digests, locators or exact site facts | deny-by-default public boundary |

The exact approved site and baseline references are already present in their protected registries and need not be repeated in public documents.

## 4. Decision sequence

1. owner confirmed the source/registry and concrete role assignments;
2. owner selected the approved setup-baseline effective start and `UNBOUNDED` end mode;
3. Architecture Office records the protected source decision only in this package;
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

F3-A2-D3 owner input is complete. Repository completion requires integration of the protected decision evidence through exact-head CI, ARB, Release Quality, expected-head merge and post-merge verification. Completion does not authorize assignment approval or runtime work.

## 7. Handoff

After decision-evidence integration, hand off `BKL-031-F3-A2-D4` as a bounded DRAFT materialization package to the Solution Architect. The package must reuse the accepted F3-A2 contract and validation plan, preserve protected/public separation, and implement executable identity, interval, approval, conflict and privacy gates before any lifecycle promotion.
