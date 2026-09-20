# Report sessione 2026-09-19_2026-09-20

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 16 |
| Pose LIGHT completate | 16 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 112 |
| Esposizioni tecniche stimate | 96 |
| Integrazione LIGHT totale | 2.67 h |
| Autofocus avviati | 12 |
| Autofocus completati | 6 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 31 |
| Segmenti di guida PHD2 | 15 |
| Profili PHD2 | C8_QHY695A |
| Campioni guida totali | 3402 |
| Campioni guida validi | 3048 |
| Campioni saturi inclusi | 448 |
| Campioni rifiutati | 126 |
| Campioni esclusi durante settling | 245 |
| Settling falliti | 20 |
| RMS AR | 1.36 arcsec |
| RMS DEC | 1.017 arcsec |
| RMS totale | 1.698 arcsec |
| Lost Star | 126 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9000 mag/arcsec² |
| SQM medio | 19.6055 mag/arcsec² |
| SQM massimo | 20.9900 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 352 |

## Anomalie e osservazioni

- Lost star ripetuti: 126

## Note metodologiche

- Le esposizioni tecniche non sono conteggiate come pose LIGHT fallite.
- I segmenti PHD2 indicano avvii/arresti della guida e non sono automaticamente anomalie.
- L RMS PHD2 usa RARawDistance e DECRawDistance, convertiti in arcsec con la scala pixel dichiarata in ciascun segmento.
- I campioni PHD2 durante il settling sono esclusi; ErrorCode 0 e STAR_SATURATED (1) sono inclusi nel calcolo RMS e i saturi restano tracciati separatamente.
- I valori SQM minimo, medio e massimo provengono dalla proiezione canonica della sessione; `n/d` indica che la sessione non dispone di telemetria SQM storicizzata.
- La telemetria SQM e scientifica e non costituisce Safety Authority.
- Lo stato meteo Unsafe della finestra completa e informativo; la correlazione con sequenza attiva e cupola aperta sara introdotta nella versione successiva.

## Passo successivo

- `GREEN` o `YELLOW`: archiviazione ordinaria e verifica delle ottimizzazioni.
- `ORANGE` o `RED`: diagnostica di secondo livello e raccolta dei log specialistici.
