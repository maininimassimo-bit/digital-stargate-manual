# Collaudo privato P6 — ambiente isolato

Prova approvata dall’Owner il 7 ottobre 2026, separata dal pilota operativo. Usa soltanto richieste e immagini sintetiche: nessuna foto è caricata, accettata o pubblicata. La pagina non avvia PixInsight. Le credenziali Google rimangono in memoria; il servizio verifica l’identità Owner.

<div data-piai-p6-check>
  <button data-p6-connect type="button">Accedi al collaudo isolato</button>
  <div data-p6-signin></div>
  <p data-p6-message role="status">Accedi per verificare il servizio di prova.</p>
  <button data-p6-probe type="button" disabled>Verifica richieste concorrenti e annulla la prova</button>
  <button data-p6-prepare type="button" disabled>Prepara due job per la prova di recupero</button>
  <button data-p6-status type="button" disabled>Leggi stato dei due job di recupero</button>
  <pre data-p6-result></pre>
</div>

La prova di recupero interrompe soltanto un’istanza PixInsight isolata su copie sintetiche. Il comportamento atteso è **RECOVERY_REQUIRED** con prenotazione conservata e secondo job ancora in coda. Nessun replay, sblocco o riassegnazione automatici. Un'interruzione della connessione richiede di conservare questa pagina e ripetere la medesima operazione: le identità restano stabili finché la pagina rimane aperta.

Il servizio serializza le richieste: due chiamate client contemporanee non attestano un interleaving CAS interno. Il collaudo non dimostra perdita di alimentazione, ripartenza del desktop o recupero automatico.

[Perimetro P6 e prove storiche](../project/PIAI-P6-CANDIDATE-2026-10-06.md). La chiusura richiede le evidenze reali, la riconciliazione e l'accettazione operativa finale Owner.
