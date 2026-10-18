# Report sessione 2026-09-05_2026-09-06

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 34 |
| Pose LIGHT completate | 33 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 125 |
| Esposizioni tecniche stimate | 91 |
| Integrazione LIGHT totale | 5.50 h |
| Autofocus avviati | 12 |
| Autofocus completati | 6 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 64 |
| Segmenti di guida PHD2 | 9 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 9043 |
| Campioni guida validi | 8487 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 303 |
| Campioni esclusi durante settling | 258 |
| Settling falliti | 1 |
| RMS AR | 1.435 arcsec |
| RMS DEC | 1.387 arcsec |
| RMS totale | 1.996 arcsec |
| Lost Star | 303 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 19.1400 mag/arcsec² |
| SQM massimo | 20.9800 mag/arcsec² |
| Righe meteo (finestra completa) | 3958 |
| Righe meteo Unsafe (finestra completa) | 1037 |

## Anomalie e osservazioni

- Lost star ripetuti: 303

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/09/2026-09-05_2026-09-06/manifest.json`.
- Finestra dichiarata: 2026-09-05T19:00:00+02:00 → 2026-09-06T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 0. Log originali conservati.