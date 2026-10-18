# Report sessione 2026-09-06_2026-09-07

**Stato:** `YELLOW`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose LIGHT avviate | 37 |
| Pose LIGHT completate | 37 |
| Pose LIGHT fallite esplicitamente | 0 |
| Pose LIGHT non abbinate/interrotte | 0 |
| Esposizioni camera totali | 203 |
| Esposizioni tecniche stimate | 166 |
| Integrazione LIGHT totale | 6.17 h |
| Autofocus avviati | 22 |
| Autofocus completati | 9 |
| Autofocus falliti esplicitamente | 4 |
| Dither richiesti | 72 |
| Segmenti di guida PHD2 | 22 |
| Profili PHD2 | C8_QHY695A, SW4P_EVO |
| Campioni guida totali | 7303 |
| Campioni guida validi | 6107 |
| Campioni saturi inclusi | 5935 |
| Campioni rifiutati | 765 |
| Campioni esclusi durante settling | 469 |
| Settling falliti | n/d |
| RMS AR | 2.505 arcsec |
| RMS DEC | 1.246 arcsec |
| RMS totale | 2.797 arcsec |
| Lost Star | 765 |
| PulseGuide failures | 0 |
| SQM minimo | 16.3100 mag/arcsec² |
| SQM medio | 20.7599 mag/arcsec² |
| SQM massimo | 21.0600 mag/arcsec² |
| Righe meteo (finestra completa) | 3960 |
| Righe meteo Unsafe (finestra completa) | 479 |

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


## Eventi PHD2 con attribuzione incerta

- Metodo: `DSG-PHD-EVENT-BOUNDS-1.0`. 1 eventi non collocabili con certezza nella finestra; il contatore interessato è `n/d`, non zero. Riferimenti e limiti temporali nel normalizzato sorgente.

## Attribuzione temporale

- Metodo: `DSG-MANIFEST-LIGHT-1.0`; manifest: `data/sessions/2026/09/2026-09-06_2026-09-07/manifest.json`.
- Finestra dichiarata: 2026-09-06T19:00:00+02:00 → 2026-09-07T06:00:00+02:00 (Europe/Rome); inizio incluso, fine esclusa.
- Le pose sono attribuite in base all’avvio; il completamento della stessa posa può oltrepassare la fine della finestra.
- Avvii LIGHT esterni esclusi: 0. Log originali conservati.