# BKL-049 F5 — Gallery workflow reader

| Field | Value |
|---|---|
| Date | 2026-10-01 |
| Scope | Bounded collection, Scientific Data Engine reader and gallery panel |
| State | Implemented with synthetic verification; release evidence tracked in the delivery PR |
| Real-data gate | OPEN: no accepted real collection, preview or association is published |
| Authority | Processing evidence only; action/catalog/Safety Authority unchanged |

## User-visible behavior

The gallery gains a separate “Workflow delle immagini” panel, backed by the [F5 producer](BKL-049-F5-Public-Projection-Builder.md). It shows selected process labels, exact lexical parameter text, exported order, explicit omissions and DECLARED/PARTIAL or UNAVAILABLE state. It never represents the exported order as observed execution. Native disclosure controls support keyboard use; values are inserted through text APIs, not HTML.

A direct link carries all three approved public aliases: image, immutable image version and workflow. Missing, repeated, invalid or mismatched references return unavailable without selecting another record. An unfiltered view lists the current approved collection. These cards do not infer links to the existing BKL-034 fixture cards, whose closed schema has no real version identity. Integrating an authorized real preview with its version remains a later gate; there is no upload control in this increment.

The committed collection is **empty**, with null publication/expiry times. No synthetic workflow or real scientific data is published. Existing fixture cards remain labelled as fixtures; absence of real workflow records never falls back to them. Without JavaScript, only the explicit unavailable explanation is visible.

## Data and transport boundary

`bkl049-workflow-contract.js` validates the single-record producer profile plus the additive `schemas/bkl049-public-workflow-collection.schema.json`. It enforces closed fields, authority constants, allowed identifiers, exact fixed method citation and gap vocabulary, strictly increasing source ordinals, bounded counts and unique parameter names. Collections reject duplicate image/version pairs and reused workflow IDs before lookup. Different versions of an image need different workflow IDs. Validation consumes published evidence; it does not register assets, establish scientific quality or approve publication.

Limits: 8 records, 256 KiB per record and 2 MiB per collection; existing 512-step, 128-selected-parameter and 4096-character display limits remain. Canonical sorted JSON, ASCII escaping and at most one trailing LF or CRLF are required; duplicate JSON keys and extra payloads reject. The browser profile is tested against an actual synthetic Python producer result. Existing PXP, catalog, manifest and BKL-034 schemas are unchanged.

Only `DSGScientificDataEngine.getPublicWorkflowCollection` performs the fetch. Its fixed same-origin collection route is derived from the engine script location; it accepts no user-controlled URL. Reads omit credentials, reject redirects, bypass the browser cache, use fatal UTF-8 decoding and bound streamed bytes before JSON parsing. A ten-second abort bounds the request. It has no old-result/fixture fallback and does not feed workflows into the session store. Existing session APIs retain their semantics.

The panel lazily loads the existing engine only when mounted. It clears old cards immediately on refresh, aborts obsolete loads and ignores late responses. The established component lifecycle handles navigation/remount cleanup; browser history and return-to-visible trigger fresh verification. No timer polls external services, no observer command path and no new service are introduced.

## Freshness and withdrawal

Nonempty collections require UTC publication and expiry times, with publication not in the future and expiry strictly after the current browser time. The maximum validity interval is 24 hours: an engineering ceiling for this public read model, not a scientific quality threshold. The publisher must revalidate the current authoritative snapshot and current field approval before renewing; extending a timestamp alone is not legitimate renewal. The publisher is **not implemented or authorized** by this reader.

Cards are removed at expiry, on a failed refresh or when a refreshed collection withdraws the record. A null-time empty collection is the deliberate unavailable state, not a never-expiring accepted collection. Browser clock errors, suspended tabs and already downloaded copies prevent a guarantee of immediate global revocation. Return-to-visible rechecks the collection; real publication still requires the governed retention/publication procedure and current authority evidence. No cost or availability guarantee follows.

## Verification and residual gates

Synthetic integration checks cover Python producer compatibility, exact triple matching, duplicate/colliding identity, closed fields, canonical parsing, unsafe identifiers/citations, resource bounds, expiry, no-cache withdrawal and cancellation. Browser checks cover direct refresh, wrong/repeated query references, text-only markup, keyboard focus/disclosure, mobile width, dark mode, lifecycle remount, offline failure, withdrawal, expiry and no-JavaScript behavior. Browser fixtures are intercepted in memory and external requests blocked; none enter the published collection. Local tests use the existing browser/runtime with an in-process loopback test server; no tool installation or real image access is required.

The dedicated BKL-049 workflow runs the contract/engine suite on Windows and Linux. The portal workflow runs the browser suite before existing portal regressions. The new tests do not claim independent scientific acceptance or real gallery OAT.

Still required: the [governed external registration route](BKL-049-External-Origin-Registration-Plan.md), accepted real asset/context snapshot, exact retained binding, approved public aliases/fields, reviewed publisher with immutable public version policy, authorized preview access/upload and real end-to-end gallery OAT. F4 real binding, full F5 and BKL-049 remain OPEN. BKL-043 stays current.

Rollback reverts the additive panel, collection reader/schema and scripts, leaving the former fixture gallery and private archive intact. To withdraw future records, publish the reviewed empty collection; disabling this feature grants no authority to delete private originals or change cloud access.
