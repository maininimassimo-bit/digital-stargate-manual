# Report sessione 2026-07-14_2026-07-15

**Stato:** `GREEN`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 20 |
| Pose LIGHT completate | 19 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 209 |
| Esposizioni tecniche stimate | 189 |
| Integrazione LIGHT totale | 3.17 h |
| Autofocus avviati | 40 |
| Autofocus completati | 20 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 41 |
| Segmenti di guida PHD2 | 21 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 6254 |
| Campioni guida validi | 5996 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 0 |
| Campioni esclusi durante settling | 258 |
| Settling falliti | 0 |
| RMS AR | 0.448 arcsec |
| RMS DEC | 0.618 arcsec |
| RMS totale | 0.763 arcsec |
| Lost Star | 0 |
| PulseGuide failures | 0 |
| SQM minimo | n/d |
| SQM medio | n/d |
| SQM massimo | n/d |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 1251 |

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/07/2026-07-14_2026-07-15/manifest.json`.
- Finestra dichiarata: 2026-07-14T19:00:00+02:00 → 2026-07-15T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 29. Log originali conservati.