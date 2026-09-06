# Report sessione 2026-09-05_2026-09-06

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 34 |
| Pose LIGHT completate | 33 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 125 |
| Esposizioni tecniche stimate | 91 |
| Integrazione LIGHT totale | 5.50 h |
| Autofocus avviati | 12 |
| Autofocus completati | 6 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 64 |
| Segmenti di guida PHD2 | 9 |
| Campioni guida validi | 8495 |
| RMS AR | 0.321 arcsec |
| RMS DEC | 0.468 arcsec |
| RMS totale | 0.568 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 19.1400 mag/arcsec² |
| SQM massimo | 20.9800 mag/arcsec² |
| Righe meteo (finestra completa) | 3958 |
| Righe meteo Unsafe (finestra completa) | 1037 |

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
