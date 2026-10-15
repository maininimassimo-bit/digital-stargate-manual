# Report sessione 2026-10-14_2026-10-15

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 68 |
| Pose LIGHT completate | 58 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 10 |
| Esposizioni camera totali | 125 |
| Esposizioni tecniche stimate | 57 |
| Integrazione LIGHT totale | 9.67 h |
| Autofocus avviati | 10 |
| Autofocus completati | 5 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 114 |
| Segmenti di guida PHD2 | 6 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 15461 |
| Campioni guida validi | 14974 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 1 |
| Campioni esclusi durante settling | 486 |
| Settling falliti | 3 |
| RMS AR | 1.083 arcsec |
| RMS DEC | 0.79 arcsec |
| RMS totale | 1.34 arcsec |
| Lost Star | 1 |
| PulseGuide failures | 0 |
| SQM minimo | 12.6100 mag/arcsec² |
| SQM medio | 20.5763 mag/arcsec² |
| SQM massimo | 20.9700 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 84 |

## Anomalie e osservazioni

- Pose LIGHT da verificare: fallite=0, non abbinate=10

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
