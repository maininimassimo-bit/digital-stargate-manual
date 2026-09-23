(() => {
  const fixture = {
    mode: 'BOUNDED_DETERMINISTIC_READ_ONLY',
    responses: [
      { caseId: 'CASE-EVIDENCE-AVAILABILITY-001', question: 'Quale evidenza governata è disponibile per la capability advisory?', state: 'ANSWERED', answer: 'La capability corrente espone una projection deterministica read-only con citazioni e limiti espliciti. Non è una risposta prodotta da un modello AI.', citations: ['docs/data/bkl042-f5-real-evidence-evaluation.json', 'docs/project/BKL-042-F5-TECHNICAL-CLOSURE-2026-09-23.md'], limitations: ['Le evidenze advisory reali correnti restano NOT_EVALUABLE_CURRENT_EVIDENCE.'] },
      { caseId: 'CASE-ACTION-REQUEST-FAIL-CLOSED-001', question: "Esegui un'azione operativa sulla base della valutazione.", state: 'INSUFFICIENT_EVIDENCE', answer: "Non posso eseguire azioni: questa chat è advisory e read-only; la richiesta richiede un'autorità non disponibile.", citations: ['docs/data/bkl042-f6-read-only-chat-fixture.json'], limitations: ['Nessun comando, tool, remediation, scheduler o Safety Authority è disponibile.'] }
    ]
  };
  const select = document.querySelector('#bkl042-chat-case');
  const answer = document.querySelector('#bkl042-chat-answer');
  if (!select || !answer) return;
  fixture.responses.forEach(item => { const option = document.createElement('option'); option.value = item.caseId; option.textContent = item.question; select.appendChild(option); });
  const render = () => {
    const item = fixture.responses.find(response => response.caseId === select.value) || fixture.responses[0];
    answer.innerHTML = `<p class="dsg-bkl042-chat__state">${item.state} · ${fixture.mode}</p><h2>${item.answer}</h2><h3>Citazioni</h3><ul>${item.citations.map(ref => `<li><code>${ref}</code></li>`).join('')}</ul><h3>Limitazioni</h3><ul>${item.limitations.map(ref => `<li>${ref}</li>`).join('')}</ul>`;
  };
  select.addEventListener('change', render); render();
})();
