# Report sessione 2026-07-15_2026-07-16

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 81 |
| Pose LIGHT completate | 80 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 360 |
| Esposizioni tecniche stimate | 279 |
| Integrazione LIGHT totale | 13.33 h |
| Autofocus avviati | 52 |
| Autofocus completati | 26 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 162 |
| Segmenti di guida PHD2 | 27 |
| Campioni guida validi | 15950 |
| RMS AR | 0.368 arcsec |
| RMS DEC | 0.236 arcsec |
| RMS totale | 0.437 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 1230 |

## Anomalie e osservazioni

- Nessuna anomalia grave rilevata dai criteri v0.1.1.

## Note metodologiche

- Le esposizioni tecniche non sono conteggiate come pose LIGHT fallite.
- I segmenti PHD2 indicano avvii/arresti della guida e non sono automaticamente anomalie.
- I campioni PHD2 durante il settling sono esclusi dal calcolo RMS.
- Lo stato meteo Unsafe della finestra completa e informativo; la correlazione con sequenza attiva e cupola aperta sara introdotta nella versione successiva.

## Passo successivo

- `GREEN` o `YELLOW`: archiviazione ordinaria e verifica delle ottimizzazioni.
- `ORANGE` o `RED`: diagnostica di secondo livello e raccolta dei log specialistici.
