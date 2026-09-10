# Portal Publication Guidelines

| Campo | Valore |
|---|---|
| Identificativo | DSG-DEV-001 |
| Versione | 2.0 |
| Stato | Active |
| Data | 10/09/2026 |
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

L'aggiunta di una nuova projection session-driven richiede modifica atomica a generatore, governed_paths, test e documentazione. Un nuovo consumer di projection esistenti non deve ampliare permessi o automazioni di push/deploy.

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
| 2.0 | 10/09/2026 | Active | Governance dinamica e quality gate UI 7.0; ARB-UI-7 APPROVED |
