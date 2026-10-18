# Report sessione 2026-08-14_2026-08-15

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 37 |
| Pose LIGHT completate | 37 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 127 |
| Esposizioni tecniche stimate | 90 |
| Integrazione LIGHT totale | 6.17 h |
| Autofocus avviati | 10 |
| Autofocus completati | 5 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 72 |
| Segmenti di guida PHD2 | 5 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 9803 |
| Campioni guida validi | 9513 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 0 |
| Campioni esclusi durante settling | 290 |
| Settling falliti | 0 |
| RMS AR | 0.947 arcsec |
| RMS DEC | 0.559 arcsec |
| RMS totale | 1.1 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | n/d |
| SQM medio | n/d |
| SQM massimo | n/d |
| Righe meteo (finestra completa) | 3970 |
| Righe meteo Unsafe (finestra completa) | 817 |

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


## Attribuzione temporale

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/08/2026-08-14_2026-08-15/manifest.json`.
- Finestra dichiarata: 2026-08-14T19:00:00+02:00 → 2026-08-15T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 0. Log originali conservati.