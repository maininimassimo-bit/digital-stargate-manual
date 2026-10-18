# Report sessione 2026-09-04_2026-09-05

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 42 |
| Pose LIGHT completate | 41 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 166 |
| Esposizioni tecniche stimate | 124 |
| Integrazione LIGHT totale | 6.83 h |
| Autofocus avviati | 16 |
| Autofocus completati | 7 |
| Autofocus falliti esplicitamente | 2 |
| Dither richiesti | 82 |
| Segmenti di guida PHD2 | 9 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 11195 |
| Campioni guida validi | 10541 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 343 |
| Campioni esclusi durante settling | 323 |
| Settling falliti | 1 |
| RMS AR | 1.617 arcsec |
| RMS DEC | 1.652 arcsec |
| RMS totale | 2.312 arcsec |
| Lost Star | 343 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 18.8514 mag/arcsec² |
| SQM massimo | 21.0100 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 509 |

## Anomalie e osservazioni

- Autofocus falliti esplicitamente: 2

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/09/2026-09-04_2026-09-05/manifest.json`.
- Finestra dichiarata: 2026-09-04T19:00:00+02:00 → 2026-09-05T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 0. Log originali conservati.