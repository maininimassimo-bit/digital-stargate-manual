# Report sessione 2026-10-14_2026-10-15

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 56 |
| Pose LIGHT completate | 56 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 105 |
| Esposizioni tecniche stimate | 49 |
| Integrazione LIGHT totale | 9.33 h |
| Autofocus avviati | 10 |
| Autofocus completati | 4 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 112 |
| Segmenti di guida PHD2 | 5 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 14928 |
| Campioni guida validi | 14458 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 0 |
| Campioni esclusi durante settling | 470 |
| Settling falliti | 3 |
| RMS AR | 1.094 arcsec |
| RMS DEC | 0.798 arcsec |
| RMS totale | 1.354 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | 12.6100 mag/arcsec² |
| SQM medio | 20.5763 mag/arcsec² |
| SQM massimo | 20.9700 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 84 |

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/10/2026-10-14_2026-10-15/manifest.json`.
- Finestra dichiarata: 2026-10-14T19:00:00+02:00 → 2026-10-15T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 2. Log originali conservati.