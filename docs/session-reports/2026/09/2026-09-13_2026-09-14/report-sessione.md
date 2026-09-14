# Report sessione 2026-09-13_2026-09-14

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 27 |
| Pose LIGHT completate | 27 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 91 |
| Esposizioni tecniche stimate | 64 |
| Integrazione LIGHT totale | 4.50 h |
| Autofocus avviati | 8 |
| Autofocus completati | 4 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 52 |
| Segmenti di guida PHD2 | 7 |
| Profili PHD2 | C8_QHY695A |
| Campioni guida totali | 6189 |
| Campioni guida validi | 5501 |
| Campioni saturi inclusi | 5501 |
| Campioni rifiutati | 346 |
| Campioni esclusi durante settling | 358 |
| Settling falliti | 26 |
| RMS AR | 1.21 arcsec |
| RMS DEC | 0.731 arcsec |
| RMS totale | 1.414 arcsec |
| Lost Star | 346 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9000 mag/arcsec² |
| SQM medio | 19.5977 mag/arcsec² |
| SQM massimo | 21.0300 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 414 |

## Anomalie e osservazioni

- Lost star ripetuti: 346

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
