---
title: Chat AI read-only
---

<link rel="stylesheet" href="../styles/bkl042-chat.css">
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script type="module" src="../javascripts/bkl042-chat.js"></script>

<section class="dsg-bkl042-chat" data-bkl042-chat>
  <div class="dsg-bkl042-chat__hero"><span>BKL-042 · F6 BOUNDED CHAT</span><h1>Consultazione verificabile</h1><p>Consumer read-only con citazioni e gateway Google autenticato.</p></div>
  <div id="bkl042-google-signin" class="dsg-bkl042-chat__signin"></div>
  <p id="bkl042-chat-auth-status" class="dsg-bkl042-chat__auth-status">Accesso Google richiesto per la consultazione live; il fixture statico resta disponibile.</p>
  <div class="dsg-bkl042-chat__controls"><label for="bkl042-chat-case">Domanda dimostrativa</label><select id="bkl042-chat-case"></select></div>
  <button id="bkl042-chat-live" class="dsg-bkl042-chat__live" type="button" disabled>Invia al relay AI read-only</button>
  <article id="bkl042-chat-answer" class="dsg-bkl042-chat__answer" aria-live="polite"></article>
  <p class="dsg-bkl042-chat__boundary"><strong>Nessuna azione:</strong> la consultazione live usa solo il gateway autenticato e resta bounded read-only; non esegue tool, upload, PixInsight apply, comandi o remediation.</p>
</section>
