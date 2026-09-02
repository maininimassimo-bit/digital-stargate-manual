# Report sessione 2026-09-01_2026-09-02

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 59 |
| Pose LIGHT completate | 58 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 356 |
| Esposizioni tecniche stimate | 297 |
| Integrazione LIGHT totale | 9.67 h |
| Autofocus avviati | 42 |
| Autofocus completati | 18 |
| Autofocus falliti esplicitamente | 9 |
| Dither richiesti | 128 |
| Segmenti di guida PHD2 | 37 |
| Campioni guida validi | 17888 |
| RMS AR | 0.372 arcsec |
| RMS DEC | 0.383 arcsec |
| RMS totale | 0.534 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | n/d |
| SQM medio | n/d |
| SQM massimo | n/d |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 535 |

## Anomalie e osservazioni

- Autofocus falliti esplicitamente: 9

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
