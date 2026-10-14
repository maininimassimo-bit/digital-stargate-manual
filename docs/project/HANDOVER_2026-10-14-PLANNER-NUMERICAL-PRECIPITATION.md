# Planner: precipitazioni numericamente trascurabili — 14 ottobre 2026

Richiesta Owner: correggere pioggia indicata per giorni con cielo sereno.
Il run pubblico ICON-2I 2026101412 è aggiornato; il riepilogo classifica come
piovose tutte le 16 ore perché ogni incremento è positivo, ma il picco è
2.946505750977754e-16 mm. Nuvolosità media 4,65625%, 12 ore allo 0%.

La policy advisory 1.3 normalizza a zero solo (0, 1e-12] mm, conservando il
numero originale in `precipitationNumericalTraceMm`. È una tolleranza numerica
esplicita: non è stata derivata automaticamente dal packingError né autorizza
ad azzerare precipitazioni meteorologicamente significative entro quell'errore.
Tracce da 1e-7 mm, pioggia debole, ore indeterminate e altri vincoli restano
bloccanti. Tutti i consumatori e le finestre usano la stessa projection normalizzata.

Il comando governato `--normalize-existing` conserva orologi, origine e hash,
ricalcola fattori meteo e finestre e valida il risultato completo. Non introduce
provider traffic né rinnova la freshness. Le future acquisizioni applicano la
stessa correzione. I dettagli e il rollback sono nella
[specifica F9](../architecture/scientific-assets/BKL-031-F9-Repeatable-Current-Night-Planner.md#numerical-zero-for-negligible-positive-traces-14-october-2026).

Verifica richiesta: regressioni native Python, consumer e browser cielo/refesh,
CI exact-head, ARB indipendente, RQ successiva, gate post-merge, Pages e riscontro
pubblico. La ricevuta della PR deve riportare i risultati reali. Per la notte
esaminata i vincoli di vento/raffiche e di buio restano indipendenti: non è promessa
di finestre GO. Nessuna autorità di comando, Safety o readiness viene aggiunta.
