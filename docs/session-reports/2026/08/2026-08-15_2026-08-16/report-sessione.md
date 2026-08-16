# Report sessione 2026-08-15_2026-08-16

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 71 |
| Pose LIGHT completate | 69 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 2 |
| Esposizioni camera totali | 255 |
| Esposizioni tecniche stimate | 184 |
| Integrazione LIGHT totale | 11.50 h |
| Autofocus avviati | 18 |
| Autofocus completati | 8 |
| Autofocus falliti esplicitamente | 2 |
| Dither richiesti | 139 |
| Segmenti di guida PHD2 | 11 |
| Campioni guida validi | 15866 |
| RMS AR | 0.2 arcsec |
| RMS DEC | 0.122 arcsec |
| RMS totale | 0.234 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 803 |

## Anomalie e osservazioni

- Pose LIGHT da verificare: fallite=0, non abbinate=2
- Autofocus falliti esplicitamente: 2

## Note metodologiche

- Le esposizioni tecniche non sono conteggiate come pose LIGHT fallite.
- I segmenti PHD2 indicano avvii/arresti della guida e non sono automaticamente anomalie.
- I campioni PHD2 durante il settling sono esclusi dal calcolo RMS.
- Lo stato meteo Unsafe della finestra completa e informativo; la correlazione con sequenza attiva e cupola aperta sara introdotta nella versione successiva.

## Passo successivo

- `GREEN` o `YELLOW`: archiviazione ordinaria e verifica delle ottimizzazioni.
- `ORANGE` o `RED`: diagnostica di secondo livello e raccolta dei log specialistici.
