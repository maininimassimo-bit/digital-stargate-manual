# Report sessione 2026-09-01_2026-09-02

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 37 |
| Pose LIGHT completate | 36 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 231 |
| Esposizioni tecniche stimate | 194 |
| Integrazione LIGHT totale | 6.00 h |
| Autofocus avviati | 26 |
| Autofocus completati | 12 |
| Autofocus falliti esplicitamente | 2 |
| Dither richiesti | 79 |
| Segmenti di guida PHD2 | 15 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 10218 |
| Campioni guida validi | 9769 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 130 |
| Campioni esclusi durante settling | 319 |
| Settling falliti | 0 |
| RMS AR | 1.569 arcsec |
| RMS DEC | 1.299 arcsec |
| RMS totale | 2.036 arcsec |
| Lost Star | 130 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 17.7380 mag/arcsec² |
| SQM massimo | 20.9200 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 535 |

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/09/2026-09-01_2026-09-02/manifest.json`.
- Finestra dichiarata: 2026-09-01T19:00:00+02:00 → 2026-09-02T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 22. Log originali conservati.