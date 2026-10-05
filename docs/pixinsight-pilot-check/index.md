# Verifica privata del pilota PixInsight

Questa pagina serve alla prova di accesso P4. Usa una richiesta di prova che viene subito annullata: non carica foto, non avvia PixInsight e non pubblica immagini. L’accesso è riservato al proprietario.

<div data-piai-check>
  <label>Indirizzo del servizio approvato <input data-piai-origin type="url" autocomplete="off" placeholder="https://…run.app" /></label>
  <button data-piai-connect type="button">Verifica servizio e accedi</button>
  <div data-piai-signin></div>
  <p data-piai-message role="status">Inserisci l’indirizzo comunicato per la prova.</p>
  <button data-piai-probe type="button" disabled>Verifica accesso e annulla la prova</button>
  <pre data-piai-result></pre>
</div>

La credenziale Google rimane solo nella memoria di questa pagina. Il risultato riporta identificativi di prova; nessun token viene salvato o mostrato. Se la connessione si interrompe, ripeti il pulsante nella stessa pagina: viene mantenuta la stessa richiesta. Dopo la prova non è abilitato alcun comando di elaborazione dal portale.

[Piano e limiti del pilota](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md)
