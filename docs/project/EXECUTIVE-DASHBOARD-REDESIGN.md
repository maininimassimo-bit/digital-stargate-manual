# Executive Dashboard — redesign e aggiornamento automatico

La dashboard generata da build_dashboard_v31.py conserva i KPI e i calcoli esistenti. Nuovo layout coerente con il portale: Hero navy con anelli decorativi, navigazione interna, KPI compatti, grafico mensile SVG con ore e indicatori percentuali separati, barre per target e setup, dettagli espandibili e ricerca nelle ultime dodici sessioni.

I grafici sono generati dagli stessi aggregati delle tabelle. Non vengono modificati severity, soglie o interpretazione meteo. UNKNOWN resta visibile tra le configurazioni e non rappresenta un terzo setup identificato. I valori mancanti mantengono il trattino; le barre non impongono una lunghezza minima ai valori zero.

La pipeline scientifica richiama già refresh-analytics-center.sh dopo ogni importazione, che rigenera dashboard.md, finalizza severity e normalizza il timestamp dalle sorgenti. La modifica è nel generatore, non solo nell'HTML prodotto. Un hash dei tre dataset rende identificabile lo snapshot anche se il timestamp resta uguale. Il browser controlla la pagina ogni cinque minuti se visibile e aggiorna il contenuto quando cambia l'hash. In caso di errore conserva lo storico datato con avviso esplicito di aggiornamento non verificabile. Nessun nuovo backend o accesso ai dispositivi.

Accessibilità e prestazioni: HTML/SVG server-generated disponibile senza JavaScript, tabelle complete, focus visibile, ricerca da tastiera, grafici e tabelle con scorrimento interno su mobile, nessun loop WebGL o animazione continua aggiuntivi. Tema del portale mantenuto; i grafici usano un pannello scuro ad alto contrasto.
