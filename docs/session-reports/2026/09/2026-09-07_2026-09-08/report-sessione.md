# Report sessione 2026-09-07_2026-09-08

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 6 |
| Pose LIGHT completate | 4 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 2 |
| Esposizioni camera totali | 178 |
| Esposizioni tecniche stimate | 172 |
| Integrazione LIGHT totale | 0.67 h |
| Autofocus avviati | 10 |
| Autofocus completati | 3 |
| Autofocus falliti esplicitamente | 2 |
| Dither richiesti | 11 |
| Segmenti di guida PHD2 | 8 |
| Campioni guida validi | 0 |
| RMS AR | n/d |
| RMS DEC | n/d |
| RMS totale | n/d |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 19.4066 mag/arcsec² |
| SQM massimo | 21.0500 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 474 |

## Anomalie e osservazioni

- Pose LIGHT da verificare: fallite=0, non abbinate=2
- Autofocus falliti esplicitamente: 2

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
