# Report sessione 2026-08-31_2026-09-01

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 32 |
| Pose LIGHT completate | 32 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 186 |
| Esposizioni tecniche stimate | 154 |
| Integrazione LIGHT totale | 5.33 h |
| Autofocus avviati | 22 |
| Autofocus completati | 9 |
| Autofocus falliti esplicitamente | 4 |
| Dither richiesti | 68 |
| Segmenti di guida PHD2 | 22 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 8972 |
| Campioni guida validi | 8194 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 492 |
| Campioni esclusi durante settling | 378 |
| Settling falliti | 8 |
| RMS AR | 8.831 arcsec |
| RMS DEC | 4.887 arcsec |
| RMS totale | 10.093 arcsec |
| Lost Star | 492 |
| PulseGuide failures | 0 |
| SQM minimo | 8.9100 mag/arcsec² |
| SQM medio | 17.5395 mag/arcsec² |
| SQM massimo | 20.4200 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 590 |

## Anomalie e osservazioni

- Autofocus falliti esplicitamente: 4

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/08/2026-08-31_2026-09-01/manifest.json`.
- Finestra dichiarata: 2026-08-31T19:00:00+02:00 → 2026-09-01T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 0. Log originali conservati.