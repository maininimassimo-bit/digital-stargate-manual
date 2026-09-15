# Report sessione 2026-09-14_2026-09-15

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 22 |
| Pose LIGHT completate | 21 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 139 |
| Esposizioni tecniche stimate | 117 |
| Integrazione LIGHT totale | 3.50 h |
| Autofocus avviati | 14 |
| Autofocus completati | 6 |
| Autofocus falliti esplicitamente | 3 |
| Dither richiesti | 42 |
| Segmenti di guida PHD2 | 18 |
| Profili PHD2 | C8_QHY695A |
| Campioni guida totali | 5073 |
| Campioni guida validi | 4422 |
| Campioni saturi inclusi | 4422 |
| Campioni rifiutati | 321 |
| Campioni esclusi durante settling | 372 |
| Settling falliti | 26 |
| RMS AR | 1.346 arcsec |
| RMS DEC | 0.784 arcsec |
| RMS totale | 1.557 arcsec |
| Lost Star | 321 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9000 mag/arcsec² |
| SQM medio | 20.1101 mag/arcsec² |
| SQM massimo | 20.9300 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 501 |

## Anomalie e osservazioni

- Autofocus falliti esplicitamente: 3

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
