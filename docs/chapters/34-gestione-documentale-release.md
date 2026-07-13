# Capitolo 34 – Gestione Documentale e Release

**Codice documento:** DSG-TM-001-34  
**Revisione:** 0.1 Draft

## 34.1 Scopo

Definire le regole con cui il repository Docs-as-Code diventa la fonte ufficiale del Manuale Tecnico Digital StarGate.

## 34.2 Fonte unica di verità

I file Markdown versionati nel repository costituiscono il sorgente ufficiale. Word, PDF e sito MkDocs sono prodotti derivati e non devono essere modificati manualmente come fonte primaria.

## 34.3 Struttura minima

```text
docs/
  chapters/
  appendices/
  assets/
templates/
scripts/
build/
release/
.github/workflows/
```

## 34.4 Regole di versionamento

Adottare versioni semanticamente leggibili:

- `0.x` per sviluppo;
- `1.0` per prima baseline approvata;
- `1.x` per aggiornamenti compatibili;
- `2.0` per revisioni architetturali rilevanti.

## 34.5 Procedura DSG-PROC-034-01 – Creazione release

1. Eseguire `mkdocs build --strict`.
2. Generare il Word con `build.ps1`.
3. Verificare indice, tabelle e immagini.
4. Aggiornare registro revisioni.
5. Creare commit di release.
6. Creare tag Git.
7. Pubblicare artifact e sito.

Esempio:

```powershell
git add .
git commit -m "Release DSG-TM-001 v0.8"
git tag -a v0.8 -m "DSG-TM-001 v0.8"
git push origin main --tags
```

## 34.6 Controlli pre-release

- nessun link rotto;
- nessun placeholder non classificato;
- tutti i capitoli presenti in `mkdocs.yml`;
- Word generato senza errori;
- registro revisioni aggiornato;
- file sensibili esclusi dal repository.

## 34.7 Conservazione

Conservare per ogni release:

- sorgente Git taggato;
- Word;
- PDF, quando disponibile;
- changelog;
- checksum degli artifact;
- data e responsabile della release.
