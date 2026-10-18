# Report sessione 2026-07-15_2026-07-16

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 32 |
| Pose LIGHT completate | 32 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 61 |
| Esposizioni tecniche stimate | 29 |
| Integrazione LIGHT totale | 5.33 h |
| Autofocus avviati | 4 |
| Autofocus completati | 2 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 64 |
| Segmenti di guida PHD2 | 6 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 10288 |
| Campioni guida validi | 9954 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 94 |
| Campioni esclusi durante settling | 240 |
| Settling falliti | 0 |
| RMS AR | 1.989 arcsec |
| RMS DEC | 0.866 arcsec |
| RMS totale | 2.17 arcsec |
| Lost Star | 94 |
| PulseGuide failures | 0 |
| SQM minimo | n/d |
| SQM medio | n/d |
| SQM massimo | n/d |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 1230 |

## Anomalie e osservazioni

- Lost star ripetuti: 94

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/07/2026-07-15_2026-07-16/manifest.json`.
- Finestra dichiarata: 2026-07-15T19:00:00+02:00 → 2026-07-16T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 49. Log originali conservati.