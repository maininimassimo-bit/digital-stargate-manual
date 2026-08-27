# Report sessione 2026-08-26_2026-08-27

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 0 |
| Pose LIGHT completate | 0 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 539 |
| Esposizioni tecniche stimate | 539 |
| Integrazione LIGHT totale | 0.00 h |
| Autofocus avviati | 2 |
| Autofocus completati | 1 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 0 |
| Segmenti di guida PHD2 | 0 |
| Campioni guida validi | 0 |
| RMS AR | n/d |
| RMS DEC | n/d |
| RMS totale | n/d |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 1644 |

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
