# Report sessione 2026-07-16_2026-07-17

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 63 |
| Pose LIGHT completate | 63 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 139 |
| Esposizioni tecniche stimate | 76 |
| Integrazione LIGHT totale | 10.50 h |
| Autofocus avviati | 10 |
| Autofocus completati | 5 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 125 |
| Segmenti di guida PHD2 | 9 |
| Campioni guida validi | 18809 |
| RMS AR | 0.338 arcsec |
| RMS DEC | 0.208 arcsec |
| RMS totale | 0.397 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| Righe meteo (finestra completa) | 4680 |
| Righe meteo Unsafe (finestra completa) | 1943 |

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
