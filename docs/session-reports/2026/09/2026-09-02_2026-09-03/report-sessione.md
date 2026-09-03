# Report sessione 2026-09-02_2026-09-03

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 78 |
| Pose LIGHT completate | 77 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 373 |
| Esposizioni tecniche stimate | 295 |
| Integrazione LIGHT totale | 12.83 h |
| Autofocus avviati | 40 |
| Autofocus completati | 19 |
| Autofocus falliti esplicitamente | 3 |
| Dither richiesti | 160 |
| Segmenti di guida PHD2 | 8 |
| Campioni guida validi | 10754 |
| RMS AR | 0.194 arcsec |
| RMS DEC | 0.147 arcsec |
| RMS totale | 0.244 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 18.1931 mag/arcsec² |
| SQM massimo | 20.8400 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 521 |

## Anomalie e osservazioni

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
