# Capitolo 43 — Accettazione del manuale e release 1.0

**Codice documento:** DSG-TM-001-43  
**Revisione:** 1.0 Draft

## 43.1 Scopo

Il capitolo definisce i criteri per dichiarare il Manuale Tecnico Digital StarGate completo, verificato e idoneo alla pubblicazione come release 1.0.

## 43.2 Oggetti dell'accettazione

La release comprende:

- sorgenti Markdown;
- configurazione MkDocs;
- script di build;
- documento Word;
- eventuale PDF;
- sito statico;
- immagini e diagrammi;
- registri e modelli;
- cronologia Git;
- release notes.

## 43.3 Criteri documentali

| Criterio | Esito richiesto |
|---|---|
| Capitoli previsti presenti | 100% |
| Collegamenti interni validi | Nessun errore critico |
| Build MkDocs `--strict` | Superata |
| Build Word Pandoc | Superata |
| Indice Word | Generato e aggiornabile |
| Dati sensibili | Assenti dalla release pubblica |
| Dati da validare | Identificati chiaramente |
| Registro revisioni | Aggiornato |

## 43.4 Criteri tecnici

- procedure safety coerenti tra loro;
- nessuna contraddizione tra apertura, chiusura e recovery;
- configurazioni hardware associate agli asset corretti;
- riferimenti a software e driver verificati;
- test di failover e recovery documentati;
- inventario minimo disponibile;
- responsabilità assegnate.

## 43.5 Gate di release

### Gate G1 — Completezza

Tutti i capitoli, allegati e registri previsti sono presenti.

### Gate G2 — Coerenza

Terminologia, codici, riferimenti e procedure sono uniformi.

### Gate G3 — Validazione tecnica

Le parti critiche sono state confrontate con l'impianto reale.

### Gate G4 — Build

Word e sito vengono generati senza errori.

### Gate G5 — Approvazione

Il proprietario del documento approva formalmente la release.

## 43.6 Procedura DSG-PROC-043-001

1. creare un branch `release/v1.0`;
2. bloccare modifiche non essenziali;
3. eseguire `mkdocs build --strict`;
4. eseguire `build.ps1` e `release.ps1`;
5. controllare Word, sito e allegati;
6. aggiornare registro revisioni e release notes;
7. risolvere le non conformità;
8. creare il tag Git `v1.0.0`;
9. generare il pacchetto di release;
10. archiviare una copia immutabile.

## 43.7 Comandi Git consigliati

```powershell
git switch -c release/v1.0
git status
powershell -ExecutionPolicy Bypass -File .\release.ps1
git add .
git commit -m "Prepara release DSG-TM-001 v1.0"
git tag -a v1.0.0 -m "Digital StarGate Technical Manual v1.0"
git push origin release/v1.0 --tags
```

## 43.8 Verifica visuale del Word

Controllare almeno:

- copertina;
- indice;
- interruzioni di pagina;
- titoli isolati;
- tabelle oltre i margini;
- diagrammi leggibili;
- intestazioni e piè di pagina;
- numerazione;
- caratteri accentati;
- riferimenti alle appendici.

## 43.9 Non conformità

| Classe | Esempio | Effetto sulla release |
|---|---|---|
| Critica | Procedura safety errata | Release bloccata |
| Maggiore | Capitolo mancante o build fallita | Release bloccata |
| Minore | Refuso o impaginazione locale | Correzione pianificata |
| Osservazione | Miglioria futura | Non blocca |

## 43.10 Release notes

Le note devono includere:

- numero versione;
- data;
- contenuti aggiunti;
- correzioni;
- dati ancora da validare;
- incompatibilità note;
- istruzioni di aggiornamento;
- hash o tag Git.

## 43.11 Pacchetto di rilascio

Struttura suggerita:

```text
release/
├── DSG-TM-001_v1.0.docx
├── DSG-TM-001_v1.0.pdf
├── DSG-TM-001_Source_v1.0.zip
├── RELEASE-NOTES-v1.0.md
└── checksums.txt
```

## 43.12 Checklist DSG-CHK-043-001

- [ ] Gate G1 superato.
- [ ] Gate G2 superato.
- [ ] Gate G3 superato.
- [ ] Gate G4 superato.
- [ ] Gate G5 approvato.
- [ ] Tag Git creato.
- [ ] Pacchetto archiviato.
- [ ] Backup verificato.

## 43.13 Dati da validare

- formato ufficiale del PDF;
- firmatari dell'approvazione;
- destinazione dell'archivio immutabile;
- politica delle release successive;
- visibilità pubblica o privata del sito.
