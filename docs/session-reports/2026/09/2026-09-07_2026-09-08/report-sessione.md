# Report sessione 2026-09-07_2026-09-08

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 6 |
| Pose LIGHT completate | 4 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 2 |
| Esposizioni camera totali | 178 |
| Esposizioni tecniche stimate | 172 |
| Integrazione LIGHT totale | 0.67 h |
| Autofocus avviati | 10 |
| Autofocus completati | 3 |
| Autofocus falliti esplicitamente | 1 |
| Dither richiesti | 11 |
| Segmenti di guida PHD2 | 8 |
| Profili PHD2 | C8_QHY695A |
| Campioni guida totali | 821 |
| Campioni guida validi | 584 |
| Campioni saturi inclusi | 584 |
| Campioni rifiutati | 154 |
| Campioni esclusi durante settling | 87 |
| Settling falliti | 10 |
| RMS AR | 1.814 arcsec |
| RMS DEC | 0.846 arcsec |
| RMS totale | 2.001 arcsec |
| Lost Star | 154 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 19.4066 mag/arcsec² |
| SQM massimo | 21.0500 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 474 |

## Anomalie e osservazioni

- Pose LIGHT da verificare: fallite=0, non abbinate=2
- Autofocus falliti esplicitamente: 1

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/09/2026-09-07_2026-09-08/manifest.json`.
- Finestra dichiarata: 2026-09-07T19:00:00+02:00 → 2026-09-08T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 0. Log originali conservati.