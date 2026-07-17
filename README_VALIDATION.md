# Workflow di validazione DSG-TM-001

## Installazione

Copia la cartella `scripts` nella root del repository.

## Estrazione dei campi

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\find-validation.ps1 `
  -RepoRoot "." `
  -OutputDir ".\reports"
```

Output:
- `reports\registro-validazioni.csv`
- `reports\registro-validazioni.md`
- `reports\riepilogo-validazioni.txt`

## Stati ammessi

- Aperto
- In verifica
- Validato
- Non applicabile
- Rinviato

## Priorita

- P1: sicurezza e continuita operativa
- P2: configurazioni necessarie alla ripetibilita
- P3: dati descrittivi o editoriali

## Regola di chiusura

Per lo stato `Validato` sono obbligatori:
- ValoreConfermato
- Fonte
- ValidatoDa
- DataValidazione

## Controllo formale

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-validation-register.ps1 `
  -CsvPath ".\reports\registro-validazioni.csv"
```

Non inserire password, chiavi VPN, token o credenziali nel repository.
