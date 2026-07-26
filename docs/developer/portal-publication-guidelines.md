# Portal Publication Guidelines

| Campo | Valore |
|---|---|
| Documento | Portal Publication Guidelines |
| Identificativo | DSG-DEV-001 |
| Versione | 1.0 |
| Stato | Draft |
| Release | 4.0 M1 |

## 1. Scopo

Questo documento definisce il processo standard per pubblicare nuove pagine nel portale Digital StarGate.

## 2. Workflow

1. Creare una branch dedicata.
2. Realizzare il contenuto Markdown.
3. Riutilizzare i componenti del Design System.
4. Aggiornare `mkdocs.yml`.
5. Eseguire `mkdocs build --strict`.
6. Verificare il rendering in modalità chiara e scura.
7. Eseguire il commit con un messaggio descrittivo.

## 3. Convenzioni

- File in minuscolo.
- Nomi separati da trattini.
- Nessuno spazio nei nomi.
- Immagini sotto `docs/assets/images`.
- CSS condiviso in `docs/styles`.
- JavaScript condiviso in `docs/javascripts`.

## 4. Checklist pre-pubblicazione

- [ ] Titolo coerente con la navigazione.
- [ ] Collegamenti verificati.
- [ ] Immagini ottimizzate.
- [ ] Build MkDocs completata senza errori.
- [ ] Nessun file temporaneo nel repository.
- [ ] `git status` contiene solo modifiche previste.

## 5. Workflow Git

```text
feature/*
↓
Verifica locale
↓
mkdocs build --strict
↓
Commit
↓
Push
↓
Merge
```

## 6. Criteri di qualità

Ogni pagina deve:

- rispettare il Design System;
- essere responsive;
- utilizzare componenti esistenti;
- evitare duplicazioni;
- mantenere una struttura documentale coerente.

## 7. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 26/07/2026 | Prima emissione |
