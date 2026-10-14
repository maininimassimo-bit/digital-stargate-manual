# Report sessione 2026-10-13_2026-10-14

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 57 |
| Pose LIGHT completate | 57 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 125 |
| Esposizioni tecniche stimate | 68 |
| Integrazione LIGHT totale | 9.50 h |
| Autofocus avviati | 12 |
| Autofocus completati | 6 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 113 |
| Segmenti di guida PHD2 | 7 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 14950 |
| Campioni guida validi | 14500 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 0 |
| Campioni esclusi durante settling | 450 |
| Settling falliti | 6 |
| RMS AR | 1.056 arcsec |
| RMS DEC | 1.331 arcsec |
| RMS totale | 1.699 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | 11.7000 mag/arcsec² |
| SQM medio | 20.5353 mag/arcsec² |
| SQM massimo | 20.9100 mag/arcsec² |
| Righe meteo (finestra completa) | 3958 |
| Righe meteo Unsafe (finestra completa) | 104 |

## Anomalie e osservazioni

- Nessuna anomalia grave rilevata dai criteri v0.2.0.

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
