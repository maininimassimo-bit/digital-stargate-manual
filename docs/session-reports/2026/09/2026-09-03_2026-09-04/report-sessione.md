# Report sessione 2026-09-03_2026-09-04

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 34 |
| Pose LIGHT completate | 30 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 4 |
| Esposizioni camera totali | 81 |
| Esposizioni tecniche stimate | 47 |
| Integrazione LIGHT totale | 5.00 h |
| Autofocus avviati | 6 |
| Autofocus completati | 2 |
| Autofocus falliti esplicitamente | 3 |
| Dither richiesti | 62 |
| Segmenti di guida PHD2 | 7 |
| Campioni guida validi | 8676 |
| RMS AR | 0.579 arcsec |
| RMS DEC | 2.657 arcsec |
| RMS totale | 2.72 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 18.4790 mag/arcsec² |
| SQM massimo | 20.9500 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 912 |

## Anomalie e osservazioni

- Pose LIGHT da verificare: fallite=0, non abbinate=4
- Autofocus falliti esplicitamente: 3

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
