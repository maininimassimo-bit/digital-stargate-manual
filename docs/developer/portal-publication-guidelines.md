# Portal Publication Guidelines

| Campo | Valore |
|---|---|
| Identificativo | DSG-DEV-001 |
| Versione | 2.1 |
| Stato | Active |
| Data | 14/10/2026 |
| Release | UI 7.0 |

## 1. Purpose

Definire come creare o modificare pagine del portale senza introdurre duplicazioni, contenuto stale o regressioni nella pubblicazione automatica.

## 2. Source rules

- GitHub è la source of truth.
- Roadmap, cataloghi e stato piattaforma sono projection, non authority.
- Una pagina dinamica deve dichiarare fonte, schema, freshness e fallback.
- I valori current non vengono copiati manualmente quando esiste una projection.
- Documenti datati restano snapshot storici e non vengono promossi come current.

## 3. Publication workflow

1. verificare main, package corrente e file sovrapposti;
2. definire percorso utente e fonte dei dati;
3. riusare DSG-UI-001 e i componenti esistenti;
4. mantenere URL e compatibility contract;
5. aggiornare mkdocs.yml;
6. eseguire generatori e regression test;
7. eseguire JavaScript syntax check e mkdocs build --strict;
8. ottenere review ARB e Release Quality quando il cambiamento è strutturale;
9. integrare con expected-head protection;
10. verificare workflow e Pages sul merge SHA.

## 4. Dynamic page checklist

Per ogni pagina popolata da dati:

- [ ] producer autorevole identificato;
- [ ] projection versionata identificata;
- [ ] trigger di rigenerazione definito;
- [ ] file incluso nel publish set;
- [ ] fetch no-store quando appropriato;
- [ ] loading, empty, error e stale state;
- [ ] missing evidence non convertita in zero;
- [ ] aggiornamento dopo nuova sessione coperto da test;
- [ ] deploy Pages attivato dopo il commit delle projection.

## 5. Session-driven surfaces

Il workflow analyze-session-automatic.yml deve rigenerare e pubblicare insieme le projection usate da:

- homepage, tramite catalogo e latest observation;
- latest observation;
- catalogo e dettaglio sessioni;
- report e indice;
- Analytics Center;
- Equipment Performance;
- Session Comparison;
- ulteriori projection esplicitamente dichiarate nel workflow.

Per una projection committata dal bot, l’aggiunta richiede modifica atomica a generatore, governed_paths, test e documentazione. Una projection prodotta solo nel build Pages, come session-package-transfer.json, deve invece essere generata prima del build/publish e restare fuori Git: non ampliare governed_paths per un artefatto ignorato. Un nuovo consumer di projection esistenti non deve ampliare permessi o automazioni di push/deploy.

## 6. UX and accessibility checklist

- [ ] task primario disponibile senza percorsi ridondanti;
- [ ] un solo H1;
- [ ] testo e controlli leggibili;
- [ ] navigazione da tastiera;
- [ ] focus visibile;
- [ ] stato non affidato al solo colore;
- [ ] mobile e zoom 200%;
- [ ] reduced motion;
- [ ] contenuto statico utile senza JavaScript;
- [ ] realtime e storico chiaramente distinti.

## 7. File conventions

- contenuti ordinari in minuscolo con trattini;
- immagini in docs/assets/images;
- CSS in docs/styles;
- JavaScript in docs/javascripts;
- classi con prefisso dsg-;
- niente script inline per logica riusabile;
- nessun asset temporaneo o locale nel repository.

## 8. Rollback

Il rollback ripristina file UI, navigation e generatori del commit precedente. Non modifica dataset sorgente, evidence di sessione, runtime EAGLE o Safety Authority.

## 9. Revision history

| Versione | Data | Stato | Descrizione |
|---|---|---|---|
| 1.0 | 26/07/2026 | Superseded | Workflow editoriale UI 6.1 |
| 2.0 | 10/09/2026 | Baseline storica | Governance dinamica e quality gate UI 7.0; ARB-UI-7 APPROVED |
| 2.1 | 14/10/2026 | Active | Consumer di catena, artefatto manifest build-only e brand comune; nessuna nuova authority |

## Addendum — manutenzione del portale immersivo (29/09/2026)

- Non copiare fixture dai prototipi nelle pagine produttive.
- Non associare stato di cupola o orientamento del modello a valori assenti/scaduti.
- Mantenere i marker `DSG:IMMERSIVE-SCENE` fuori dai blocchi rigenerati dalle pipeline.
- Non cambiare binding dei consumer per adattarli alla geometria del modello.
- Per aggiungere scene o aggiornare Three.js seguire
  [DSG-UI-IMMERSIVE-001](../ui/immersive-portal-implementation.md).
- Eseguire `verify-immersive-assets.mjs` e `test-immersive-portal.cjs`, oltre ai gate
  esistenti. Verificare tema chiaro/scuro, mobile, navigazione, riduzione movimento,
  assenza WebGL e round-trip della modalità essenziale.
- Il workflow Immersive portal validation esegue soltanto verifiche; il proprietario
  del deployment resta `deploy-pages.yml`.
- Registrare separatamente test locali, exact-head CI, review e deployment verificato.

## Manutenzione delle catene e del brand — 14 ottobre 2026

Usare il [riferimento implementativo](session-lineage-and-mission-control.md) per session detail e Mission Control: fonti distinte, identificatori esatti, fetch bounded/no-store, refresh visibile/manuale, ritiro e failure indipendenti. Valori correnti, inventario e pubblicazione non si correggono copiando i conteggi delle ricevute nelle tile. Discovery 203/203 e scheduler documentati sono storici, Manifest catalogo non equivale a pacchetto verificato, associazione Owner non equivale a esecuzione o RAW inventory.

Il logo comune è `docs/assets/images/dsg-brand-mark.png`: configurarlo in MkDocs/header/favicon e preservare trasparenza/proporzioni con CSS, senza introdurre copie per pagina. [Esiti PR587–589](../releases/2026-10-14-session-lineage-and-brand.md). Una riconciliazione documentale ha CI/review/merge/Pages propri; non riscrive retroattivamente le evidenze di acceptance.
