# Report sessione 2026-09-03_2026-09-04

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 34 |
| Pose LIGHT completate | 30 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 4 |
| Esposizioni camera totali | 81 |
| Esposizioni tecniche stimate | 47 |
| Integrazione LIGHT totale | 5.00 h |
| Autofocus avviati | 6 |
| Autofocus completati | 2 |
| Autofocus falliti esplicitamente | 2 |
| Dither richiesti | 62 |
| Segmenti di guida PHD2 | 7 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 9081 |
| Campioni guida validi | 8677 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 152 |
| Campioni esclusi durante settling | 252 |
| Settling falliti | 1 |
| RMS AR | 2.544 arcsec |
| RMS DEC | 7.741 arcsec |
| RMS totale | 8.148 arcsec |
| Lost Star | 152 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 18.4790 mag/arcsec² |
| SQM massimo | 20.9500 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 912 |

## Anomalie e osservazioni

- Pose LIGHT da verificare: fallite=0, non abbinate=4
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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/09/2026-09-03_2026-09-04/manifest.json`.
- Finestra dichiarata: 2026-09-03T19:00:00+02:00 → 2026-09-04T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 0. Log originali conservati.