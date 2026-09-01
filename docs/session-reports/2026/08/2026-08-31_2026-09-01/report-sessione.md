# Report sessione 2026-08-31_2026-09-01

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 32 |
| Pose LIGHT completate | 32 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 186 |
| Esposizioni tecniche stimate | 154 |
| Integrazione LIGHT totale | 5.33 h |
| Autofocus avviati | 22 |
| Autofocus completati | 9 |
| Autofocus falliti esplicitamente | 6 |
| Dither richiesti | 68 |
| Segmenti di guida PHD2 | 22 |
| Campioni guida validi | 8119 |
| RMS AR | 0.388 arcsec |
| RMS DEC | 0.324 arcsec |
| RMS totale | 0.505 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 590 |

## Anomalie e osservazioni

- Autofocus falliti esplicitamente: 6

## Note metodologiche

- Le esposizioni tecniche non sono conteggiate come pose LIGHT fallite.
- I segmenti PHD2 indicano avvii/arresti della guida e non sono automaticamente anomalie.
- I campioni PHD2 durante il settling sono esclusi dal calcolo RMS.
- Lo stato meteo Unsafe della finestra completa e informativo; la correlazione con sequenza attiva e cupola aperta sara introdotta nella versione successiva.

## Passo successivo

- `GREEN` o `YELLOW`: archiviazione ordinaria e verifica delle ottimizzazioni.
- `ORANGE` o `RED`: diagnostica di secondo livello e raccolta dei log specialistici.
