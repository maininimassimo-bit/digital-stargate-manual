# Release Playbook

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-REL-001 |
| Versione | 1.1 |
| Stato | Active |

## 1. Scopo

Definire il processo obbligatorio per preparare, validare, pubblicare e accettare una release o hotfix del Digital StarGate Enterprise Portal e degli artefatti correlati.

## 2. Tipi di rilascio

- **Major/Minor release**: nuove capability, boundary o contratti.
- **Patch/Hotfix**: correzione circoscritta senza modifica di authority o invarianti.
- **Documentation release**: aggiornamenti governati a documentazione, roadmap o evidence.
- **Architecture package release**: pacchetto coerente con AP, ADR, review, roadmap e traceability.

## 3. Pre-release gate

Prima del commit finale:

1. verificare branch e commit corrente;
2. identificare file e componenti coinvolti;
3. aggiornare context, backlog, debt e decision log quando applicabile;
4. verificare link e navigazione;
5. eseguire i quality gate applicabili;
6. registrare test eseguiti e non eseguiti;
7. assicurare rollback o ripristino documentato.

## 4. Quality gate standard

```bash
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release --no-restore
dotnet test DigitalStarGate.sln --configuration Release --no-build
dotnet format DigitalStarGate.sln --verify-no-changes --no-restore
mkdocs build --strict
```

Per il portale aggiungere:

- light/dark;
- refresh diretto;
- Instant Navigation;
- desktop/tablet;
- tastiera e focus;
- pagine principali e componenti toccati.

## 5. Commit e push

- commit coerente e atomico;
- Conventional Commit;
- nessuna affermazione di successo non verificata;
- push su branch previsto;
- per modifiche rilevanti usare PR con descrizione, rischio, test e rollback.

## 6. GitHub Actions

Workflow autorevoli:

- `developer-foundation.yml` per restore, build, test, format e MkDocs;
- `deploy-pages.yml` per build e deploy GitHub Pages;
- workflow specialistici per history, session package e analisi scientifica.

Un commit non prova il deployment. La release è pubblicata solo dopo workflow positivo e verifica del sito.

### 6.1 Merge senza ruleset

Quando `main` non dispone di ruleset o branch protection, `W-DSG-AEM-RULESET-001` è applicabile soltanto con exact-head CI completa, branch zero behind, PR mergeable, nessun Blocker/Major, Minor disposta, rollback e classificazione dati verificati. L'uso deve essere commentato nella PR e seguito da verifica post-merge sul merge SHA.

## 7. Release Acceptance Review

Verificare:

- contenuto atteso pubblicato;
- nessuna regressione evidente;
- navigation e link corretti;
- tema e responsive layout;
- dataset coerenti con authority;
- stato e versioni corretti;
- errori console e richieste fallite;
- backlog e technical debt aggiornati.

Gli esiti sono: `Accepted`, `Accepted with conditions`, `Rejected`, `Rolled back`.

## 8. Hotfix

Una hotfix deve:

- avere scope minimo;
- rimuovere la causa, non solo mascherare il sintomo;
- evitare nuove responsabilità nel componente errato;
- includere test di non regressione;
- aggiornare release state e context.

## 9. Rollback

Il rollback deve identificare:

- commit stabile precedente;
- file/dataset coinvolti;
- eventuale invalidazione di cache o artifact;
- verifica Pages dopo il ripristino;
- aggiornamento del Decision Log e del backlog.

## 10. Definition of Done

La release è completata solo quando commit, push, workflow, deployment, verifica visiva e aggiornamento governance risultano tutti tracciati.
