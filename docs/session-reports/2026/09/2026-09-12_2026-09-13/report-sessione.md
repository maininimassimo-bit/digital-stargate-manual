# Report sessione 2026-09-12_2026-09-13

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 29 |
| Pose LIGHT completate | 28 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 63 |
| Esposizioni tecniche stimate | 34 |
| Integrazione LIGHT totale | 4.67 h |
| Autofocus avviati | 4 |
| Autofocus completati | 2 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 57 |
| Segmenti di guida PHD2 | 3 |
| Campioni guida validi | 7387 |
| RMS AR | 0.344 arcsec |
| RMS DEC | 0.184 arcsec |
| RMS totale | 0.39 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9000 mag/arcsec² |
| SQM medio | 19.6158 mag/arcsec² |
| SQM massimo | 21.0600 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 467 |

## Anomalie e osservazioni

- Nessuna anomalia grave rilevata dai criteri v0.2.0.

## Note metodologiche

- Le esposizioni tecniche non sono conteggiate come pose LIGHT fallite.
- I segmenti PHD2 indicano avvii/arresti della guida e non sono automaticamente anomalie.
- I campioni PHD2 durante il settling sono esclusi dal calcolo RMS.
- I valori SQM minimo, medio e massimo provengono dalla proiezione canonica della sessione; `n/d` indica che la sessione non dispone di telemetria SQM storicizzata.
- La telemetria SQM e scientifica e non costituisce Safety Authority.
- Lo stato meteo Unsafe della finestra completa e informativo; la correlazione con sequenza attiva e cupola aperta sara introdotta nella versione successiva.

## Passo successivo

- `GREEN` o `YELLOW`: archiviazione ordinaria e verifica delle ottimizzazioni.
- `ORANGE` o `RED`: diagnostica di secondo livello e raccolta dei log specialistici.
