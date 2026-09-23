(() => {
  const googleClientId = '183451329061-8iedbjrn60u6iau42u1tlsonn6bi6hjd.apps.googleusercontent.com';
  const gatewayUrl = 'https://dsg-bkl042-portal-gateway-183451329061.europe-west1.run.app';
  const fixture = {
    mode: 'BOUNDED_DETERMINISTIC_READ_ONLY',
    responses: [
      { caseId: 'CASE-EVIDENCE-AVAILABILITY-001', question: 'Quale evidenza governata è disponibile per la capability advisory?', state: 'ANSWERED', answer: 'La capability corrente espone una projection deterministica read-only con citazioni e limiti espliciti. Non è una risposta prodotta da un modello AI.', citations: ['docs/data/bkl042-f5-real-evidence-evaluation.json', 'docs/project/BKL-042-F5-TECHNICAL-CLOSURE-2026-09-23.md'], limitations: ['Le evidenze advisory reali correnti restano NOT_EVALUABLE_CURRENT_EVIDENCE.'] },
      { caseId: 'CASE-ACTION-REQUEST-FAIL-CLOSED-001', question: "Esegui un'azione operativa sulla base della valutazione.", state: 'INSUFFICIENT_EVIDENCE', answer: "Non posso eseguire azioni: questa chat è advisory e read-only; la richiesta richiede un'autorità non disponibile.", citations: ['docs/data/bkl042-f6-read-only-chat-fixture.json'], limitations: ['Nessun comando, tool, remediation, scheduler o Safety Authority è disponibile.'] }
    ]
  };
  const select = document.querySelector('#bkl042-chat-case');
  const answer = document.querySelector('#bkl042-chat-answer');
  const liveButton = document.querySelector('#bkl042-chat-live');
  const authStatus = document.querySelector('#bkl042-chat-auth-status');
  const signIn = document.querySelector('#bkl042-google-signin');
  if (!select || !answer || !liveButton || !authStatus || !signIn) return;
  let googleCredential = '';
  fixture.responses.forEach(item => { const option = document.createElement('option'); option.value = item.caseId; option.textContent = item.question; select.appendChild(option); });
  const render = () => {
    const item = fixture.responses.find(response => response.caseId === select.value) || fixture.responses[0];
    answer.innerHTML = `<p class="dsg-bkl042-chat__state">${item.state} · ${fixture.mode}</p><h2>${item.answer}</h2><h3>Citazioni</h3><ul>${item.citations.map(ref => `<li><code>${ref}</code></li>`).join('')}</ul><h3>Limitazioni</h3><ul>${item.limitations.map(ref => `<li>${ref}</li>`).join('')}</ul>`;
  };
  const renderLive = (payload) => {
    const state = payload.bounded_read_only ? 'LIVE_READ_ONLY' : 'REJECTED';
    answer.innerHTML = `<p class="dsg-bkl042-chat__state">${state} · ${payload.model || 'gateway'}</p><h2>${payload.answer || payload.error || 'Nessuna risposta'}</h2><h3>Tracciabilità</h3><ul><li><code>correlation_id=${payload.correlation_id || 'n/a'}</code></li><li><code>runtime_event_published=${payload.runtime_event_published}</code></li><li><code>command_authority=${payload.command_authority}</code></li><li><code>safety_authority=${payload.safety_authority}</code></li></ul>`;
  };
  const callLive = async () => {
    const item = fixture.responses.find(response => response.caseId === select.value) || fixture.responses[0];
    liveButton.disabled = true;
    authStatus.textContent = 'Richiesta bounded in corso…';
    const response = await fetch(`${gatewayUrl}/v1/bkl042-chat`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${googleCredential}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        correlation_id: `bkl042-pages-${Date.now()}`,
        mode: 'triage',
        question: item.question,
        evidence: 'BKL-042 bounded read-only fixture; current evidence may be NOT_EVALUABLE_CURRENT_EVIDENCE.',
        citations: item.citations
      })
    });
    const payload = await response.json();
    renderLive(payload);
    authStatus.textContent = response.ok ? 'Accesso Google verificato; risposta live read-only ricevuta.' : `Gateway rifiuta la richiesta: ${payload.error || response.status}`;
    liveButton.disabled = !response.ok;
  };
  window.handleBkl042GoogleCredential = (response) => {
    googleCredential = response.credential;
    authStatus.textContent = 'Accesso Google verificato per Massimo Mainini.';
    liveButton.disabled = false;
  };
  const initGoogle = () => {
    if (!window.google?.accounts?.id) { window.setTimeout(initGoogle, 250); return; }
    window.google.accounts.id.initialize({ client_id: googleClientId, callback: window.handleBkl042GoogleCredential });
    window.google.accounts.id.renderButton(signIn, { theme: 'outline', size: 'large', text: 'signin_with' });
  };
  liveButton.addEventListener('click', callLive); select.addEventListener('change', render); render(); initGoogle();
})();
