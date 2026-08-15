# Report sessione 2026-08-14_2026-08-15

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 37 |
| Pose LIGHT completate | 37 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 127 |
| Esposizioni tecniche stimate | 90 |
| Integrazione LIGHT totale | 6.17 h |
| Autofocus avviati | 10 |
| Autofocus completati | 5 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 72 |
| Segmenti di guida PHD2 | 5 |
| Campioni guida validi | 9513 |
| RMS AR | 0.208 arcsec |
| RMS DEC | 0.139 arcsec |
| RMS totale | 0.25 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| Righe meteo (finestra completa) | 3970 |
| Righe meteo Unsafe (finestra completa) | 817 |

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
