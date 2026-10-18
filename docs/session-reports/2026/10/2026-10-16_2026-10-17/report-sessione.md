# Report sessione 2026-10-16_2026-10-17

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 23 |
| Pose LIGHT completate | 22 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 1 |
| Esposizioni camera totali | 59 |
| Esposizioni tecniche stimate | 36 |
| Integrazione LIGHT totale | 3.67 h |
| Autofocus avviati | 6 |
| Autofocus completati | 3 |
| Autofocus falliti esplicitamente | 0 |
| Dither richiesti | 43 |
| Segmenti di guida PHD2 | 4 |
| Profili PHD2 | SW4P_EVO |
| Campioni guida totali | 6066 |
| Campioni guida validi | 5774 |
| Campioni saturi inclusi | 0 |
| Campioni rifiutati | 144 |
| Campioni esclusi durante settling | 148 |
| Settling falliti | 0 |
| RMS AR | 0.743 arcsec |
| RMS DEC | 0.628 arcsec |
| RMS totale | 0.973 arcsec |
| Lost Star | 144 |
| PulseGuide failures | 0 |
| SQM minimo | 13.1800 mag/arcsec² |
| SQM medio | 20.3411 mag/arcsec² |
| SQM massimo | 20.7800 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 66 |

## Anomalie e osservazioni

- Lost star ripetuti: 144

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

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/10/2026-10-16_2026-10-17/manifest.json`.
- Finestra dichiarata: 2026-10-16T19:00:00+02:00 → 2026-10-17T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 0. Log originali conservati.