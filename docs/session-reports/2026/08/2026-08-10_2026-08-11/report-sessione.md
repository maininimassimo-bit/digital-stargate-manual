# Report sessione 2026-08-10_2026-08-11

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 0 |
| Pose LIGHT completate | 0 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 0 |
| Esposizioni tecniche stimate | 0 |
| Integrazione LIGHT totale | 0.00 h |
| Autofocus avviati | 0 |
| Autofocus completati | 0 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 0 |
| Segmenti di guida PHD2 | 3 |
| Campioni guida validi | 8456 |
| RMS AR | 0.198 arcsec |
| RMS DEC | 0.111 arcsec |
| RMS totale | 0.226 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| Righe meteo (finestra completa) | 3600 |
| Righe meteo Unsafe (finestra completa) | 527 |

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
