# Release Notes 4.2

## Obiettivo

Rendere ogni build osservabile, misurabile e ricostruibile.

## Nuovo modello di esecuzione

Ogni build riceve un identificatore univoco e produce:

1. un log testuale;
2. un report strutturato dell'ultima esecuzione;
3. una riga nello storico permanente.

## Stati supportati

Build:

- `running`
- `success`
- `failed`

Step:

- `pending`
- `running`
- `success`
- `failed`

Gli step esclusi dal piano sono riportati separatamente con la motivazione.

## Compatibilità

La Release 4.2 mantiene:

- `platform.yml`;
- `pipeline.yml`;
- il motore delle dipendenze della Release 4.1;
- gli argomenti `--skip-dashboard`, `--skip-status` e `--skip-homepage`.

Aggiunge:

- `--verbose`.
