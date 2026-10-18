# Report sessione 2026-07-16_2026-07-17

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 31 |
| Pose LIGHT completate | 31 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 76 |
| Esposizioni tecniche stimate | 45 |
| Integrazione LIGHT totale | 5.17 h |
| Autofocus avviati | 6 |
| Autofocus completati | 3 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 61 |
| Segmenti di guida PHD2 | 3 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 9412 |
| Campioni guida validi | 9105 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 69 |
| Campioni esclusi durante settling | 242 |
| Settling falliti | 1 |
| RMS AR | 0.337 arcsec |
| RMS DEC | 0.437 arcsec |
| RMS totale | 0.552 arcsec |
| Lost Star | 69 |
| PulseGuide failures | 0 |
| SQM minimo | n/d |
| SQM medio | n/d |
| SQM massimo | n/d |
| Righe meteo (finestra completa) | 4680 |
| Righe meteo Unsafe (finestra completa) | 1943 |

## Anomalie e osservazioni

- Lost star ripetuti: 69

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/07/2026-07-16_2026-07-17/manifest.json`.
- Finestra dichiarata: 2026-07-16T18:00:00+02:00 → 2026-07-17T07:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 32. Log originali conservati.