(() => {
  const googleClientId = '183451329061-8iedbjrn60u6iau42u1tlsonn6bi6hjd.apps.googleusercontent.com';
  const gatewayUrl = 'https://dsg-bkl042-portal-gateway-183451329061.europe-west1.run.app';
  const question = document.querySelector('#bkl042-chat-question');
  const answer = document.querySelector('#bkl042-chat-answer');
  const liveButton = document.querySelector('#bkl042-chat-live');
  const authStatus = document.querySelector('#bkl042-chat-auth-status');
  const signIn = document.querySelector('#bkl042-google-signin');
  if (!question || !answer || !liveButton || !authStatus || !signIn) return;
  let googleCredential = '';

  const render = (payload) => {
    answer.replaceChildren();
    const state = document.createElement('p');
    state.className = 'dsg-bkl042-chat__state';
    state.textContent = `${payload.state || 'ERRORE'} · ${payload.model || 'proiezioni governate'}`;
    answer.append(state);
    const text = document.createElement('p');
    text.textContent = payload.answer || payload.error || 'Risposta non disponibile.';
    answer.append(text);
    const appendItems = (title, items) => {
      if (!Array.isArray(items) || !items.length) return;
      const heading = document.createElement('h3'); heading.textContent = title; answer.append(heading);
      const list = document.createElement('ul');
      items.forEach((item) => {
        const li = document.createElement('li');
        li.textContent = typeof item === 'string' ? item : item.text || '';
        if (typeof item === 'object' && Array.isArray(item.citation_refs) && item.citation_refs.length) {
          li.append(document.createTextNode(` — fonti: ${item.citation_refs.join(', ')}`));
        }
        list.append(li);
      });
      answer.append(list);
    };
    appendItems('Fatti verificabili', payload.facts);
    appendItems('Interpretazione', payload.inferences);
    appendItems('Suggerimenti non vincolanti', payload.recommendations);
    if (Array.isArray(payload.citations) && payload.citations.length) {
      const heading = document.createElement('h3'); heading.textContent = 'Fonti'; answer.append(heading);
      const list = document.createElement('ul');
      payload.citations.forEach((citation) => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        const url = new URL(citation.url || '', 'https://maininimassimo-bit.github.io');
        if (url.origin === 'https://maininimassimo-bit.github.io' && url.pathname.startsWith('/digital-stargate-manual/')) {
          link.href = url.href; link.textContent = `${citation.title || citation.source_id || 'Fonte governata'} (${citation.ref || 'ref n/d'})`;
          link.rel = 'noopener'; li.append(link);
        } else {
          li.textContent = 'Fonte non disponibile: collegamento non valido.';
        }
        if (citation.freshness) { const small = document.createElement('small'); small.textContent = ` — ${citation.freshness}`; li.append(small); }
        if (citation.digest) { const digest = document.createElement('small'); digest.textContent = ` · ${citation.digest}`; li.append(digest); }
        list.append(li);
      });
      answer.append(list);
    }
    if (Array.isArray(payload.limitations) && payload.limitations.length) {
      const heading = document.createElement('h3'); heading.textContent = 'Limiti'; answer.append(heading);
      const list = document.createElement('ul');
      payload.limitations.forEach((value) => { const li = document.createElement('li'); li.textContent = value; list.append(li); });
      answer.append(list);
    }
    const trace = document.createElement('p');
    trace.textContent = `correlation_id=${payload.correlation_id || 'n/d'} · method=${payload.method_version || 'n/d'} · model=${payload.model || 'NONE'}`;
    answer.append(trace);
    if (Array.isArray(payload.sources) && payload.sources.length) {
      const sourceList = document.createElement('ul');
      payload.sources.forEach((source) => {
        const li = document.createElement('li');
        li.textContent = `${source.source_id || 'source'} · ${source.status || 'UNKNOWN'} · ${source.digest || 'digest unavailable'}`;
        sourceList.append(li);
      });
      answer.append(sourceList);
    }
    const boundary = document.createElement('p');
    boundary.textContent = `command_authority=${payload.command_authority || 'NONE'} · execution_authority=${payload.execution_authority || 'NONE'} · safety_authority=${payload.safety_authority || 'NONE'} · decision=${payload.human_decision_required ? 'HUMAN ONLY' : 'N/A'}`;
    answer.append(boundary);
  };

  const callLive = async () => {
    const prompt = question.value.trim();
    if (!prompt || prompt.length > 12000 || !googleCredential) return;
    liveButton.disabled = true;
    authStatus.textContent = 'Consultazione delle sole proiezioni pubbliche in corso…';
    try {
      const response = await fetch(`${gatewayUrl}/v1/bkl042-chat`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${googleCredential}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ correlation_id: `bkl042-pages-${crypto.randomUUID()}`, mode: 'consultative', question: prompt })
      });
      const payload = await response.json();
      render(payload);
      authStatus.textContent = response.ok ? 'Risposta bounded read-only ricevuta.' : `Richiesta non completata (${response.status}).`;
    } catch (_) {
      authStatus.textContent = 'Servizio temporaneamente non disponibile; nessuna risposta è stata prodotta.';
      render({ state: 'NON DISPONIBILE', answer: 'Riprova più tardi.', command_authority: 'NONE', safety_authority: 'NONE' });
    } finally {
      liveButton.disabled = !googleCredential || !question.value.trim();
    }
  };

  window.handleBkl042GoogleCredential = (response) => {
    googleCredential = response.credential;
    authStatus.textContent = 'Accesso Google verificato per Massimo Mainini.';
    liveButton.disabled = !question.value.trim();
  };
  const initGoogle = () => {
    if (!window.google?.accounts?.id) { window.setTimeout(initGoogle, 250); return; }
    window.google.accounts.id.initialize({ client_id: googleClientId, callback: window.handleBkl042GoogleCredential });
    window.google.accounts.id.renderButton(signIn, { theme: 'outline', size: 'large', text: 'signin_with' });
  };
  liveButton.addEventListener('click', callLive);
  question.addEventListener('input', () => { liveButton.disabled = !googleCredential || !question.value.trim(); });
  initGoogle();
})();
