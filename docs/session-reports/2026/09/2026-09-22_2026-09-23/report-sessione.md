# Report sessione 2026-09-22_2026-09-23

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 41 |
| Pose LIGHT completate | 38 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 3 |
| Esposizioni camera totali | 100 |
| Esposizioni tecniche stimate | 59 |
| Integrazione LIGHT totale | 6.33 h |
| Autofocus avviati | 8 |
| Autofocus completati | 4 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 77 |
| Segmenti di guida PHD2 | 0 |
| Profili PHD2 | n/d |
| Campioni guida totali | 0 |
| Campioni guida validi | 0 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 0 |
| Campioni esclusi durante settling | 0 |
| Settling falliti | 0 |
| RMS AR | n/d |
| RMS DEC | n/d |
| RMS totale | n/d |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9000 mag/arcsec² |
| SQM medio | 19.0268 mag/arcsec² |
| SQM massimo | 21.0500 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 3630 |

## Anomalie e osservazioni

- Pose LIGHT da verificare: fallite=0, non abbinate=3

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
