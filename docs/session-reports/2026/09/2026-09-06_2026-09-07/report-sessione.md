# Report sessione 2026-09-06_2026-09-07

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 37 |
| Pose LIGHT completate | 37 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 203 |
| Esposizioni tecniche stimate | 166 |
| Integrazione LIGHT totale | 6.17 h |
| Autofocus avviati | 22 |
| Autofocus completati | 9 |
| Autofocus falliti esplicitamente | 6 |
| Dither richiesti | 72 |
| Segmenti di guida PHD2 | 22 |
| Campioni guida validi | 172 |
| RMS AR | 1.757 arcsec |
| RMS DEC | 0.519 arcsec |
| RMS totale | 1.832 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | 16.3100 mag/arcsec² |
| SQM medio | 20.7599 mag/arcsec² |
| SQM massimo | 21.0600 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 479 |

## Anomalie e osservazioni

- Autofocus falliti esplicitamente: 6

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
