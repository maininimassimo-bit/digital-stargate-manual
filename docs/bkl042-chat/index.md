---
title: Chat AI read-only
---

<link rel="stylesheet" href="../styles/bkl042-chat.css?v=bkl042-retrieval-20260923">
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script type="module" src="../javascripts/bkl042-chat.js?v=bkl042-retrieval-20260923"></script>

<h2 class="dsg-bkl042-chat-title">Chat AI read-only</h2>

<section class="dsg-bkl042-chat" data-bkl042-chat>
  <div class="dsg-bkl042-chat__hero"><span>BKL-042 · F6 BOUNDED CHAT</span><h1>Consultazione verificabile</h1><p>Consumer read-only con citazioni e gateway Google autenticato.</p></div>
  <div id="bkl042-google-signin" class="dsg-bkl042-chat__signin"></div>
  <p id="bkl042-chat-auth-status" class="dsg-bkl042-chat__auth-status">Accesso Google richiesto. Le risposte useranno esclusivamente le proiezioni pubbliche governate.</p>
  <div class="dsg-bkl042-chat__controls"><label for="bkl042-chat-question">Domanda</label><textarea id="bkl042-chat-question" rows="3" maxlength="12000" placeholder="Chiedi informazioni su sessioni astronomiche e proiezioni pubblicate…"></textarea></div>
  <button id="bkl042-chat-live" class="dsg-bkl042-chat__live" type="button" disabled>Invia al relay AI read-only</button>
  <article id="bkl042-chat-answer" class="dsg-bkl042-chat__answer" aria-live="polite"></article>
  <p class="dsg-bkl042-chat__boundary"><strong>Solo consultazione:</strong> il relay recupera dati da proiezioni pubbliche allowlistate e associa citazioni verificate. I dati storici o versionati non sono stato live. Nessun tool, upload, PixInsight apply, comando, remediation o Safety Authority è disponibile.</p>
</section>
